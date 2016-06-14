__author__ = 'Andreas Kring <andreas@magenta.dk>'

from flask import jsonify, request, abort
from oms import app
from db_model import *
from sqlalchemy import exc

@app.route('/getItems', methods = ['GET'])
def get_items():
    order_id = request.args.get('orderId')
    # Should be refactored - use join or make 'normal' SQL query instead
    try:
        item_list = []
        belongs_to = BelongsTo.select(BelongsTo.c.orderId == order_id).execute().fetchall()
        for i in belongs_to:
            item_list.append(OrderItems.select(OrderItems.c.refCode == i['refCode']).execute().first())
        item_dict = sql_query_to_dict(item_list, 'orderItems')
        return jsonify(item_dict)
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})
