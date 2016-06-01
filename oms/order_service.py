__author__ = 'Andreas Kring <andreas@magenta.dk>'

from flask import jsonify, request, abort
from oms import app
from db_model import *
from sqlalchemy import exc
import uuid

@app.route('/deleteOrder', methods = ['DELETE'])
def delete_order():
    order_id = request.args.get('orderId')
    print order_id
    order_items = BelongsTo.select(BelongsTo.c.orderId == order_id).execute().fetchall()
    try:
        Orders.delete().where(Orders.c.orderId == order_id).execute()
        for item in order_items:
            OrderItems.delete().where(OrderItems.c.refCode == item['refCode']).execute()
        return jsonify({'status': 'ok'})
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})
    

@app.route('/getOrderStatus', methods = ['GET'])
def get_order_status():
    order_id = request.args.get('orderId')
    try:
        order = Orders.select(Orders.c.orderId == order_id).execute().first()
        ordered_by = OrderedBy.select(OrderedBy.c.orderId == order_id).execute().first()
        print ordered_by
        responsible = Responsible.select(Responsible.c.uid == order_id).execute().first()
        print responsible
        belongs_to = BelongsTo.select(BelongsTo.c.orderId == order_id).execute().fetchall()
        
        order_dict = dict(zip(order.keys(), order.values()))
        order_dict['endUserId'] = ordered_by['uid']
        if responsible:
            order_dict['assignee'] = responsible['uid']
        else:
            order_dict['assignee'] = 'none'
        
        order_dict['itemRefCodes'] = [b['refCode'] for b in belongs_to] 
        
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
        # order['orderId'] = uuid.uuid4().hex
        order['orderId'] = 'fixedUUID'
        Orders.insert(order).execute()
        
        # Insert the order items
        for item in items:
            item['refCode'] = uuid.uuid4().hex
            OrderItems.insert(item).execute()
            BelongsTo.insert({'orderId': order['orderId'], 'refCode': item['refCode']}).execute()
            
        # Relations
        OrderedBy.insert({'orderId': order['orderId'], 'uid': user['uid'], 'endUserOrderNote': endUserOrderNote}).execute()
                
        return jsonify({'status': 'ok',
                        'orderId': order['orderId']})
         
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})


@app.route('/test', methods = ['GET'])
def test():
    return jsonify({'foo': 'bar'})

       
        
