__author__ = 'Andreas Kring <andreas@magenta.dk>'

from flask import jsonify, request, abort
from oms import app
from db_model import *
from sqlalchemy import exc

@app.route('/deletePerson', methods = ['DELETE'])
def delete_person():
    userName = request.args.get('userName')
    try:
        Person.delete().where(Person.c.userName == userName).execute()
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
            archivist_list.append(Person.select(Person.c.userName == a['userName']).execute().first())
        archivist_dict = sql_query_to_dict(archivist_list, 'archivists')
        return jsonify(archivist_dict)
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})
    

@app.route('/getPerson', methods = ['GET'])
def get_person():
    userName = request.args.get('userName')
    try:
        person = Person.select().where(Person.c.userName == userName).execute().first()
        person_dict = sql_query_to_dict(person)
        person_dict['role'] = get_role(userName)
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
        userName = request.json['userName']
        pwd = request.json['password']
        
        person = Person.select(Person.c.userName == userName).execute().first()
        
        if not person or not person['password'] == pwd:
            return jsonify({'status': 'ok', 'login': 'failed'})
        
        return jsonify({'firstname': person['firstname'], 'lastname': person['lastname'], 'role': get_role(userName)})
        
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
            if key != 'userName':
                Person.update().where(Person.c.userName == person['userName']).values({key: person[key]}).execute()
        return jsonify({'status': 'ok'})
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error',
                        'message': e.message})
        
 