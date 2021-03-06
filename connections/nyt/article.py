import sys
import urllib
import datetime
import hashlib
import csv

import connections.connection
import connections.queue

import tornado.httpclient

import math
import threading

class Article(connections.connection.Connection,connections.queue.Queue):
  
#### START CONNECTION-SPECIFIC MEMBERS
  name = 'NYT Article API Connection'
  description = 'With the Article Search API, you can search New York Times articles from 1981 to today, retrieving headlines, abstracts, lead paragraphs and links to associated multimedia. Along with standard keyword searching, the API also offers faceted searching. The available facets include Times-specific fields such as sections, taxonomic classifiers and controlled vocabulary terms (names of people, organizations and geographic locations). Supports CSV Output.'
  source = 'http://developer.nytimes.com/docs/article_search_api/'
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
  
  def process_request(self,apirequest):
    print 'connections.nyt.article.Article.process_request'
    http = tornado.httpclient.AsyncHTTPClient()
    
    if 'n_to_fetch' in apirequest.pars and apirequest.pars['n_to_fetch'] is not None and float(apirequest.pars['n_to_fetch']) > 10:
      apirequest.run['n_requests'] = int(math.ceil(float(apirequest.pars['n_to_fetch'])/10.0))
    
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
  
  @staticmethod
  def csv(data):
    print 'connections.nyt.article.Article.csv'
    header = []
    rows = []
    
    for i in data:
      if u'results' in i:
        for j in i[u'results']:
          row = list("" for i in range(0,100))
          for k in j:
            try:
              hi = header.index(k)
            except ValueError:
              header.append(unicode(k))
              hi = len(header) - 1
            row[hi] = u'"'+unicode(j[k])+u'"'
          rows.append(row)
    output = unicode(u'\t'.join(header))
    for i in rows:
      i = i[0:len(header)]
      output = output + '\n' + unicode(u'\t'.join(i))
    return output
  
  ################### END process_request
  