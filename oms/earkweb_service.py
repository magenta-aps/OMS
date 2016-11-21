from oms import app
from flask import jsonify, request, abort
import requests
from db_model import *
from sqlalchemy import exc
from sqlalchemy.sql import and_, or_
import time
from request_validator import OrderIdValidator
import uuid

EARKWEB_LOGIN_URL = 'http://localhost:8000/earkweb/admin/login/'
SUBMIT_ORDER_URL = 'http://localhost:8000/earkweb/search/submit_order/' 
ORDER_STATUS_URL = 'http://localhost:8000/earkweb/search/jobstatus/'
PREPARE_DIP = 'http://localhost:8000/earkweb/search/prepareDIPWorkingArea'
CREATE_DIP = 'http://localhost:8000/earkweb/search/createDIP'

# TODO: do not hard code username and password 
USERNAME = 'eark'
PASSWORD = 'eark'


@app.route('/earkweb/createDIP', methods = ['POST'])
def create_dip():
    """
        Must receive JSON like this:
        {
            "orderId": "c1b1c16e-2c00-474f-b99b-42019b3eaeed"
        }
    """

    # TODO: refactor (code duplication)
    # Check the posted JSON
    mandatory_keys = ['orderId']
    if not request.json:
        abort(400)
    if not json_keys_valid(request.json, mandatory_keys):
        return jsonify({'success': False, 'message': 'Request JSON must contain the keys ' + ', '.join(mandatory_keys)}), 500
    order_id = request.json['orderId']
    validator = OrderIdValidator(order_id)
    if not validator.is_order_id_valid():
        return validator.get_error_json()

    # Return error if the order does not exists or is not "processing"
    try:
        order = Orders.select(Orders.c.orderId == order_id).execute().first()
    except exc.SQLAlchemyError as e:
        return jsonify({'success': False, 'message': e.message}), 500
    if not order:
        return jsonify({'success': False, 'message': 'No orders with orderId: ' + order_id}), 404
    else:
        # Check if the orderStatus is "processing"
        order_dict = sql_query_to_dict(order)
        order_status = order_dict['orderStatus']
        if not order_status == 'processing':
            return jsonify({'success': False, 'message': 'The order must have status \'processing\' before DIP the creation can be initiated'})
    
    # Login in to earkweb and get cookies
    try:
        earkweb_session = get_session(EARKWEB_LOGIN_URL)
    except Exception as e:
        return jsonify({'success': False, 'message': e.message}), 500
    
    # Get order details and construct payload
    try:
        process_id = get_order_value(order_id, 'processId')
    except exc.SQLAlchemyError as e:
        return jsonify({'success': False, 'message': e.message}), 500
    payload = {'process_id': process_id}
    
    resp = earkweb_session.post(CREATE_DIP, json = payload, headers = {'Referer':EARKWEB_LOGIN_URL})
    if resp.status_code == 201:
        json = resp.json()
        print json
        # Put data into DB
        try:
            Orders.update().where(Orders.c.orderId == order_id).values({'jobId': json['jobid'], 'orderStatus': 'packaging'}).execute()
        except exc.SQLAlchemyError as e:
            return jsonify({'success': False, 'message': e.message}), 500
        return jsonify(resp.json()), 201
    else:
        return jsonify(resp.json()), resp.status_code



@app.route('/earkweb/submitOrder', methods = ['POST'])
def submit_order():
    """
    Must receive JSON like this
    {
        "orderId": "0924e01714244d9693cc3b1774e6b88e"
    }
    where orderId is the unique id of the order
    """

    # TODO: refactor (code duplication)
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
    else:
        # Check that orderStatus is "new"
        order_status = sql_query_to_dict(order)['orderStatus']
        if order_status != 'new':
            return jsonify({'success': False, 'message': 'Can only submit order with status \'new\''}) 

    # Login in to earkweb and get cookies
    # TODO: should be able to reuse a session
    try:
        earkweb_session = get_session(EARKWEB_LOGIN_URL)
    except Exception as e:
        return jsonify({'success': False, 'message': e.message})
    
    # Get order details and construct payload
    try:
        package_ids = get_packageIds(order_id)
        order_title = get_order_value(order_id, 'title') + '_' + uuid.uuid4().hex
    except exc.SQLAlchemyError as e:
        return jsonify({'success': False, 'message': e.message})
    payload = {'order_title': order_title, 'aip_identifiers': package_ids}
    
    # Post the order    
    resp = earkweb_session.post(SUBMIT_ORDER_URL, json = payload, headers = {'Referer':EARKWEB_LOGIN_URL})
    if (resp.status_code != 200):
        return jsonify({'success': False,
                        'message': 'There was a problem submitting the order to ' + SUBMIT_ORDER_URL + ' (status code: ' + resp.status_code + ')'})
    else:
        # Check the JSON response from earkweb
        json = resp.json() # dict
        if 'error' in json.keys():
            # Set order status to error in the DB 
            try:
                Orders.update().where(Orders.c.orderId == order_id).values({'orderStatus': 'error'}).execute()
            except exc.SQLAlchemyError as e:
                return jsonify({'success': False, 'message': e.message})
            return jsonify({'success': False, 'message':json['error']})
        else:
            # Update order status in the DB
            try:
                Orders.update().where(Orders.c.orderId == order_id).values({'processId': json['process_id']}).execute()
            except exc.SQLAlchemyError as e:
                return jsonify({'success': False, 'message': e.message})
            
            # Initiate the first three earkweb AIP to DIP conversion tasks
            payload = {'process_id': json['process_id']}
            resp2 = earkweb_session.post(PREPARE_DIP, json = payload, headers = {'Referer':EARKWEB_LOGIN_URL})
            json2 = resp2.json()
            if resp2.status_code == 201:
                # Update jobId in the DB
                try:
                    Orders.update().where(Orders.c.orderId == order_id).values({'jobId': json2['jobid'], 'orderStatus':'submitted'}).execute()
                except exc.SQLAlchemyError as e:
                    return jsonify({'success': False, 'message': e.message})
                
                return jsonify({'success': True, 'message':'The order was successfully submitted'})
            else:
                # Set order status to error in the DB 
                try:
                    Orders.update().where(Orders.c.orderId == order_id).values({'orderStatus': 'error'}).execute()
                except exc.SQLAlchemyError as e:
                    return jsonify({'success': False, 'message': e.message})
                return jsonify(resp.json()), resp.status_code


@app.route('/earkweb/updateAllOrderStatus', methods = ['GET'])
def update_all_order_status():

    # Get all orders in the DB that are not new, open or ready
    try:
        orders = sql_query_to_dict(Orders.select(and_(Orders.c.orderStatus != 'new', Orders.c.orderStatus != 'open', Orders.c.orderStatus != 'ready')).execute().fetchall(), 'orders')['orders'] # list of dictionaries
    except exc.SQLAlchemyError as e:
        return jsonify({'success': False, 'message': e.message}), 500

    # Log in to earkweb     
    try:
        earkweb_session = get_session(EARKWEB_LOGIN_URL)
    except Exception as e:
        return jsonify({'success': False, 'message': e.message}), 500

    # Update the status for each order
    orders_with_changed_status = []
    orders_where_status_request_failed = []
    for order in orders:
        order_id = order['orderId']
        print order_id
        r = get_earkweb_order_status(order, earkweb_session)
        status_code = r[1]
        json = r[0]
        try:
            if status_code == 200:
                status = json['message']
                old_order_status = get_order_value(order_id, 'orderStatus')
                if status == 'DIP preparation finished.':
                    new_order_status = 'processing'
                elif status == 'DIP creation finished successfully.':
                    new_order_status = 'ready'
                if old_order_status != new_order_status:
                    Orders.update().where(Orders.c.orderId == order_id).values({'orderStatus': new_order_status}).execute()
                    orders_with_changed_status.append(order_id)
            else:
                Orders.update().where(Orders.c.orderId == order_id).values({'orderStatus': 'error'}).execute()
                orders_where_status_request_failed.append([order_id, json])
        except exc.SQLAlchemyError as e:
            return jsonify({'success': False, 'message': e.message}), 500
        
    if len(orders_where_status_request_failed) == 0:
        # All order statuses updated correctly
        return jsonify({'success': True, 'message': 'Status of the orders are updated in the DB',
                        'ordersUpdated': orders_with_changed_status,
                        'ordersWhereStatusRequestFailed': orders_where_status_request_failed})
    else:
        # At least one order status could not be updated correctly
        return jsonify({'success': False, 'message': 'Not all orders could be updated',
                        'ordersUpdated': orders_with_changed_status,
                        'ordersWhereEarkwebStatusRequestFailed': orders_where_status_request_failed})
            


        
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

        
    
def get_order_value(order_id, key):
    """Get the order title (string) of the order with the given orderId"""
    value = sql_query_to_dict(Orders.select(Orders.c.orderId == order_id).execute().first())[key]
    return value

        


def json_keys_valid(json, keys):
    """Return True if json (dict) contains the mandatory keys (list)"""
    for key in keys:
        if not key in json.keys():
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
        Get the order status for a single order
    """
    url = ORDER_STATUS_URL + order_dict['jobId']
    resp = session.get(url, headers = {'Referer':EARKWEB_LOGIN_URL})
    return resp.json(), resp.status_code
