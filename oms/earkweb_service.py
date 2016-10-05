from oms import app
from flask import jsonify, request, abort
import requests
from db_model import *
from sqlalchemy import exc
import time

EARKWEB_LOGIN_URL = 'http://localhost:8000/earkweb/admin/login/'
SUBMIT_ORDER_URL = 'http://localhost:8000/earkweb/search/submit_order/' 

# TODO: do not hard code username and password 
USERNAME = 'eark'
PASSWORD = 'eark'
cookie_to_check_for_expiration = 'sessionid'

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
    
    # Login in to earkweb and get cookies
    # TODO: should be able to reuse a session
    try:
        earkweb_session = get_session(EARKWEB_LOGIN_URL)
    except Exception as e:
        return jsonify({'success':False, 'message': e.message})
    
    # Get order details and construct payload
    order_id = request.json['orderId']
    try:
        package_ids = get_packageIds(order_id)
        order_title = get_orderTitle(order_id)
    except exc.SQLAlchemyError as e:
        return jsonify({'status': 'error', 'message': e.message})
    payload = {'order_title': order_title, 'aip_identifiers': package_ids}
    print payload
    
    # Post the order    
    resp = earkweb_session.post(SUBMIT_ORDER_URL, json = payload, headers = {'Referer':EARKWEB_LOGIN_URL})
    if (resp.status_code != 200):
        return jsonify({'success':False,
                        'message': 'There was a problem submitting the order to ' + SUBMIT_ORDER_URL + ' (status code: ' + resp.status_code + ')'})
    else:
        # Check the JSON response from earkweb
        json = resp.json() # dict
        if 'error' in json.keys():
            return jsonify({'success':False, 'message':json['error']})
        else:
            # Put data into DB
            return jsonify({'success': True})
        
        
def get_packageIds(order_id):
    """
        Return a list (strings) of unique packageIds belonging to the order with 
        the given orderId
    """
    
    items = BelongsTo.select(BelongsTo.c.orderId == order_id).execute().fetchall()
    items_dict = sql_query_to_dict(items,'items')
    ref_codes = [item['refCode'] for item in items_dict['items']]
    package_ids = []
    for ref_code in ref_codes:
        package_id = sql_query_to_dict(OrderItems.select(OrderItems.c.refCode == ref_code).execute().first())['packageId']
        if not package_id in package_ids:
            package_ids.append(str(package_id))
    return package_ids

        
    
def get_orderTitle(order_id):
    """Get the order title (string) of the order with the given orderId"""
    title = sql_query_to_dict(Orders.select(Orders.c.orderId == order_id).execute().first())['title']
    return title

        
    


# def isCookieValid():
#     cookies = earkweb_session.cookies.items()
#     if len(cookies) == 0:
#         return False
#     for cookie in cookies:
#         print cookie
#         if cookie.name == cookie_to_check_for_expiration:
#             expires = cookie.expires
#             now = time.time()
#             if now < expires:
#                 return True
#             else:
#                 return False
#     return False


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



def get_session(URL):
    earkweb_session = requests.session()  
    
    # Get csrftoken
    resp = earkweb_session.get(URL)
    if (resp.status_code != 200):
        raise Exception('Could not get CSRF token!')
    csrftoken = earkweb_session.cookies['csrftoken']
    
    # Login to Django
    login_data = {'username': USERNAME, 'password':PASSWORD, 'csrfmiddlewaretoken':csrftoken}
    resp = earkweb_session.post(EARKWEB_LOGIN_URL, data = login_data, headers = {'Referer':EARKWEB_LOGIN_URL}, allow_redirects = False)
    if (resp.status_code != 302):
        raise Exception('There was a problem logging in to earkweb!')

    return earkweb_session


