import sys
import urllib
import math
import hashlib
import datetime

import connections.nyt.newswire
import connections.nyt.article
import connections.nyt.comments

sys.path.append("lib")
import tornado.httpclient
import json
import pymongo
import pymongo.json_util

class today(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  def get(self):
    print 'views.newswire.today.get'
    todays_wires = newswire.get_todays_wires()
    self.write(json.dumps(todays_wires,default=pymongo.json_util.default))
    self.finish()

class live(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  def get(self):
    print 'views.newswire.live.get'
    newswire.watch(self.on_response)
  def on_response(self, data):
    print 'views.newswire.live.on_response'
    self.write(tornado.escape.json_encode(data))
    self.finish()