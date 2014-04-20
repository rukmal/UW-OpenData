import json
from bs4 import BeautifulSoup
import requests

class Directory(object):
	'''
	Author: Rukmal Weerawarana
	Description: API to get data from the University of Washington official directory.
	'''
	
	def __init__(self):
		self.DIRECTORY_URL = 'http://washington.edu/home/peopledir'

	def search_directory(self, name, querytype, database, length):
		'''Function to search the University of Washington directory.
		Args:
			name {String}
				Name of the person
			type {String}
				Field that should be searched
				Valid options:
					name - Name of the person
					dept - Department the person is in
					mail - Email of the person
					box - Box of the person
					phone - Phone number of the person
			database {String}
				Database in which the query should be run in.
				Valid options:
					both - Student and Faculty/Staff listings
					staff - Faculty/Staff listings
					student - Student listings
			length {String}
				Length of listing to be returned (i.e. summary or full)
				Valid options:
					sum - Summary listing
						Note: Summary listing returns the name, phone number (if any)
							and email
					full - Full listing
						Note: Full listing returns the name, phone number (if any),
							class standing, department and email
		Returns:
			JSON array of all results found for a given search
		Raises:
			ValueError
			ConnectionError
			HTTPError
			Timeout
		'''
		# Constructing the HTTP request
		httprequest = dict()
		httprequest['term'] = name
		httprequest['method'] = querytype
		httprequest['whichdir'] = database
		httprequest['length'] = length

		# sending POST request to directory
		data = requests.post(self.DIRECTORY_URL, params=httprequest)
		bsdata = BeautifulSoup(data.text)
		if length == 'full':
			persondata = bsdata.find_all('div', attrs={'class':'indent long'})
			print persondata
		elif length == 'sum':
			persondata = bsdata.find_all('table', attrs={'class':'table table-bordered table-striped table-condensed'})
			print persondata
		else:
			raise ValueError
		return None