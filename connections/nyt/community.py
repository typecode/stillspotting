import sys
import urllib
import math

import connections.google.geocoder
import connections.connection

sys.path.append("lib")
import tornado.httpclient

class Community(connections.connection.Connection):
  
#### START CONNECTION-SPECIFIC MEMBERS
  name = 'NYT Community API Connection'
  description = 'Connects to NYT Community API.'
  default_pars = {
    'url':{'accepted':'URL to Article Containing Comments','default':None, 'required':False},
    'offset':{'accepted':'integer offset from 0','default':str(0), 'required':False}
  }
  example_query = {
    'url':'http://www.nytimes.com/2010/12/03/opinion/03krugman.html',
    'offset':0
  }
  #DEPRECATED
  geocoder = connections.google.geocoder.Geocoder({})
  #DEPRECATED
  buffers = {}
#### END CONNECTION-SPECIFIC MEMBERS
    
  def process_request(self,req_id,pars={}):
    print 'connections.nyt.comments.Comments.process_request'
    http = tornado.httpclient.AsyncHTTPClient()
    pars['api-key'] = self.settings['api_key']
    
    print str(pars)
    
    url = 'http://api.nytimes.com/svc/community/v2/comments/url/exact-match.json?'
    url = url + urllib.urlencode(pars)
    
    def handle_response(response):
      try:
        json = tornado.escape.json_decode(response.body)
      except TypeError, ValueError:
        self.emit_api_response(req_id,[response.body])
        return
      self.emit_api_response(req_id,json)
      
    http.fetch(url,callback=handle_response)
  
  
  
  #DEPRECATED
  def getCommentsForUrl(self,req_id,query_url):
    print 'Comments.getCommentsForUrl'
    http = tornado.httpclient.AsyncHTTPClient()
    requests = []
    no_comments_fetched = 0
    def generate_url(offset):
      print 'getCommentsForUrl.generate_url'
      pars = {
        'url':query_url,
        'offset':str(offset),
        'api-key':self.api_key
      }
      url = 'http://api.nytimes.com/svc/community/v2/comments/url/exact-match.json?'
      url = url + urllib.urlencode(pars)
      return url
    def handle_initial_response(response):
      print 'getCommentsForUrl.handle_initial_response'
      json = tornado.escape.json_decode(response.body)
      print str(json[u'results'][u'totalCommentsFound'])
      n_requests = math.ceil(json[u'results'][u'totalCommentsFound']/25)
      if n_requests == 0:
        n_requests = 1
      for i in range(n_requests):
        requests.append(generate_url(i*25))
      http.fetch(requests.pop(0),callback=handle_subsequent_response)
    def handle_subsequent_response(response):
      print 'getCommentsForUrl.handle_subsequent_response'
      json = tornado.escape.json_decode(response.body)
      for c in json[u'results'][u'comments']:
        self.geocode_comment(req_id,c)
      if len(requests) > 0:
        http.fetch(requests.pop(0),callback=handle_subsequent_response)
    http.fetch(generate_url(0),callback=handle_initial_response)
  
  #DEPRECATED     
  def geocode_comment(self,req_id,comment):
    print 'Comments.geocodeComment'
    def comment_geocoded(latlng):
      print 'Comments.geocodeComment.comment_geocoded'
      comment[u'latlng'] = latlng
      self.emit(req_id,comment)
    self.geocoder.add_to_queue(comment[u'location'],comment_geocoded)
  
  #DEPRECATED
  def listen(self,req_id,callback):
    print 'Comments.listen'
    if req_id in self.buffers and self.buffers[req_id] is not None:
      if len(self.buffers[req_id]) > 0:
        return {'comments':self.buffers[req_id]}
    self.listeners[req_id] = callback
    return []
  
  #DEPRECATED
  def emit(self,req_id,data):
    print 'Comments.emit'
    if req_id in self.listeners and self.listeners[req_id] is not None:
      if isinstance(data,list) is False:
        data = [data]
      self.listeners[req_id]({'comments':data})
    elif req_id in self.buffers and self.buffers[req_id] is not None:
      self.buffers[req_id].append(data)
  
  #DEPRECATED
  def stopListening(self,req_id):
    print 'Comments.stopListening'
    if req_id in self.listeners:
      self.listeners[req_id] = None
    self.buffers[req_id] = []