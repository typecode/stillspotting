import sys
import urllib

sys.path.append("lib")
import tornado.httpclient

class Article:
  
  article_api_key = '6b386fbb1141bc111298f599fe611bab:1:49052537'
  listeners = {}
  
  def __init__(self):
    print 'Article()'
    
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
    
  def emit(self,req_id,data):
    print 'Article.emit'
    if req_id in self.listeners:
      self.listeners[req_id](data)
      self.listeners[req_id] = None
      
  def listen(self,req_id,handler):
    print 'Article.emit'
    if req_id in self.listeners and self.listeners is not None:
      handler(self.listeners[req_id])
      self.listeners = None;
    else:
      self.listeners[req_id] = handler