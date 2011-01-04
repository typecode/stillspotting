import sys
import urllib
import math
import hashlib
import datetime

sys.path.append("lib")
import tornado.httpclient
import json
import pymongo
import pymongo.json_util

class bounds(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  def get(self,ne,sw):
    print 'views.geoitem.bounds.get'
    print ne
    print sw
    self.write(json.dumps({},default=pymongo.json_util.default))
    self.finish()