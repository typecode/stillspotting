import sys
import urllib
import threading

sys.path.append("lib")
import tornado.httpclient
import pymongo

class Geocoder:
  
  local_queue = []
  local_stopped = True
  remote_queue = []
  remote_stopped = True
  request_timer = None
  
  def __init__(self,settings={}):
    print 'google.Geocoder()___________________________________________________________'
    print ' | google.Geocoder Connection Starting'
    print ' | google.Geocoder Connection Settings:'
    print ' |  '+str(settings)
    print ' |__________________________________________________________________'
    print ''
    self.mongo_conn = pymongo.Connection('localhost', 27017)
    self.db = self.mongo_conn['google']
    
  def add_to_queue(self,string,callback):
    print 'Geocoder.add_to_queue'
    item = [string,callback]  
    self.add_to_local(item)
    
  def add_to_local(self,item):
    print 'Geocoder.add_to_local'
    self.local_queue.append(item)
    if self.local_stopped is True:
      self.local_stopped = False
      self.geocode_local()
    
  def add_to_remote(self,item):
    print 'Geocoder.add_to_remote'
    self.remote_queue.append(item)
    if self.remote_stopped is True:
      self.remote_stopped = False
      t = threading.Timer(1.0,self.geocode_remote)
      t.start()
    
  def geocode_local(self):
    print 'Geocoder.geocode_local'
    if len(self.local_queue) == 0:
      self.local_stopped = True
      return
    item = self.local_queue.pop(0)
    local = self.db.geo.find_one({'query':item[0]})
    if local is not None:
      item[1](local)
    else:
      self.add_to_remote(item)
    self.geocode_local()
    
  def geocode_remote(self):
    print 'Geocoder.geocode_remote'
    http = tornado.httpclient.AsyncHTTPClient()
    if len(self.remote_queue) == 0:
      self.remote_stopped = True
      return
    item = self.remote_queue.pop(0)
    def handle_response(response):
      print 'Geocoder.geocode.handle_response'
      json = tornado.escape.json_decode(response.body)
      doc = {
        'query':item[0],
        'response':json
      }
      self.db.geo.insert(doc)
      item[1](json)
      t = threading.Timer(1.0,self.geocode_remote)
      t.start()
    pars = {
      'address':item[0].replace(' ','+'),
      'sensor':'false'
    }
    url = 'http://maps.googleapis.com/maps/api/geocode/json?'+urllib.urlencode(pars)
    http.fetch(url,callback=handle_response)