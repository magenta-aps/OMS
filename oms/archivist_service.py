__author__ = 'Andreas Kring <andreas@magenta.dk>'

from flask import jsonify, request, abort
from oms import app
from db_model import *
from sqlalchemy import exc

@app.route('/updateOrder', methods = ['PUT'])
def update_assignee():
    if not request.json:
        abort(400)
    order = request.json
    try:
        for key in order:
            print key
            if key in Orders.c.keys() and key != 'orderId':
                Orders.update().where(Orders.c.orderId == order['orderId']).values({key: order[key]}).execute()
            if key == 'endUserOrderNote':
                OrderedBy.update().where(OrderedBy.c.orderId == order['orderId']).values({key: order[key]}).execute()
            if key in Responsible.c.keys() and key != 'orderId':
                Responsible.update().where(OrderedBy.c.orderId == order['orderId']).values({key: order[key]}).execute()
    
        return jsonify({'status': 'ok'})

    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})
