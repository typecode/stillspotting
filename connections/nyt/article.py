import sys
import urllib
import datetime
import hashlib

import connections.connection

import tornado.httpclient

class Article(connections.connection.Connection):
  
  listeners = {}
  default_pars = {
    'query':'',
    'facets':'geo_facet'
  }
  
  def __init__(self,settings):
    self.settings = settings
    self.api_key = self.settings['api_key']
    print str(self)
  
  def __repr__(self):
      return 'connections.nyt.article.Article()______________________________________\n\r\
| connections.nyt.article.Article Starting\n\r\
|   Connects to NYT Article API.\n\r\
|\n\r\
| connections.nyt.article.Article Settings:\n\r\
|  '+str(self.settings)+'\n\r\
|__________________________________________________________________\n\r'
  
  def process_request(self,req_id,pars):
    print 'connections.nyt.article.Article.process_request'
    http = tornado.httpclient.AsyncHTTPClient()
    
    for i in self.default_pars:
      if i not in pars:
        pars[i] = self.default_pars[i]
    
    pars['api-key'] = self.api_key
    
    url = 'http://api.nytimes.com/svc/search/v1/article?'
    url = url + urllib.urlencode(pars)
    print url
    
    def handle_response(response):
      try:
        json = tornado.escape.json_decode(response.body)
        self.emit_api_response(req_id,json)
      except TypeError:
        self.emit_api_response(req_id,[response.body])
      
    http.fetch(url,callback=handle_response)
  
  
  #DEPRECATED
  def getArticleByUrl(self,req_id,query_url):
    print 'Article.getArticleByUrl'
    http = tornado.httpclient.AsyncHTTPClient()
    
    pars = {
      'query':'url:'+query_url,
      'facets':'geo_facet',
      'api-key':self.article_api_key
    }
    url = 'http://api.nytimes.com/svc/search/v1/article?'
    url = url + urllib.urlencode(pars)
    
    def handle_response(response):
      print 'getArticleByUrl.on_response'
      json = tornado.escape.json_decode(response.body)
      self.emit(req_id,json)
    
    http.fetch(url,callback=handle_response)
  
  #DEPRECATED
  def listen(self,req_id,handler):
    print 'Article.listen'
    self.listeners[req_id] = handler
    return []
    
  #DEPRECATED
  def emit(self,req_id,data):
    print 'Article.emit'
    if req_id in self.listeners and self.listeners[req_id] is not None:
      self.listeners[req_id]({'articles':data})
  
  #DEPRECATED
  def stopListening(self,req_id):
    print 'Article.stopListening'
    if req_id in self.listeners:
      self.listeners[req_id] = None