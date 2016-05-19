import MySQLdb
from flask import Flask
from flask_cors.extension import CORS

app = Flask(__name__)
CORS(app)

global dbase

def readSystemProps():
    global sysProperties
    sysProperties = {}
    propsFile = "system/global.properties"
    f = open(propsFile, 'r')
    for line in f:
        # print line
        if(line[0] == '#'):
            continue
        a,b = line.split('=')
        sysProperties[a]=b[:-1]

readSystemProps()


# Hard-coded DB settings until the properties stuff is done
DB_HOST = sysProperties['db.connection.host']
DB_USER = sysProperties['db.connection.user']
DB_PWD = sysProperties['db.connection.password']
DB_NAME = sysProperties['db.connection.name']

dbase = MySQLdb.connect(DB_HOST, DB_USER, DB_PWD, DB_NAME)

print "The db name is: ", DB_NAME