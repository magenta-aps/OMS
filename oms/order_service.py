__author__ = 'Andreas Kring <andreas@magenta.dk>'

from flask import jsonify, request, abort
from oms import app
from db_model import *
from sqlalchemy import exc
import uuid

@app.route('/deleteOrder', methods = ['DELETE'])
def delete_order():
    order_id = request.args.get('orderId')
    order_items = BelongsTo.select(BelongsTo.c.orderId == order_id).execute().fetchall()
    try:
        Orders.delete().where(Orders.c.orderId == order_id).execute()
        for item in order_items:
            OrderItems.delete().where(OrderItems.c.refCode == item['refCode']).execute()
        return jsonify({'status': 'ok'})
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})
    

@app.route('/getOrders', methods = ['GET'])
def get_orders():
    try:
        # order_id = request.args.get('orderId')
        status = request.args.get('status')
        not_status = request.args.get('notStatus')
        print not_status
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

    order = request.json['order']
    user = order.pop('user', None)
    items = order.pop('items', None) 
    endUserOrderNote = order.pop('endUserOrderNote', None)
    
    try:
        # Check, if the user is aldready in the DB - and insert user if not
        insert_user(user)
    
        # Insert order itself    
        order['orderId'] = uuid.uuid4().hex
        order['orderStatus'] = 'new'
        # order['orderId'] = 'fixedUUID'
        Orders.insert(order).execute()
        
        # Insert the order items
        for item in items:
            item['refCode'] = uuid.uuid4().hex
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
        
