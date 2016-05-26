from oms import db

"""
class Person(db.Model):
    #__tablename__ = 'Person'
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
        return '<Person %r> ' % self.uid
"""


"""
class EndUser(db.Model):
    # __tablename__ = 'end_user'
    id = db.Column(db.Integer, primary_key = True)
    # uid = db.Column(db.String(32), db.ForeignKey('person.uid'))
    orders = db.relationship('Orders', backref = 'enduser', lazy = 'dynamic')
    
    def __init__(self, id, orders):
        self.id = id
        self.orders = orders
    
    def __repr__(self):
        return '<EndUser %r> ' % self.id
    

class Orders(db.Model):
    orderId = db.Column(db.String(32), primary_key = True)
    orderStatus = db.Column(db.String(10))
    uid = db.Column(db.String(32), db.ForeignKey('end_user.id'))
    
    def __init__(self, orderId, orderStatus, uid):
        self.orderId = orderId
        self.orderStatus = orderStatus
        self.uid = uid
    
    def __repr__(self):
        return None
"""