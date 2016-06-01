__author__ = 'Andreas Kring <andreas@magenta.dk>'

from flask import jsonify, request, abort
from oms import app
from db_model import *
from sqlalchemy import exc

@app.route('/getOrdersForUser', methods = ['GET'])
def get_order_for_user():
    uid = request.args.get('uid')
    orders = OrderedBy.select(OrderedBy.c.uid == uid).execute().fetchall()
    print orders
    order_ids = []
    return 'hurra'