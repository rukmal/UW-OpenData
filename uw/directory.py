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

	def search_directory(self, name, searchcriteria, database):
		'''Function to search the University of Washington directory.
		Args:
			name {str}
				Name of the person
			searchcriteria {str}
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
			{str}	JSON array of all results found for a given search.
			The JSON array will have the following possible fields.
			[
				{
					"name": <name>,
					"email": <email>,
					"organization": <organization>,
					"department": <department>,
					"phone": <phone>,
					"title": <title>,
					"addresss": <address>
				}
			]
		Raises:
			ValueError
			ConnectionError
			HTTPError
			TimeoutError
		'''
		# Constructing the HTTP request
		httprequest = dict()
		httprequest['term'] = name
		httprequest['method'] = searchcriteria
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
			# Extracting full name from vCard and prettifying
			persondata['name'] = parsedvcard.fn.value.title()
			# Extracting email from vCard
			try:
				persondata['email'] = parsedvcard.email.value
			except:
				pass
			# Extracting organization data from vCard
			orgdata = list(parsedvcard.org.value)
			try:
				persondata['organization'] = orgdata[0]
			except:
				pass
			# Extracting department department info from vCard
			try:
				persondata['department'] = orgdata[1]
			except:
				pass
			# Extracting title information from vCard
			try:
				persondata['title'] = parsedvcard.title.value
			except:
				pass
			# Extracting phone number information from vCard
			try:
				persondata['phone'] = parsedvcard.tel.value
			except:
				pass
			# Extracting address information from vCard
			try:
				persondata['address'] = str(parsedvcard.adr.value).replace('\n', ';')
			except:
				pass
			# Adding person to the output array
			print parsedvcard
			output.append(persondata)
		# JSONifying and returning the output
		return json.dumps(output, separators=(',',':'))