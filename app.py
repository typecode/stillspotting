#! /usr/bin/env python

import sys
import os
import datetime
import hashlib

import connections.nyt.article
import connections.nyt.community
import connections.nyc311.noiseComplaints
import connections.flickr.photos.geo.photosForLocation

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

print '\n\r\n\r\n\r\n\r\n\r\n\r'
print '========================================================================='
print ''
print 'StillSpotting'
print 'By SIDL'
print ''
print 'starting..........................'
print ''
print ''

print 'StillSpotting: Opening MongoDB Connection'
database = pymongo.Connection('localhost', 27017)
print ''

print 'StillSpotting: Starting Connections'
print ''

connections = {
  'generic' : connections.connection.Connection({
    'database':database
  }),
  'nytarticle': connections.nyt.article.Article({
    'api_key':'1b9f2c309a5bb7426b1aa181b2f1a1cc:13:62473522'
  }),
  'nytcommunity': connections.nyt.community.Community({
    'api_key':'3cd7b97dd0c16c8523ea7ccba7f5fdd1:13:49052537'
  }),
  'googlegeocode': connections.google.geocoder.Geocoder({}),
  'nyc311noiseComplaints': connections.nyc311.noiseComplaints.NoiseComplaints({}),
  'flickrimages': connections.flickr.photos.geo.photosForLocation.PhotosForLocation({
    'api_key':'9ce620aec9b49f8de2cafa5144ab3876',
    'secret':'05b101b95c7e75d6'
  })
}

tornado_settings = {
  "static_path": os.path.join(os.path.dirname(__file__), "ui"),
  "cookie_secret":"This is my tornado secure cookie secret.",
  "login_url": "/login/"
}

application = tornado.web.Application([
  (r"/article/community", views.article.comments),
  (r"/article/updates", views.article.updates),
  (r"/geoitem/bounds/(.*)/(.*)/(.*)/", views.geoitem.bounds),
  (r"/api/info/", views.api.info,dict(connections=connections)),
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