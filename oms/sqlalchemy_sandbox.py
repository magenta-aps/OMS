from oms import app
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://andreas:hemmeligt@localhost/temp'

db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'Person'
    uid = db.Column(db.String(32), primary_key = True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(255))

    def __init__(self, uid, firstname, lastname, email   ):
        self.uid = uid
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
    
    def __repr__(self):
        return None


