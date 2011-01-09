import sys
import urllib
import math

sys.path.append("lib")
import tornado.httpclient
import pymongo

class api_query:

  def __init__(self,lat,lng):
    print 'tc.api_query()'
    self.results = None