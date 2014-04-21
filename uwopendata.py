#!/usr/bin/env python

from flask import Flask, jsonify, request
import json

from uw import CourseCatalog
from uw import Directory

catalog = CourseCatalog()
directory = Directory()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
	programInfo = dict()
	programInfo['authors'] = 'Amit Burstein [http://amitburst.me] and Rukmal Weerawarana [http://rukmal.me]'
	programInfo['name'] = 'UW Open Data API'
	programInfo['version'] = '1.0.0'
	programInfo['project_url'] = 'http://uwopendata.herokuapp.com'
	programInfo['source_url'] = 'http://github.com/rukmal/UW-OpenData'
	programInfo['description'] = 'RESTful API for (hopefully) all UW online services'
	programInfo['license'] = 'MIT'
	programInfo['original_author'] = 'Karan Goel [http://github.com/karan]'
	return jsonify(programInfo)

@app.route('/coursecatalog/<code>', methods=['GET'])
def courseget(code):
	return catalog.get_course(code)

@app.route('/directory/', methods=['GET', 'POST'])
def directoryget():
	if request.method == 'GET':
		return 'intructions'
	elif request.method == 'POST':
		try:
			name = request.form['name']
			searchcriteria = request.form['searchcriteria']
			database = request.form['database']
			return directory.search_directory(name, searchcriteria, database)
		except:
			return jsonify({'error':'Invalid request'})

if __name__ == '__main__':
	app.run(debug=True)