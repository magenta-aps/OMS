__author__ = 'Andreas Kring <andreas@magenta.dk>'

from flask import jsonify, request, abort
from oms import app
from db_model import *
from sqlalchemy import exc
import uuid
from json_utils import is_dict_valid
from request_validator import OrderIdValidator

@app.route('/deleteOrder', methods = ['DELETE'])
def delete_order():
    order_id = request.args.get('orderId')
    
    # Check if the request parameter is valid
    validator = OrderIdValidator(order_id)
    if not validator.is_order_id_valid():
        return validator.get_error_json()
    
    try:
        order = Orders.select(Orders.c.orderId == order_id).execute().first()
        if not order:
            return jsonify({'status':'error', 'message': 'No orders with orderId: ' + order_id})
        order_items = BelongsTo.select(BelongsTo.c.orderId == order_id).execute().fetchall()
        Orders.delete().where(Orders.c.orderId == order_id).execute()
        if order_items:
            for item in order_items:
                OrderItems.delete().where(OrderItems.c.refCode == item['refCode']).execute()
        return jsonify({'status': 'ok'})
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})
    

@app.route('/getOrders', methods = ['GET'])
def get_orders():

    # Check request parameters    
    number_of_parameters = len(request.args.keys())
    error_json = jsonify({'status':'error',
                          'message':'The request should contain no parameters or exactly one of: status, notStatus, assignee or userName'})
    if not number_of_parameters in [0, 1]:
        return error_json
    if number_of_parameters == 1:
        parameter = request.args.keys()[0]
        if not parameter in ['status', 'notStatus', 'assignee', 'userName']:
            return error_json
    
    try:
        status = request.args.get('status')
        not_status = request.args.get('notStatus')
        assignee = request.args.get('assignee')
        userName = request.args.get('userName')
        
        # Further filtering should be done from the front-end
        if status:
            orders = Orders.select(Orders.c.orderStatus == status).execute().fetchall()
        elif not_status:
            orders = Orders.select(Orders.c.orderStatus != not_status).execute().fetchall()
        elif assignee:
            orders = Responsible.select(Responsible.c.userName == assignee).execute().fetchall()
        elif userName:
            orders = OrderedBy.select(OrderedBy.c.userName == userName).execute().fetchall()
        else:
            orders = Orders.select().execute().fetchall()
        order_ids = [order['orderId'] for order in orders]

        order_list = []
        for order_id in order_ids:
            order_dict = get_order_data_helper(order_id)            
            order_list.append(order_dict)
        return jsonify({'orders': order_list})
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})


@app.route('/getOrderData', methods = ['GET'])
def get_order_data():
    order_id = request.args.get('orderId')
    
    # Check if the request parameter is valid
    validator = OrderIdValidator(order_id)
    if not validator.is_order_id_valid():
        return validator.get_error_json()
    
    try:
        order_dict = get_order_data_helper(order_id)
        return jsonify(order_dict)
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})


@app.route('/newOrder', methods = ['POST'])
def new_order():
    if not request.json:
        abort(400)

    checker = JsonChecker(request.json)
    if not checker.is_order_json_correct():
        return checker.get_error_message()

    # Everything ok - insert order into DB
    
    order = request.json['order']
    user = order.pop(u'user', None)
    packages = order.pop('items', None)
    endUserOrderNote = order.pop('endUserOrderNote', None)
    
    try:
        # Check, if the user is already in the DB - and insert user if not
        insert_user(user)
    
        # Insert order itself    
        order['orderId'] = uuid.uuid4().hex
        order['orderStatus'] = 'new'
        Orders.insert(order).execute()
        
        # Insert the order items
        for package in packages:
            packageId = package['packageId']
            items = package['items']
            for item in items:
                # "Old" values
                item['refCode'] = uuid.uuid4().hex
                item['aipTitle'] = None
                item['aipURI'] = None
                item['levelOfDescription'] = 'package'
                
                OrderItems.insert(item).execute()
                BelongsTo.insert({'orderId': order['orderId'], 'refCode': item['refCode']}).execute()
            
        # Relations
        OrderedBy.insert({'orderId': order['orderId'], 'userName': user['userName'], 'endUserOrderNote': endUserOrderNote}).execute()
                
        return jsonify({'status': 'ok',
                        'orderId': order['orderId']})
         
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})


@app.route('/test', methods = ['GET'])
def test():
    return jsonify({'foo': 'bar'})

       
@app.route('/updateOrder', methods = ['PUT'])
def update_order():
    if not request.json:
        abort(400)
    order = request.json
    if 'assignee' in order:
        userName = order.pop('assignee')
        order['userName'] = userName
    try:
        for key in order:
            if key in Orders.c.keys() and key != 'orderId':
                Orders.update().where(Orders.c.orderId == order['orderId']).values({key: order[key]}).execute()
            if key == 'endUserOrderNote':
                OrderedBy.update().where(OrderedBy.c.orderId == order['orderId']).values({key: order[key]}).execute()
            if key in Responsible.c.keys() and key != 'orderId':
                if key == 'userName':
                    responsible = Responsible.select(Responsible.c.orderId == order['orderId']).execute().first()
                    # Should check if orderId already there - otherwise insert
                    if responsible:
                        if userName == 'none':
                            Responsible.delete().where(Responsible.c.orderId == order['orderId']).execute()
                        else:
                            Responsible.update().where(Responsible.c.orderId == order['orderId']).values({key: order[key]}).execute()
                    else:
                        Responsible.insert({'orderId': order['orderId'], 'userName': order['userName']}).execute()
                else:
                    Responsible.update().where(Responsible.c.orderId == order['orderId']).values({key: order[key]}).execute()
    
        return jsonify({'status': 'ok'})

    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})
        

    

# TODO: refactor - write a more general method that can take a dictionary (with empty values) of the 
# correct form and check if the incoming JSON keys matches the keys in this dictionary

class JsonChecker(object):
    
    def __init__(self, json):
        self.json = json
        self.error_message_json = None
    
    def is_order_json_correct(self):
    
        json = self.json
    
        # Check if "order" is present in the JSON
        if not is_dict_valid(json, ['order']):
            self.json = jsonify({'success':False, 'message': 'The request JSON must have the keys: order'})
            return False
    
        # Check if "order" contains the correct keys    
        order = json['order']
        mandatory_keys = ['title', 'origin', 'endUserOrderNote', 'orderDate', 'plannedDate', 'user', 'items', 'deliveryFormat']
        if not is_dict_valid(order, mandatory_keys):
            self.json = jsonify({'success':False, 'message':'The \'order\' must have the keys (no more, no less): ' + ', '.join(mandatory_keys)})
            return False
        
        # Check if "user" contains the correct keys
        user = order['user']
        mandatory_keys = ['userName', 'firstname', 'lastname', 'email']
        if not is_dict_valid(user, mandatory_keys):
            self.json = jsonify({'success':False, 'message':'The \'user\' must have the keys: ' + ', '.join(mandatory_keys)})
            return False
        
        # Check if the items contains a list of JSON objects
        packages = order['items']
        if not isinstance(packages, list):
            self.json = jsonify({'success':False, 'message': 'The \'items\' in \'order\' must have list of JSON objects'})
            return False
        
        # Check if the JSON objects in the order items list are ok
        mandatory_keys = ['packageId', 'items']
        itm_mandatory_keys = ['title', 'packageId', 'confidential', 'path', 'contentType', 'size']
        for o in packages:
            if not is_dict_valid(o, mandatory_keys):
                self.json = jsonify({'success':False, 'message':'The \'items\' for each packageId must have the keys: ' + ', '.join(mandatory_keys)})
                return False
            # Check that the items are ok
            for itm in o['items']:
                if not is_dict_valid(itm, itm_mandatory_keys):
                    self.json = jsonify({'success':False, 'message':'The (leaf) \'items\' for must have the keys: ' + ', '.join(itm_mandatory_keys)})
                    return False
        
        return True
    
    
    def get_error_message(self):
        return self.json