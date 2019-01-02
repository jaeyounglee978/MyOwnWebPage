import sys

from flask import Flask
from flask import request
from flask import render_template

from parser import *

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def hello_web():
    return render_template('top.html')


@app.route('/test')
def test():
	return "Hello, World!"


@app.route('/my_info')
def my_info():
	c = [[1, [2, 3, 4]]]

	cvData = cvParser("static/cv.txt")

	return render_template('my_info.html', items=cvData)

@app.route('/daily-saechi')
def saechi():

	return render_template('top.html')