from oms import db
from sqlalchemy import create_engine, MetaData, Table

# engine = create_engine('mysql://andreas:hemmeligt@localhost/temp', convert_unicode = True)
metadata = MetaData(bind = db.engine)

# Entity sets - see E/R diagram
Person = Table('Person', metadata, autoload = True)
EndUser = Table('EndUser', metadata, autoload = True)
Archivist = Table('Archivist', metadata, autoload = True)
Orders = Table('Orders', metadata, autoload = True)
OrderItems = Table('OrderItems', metadata, autoload = True)

# Relationships - see E/R diagram
OrderedBy = Table('OrderedBy', metadata, autoload = True)
Responsible = Table('Responsible', metadata, autoload = True)
BelongsTo = Table('BelongsTo', metadata, autoload = True)




### Example of SELECT, INSERT, UPDATE and DELETE

# Person.select().execute().fetchall()
# OrderedBy.insert().execute({'uid':'uid1000', 'orderId':'orderId1'})
# Person.update().where(Person.c.firstname == 'Bill').values(lastname='ssdsd').execute()
# Person.delete().where(Person.c.uid == 'uid1000').execute()