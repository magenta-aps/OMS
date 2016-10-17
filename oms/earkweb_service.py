from oms import app
from flask import jsonify, request, abort
import requests
from db_model import *
from sqlalchemy import exc
import time
from request_validator import OrderIdValidator
import uuid

EARKWEB_LOGIN_URL = 'http://localhost:8000/earkweb/admin/login/'
SUBMIT_ORDER_URL = 'http://localhost:8000/earkweb/search/submit_order/' 
ORDER_STATUS_URL = 'http://localhost:8000/earkweb/search/order_status'

# TODO: do not hard code username and password 
USERNAME = 'eark'
PASSWORD = 'eark'
# cookie_to_check_for_expiration = 'sessionid'

# Must take appropriate parameter
@app.route('/earkweb/orderStatus', methods = ['GET'])
def status():
    """
        Update order status for a single order (identified by it's orderId)
    """
    order_id = request.args.get('orderId')
    
    # Check if the request parameter is valid
    validator = OrderIdValidator(order_id)
    if not validator.is_order_id_valid():
        return validator.get_error_json()

    # Return error if the order does not exists or is not "submitted"
    try:
        order = Orders.select(Orders.c.orderId == order_id).execute().first()
    except exc.SQLAlchemyError as e:
        return jsonify({'success': False, 'message': e.message})
    if not order:
        return jsonify({'success': False, 'message': 'No orders with orderId: ' + order_id})
    else:
        # Check if the orderStatus is submitted
        order_dict = sql_query_to_dict(order)
        order_status = order_dict['orderStatus']
        if not order_status == 'submitted':
            return jsonify({'status': False, 'message': 'The order must be submitted before querying it\'s status'})
   
    # Login in to earkweb and get cookies
    # TODO: should be able to reuse a session
    try:
        earkweb_session = get_session(ORDER_STATUS_URL)
    except Exception as e:
        return jsonify({'success': False, 'message': e.message})

    # Update the status for the order
    try:
        done = get_earkweb_order_status(order, earkweb_session)
        if done:
            process_status = 'done'
        else:
            process_status = 'processing'
    except Exception as e:
        return jsonify({'success': False, 'message': e.message})
    
    return jsonify({'success': True, 'processStatus': process_status})
    



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
    order_id = request.json['orderId']
    validator = OrderIdValidator(order_id)
    if not validator.is_order_id_valid():
        return validator.get_error_json()

    # Return error if the order does not exists
    try:
        order = Orders.select(Orders.c.orderId == order_id).execute().first()
    except exc.SQLAlchemyError as e:
        return jsonify({'success': False, 'message': e.message})
    if not order:
        return jsonify({'success': False, 'message': 'No orders with orderId: ' + order_id})

    # Login in to earkweb and get cookies
    # TODO: should be able to reuse a session
    try:
        earkweb_session = get_session(EARKWEB_LOGIN_URL)
    except Exception as e:
        return jsonify({'success': False, 'message': e.message})
    
    # Get order details and construct payload
    try:
        package_ids = get_packageIds(order_id)
        order_title = get_orderTitle(order_id) + '_' + uuid.uuid4().hex
    except exc.SQLAlchemyError as e:
        return jsonify({'success': False, 'message': e.message})
    payload = {'order_title': order_title, 'aip_identifiers': package_ids}
    print payload
    
    # Post the order    
    resp = earkweb_session.post(SUBMIT_ORDER_URL, json = payload, headers = {'Referer':EARKWEB_LOGIN_URL})
    if (resp.status_code != 200):
        return jsonify({'success': False,
                        'message': 'There was a problem submitting the order to ' + SUBMIT_ORDER_URL + ' (status code: ' + resp.status_code + ')'})
    else:
        # Check the JSON response from earkweb
        json = resp.json() # dict
        if 'error' in json.keys():
            return jsonify({'success': False, 'message':json['error']})
        else:
            # Put data into DB
            try:
                Orders.update().where(Orders.c.orderId == order_id).values({'processId': json['process_id'], 'orderStatus': 'submitted'}).execute()
            except exc.SQLAlchemyError as e:
                return jsonify({'success': False, 'message': e.message})
            return jsonify({'success': True, 'message':'The order was successfully submitted'})
        


@app.route('/earkweb/updateAllOrderStatus', methods = ['GET'])
def update_all_order_status():

    # Get all orders in the DB
    try:
        orders = sql_query_to_dict(Orders.select(Orders.c.orderStatus == 'submitted').execute().fetchall(), 'orders')['orders'] # list of dictionaries
    except exc.SQLAlchemyError as e:
        return jsonify({'success': False, 'message': e.message})

    # Log in to earkweb     
    try:
        earkweb_session = get_session(ORDER_STATUS_URL)
    except Exception as e:
        return jsonify({'success': False, 'message': e.message})

    # Update the status for each order
    try:
        orders_updated_to_done = []
        for order in orders:
            done = get_earkweb_order_status(order, earkweb_session)
            if done:
                orders_updated_to_done.append(order['orderId'])
    except Exception as e:
        return jsonify({'success': False, 'message': e.message})
        
    return jsonify({'success': True, 'message': 'Status of the orders are updated in the DB', 'ordersUpdatedToDone': orders_updated_to_done})


        
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
    # return title+uuid.uuid4().hex # TODO: fix this
    return title

        


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


def get_earkweb_order_status(order_dict, session):
    """
        Parameters: order_dict of an order having orderStatus 'submitted'
        Return: True if the order is done and False otherwise
        
        Exceptions: raises exception in case of earkweb error or SQL error 
    """
    
    parameters = {'process_id': order_dict['processId']}
    resp = session.get(ORDER_STATUS_URL, params=parameters, headers = {'Referer':EARKWEB_LOGIN_URL})
    if (resp.status_code != 200):
        raise Exception('There was a querying the order status at ' + ORDER_STATUS_URL + ' (status code: ' + resp.status_code + ')')
    else:
        json = resp.json()
        dip_storage = json['dip_storage']
        if not dip_storage:
            return False
        else:
            # Put path to DIP into the DB and update the orderStatus in the DB
            try:
                Orders.update().where(Orders.c.orderId == order_dict['orderId']).values({'orderStatus': 'ready'}).execute()
                order_items = BelongsTo.select(BelongsTo.c.orderId == order_dict['orderId']).execute().fetchall()
                if order_items:
                    for item in order_items:
                        OrderItems.update().where(OrderItems.c.refCode == item['refCode']).values({'aipURI': dip_storage}).execute()
            except exc.SQLAlchemyError as e:
                raise e
            return True

