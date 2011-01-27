import sys
import urllib
import math
import threading
import datetime
import time

import connections.google.geocoder
import connections.connection
import connections.queue

sys.path.append("lib")
import tornado.httpclient

class Search(connections.connection.Connection,connections.queue.Queue):
  
#### START CONNECTION-SPECIFIC MEMBERS
  name = 'Twitter Search API Connection'
  description = 'Returns tweets that match a specified query. Supports CSV Output.'
  source = 'http://dev.twitter.com/doc/get/search'
  default_pars = {
    'q':{'accepted':'Search query.','default':None,'required':True},
    'geocode':{'accepted':'Returns tweets by users located within a given radius of the given latitude/longitude. The location is preferentially taking from the Geotagging API, but will fall back to their Twitter profile. The parameter value is specified by "latitude,longitude,radius", where radius units must be specified as either "mi" (miles) or "km" (kilometers). Note that you cannot use the near operator via the API to geocode arbitrary locations; however you can use this geocode parameter to search near geocodes directly.','default':None, 'required':False},
    'n_to_fetch':{'accepted':"Number of rows to fetch",'default':15,'required':False},
    'rpp':{'accepted':"Rows per page",'default':15,'required':True},
    'output':{'accepted':'json, csv','default':'csv','required':'true'}
  }
  example_query = {
    'q':'noise',
    'geocode':'40.716667,-74,5mi',
    'n_to_fetch':1000,
    'rpp':100,
    'output':'csv'
  }
#### END CONNECTION-SPECIFIC MEMBERS
    
  def process_request(self,apirequest):
    print 'connections.twitter.search.Search.process_request'
    http = tornado.httpclient.AsyncHTTPClient()
    
    request_pars = self.handle_pars(apirequest.pars)
    
    if 'n_to_fetch' in apirequest.pars and apirequest.pars['n_to_fetch'] is not None and float(apirequest.pars['n_to_fetch']) > 10:
      apirequest.run['n_requests'] = int(math.ceil(float(apirequest.pars['n_to_fetch'])/request_pars['rpp']))
    
    def handle_response(response):
      print 'connections.twitter.search.Search.process_request.handle_response'
      try:
        data = tornado.escape.json_decode(response.body)
      except TypeError, ValueError:
        apirequest.handle_error('Twitter Error')
        self.run_queue()
        return
      apirequest.handle_data(data)
      
      print '\n\r\n\r'
      print str(data)
      print '\n\r\n\r'
      print str(len(data[u'results']))
      print '\n\r\n\r'
      
      if apirequest.run['n_requests_received'] < apirequest.run['n_requests']:
        if u'next_page' in data:
          self.add_to_queue({
            'url':'http://search.twitter.com/search.json'+data[u'next_page'],
            'callback':handle_response
          })
        elif u'results' in data and len(data[u'results']) > 0:
          next_request_pars = request_pars
          
          #Fri, 21 Jan 2011 23:01:07 +0000
          oldest_date_string = data[u'results'][len(data[u'results'])-1][u'created_at'][0:len(data[u'results'][len(data[u'results'])-1][u'created_at'])-6]
          print oldest_date_string
          oldest_date = datetime.datetime.strptime(oldest_date_string, '%a, %d %b %Y %H:%M:%S')
          print str(oldest_date)
          #YYYY-MM-DD
          until = oldest_date.strftime('%Y-%m-%d')
          print until
          next_request_pars['until'] = until
          print str(next_request_pars)
          url = 'http://search.twitter.com/search.json?' + urllib.urlencode(next_request_pars)
          print url
          self.add_to_queue({
            'url':url,
            'callback':handle_response
          })
        else:
          apirequest.finish()
        
      self.run_queue()
    
    print '\n\r\n\r'
    print str(request_pars)
    url = 'http://search.twitter.com/search.json?' + urllib.urlencode(request_pars)
    print url
    print '\n\r\n\r'
    
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
