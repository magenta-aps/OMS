from oms import db
# from oms import db_model
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, MetaData, Table

"""
Base = automap_base()
engine = create_engine('mysql://eark:eark@localhost/oms')

Base.prepare(engine, reflect = True)
"""

engine = create_engine('mysql://eark:eark@localhost/oms', convert_unicode = True)
metadata = MetaData(bind = engine)

Person = Table('Person', metadata, autoload = True)

"""
db.create_all()

Person = db_model.Person
Orders = db_model.Orders

clint = Person('0', 'Clint', 'Eastwood', 'mail@example.org')
db.session.add(person)
db.session.commit()

order = Orders('no1', 'pending', clint)
db.session.add(order)

db.session.commit()
"""
