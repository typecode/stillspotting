import sys
import urllib
import datetime
import hashlib
import md5
import string

import connections.connection
import connections.flickr.flickrConnection

import tornado.httpclient
import pymongo

class Search(connections.flickr.flickrConnection.FlickrConnection):
  
#### START CONNECTION-SPECIFIC MEMBERS
  name = 'Flickr Photo Search'
  description = ''
  default_pars = {
    
  }
  example_query = {
    'bbox':'-73.9873289,40.720113,-73.972849,40.731099'
  }
#### END CONNECTION-SPECIFIC MEMBERS
  
  def process_request(self,user,req_id,pars={}):
    print 'connections.flickr.photos.search.Search.process_request'
    http = tornado.httpclient.AsyncHTTPClient()
    print str(pars)
    request_pars = self.handle_pars(pars)
    
    request_pars['api_key'] = self.settings['api_key']
    request_pars['auth_token'] = user.user_data['flickr']['auth']['token']['_content']
    request_pars['method'] = 'flickr.photos.search'
    request_pars['format'] = 'json'
    
    m = md5.new()
    m.update(self.settings['secret'])
    for i in sorted(request_pars.iterkeys()):
      m.update(i)
      m.update(str(request_pars[i]))
    request_pars['api_sig'] = m.hexdigest()
    
    url = 'http://api.flickr.com/services/rest/?'
    url = url + urllib.urlencode(request_pars)
    
    def handle_response(response):
      json_string = string.lstrip(response.body,'jsonFlickrApi(')
      json_string = string.rstrip(json_string,');')
      try:
        json = tornado.escape.json_decode(json_string)
      except TypeError, ValueError:
        self.emit_api_response(req_id,[response.body])
        return
      print str(json)
      self.emit_api_response(req_id,json)
      
    http.fetch(url,callback=handle_response)