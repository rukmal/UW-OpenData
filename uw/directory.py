import json
import re
from bs4 import BeautifulSoup
import requests
import vobject

class Directory(object):
	'''
	Author: Rukmal Weerawarana
	Description: API to get data from the University of Washington official directory.
	'''
	
	def __init__(self):
		# Note: Trailing backslash is REQUIRED
		self.DIRECTORY_URL = 'http://washington.edu/home/peopledir/'

	def __prettifyName(self, name):
		'''Function to prettify and standardize format of a name
		eg: 
		Args:
			name {str}
				Name of the person
		Returns:
			{str}	Prettified version of the input name
		'''

	def search_directory(self, name, querytype, database):
		'''Function to search the University of Washington directory.
		Args:
			name {str}
				Name of the person
			queryType {str}
				Field that should be searched
				Valid options:
					name - Name of the person
					dept - Department the person is in
					mail - Email of the person
					box - Box of the person
					phone - Phone number of the person
			database {str}
				Database in which the query should be run in.
				Valid options:
					both - Student and Faculty/Staff listings
					staff - Faculty/Staff listings
					student - Student listings
		Returns:
			{str}	JSON array of all results found for a given search
		Raises:
			ValueError
			ConnectionError
			HTTPError
			TimeoutError
		'''
		# Constructing the HTTP request
		httprequest = dict()
		httprequest['term'] = name
		httprequest['method'] = querytype
		httprequest['whichdir'] = database
		# Type of listing. Options: full, sum. Note: will NOT work with summary listing
		httprequest['length'] = 'full'

		# Sending POST request to directory
		data = requests.post(self.DIRECTORY_URL, params=httprequest)

		# Parsing result with BeautifulSoup
		bsdata = BeautifulSoup(data.text)

		output = []

		vcardurls = bsdata.find_all('form', attrs={'class':'vcard'})
		for vcardurl in vcardurls:
			# Constructing HTTP post request for vcards
			vcardrequest = dict()
			requestdata = vcardurl.find_all('input', attrs={'type':'hidden', 'name':'dn'})
			vcardrequest['dn'] = requestdata[0]['value']
			vcard = requests.post(self.DIRECTORY_URL + vcardurl['action'], params=vcardrequest)
			# Isolating vCard, parsing using vobject
			parsedvcard = vobject.readOne(vcard.content)
			persondata = dict()
			persondata['name'] = parsedvcard.fn.value # Extracting full name from vCard
			# Extracting email from vCard
			try:
				persondata['email'] = parsedvcard.email.value
			except:
				persondata['email'] = None
			# Adding person to the output array
			output.append(persondata)
		# JSONifying and returning the output
		return json.dumps(output)