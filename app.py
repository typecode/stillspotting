#! /usr/bin/env python

import sys
import os
import datetime
import hashlib

import connections.nyt.article
import connections.nyt.community

sys.path.append("lib")
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web

import pymongo

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
  'nytarticle':connections.nyt.article.Article({
    'api_key':'1b9f2c309a5bb7426b1aa181b2f1a1cc:13:62473522'
  }),
  'nytcommunity':connections.nyt.community.Community({
    'api_key':'3cd7b97dd0c16c8523ea7ccba7f5fdd1:13:49052537'
  }),
  'googlegeocode':connections.google.geocoder.Geocoder({})
}

tornado_settings = {
  "static_path": os.path.join(os.path.dirname(__file__), "ui")
}

application = tornado.web.Application([
  (r"/article/community", views.article.comments),
  (r"/article/updates", views.article.updates),
  (r"/geoitem/bounds/(.*)/(.*)/(.*)/", views.geoitem.bounds),
  (r"/api/info/", views.api.info,dict(connections=connections)),
  (r"/api/(.*)/", views.api.api,dict(connections=connections))
],**tornado_settings)

if __name__ == "__main__":
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8888)
  tornado.ioloop.IOLoop.instance().start()