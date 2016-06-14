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


@app.route('/getArchivists', methods = ['GET'])
def get_archivists():
    # Should be refactored - use join or make 'normal' SQL query instead
    try:
        archivist_list = []
        archivists = Archivist.select().execute().fetchall()
        for a in archivists:
            archivist_list.append(Person.select(Person.c.uid == a['uid']).execute().first())
        archivist_dict = sql_query_to_dict(archivist_list, 'archivists')
        return jsonify(archivist_dict)
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
    

@app.route('/newPerson', methods = ['POST'])
def new_person():
    if not request.json:
        abort(400)
    user = request.json
    try:
        user_type = user.pop('type')
        if user_type == 'enduser':
            # User is an EndUser
            insert_user(user)
        elif user_type == 'archivist':
            # User ia an archivist
            insert_archivist(user)
        else:
            return jsonify({'status': 'error', 'message': 'Incorrect type'})
        return jsonify({'status': 'ok'})
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})
        

@app.route('/login', methods = ['POST'])
def login():
    if not request.json:
        abort(400)
    try:
        uid = request.json['uid']
        pwd = request.json['password']
        
        person = Person.select(Person.c.uid == uid).execute().first()
        
        if not person or not person['password'] == pwd:
            return jsonify({'status': 'ok', 'login': 'failed'})
        
        enduser = EndUser.select(EndUser.c.uid == uid).execute().first()
        
        if enduser:
            return jsonify({'firstname': person['firstname'], 'lastname': person['lastname'], 'role': 'enduser'})
        else:
            # Must be archivist
            return jsonify({'firstname': person['firstname'], 'lastname': person['lastname'], 'role': 'archivist'})
        
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})
    

@app.route('/updatePerson', methods = ['PUT'])
def update_person():
    if not request.json:
        abort(400)
    person = request.json
    try:
        for key in person:
            if key != 'uid':
                Person.update().where(Person.c.uid == person['uid']).values({key: person[key]}).execute()
        return jsonify({'status': 'ok'})
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})
        
 