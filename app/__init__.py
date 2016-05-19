from flask import Flask
from flask_cors.extension import CORS

app = Flask(__name__)
CORS(app)
from app import db_connector
from app import rest

