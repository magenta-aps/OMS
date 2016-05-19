__authors__ = 'lanre, andreas'

from app import app
from flask import jsonify, request, abort
# import MySQLdb

# Hard-coded DB settings until the properties stuff is done
DB_HOST = 'localhost'
DB_USER = 'andreas'
DB_PWD = ''
DB_NAME = 'oms'

# connection = None

conn = MySQLConnector(properties...)


@app.route('/insert', methods = ['POST'])
def insert_orders():
    if not request.json:
        abort(400)
    order = request.json['order']
    items = request.json['items']
    conn.insert(order)
    print order
    return jsonify(order)

"""
def insert_order(order):
    pass

def get_connection(host, db, user, password):
    global connection
    connection = MySQLdb.connect(host = host, db = db, user = user, passwd = password)
""" 
    