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

	def findName(self):
		httprequest = {'term':'', 'method':'name', 'whichdir':'both', 'length':'sum'}
		data = requests.post(self.DIRECTORY_URL, params=httprequest)
		print data.text