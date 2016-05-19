__authors__ = 'lanre, andreas'

from app import app
from flask import jsonify, request, abort

@app.route('/insert', methods = ['POST'])
def insert_order():
    if not request.json:
        abort(400)
    order = request.json['order']
    items = request.json['items']
    
    return jsonify({"foo": "bar"})

@app.route('/testdb', methods=['GET'])
def getDbVersion():
    # prepare a cursor object using cursor() method
    cursor = dbase.cursor()
    # execute SQL query using execute() method.
    cursor.execute("SELECT VERSION()")
    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    #For now let's close the connection
    dbase.close()
    return jsonify({"version": "hurra"})