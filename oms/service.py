from flask import jsonify
from oms import app

@app.route('/test', methods = ['GET'])
def test():
    return jsonify({'foo': 'bar'})