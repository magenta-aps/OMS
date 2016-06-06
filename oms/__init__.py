from flask_sqlalchemy import SQLAlchemy
__authors__ = 'lanre, andreas'

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from oms import order_service, archivist_service, user_service, person_service

# Do not write any code below this point!
# See note on circular import at http://flask.pocoo.org/docs/0.10/patterns/packages/