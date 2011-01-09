import threading
import sys
import time
import json

import connections.connection

sys.path.append("lib")
import tornado.httpclient
import pymongo

class Newswire(connections.connection.Connection):
  
  watchers = []
  
  timer = None
  last_offset = 0
  
  def __init__(self,settings):
    print 'nyt.NewsWire()___________________________________________________________'
    if 'api_key' not in settings:
      print ' | NewsWire Missing Setting: api_key'
      print ' |____________________________________________________________________'
      return
    print ' | nyt.NewsWire Connection Starting'
    print ' |'
    print ' | nyt.NewsWire Connection Settings:'
    print ' |  '+str(settings)
    print ' |___________________________________________________________________'
    print ''
    self.api_key = settings['api_key']
    self.mongo_conn = pymongo.Connection('localhost', 27017)
    self.db = self.mongo_conn['nyt']
  
  def get_todays_wires(self):
    print 'NewsWire.get_todays_wires'
    
    begin_today = time.strftime('%Y-%m-%dT00:00:00-00:00')
    end_today = time.strftime('%Y-%m-%dT23:59:99-00:00')
    
    wires = self.db.articles\
      .find({"updated_date": {'$gt': begin_today, '$lt': end_today}})\
      .sort('updated_date',pymongo.DESCENDING)
    out = []
    for w in wires:
      out.append(w)
    return out
  
  
  def make_request(self):
    print 'NewsWire.make_request'
    http = tornado.httpclient.AsyncHTTPClient()
    url = "http://api.nytimes.com/svc/news/v3/content/nyt/all?api-key="+api_key
    http.fetch(url,callback=self.on_response)
  
  def on_response(self,response):
    print 'NewsWire.on_response'
    if response.error: raise tornado.web.HTTPError(500)
    output = []
    json = tornado.escape.json_decode(response.body)
    for r in json['results']:
      if self.db.articles.find_one({'url':r['url']}):
        print 'article already stored'
        continue
      self.db.articles.insert(r)
      output.append(r)
    
    self.emit(output)
    self.timer = threading.Timer(10,self.make_request)
    self.timer.start()
  
  def watch(self,callback):
    print 'NewsWire.watch'
    self.watchers.append(callback)
    
  def emit(self,data):
    print 'NewsWire.emit'
    for w in self.watchers:
      w(data)
    self.watchers = []