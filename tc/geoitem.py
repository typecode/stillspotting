import sys
import urllib
import math

import google.geocoder

sys.path.append("lib")
import tornado.httpclient
import pymongo

database = pymongo.Connection('localhost', 27017).tc.geoitems

class geoitem:
  
  data = {
    loc:None
  }
  
  def __init__(self,lat,lng):
    print 'tc.geoitem()'
    if lat is None or lng is None:
      return False
    self.set_location(lat,lng)
    self.save()
    
  def set_location(self,lat,lng):
    if self.data.loc is None:
      self.data.loc = []
    self.data.loc[0] = lat
    self.data.loc[1] = lng
    
  def save(self):
    if self.data.loc is None:
      return False
    _id = database.insert(self.data)
    self.data._id = _id
    