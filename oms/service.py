__author__ = 'andreas'

from flask import jsonify, request, abort
from oms import app
from db_model import *
from sqlalchemy import exc
import uuid

# print EndUser.select().execute().fetchall()

@app.route('/getPerson', methods = ['GET'])
def get_end_user():
    # Parameter existence could be checked
    uid = request.args.get('uid')
    person = Person.select(Person.c.uid == uid).execute().first()
    return person[0][0]

@app.route('/newOrder', methods = ['POST'])
def new_order():
    if not request.json:
        abort(400)

    order = request.json['order']
    user = order.pop('user', None)
    items = order.pop('items', None) 
    endUserOrderNotes = order.pop('endUserOrderNotes', None)
    
    # Check, if the user is aldready in the DB - and insert user if not
    insert_user(user)

    # Insert order    
    order['orderId'] = str(uuid.uuid4())
    Orders.insert(order).execute()
    
    return jsonify({'status': 'ok'})
    
    

@app.route('/test', methods = ['GET'])
def test():
    return jsonify({'foo': 'bar'})

@app.route('/dbtest', methods = ['GET'])
def dbtest():
    return db_model.Person.select().execute().fetchall()[0][0]



        
        
