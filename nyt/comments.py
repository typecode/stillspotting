import sys
import urllib
import math

import google.geocoder

sys.path.append("lib")
import tornado.httpclient

class Comments:
  
  comments_api_key = '3cd7b97dd0c16c8523ea7ccba7f5fdd1:13:49052537'
  geocoder = google.geocoder.Geocoder()
  
  def __init__(self):
    print 'Comments()'
    
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
        'api-key':self.comments_api_key
      }
      
      url = 'http://api.nytimes.com/svc/community/v2/comments/url/exact-match.json?'
      url = url + urllib.urlencode(pars)
      return url
    
    def handle_initial_response(response):
      print 'getCommentsForUrl.handle_initial_response'
      json = tornado.escape.json_decode(response.body)
      print str(json[u'results'][u'totalCommentsFound'])
      if json[u'results'][u'totalCommentsFound'] > 25:
        n_requests = math.ceil(json[u'results'][u'totalCommentsFound']/25)
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
      else:
        print 'ALL REQUESTS MADE'
        
    http.fetch(generate_url(0),callback=handle_initial_response)
        
  def geocode_comment(self,req_id,comment):
    print 'Comments.geocodeComment'
    def comment_geocoded(latlng):
      comment[u'latlng'] = latlng
    self.geocoder.add_to_queue(comment[u'location'],comment_geocoded)
    
    
    