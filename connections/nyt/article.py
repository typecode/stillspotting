import sys
import urllib
import datetime
import hashlib

import connections.connection

import tornado.httpclient

import math
import threading

class Article(connections.connection.Connection):
  
#### START CONNECTION-SPECIFIC MEMBERS
  name = 'NYT Article API Connection'
  description = 'Connects to NYT Article API.'
  default_pars = {
    'query':{'accepted':'text string','default':None,'required':True,
      'more_info':'http://developer.nytimes.com/docs/read/article_search_api#h2-queries'},
    'begin_date':{'accepted':'YYYYMMDD','default':None,'required':False},
    'end_date':{'accepted':'YYYYMMDD','default':None,'required':False},
    'facets':{'accepted':'facets','default':None,'required':False,
      'more_info':'http://developer.nytimes.com/docs/read/article_search_api#h3-facets'},
    'fields':{'accepted':'facets','default':None,'required':False,
      'more_info':'http://developer.nytimes.com/docs/read/article_search_api#h2-responses'},
    'offset':{'accepted':'Number of Records to offset by.','default':0,'required':False},
    'rank':{'accepted':'newest, oldest, closest','default':'newest','required':False},
    'n_to_fetch':{'accepted':"Number of items to fetch",'default':10,'required':False}
  }
  example_query = {
    'query':'Adirondacks'
  }
#### END CONNECTION-SPECIFIC MEMBERS
  
  request_queue = []
  request_queue_stopped = True
  request_queue_timer = None
  
  def __init__(self,settings):
    self.settings = settings
    print str(self)
  
  def process_request(self,req_id,pars):
    print 'connections.nyt.article.Article.process_request'
    http = tornado.httpclient.AsyncHTTPClient()
    
    n_requests = 1
    if 'n_to_fetch' in pars and pars['n_to_fetch'] is not None and float(pars['n_to_fetch']) > 10:
      n_requests = math.ceil(float(pars['n_to_fetch'])/10.0)
    
    def handle_response(response):
      try:
        json = tornado.escape.json_decode(response.body)
        self.emit_api_response(req_id,json)
      except TypeError:
        self.emit_api_response(req_id,[response.body])
      self.run_queue()
    
    def generate_request(offset):
      request = {}
      request['pars'] = {}
      request['callback'] = handle_response
      for i in ['query','begin_date','end_date','facets','fields','offset','rank']:
        if i in pars:
          request['pars'][i] = pars[i]
          request['pars']['offset'] = offset
          request['pars']['api-key'] = self.settings['api_key']
      url = 'http://api.nytimes.com/svc/search/v1/article?'
      url = url + urllib.urlencode(request['pars'])
      request['url'] = url
      return request
    
    for i in range(0,int(n_requests)):
      if 'offset' in pars and pars['offset'] is not None:
        self.add_to_queue(generate_request(int(pars['offset'])+(i*10)))
      else:
        self.add_to_queue(generate_request(i*10))
  
  def add_to_queue(self,item):
    print 'connections.nyt.article.Article.add_to_queue'
    self.request_queue.append(item)
    if self.request_queue_stopped is True:
      self.run_queue()
      
  def run_queue(self):
    print 'connections.nyt.article.Article.run_queue'
    if self.request_queue_stopped is True:
      self.request_queue_stopped = False
    t = threading.Timer(1.0,self.make_request)
    t.start()
  
  def make_request(self):
    print 'connections.nyt.article.Article.make_request'
    http = tornado.httpclient.AsyncHTTPClient()
    if len(self.request_queue) == 0:
      self.request_queue_stopped = True
      return
    item = self.request_queue.pop(0)
    http.fetch(item['url'],callback=item['callback'])
  
  
  
  
  
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