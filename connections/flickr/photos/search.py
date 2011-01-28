import sys
import urllib
import datetime
import hashlib
import string

import connections.connection
import connections.flickr.flickrConnection

import tornado.httpclient
import pymongo

class Search(connections.flickr.flickrConnection.FlickrConnection):
  
#### START CONNECTION-SPECIFIC MEMBERS
  name = 'Flickr Photo Search'
  description = 'Return a list of photos matching some criteria. Only photos visible to the calling user will be returned. To return private or semi-private photos, the caller must be authenticated with \'read\' permissions, and have permission to view the photos. Unauthenticated calls will only return public photos.'
  source = 'http://www.flickr.com/services/api/flickr.photos.search.html'
  default_pars = {
    
  }
  example_query = {
    'bbox':'-73.9873289,40.720113,-73.972849,40.731099'
  }
#### END CONNECTION-SPECIFIC MEMBERS
  
  def process_request(self,apirequest):
    print 'connections.flickr.photos.search.Search.process_request'
    #if self.is_user_authenticated(apirequest.user) is False:
    #  return
    http = tornado.httpclient.AsyncHTTPClient()
    request_pars = self.handle_pars(apirequest.pars)
    
    request_pars['api_key'] = self.settings['api_key']
    request_pars['auth_token'] = apirequest.user.user_data['flickr']['auth']['token']['_content']
    request_pars['method'] = 'flickr.photos.search'
    request_pars['format'] = 'json'
    
    request_pars['api_sig'] = self.generate_api_sig(request_pars)
    
    url = 'http://api.flickr.com/services/rest/?'
    url = url + urllib.urlencode(request_pars)
    
    def handle_response(response):
      json_string = string.lstrip(response.body,'jsonFlickrApi(')
      json_string = string.rstrip(json_string,');')
      try:
        data = tornado.escape.json_decode(json_string)
      except TypeError, ValueError:
        apirequest.handle_error('Flickr Error')
        return
      apirequest.handle_data(data)
      
    http.fetch(url,callback=handle_response)