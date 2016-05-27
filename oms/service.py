__author__ = 'andreas'

from flask import jsonify, request
from oms import app
from db_model import Person, EndUser, Archivist, Orders, OrderItems, OrderedBy, Responsible, BelongsTo

# print EndUser.select().execute().fetchall()

@app.route('/getPerson', methods = ['GET'])
def get_end_user():
    # Parameter existence could be checked
    uid = request.args.get('uid')
    person = Person.select(Person.c.uid == uid).execute().first()
    return person[0][0]

@app.route('/test', methods = ['GET'])
def test():
    return jsonify({'foo': 'bar'})

@app.route('/dbtest', methods = ['GET'])
def dbtest():
    return db_model.Person.select().execute().fetchall()[0][0]
