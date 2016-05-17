__author__ = 'lanre'

from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Lanre'}
    return render_template('index.html', title='E-Ark', user=user)