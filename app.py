#! /usr/bin/env python

import sys
import os
import datetime
import hashlib

import connections.nyt.article
import connections.nyt.community
import connections.nyc311.noiseComplaints
import connections.flickr.photos.search
import connections.flickr.photos.geo.photosForLocation
import connections.twitter.twitterConnection
import connections.twitter.search

sys.path.append("lib")
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web

import pymongo

import views.handler
import views.user
import views.api
import views.article
import views.geoitem

print '\n\r\n\r'
print '========================================================================='
print ''
print 'StillSpotting'
print 'By SIDL'
print ''
print 'starting..........................'
print ''

print 'StillSpotting: Loading Configuration Files'
print ''

config_file = open('env.json','r')
try:
  config = tornado.escape.json_decode(config_file.read())
except TypeError, ValueError:
  print 'StillSpotting: ERROR Loading Configuration Files'
  
if sys.argv[1] is not None:
  config = config[sys.argv[1]]
else:
  config = config['local']

print 'StillSpotting: Opening MongoDB Connection'
database = pymongo.Connection('localhost', 27017)
print ''

print 'StillSpotting: Starting Connections'
print ''

connections = {
  'generic' : connections.connection.Connection({
    'database':database,
    'disabled':True
  }),
  'nytarticle': connections.nyt.article.Article({
    'api_key':'1b9f2c309a5bb7426b1aa181b2f1a1cc:13:62473522'
  }),
  'nytcommunity': connections.nyt.community.Community({
    'api_key':'3cd7b97dd0c16c8523ea7ccba7f5fdd1:13:49052537'
  }),
  'googlegeocode': connections.google.geocoder.Geocoder({}),
  'nyc311noiseComplaints': connections.nyc311.noiseComplaints.NoiseComplaints({
    'disabled':True
  }),
  'flickr': connections.flickr.flickrConnection.FlickrConnection({
    'api_key':config[u'flickrApiKey'],
    'secret':config[u'flickrApiSecret'],
    'disabled':True
  }),
  'flickrsearch': connections.flickr.photos.search.Search({
    'api_key':config[u'flickrApiKey'],
    'secret':config[u'flickrApiSecret']
  }),
  'flickrimages': connections.flickr.photos.geo.photosForLocation.PhotosForLocation({
    'api_key':config[u'flickrApiKey'],
    'secret':config[u'flickrApiSecret'],
    'disabled':True
  }),
  'twitter': connections.twitter.twitterConnection.TwitterConnection({
    'api_key':'KJe6u0UIiI3HKPq2YBoVsw',
    'disabled':True
  }),
  'twitter_search': connections.twitter.search.Search({
  
  })
}

tornado_settings = {
  "static_path": os.path.join(os.path.dirname(__file__), "ui"),
  "cookie_secret":"This is my tornado secure cookie secret.",
  "login_url": "/login/"
}

application = tornado.web.Application([
  (r"/api/info/", views.api.info,dict(connections=connections)),
  (r"/api/(.*)/auth/", views.api.auth,dict(connections=connections)),
  (r"/api/(.*)/authenticated/", views.api.authenticated,dict(connections=connections)),
  (r"/api/(.*)/", views.api.api,dict(connections=connections)),
  (r"/user/current/", views.user.current),
  (r"/register/",views.user.register),
  (r"/login/",views.user.login),
  (r"/logout/",views.user.logout),
  (r"/",views.handler.handler)
],**tornado_settings)

if __name__ == "__main__":
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8888)
  tornado.ioloop.IOLoop.instance().start()