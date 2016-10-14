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
def get_order_data_helper(order_id):
    order = Orders.select(Orders.c.orderId == order_id).execute().first()
    ordered_by = OrderedBy.select(OrderedBy.c.orderId == order_id).execute().first()
    responsible = Responsible.select(Responsible.c.orderId == order_id).execute().first()
    belongs_to = BelongsTo.select(BelongsTo.c.orderId == order_id).execute().fetchall()
    person = Person.select(Person.c.userName == ordered_by['userName']).execute().first() 
        
    order_dict = dict(zip(order.keys(), order.values()))
    person_dict = dict(zip(person.keys(), person.values()))
    
    sql_query_to_dict(belongs_to)
    order_dict['endUser'] = person_dict
    if responsible:
        userName = responsible['userName']
        order_dict['assignee'] = sql_query_to_dict(Person.select(Person.c.userName == userName).execute().first())
    else:
        order_dict['assignee'] = 'none'
        
    items = []
    for refCode in [b['refCode'] for b in belongs_to]:
        items.append(sql_query_to_dict(OrderItems.select(OrderItems.c.refCode == refCode).execute().first()))

    for item in items:
        if item['confidential'] == 0:
            item['confidential'] = "Unrestricted"
        elif item['confidential'] == 1:
            item['confidential'] = "Restricted"
        else:
            print 'WARN: confidential not set'

    order_dict['items'] = items 
    return order_dict


def get_role(userName):
        archivist = Archivist.select(Archivist.c.userName == userName).execute().first()
        
        if archivist:
            return "archivist"
        else:
            return "enduser"


def insert_archivist(user):
    """Insert archivist to DB if not already exists
    
    Keyword arguments:
    user -- JSON containing the user details (see example)
    
    Example JSON:
        {
            "userName": "endUser-UUID1",
            "firstname": "Clint",
            "lastname": "Eastwood",
            "email": "clint@hollywood.biz
        }        
    """
    
    if Archivist.select(Archivist.c.userName == user['userName']).execute().first() == None:
        if Person.select(Person.c.userName == user['userName']).execute().first() == None:  
            Person.insert(user).execute()
        Archivist.insert({'userName': user['userName']}).execute()


def insert_user(user):
    """Insert user to DB if not already exists
    
    Keyword arguments:
    user -- JSON containing the user details (see example)
    
    Example JSON:
        {
            "userName": "endUser-UUID1",
            "firstname": "Clint",
            "lastname": "Eastwood",
            "email": "clint@hollywood.biz
        }        
    """
    
    if EndUser.select(EndUser.c.userName == user['userName']).execute().first() == None:
        if Person.select(Person.c.userName == user['userName']).execute().first() == None:
            Person.insert(user).execute()
        EndUser.insert({'userName': user['userName']}).execute()


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
# OrderedBy.insert().execute({'userName':'userName1000', 'orderId':'orderId1'})
# Person.update().where(Person.c.firstname == 'Bill').values(lastname='ssdsd').execute()
# Person.delete().where(Person.c.userName == 'userName1000').execute()