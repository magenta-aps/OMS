__author__ = 'andreas'

from flask import jsonify
from oms import app
# from sqlalchemy_sandbox import db, Person

import db_model
print db_model.Person.select().execute().fetchall()


@app.route('/test', methods = ['GET'])
def test():
    return jsonify({'foo': 'bar'})

@app.route('/dbtest', methods = ['GET'])
def dbtest():
    return db_model.Person.select().execute().fetchall()[0][0]
