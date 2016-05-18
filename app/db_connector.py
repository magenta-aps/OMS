__authors__ = 'lanre, andreas'

from app import app
from flask import jsonify, request, abort

# Hard-coded DB settings until the properties stuff is done
DB_HOST = 'localhost'
DB_USER = 'andreas'
DB_PWD = ''
DB_NAME = 'oms'

@app.route('/insert', methods = ['POST'])
def insert_order():
    if not request.json:
        abort(400)
    order = request.json['order']
    items = request.json['items']
    
    return jsonify({"foo": "bar"})