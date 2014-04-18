import json
from bs4 import BeautifulSoup
import urllib2
import urllib3

class Directory(object):
'''
Author: Rukmal Weerawarana
Description: API to get data from the University of Washington official directory.
'''
	def __init__(self):
		self.DIRECTORY_URL = 'http://washington.edu/home/peopledir'