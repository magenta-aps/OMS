__authors__ = 'lanre, andreas'

import MySQLdb

def getConnection():
    dbase = MySQLdb.connect(DB_HOST, DB_USER, DB_PWD, DB_NAME)
    return dbase

def readSystemProps():
    sysProperties = {}
    propsFile = "system/global.properties"
    f = open(propsFile, 'r')
    for line in f:
        # print line
        if(line[0] == '#'):
            continue
        a,b = line.split('=')
        sysProperties[a]=b[:-1]
    return sysProperties

sysProps = readSystemProps()

DB_HOST = sysProps['db.connection.host']
DB_USER = sysProps['db.connection.user']
DB_PWD = sysProps['db.connection.password']
DB_NAME = sysProps['db.connection.name']

print "The db name is: ", DB_NAME
