from oms import app
from flask import jsonify, request, abort
import requests
import time

EARKWEB_LOGIN_URL = 'http://localhost:8000/earkweb/admin/login/'
# TODO: do not hard code username and password 
USERNAME = 'eark'
PASSWORD = 'eark'
cookie_to_check_for_expiration = 'sessionid'

earkweb_session = requests.session()

# Must take appropriate parameter
# @app.route('/earkweb/orderStatus', methods = ['GET'])
# def status():
#     if isCookieValid():
#         # Make call to order_status URL
#         return jsonify({'cookieValid':'true'})
#     else:
#         return jsonify({'cookieValid':'false'})


@app.route('/earkweb/submitOrder', methods = ['POST'])
def submit_order():
    """
    Must receive JSON like this
    {
        "orderId": "0924e01714244d9693cc3b1774e6b88e"
    }
    where orderId is the unique id of the order
    """

    # Check the posted JSON
        
    mandatory_keys = ['orderId']
    
    if not request.json:
        abort(400)
    
    if not json_keys_valid(request.json, mandatory_keys):
        return jsonify({'success': False, 'message': 'Request JSON must contain the keys ' + ', '.join(mandatory_keys)})
    
    if not is_json_value_non_blank_string(request.json['orderId']):
        return jsonify({'success': False, 'message': 'orderId must be non-empty string'})
    
    # TODO: should match value of orderId againts regex 
    
    # Request JSON ok - check cookie
    
    if isCookieValid():
        pass
        # Post the order using the existing cookies 
    else:
        # Login in to earkweb and get cookies
        status = login(earkweb_session, EARKWEB_LOGIN_URL)
        
        # Post the order
        
        
        
        pass

    
    
    return jsonify({'success': True})
    
    

        
    


def isCookieValid():
    cookies = earkweb_session.cookies.items()
    if len(cookies) == 0:
        return False
    for cookie in cookies:
        print cookie
        if cookie.name == cookie_to_check_for_expiration:
            expires = cookie.expires
            now = time.time()
            if now < expires:
                return True
            else:
                return False
    return False


def json_keys_valid(json, keys):
    """Return True if json (dict) contains the mandatory keys (list)"""
    for key in keys:
        if not key in json.keys():
            return False
    return True


def is_json_value_non_blank_string(value):
    if not (isinstance(value, str) or isinstance(value, unicode)):
        return False
    if len(value) == 0:
        return False
    return True


def login(earkweb_session, URL):
    
    # Get csrftoken
    
    resp = earkweb_session.get(URL)
    print resp.status_code
    if (resp.status_code != 200):
        return resp.status_code
    csrftoken = earkweb_session.cookies['csrftoken']
    print csrftoken
    
    # Login to Django
    login_data = {'username': USERNAME, 'password':PASSWORD, 'csrfmiddlewaretoken':csrftoken}
    print login_data
    resp = earkweb_session.post(EARKWEB_LOGIN_URL, data = login_data, headers = {'Referer':EARKWEB_LOGIN_URL})
    print resp.status_code
    
    
    
    
    