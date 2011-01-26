import sys
import urllib
import datetime
import hashlib
import csv

import connections.connection

import tornado.httpclient

import math
import threading

class Article(connections.connection.Connection):
  
#### START CONNECTION-SPECIFIC MEMBERS
  name = 'NYT Article API Connection'
  description = 'Connects to NYT Article API. This connection supports CSV output.'
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
    'n_to_fetch':{'accepted':"Number of items to fetch",'default':10,'required':False},
    'output':{'accepted':'json, csv','default':'csv','required':'true'}
  }
  example_query = {
    'query':"abstract:noise geo_facet:[NEW YORK CITY]",
    'fields':"title,abstract,geo_facet",
    'output':'csv',
    'n_to_fetch':10
  }
#### END CONNECTION-SPECIFIC MEMBERS
  
  request_queue = []
  request_queue_stopped = True
  request_queue_timer = None
  
  def process_request(self,apirequest):
    print 'connections.nyt.article.Article.process_request'
    http = tornado.httpclient.AsyncHTTPClient()
    
    if 'n_to_fetch' in apirequest.pars and apirequest.pars['n_to_fetch'] is not None and float(apirequest.pars['n_to_fetch']) > 10:
      apirequest.run['n_requests'] = math.ceil(float(apirequest.pars['n_to_fetch'])/10.0)
    
    print apirequest.pars['n_to_fetch']
    print apirequest.run['n_requests']
    
    def handle_response(response):
      print 'connections.nyt.article.Article.process_request.handle_response'
      try:
        data = tornado.escape.json_decode(response.body)
      except TypeError, ValueError:
        apirequest.handle_error('NYT Error')
        self.run_queue()
        return
      apirequest.handle_data(data)
      self.run_queue()
    
    def generate_request(offset):
      print 'connections.nyt.article.Article.process_request.generate_request'
      request = {}
      request['pars'] = {}
      request['callback'] = handle_response
      for i in ['query','begin_date','end_date','facets','fields','offset','rank']:
        if i in apirequest.pars:
          request['pars'][i] = apirequest.pars[i]
      request['pars']['offset'] = offset
      request['pars']['api-key'] = self.settings['api_key']
      url = 'http://api.nytimes.com/svc/search/v1/article?'
      url = url + urllib.urlencode(request['pars'])
      
      print str(url)
      
      request['url'] = url
      return request
    
    for i in range(0,int(apirequest.run['n_requests'])):
      if 'offset' in apirequest.pars and apirequest.pars['offset'] is not None:
        self.add_to_queue(generate_request(int(apirequest.pars['offset'])+(i)))
      else:
        self.add_to_queue(generate_request(i))
  
  ################### END process_request
  
  @staticmethod
  def csv(data):
    print 'connections.nyt.article.Article.csv'
    generate_header = False
    header = None
    output = ""
    for i in data:
      if u'results' in i:
        for j in i[u'results']:
          row = []
          if header is None:
              generate_header = True
              header = []
          for k in j:
            if generate_header is True:
              header.append(str(k))
            row.append('"'+str(j[k])+'"')
          output = output + str('\t'.join(row)) + '\n'
          generate_header = False
    output = str('\t'.join(header)) + '\n' + output
    return output
  
  def add_to_queue(self,item):
    print 'connections.nyt.article.Article.add_to_queue'
    self.request_queue.append(item)
    if self.request_queue_stopped is True:
      self.run_queue()
      
  def run_queue(self):
    print 'connections.nyt.article.Article.run_queue'
    if len(self.request_queue) == 0:
      self.request_queue_stopped = True
      print 'connections.nyt.article.Article.run_queue[Queue Stopped]'
      return
    elif self.request_queue_stopped is True:
      print 'connections.nyt.article.Article.run_queue[Queue Started]'
      self.request_queue_stopped = False
    t = threading.Timer(1.0,self.make_request)
    t.start()
  
  def make_request(self):
    print 'connections.nyt.article.Article.make_request'
    http = tornado.httpclient.AsyncHTTPClient()
    item = self.request_queue.pop(0)
    http.fetch(item['url'],callback=item['callback'])