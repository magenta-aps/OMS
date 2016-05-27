from flask_sqlalchemy import SQLAlchemy
__authors__ = 'lanre, andreas'

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from oms import service#, db_model
# from db_model import Person
# print Person.select().execute().fetchall()

# db.create_all()
#from oms import sqlalchemy_sandbox 

# Do not write any code below this point!
# See note on circular import at http://flask.pocoo.org/docs/0.10/patterns/packages/