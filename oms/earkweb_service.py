from oms import app
from flask import jsonify, request, abort
import requests

EARKWEB_LOGIN_URL = 'http://localhost:8000/earkweb/admin/login/'
earkweb_session = requests.session()

@app.route('/earkweb/orderStatus', methods = ['GET'])
def status():
    global earkweb_session
    cookies = earkweb_session.cookies.items()
    print cookies
    return jsonify({'foo':'bar'})


def isCookiesExpired():
    cookies = earkweb_session.cookies.items()
    if cookies.is_empty():
        