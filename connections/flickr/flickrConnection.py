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

class FlickrConnection(connections.connection.Connection):
  
  def is_user_authenticated(self,user=None):
    print 'connections.Connection.is_user_authenticated'
    if user is not None:
      if 'flickr' in user.user_data\
      and 'auth' in user.user_data['flickr']\
      and 'token' in user.user_data['flickr']['auth']:
        return True
    return False
  
  def get_info(self,user=None):
    print 'connections.Connection.get_info'
    if 'disabled' in self.settings and self.settings['disabled']:
      return None
    info = {}
    info['name'] = self.name
    info['description'] = self.description
    info['default_pars'] = self.default_pars
    info['example_query'] = self.example_query
    info['authorized'] = self.is_user_authenticated(user)
    
        
    return info
    
  def generate_auth_url(self):
    print 'connections.flickr.flickrConnection.generate_auth_url'
    m = md5.new()
    m.update(self.settings['secret'])
    m.update('api_key')
    m.update(self.settings['api_key'])
    m.update('perms')
    m.update('read')
    return 'http://www.flickr.com/services/auth/?api_key='+self.settings['api_key']+'&perms=read&api_sig='+m.hexdigest()
      
  def handle_auth_response(self,pars,user,callback=None):
    print 'connections.flickr.flickrConnection.handle_auth_response'
    http = tornado.httpclient.AsyncHTTPClient()
    
    m = md5.new()
    m.update(self.settings['secret'])
    m.update('api_key')
    m.update(self.settings['api_key'])
    m.update('format')
    m.update('json')
    m.update('frob')
    m.update(pars['frob'][0])
    m.update('methodflickr.auth.getToken')
    
    url = 'http://www.flickr.com/services/rest/?'
    url = url + 'api_key='+self.settings['api_key']
    url = url + '&method=flickr.auth.getToken'
    url = url + '&format=json'
    url = url + '&frob='+pars['frob'][0]
    url = url + '&api_sig='+m.hexdigest()
    
    def handle_response(response):
      json_string = string.lstrip(response.body,'jsonFlickrApi(')
      json_string = string.rstrip(json_string,');')
      try:
        json = tornado.escape.json_decode(json_string)
      except TypeError, ValueError:
        return
      user.update('flickr',{'auth':json[u'auth']})
      if callback is not None:
        callback()
      
    http.fetch(url,callback=handle_response)
    
  def generate_api_sig(self,pars):
    print 'connections.flickr.flickrConnection.generate_api_sig'
    m = md5.new()
    m.update(self.settings['secret'])
    for i in sorted(pars.iterkeys()):
      m.update(i)
      m.update(str(pars[i]))
    return m.hexdigest()
    
    