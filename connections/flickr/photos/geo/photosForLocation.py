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

class PhotosForLocation(connections.flickr.flickrConnection.FlickrConnection):
  
#### START CONNECTION-SPECIFIC MEMBERS
  name = 'Flickr PhotosForLocation'
  description = 'Provides access to Flickr PhotosForLocation. More info found <a href="http://www.flickr.com/services/api/flickr.photos.geo.photosForLocation.html">here</a>.'
  default_pars = {
    'lat':{'accepted':'The latitude whose valid range is -90 to 90. Anything more than 6 decimal places will be truncated.','default':None,'required':True},
    'lon':{'accepted':'The longitude whose valid range is -180 to 180. Anything more than 6 decimal places will be truncated.','default':None,'required':True},
    'accuracy':{'accepted':'Recorded accuracy level of the location information. World level is 1, Country is ~3, Region ~6, City ~11, Street ~16. Current range is 1-16. Defaults to 16 if not specified.','default':None,'required':False},
    'extras':{'accepted':'A comma-delimited list of extra information to fetch for each returned record. Currently supported fields are: description, license, date_upload, date_taken, owner_name, icon_server, original_format, last_update, geo, tags, machine_tags, o_dims, views, media, path_alias, url_sq, url_t, url_s, url_m, url_z, url_l, url_o','default':None,'required':False},
    'per_page':{'accepted':'Number of photos to return per page. If this argument is omitted, it defaults to 100. The maximum allowed value is 500.','default':None,'required':False},
    'page':{'accepted':'The page of results to return. If this argument is omitted, it defaults to 1.','default':None,'required':False}
  }
  example_query = {
    'lat':41.409197,
    'lon':-122.194889
  }
#### END CONNECTION-SPECIFIC MEMBERS
  
  def process_request(self,user,req_id,pars={}):
    print 'connections.flickr.images.Images.process_request'
    http = tornado.httpclient.AsyncHTTPClient()
    print str(pars)
    request_pars = self.handle_pars(pars)
    
    request_pars['api_key'] = self.settings['api_key']
    request_pars['auth_token'] = user.user_data['flickr']['auth']['token']['_content']
    request_pars['method'] = 'flickr.photos.geo.photosForLocation'
    request_pars['format'] = 'json'
    
    m = md5.new()
    m.update(self.settings['secret'])
    for i in sorted(request_pars.iterkeys()):
      m.update(i)
      m.update(str(request_pars[i]))
    request_pars['api_sig'] = m.hexdigest()
    
    print str(request_pars)
    
    url = 'http://api.flickr.com/services/rest/?'
    url = url + urllib.urlencode(request_pars)
    
    print(str(url))
    
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