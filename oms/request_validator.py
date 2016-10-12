import re
from flask import jsonify

class OrderIdValidator(object):
    
    def __init__(self, order_id):
        self.error_message = None
        self.order_id = order_id
        
    def is_order_id_valid(self):
        """
            Returns True if the value is a UUID in Hex format, 
            e.g. 2d4df07b37ca4d3a847e262097742a8a and False otherwise
        """
        
        if not self.order_id:
            self.error_message = jsonify({'status':'error', 'message': 'orderId parameter missing'})
            return False
        if not re.match('^[a-f0-9]{32}$', self.order_id):
            self.error_message = jsonify({'status': 'error', 'message': 'orderId must be set to (hex) UUID'})
            return False
        return True

    def get_error_json(self):
        return self.error_message