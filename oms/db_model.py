__author__ = 'Andreas Kring <andreas@magenta.dk>'

from oms import db
from sqlalchemy import create_engine, MetaData, Table
from types import *

_metadata = MetaData(bind = db.engine)

# Entity sets - see E/R diagram
Person = Table('Person', _metadata, autoload = True)
EndUser = Table('EndUser', _metadata, autoload = True)
Archivist = Table('Archivist', _metadata, autoload = True)
Orders = Table('Orders', _metadata, autoload = True)
OrderItems = Table('OrderItems', _metadata, autoload = True)

# Relationships - see E/R diagram
OrderedBy = Table('OrderedBy', _metadata, autoload = True)
Responsible = Table('Responsible', _metadata, autoload = True)
BelongsTo = Table('BelongsTo', _metadata, autoload = True)

# Helpful methods
def insert_user(user):
    """Insert user to DB if not already exists
    
    Keyword arguments:
    user -- JSON containing the user details (see example)
    
    Example JSON:
        {
            "uid": "endUser-UUID1",
            "firstname": "Clint",
            "lastname": "Eastwood",
            "email": "clint@hollywood.biz
        }        
    """
    
    if EndUser.select(EndUser.c.uid == user['uid']).execute().first() == None:
        Person.insert(user).execute()
        EndUser.insert({'uid': user['uid']}).execute()


def sql_query_to_dict(sqlalchemy_table, property = None):
    """Returns a RowProxy or a list of RowProxy's
    
    (see sqlalchemy.engine.result.RowProxy)
    """
    if type(sqlalchemy_table) == ListType:
        # print 'ListType'
        l = []
        for i in sqlalchemy_table:
           l.append(dict(zip(i.keys(), i.values())))
        return {property: l} 
    else:
         # print 'non list'
         return dict(zip(sqlalchemy_table.keys(), sqlalchemy_table.values()))


### Example of SELECT, INSERT, UPDATE and DELETE

# Person.select().execute().fetchall()
# OrderedBy.insert().execute({'uid':'uid1000', 'orderId':'orderId1'})
# Person.update().where(Person.c.firstname == 'Bill').values(lastname='ssdsd').execute()
# Person.delete().where(Person.c.uid == 'uid1000').execute()