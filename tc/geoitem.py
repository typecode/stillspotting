import sys
import urllib
import math

sys.path.append("lib")
import tornado.httpclient
import pymongo

database = pymongo.Connection('localhost', 27017).tc.geoitems
database.ensureIndex( { loc : "2d" } )

class geoitem:

  def __init__(self,lat,lng):
    print 'tc.geoitem()'
    if lat is None or lng is None:
      return False
    self.data = {
      'loc':None
    }
    self.set_location(lat,lng)
    self.save()
    
  def get_id(self):
    if '_id' in self.data:
      return self.data['_id']
    
  def set_location(self,lat,lng):
    if 'loc' not in self.data or self.data['loc'] is None:
      self.data['loc'] = []
    self.data['loc'].append(lat)
    self.data['loc'].append(lng)
    
  def save(self):
    if 'loc' not in self.data:
      return False
    _id = database.insert(self.data)
    self.data['_id'] = _id
    