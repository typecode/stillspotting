import sys
import urllib
import threading

sys.path.append("lib")
import tornado.httpclient

class Geocoder:
  
  queue = []
  request_timer = None
  
  def __init__(self):
    print 'Geocoder()'
    self.check_queue()
    
  def check_queue(self):
    print 'Geocoder.check_queue'
    if len(self.queue) > 0:
      self.request_timer = threading.Timer(0.5,self.geocode)
      self.request_timer.start()
    else:
      self.request_timer = threading.Timer(5,self.check_queue)
      self.request_timer.start()
    
  def add_to_queue(self,string,callback):
    print 'Geocoder.add_to_queue'
    self.queue.append([string,callback]);
    
  def geocode(self):
    print 'Geocoder.geocode'
    
    http = tornado.httpclient.AsyncHTTPClient()
    item = self.queue.pop(0)
    
    def handle_response(response):
      print 'Geocoder.geocode.handle_response'
      print str(response.body)
      self.check_queue()
      item[1](response)
    
    pars = {
      'address':item[0].replace(' ','+')
    }
    
    url = 'http://maps.googleapis.com/maps/api/geocode/json?'+urllib.urlencode(pars)
    
    print(str(url))
    
    http.fetch(url,callback=handle_response)
  