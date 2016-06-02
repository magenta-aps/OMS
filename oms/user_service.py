__author__ = 'Andreas Kring <andreas@magenta.dk>'

from flask import jsonify, request, abort
from oms import app
from db_model import *
from sqlalchemy import exc

@app.route('/getOrders', methods = ['GET'])
def get_order_for_user():
    try:
        # order_id = request.args.get('orderId')
        status = request.args.get('status')
        not_status = request.args.get('notStatus')
        print not_status
        assignee = request.args.get('assignee')
        uid = request.args.get('uid')
        
        # Further filtering should be done from the front-end
        if status:
            orders = Orders.select(Orders.c.orderStatus == status).execute().fetchall()
        elif not_status:
            orders = Orders.select(Orders.c.orderStatus != not_status).execute().fetchall()
        elif assignee:
            orders = Responsible.select(Responsible.c.uid == assignee).execute().fetchall()
        elif uid:
            orders = OrderedBy.select(OrderedBy.c.uid == uid).execute().fetchall()
        else:
            orders = Orders.select().execute().fetchall()
        order_ids = [order['orderId'] for order in orders]
        return jsonify({'orders': order_ids})
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})
