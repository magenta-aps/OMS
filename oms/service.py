__author__ = 'andreas'

from flask import jsonify
from oms import app
from sqlalchemy_sandbox import db, Person

@app.route('/test', methods = ['GET'])
def test():
    return jsonify({'foo': 'bar'})

@app.route('/dbtest', methods = ['GET'])
def dbtest():
    person = Person('uid3', 'Bill', 'Clinton', 'bill@magenta.dk')
    db.session.add(person)
    db.session.commit()
    return jsonify({'foo': 'db'})