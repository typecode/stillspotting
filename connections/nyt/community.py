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
  description = 'With the Community API, you can get user-generated NYTimes.com content. The current release includes article comments and readers\' reviews of movies. (Other types of user-generated content will be available in a later version.)'
  source = 'http://developer.nytimes.com/docs/read/community_api'
  default_pars = {
    'url':{'accepted':'URL to Article Containing Comments','default':None, 'required':False},
    'offset':{'accepted':'integer offset from 0','default':str(0), 'required':False}
  }
  example_query = {
    'url':'http://www.nytimes.com/2010/12/03/opinion/03krugman.html',
    'offset':0
  }
#### END CONNECTION-SPECIFIC MEMBERS
    
  def process_request(self,apirequest):
    print 'connections.nyt.comments.Comments.process_request'
    http = tornado.httpclient.AsyncHTTPClient()
    request_pars = self.handle_pars(apirequest.pars)
    request_pars['api-key'] = self.settings['api_key']
    
    url = 'http://api.nytimes.com/svc/community/v2/comments/url/exact-match.json?'
    url = url + urllib.urlencode(request_pars)
    
    def handle_response(response):
      try:
        data = tornado.escape.json_decode(response.body)
      except TypeError, ValueError:
        apirequest.handle_error('NYT Error')
      apirequest.handle_data(data)
      
    http.fetch(url,callback=handle_response)
  
  ################### END process_request