#!/usr/bin/env python

from flask import Flask, jsonify
from flask.ext.restful import Resource, Api, reqparse
import json

from uw import CourseCatalog
from uw import Directory

catalog = CourseCatalog()
directory = Directory()

app = Flask(__name__)
api = Api(app)

class LandingPage(Resource):
	def get(self):
		programInfo = dict()
		programInfo['author'] = 'Rukmal Weerawarana'
		programInfo['author_url'] = 'http://rukmal.me/'
		programInfo['name'] = 'UW Open Data API'
		programInfo['version'] = '1.0.0'
		programInfo['project_url'] = 'http://uwopendata.herokuapp.com/'
		programInfo['source_url'] = 'http://github.com/rukmal/UW-OpenData/'
		programInfo['description'] = 'RESTful API for (hopefully) all UW online services'
		programInfo['license'] = 'MIT'
		programInfo['original_author'] = 'Karan Goel [http://github.com/karan/]'
		return programInfo

class CourseCatalog(Resource):
	def get(self, code):
		return catalog.get_course(code)

class Directory(Resource):
	def get(self):
		return 'instructions'

	def post(self):
		args = parser.parse_args()
		print args
		try:
			return directory.search_directory(args['search'], args['searchcriteria'], args['database'])
		except:
			return {'error':'Invalid request'}

# Adding the landing page
api.add_resource(LandingPage, '/')
# Adding the course catalog
api.add_resource(CourseCatalog, '/coursecatalog/<string:code>')
# Adding the directory. Using reqparse to define the default arguments
parser = reqparse.RequestParser()
parser.add_argument('search', type=str, help='Search string to be run in the database')
parser.add_argument('searchcriteria', type=str, help='Criteria of the search. Possible options: name, dept, mail, box or phone')
parser.add_argument('database', type=str, help='Databse to search. Possible options: student, staff, both')
api.add_resource(Directory, '/directory/')

if __name__ == '__main__':
	app.run(debug=True)
