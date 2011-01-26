import sys
import urllib
import math
import threading

import connections.google.geocoder
import connections.connection

sys.path.append("lib")
import tornado.httpclient

class Search(connections.connection.Connection):
  
#### START CONNECTION-SPECIFIC MEMBERS
  name = 'Twitter Search API Connection'
  description = 'Connects to Twitter Search API. Supports CSV Output.'
  source = 'http://dev.twitter.com/doc/get/search'
  default_pars = {
    'q':{'accepted':'Search query.','default':None,'required':True},
    'geocode':{'accepted':'Returns tweets by users located within a given radius of the given latitude/longitude. The location is preferentially taking from the Geotagging API, but will fall back to their Twitter profile. The parameter value is specified by "latitude,longitude,radius", where radius units must be specified as either "mi" (miles) or "km" (kilometers). Note that you cannot use the near operator via the API to geocode arbitrary locations; however you can use this geocode parameter to search near geocodes directly.','default':None, 'required':False},
    'n_to_fetch':{'accepted':"Number of rows to fetch",'default':15,'required':False},
    'output':{'accepted':'json, csv','default':'csv','required':'true'}
  }
  example_query = {
    'q':'noise',
    'geocode':'40.716667,-74,5mi',
    'n_to_fetch':30,
    'output':'csv'
  }
#### END CONNECTION-SPECIFIC MEMBERS
    
  def process_request(self,apirequest):
    print 'connections.twitter.search.Search.process_request'
    http = tornado.httpclient.AsyncHTTPClient()
    
    if 'n_to_fetch' in apirequest.pars and apirequest.pars['n_to_fetch'] is not None and float(apirequest.pars['n_to_fetch']) > 10:
      apirequest.run['n_requests'] = int(math.ceil(float(apirequest.pars['n_to_fetch'])/15.0))
    
    def handle_response(response):
      print 'connections.twitter.search.Search.process_request.handle_response'
      try:
        data = tornado.escape.json_decode(response.body)
      except TypeError, ValueError:
        apirequest.handle_error('Twitter Error')
        self.run_queue()
        return
      apirequest.handle_data(data)
      if apirequest.run['n_requests_received'] < apirequest.run['n_requests']:
        self.add_to_queue({
          'url':'http://search.twitter.com/search.json'+data[u'next_page'],
          'callback':handle_response
        })
      self.run_queue()
    
    request_pars = self.handle_pars(apirequest.pars)
    url = 'http://search.twitter.com/search.json?' + urllib.urlencode(request_pars)
    
    self.add_to_queue({
      'url':url,
      'callback':handle_response
    })
    
  @staticmethod
  def csv(data):
    print 'connections.twitter.search.Search.csv'
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

  request_queue = []
  request_queue_stopped = True
  request_queue_timer = None
  
  def add_to_queue(self,item):
    print 'connections.twitter.search.Search.add_to_queue'
    self.request_queue.append(item)
    if self.request_queue_stopped is True:
      self.run_queue()
      
  def run_queue(self):
    print 'connections.twitter.search.Search.process_request'
    if len(self.request_queue) == 0:
      self.request_queue_stopped = True
      print 'connections.twitter.search.Search.run_queue[Queue Stopped]'
      return
    elif self.request_queue_stopped is True:
      print 'connections.twitter.search.Searchrun_queue[Queue Started]'
      self.request_queue_stopped = False
    t = threading.Timer(1.0,self.make_request)
    t.start()
  
  def make_request(self):
    print 'connections.twitter.search.Search.make_request'
    http = tornado.httpclient.AsyncHTTPClient()
    item = self.request_queue.pop(0)
    http.fetch(item['url'],callback=item['callback'])