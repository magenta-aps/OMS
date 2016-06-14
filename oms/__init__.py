from flask_sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS
__authors__ = 'lanre, andreas'

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
CORS(app)
db = SQLAlchemy(app)

from oms import order_service, item_service, user_service, person_service

# Do not write any code below this point!
# See note on circular import at http://flask.pocoo.org/docs/0.10/patterns/packages/