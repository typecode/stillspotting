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

database = pymongo.Connection('localhost', 27017).tc.geoitems
#database.ensureIndex( { 'loc' : "2d" } )

class bounds(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  def get(self,ne,sw):
    _ne = ne.split(',')
    _ne[0] = float(_ne[0])
    _ne[1] = float(_ne[1])
    _sw = sw.split(',')
    _sw[0] = float(_sw[0])
    _sw[1] = float(_sw[1])
    
    results = database.find({'loc':{"$within" : {"$box" : [_sw,_ne]}}})
    out = {
      'bounds':[_ne[0],_ne[1],_sw[0],_sw[1]],
      'points':[]
    }
    for r in results:
      out['points'].append(r)
    self.write(json.dumps(out,default=pymongo.json_util.default))
    self.finish()