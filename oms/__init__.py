__authors__ = 'lanre, andreas'

from flask import Flask

app = Flask(__name__)
from oms import service

# Do not write any code below this point!
# See note on circular import at http://flask.pocoo.org/docs/0.10/patterns/packages/