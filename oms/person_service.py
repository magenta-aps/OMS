__author__ = 'Andreas Kring <andreas@magenta.dk>'

from flask import jsonify, request, abort
from oms import app
from db_model import *
from sqlalchemy import exc

@app.route('/deletePerson', methods = ['DELETE'])
def delete_person():
    uid = request.args.get('uid')
    try:
        Person.delete().where(Person.c.uid == uid).execute()
        return jsonify({'status': 'ok'})
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})


@app.route('/getPerson', methods = ['GET'])
def get_person():
    uid = request.args.get('uid')
    try:
        person = Person.select().where(Person.c.uid == uid).execute().first()
        person_dict = sql_query_to_dict(person)
        # TODO: make similar methods to get EndUsers and Archivists
        return jsonify(person_dict)
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})
    
"""
@app.route('/newPerson', methods = ['POST'])
def new_person():
    if not request.json:
        abort(400)
    try:
        insert_user(request.json)
        if request.json['type'] == 'enduser':
            # User is an EndUser
            EndUser.insert({'uid': user['uid']}).execute()
        else:
            # User ia an archivist
            Archivist.insert({'uid': user['uid']}).execute()
        return jsonify({'status': 'ok'})
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})
""" 