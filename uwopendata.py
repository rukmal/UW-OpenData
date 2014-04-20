#!/usr/bin/env python

from flask import Flask, jsonify
import json

from uw import CourseCatalog
from uw import Directory

catalog = CourseCatalog()
directory = Directory()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
	programInfo = dict()
	programInfo['authors'] = 'Amit Burstein and Rukmal Weerawarana'
	programInfo['name'] = 'UW Open Data API'
	programInfo['version'] = '0.0.1'
	programInfo['project_url'] = 'http://uwopendata.herokuapp.com'
	programInfo['source_url'] = 'http://github.com/rukmal/UW-OpenData'
	programInfo['description'] = 'RESTful API for (hopefully) all UW online services'
	return jsonify(programInfo)

@app.route('/coursecatalog/<code>', methods=['GET'])
def courseget(code):
	return catalog.get_course(code)

@app.route('/directory/<searchquery>', methods=['GET'])
def directoryget(searchquery):
	return directory.search_directory(query)

if __name__ == '__main__':
	app.run(debug=True)