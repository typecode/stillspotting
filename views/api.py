import sys
import urllib
import math
import hashlib
import datetime
import random
import string
import time

import views.handler

sys.path.append("lib")
import tornado.httpclient
import json
import pymongo
import pymongo.json_util

class info(views.handler.handler):
  
  def initialize(self,connections={}):
    print '-views.api.info.initialize'
    self.connections = connections
  
  @tornado.web.asynchronous
  def get(self):
    print '-views.api.info.get'
    output = {}
    for i in self.connections:
      output[i] = self.connections[i].get_info()
    self.write(json.dumps(output,default=pymongo.json_util.default))
    self.finish()



class api(views.handler.handler):
  
  def initialize(self,connections={}):
    print '-views.api.api.init'
    self.request_id = None
    self.api = None
    self.connections = connections
    
  @tornado.web.asynchronous
  def get(self,api):
    print '-views.api.api.get'
    print ' |api: '+str(api)
    if not api or api not in self.connections:
      raise tornado.web.HTTPError(404)
    self.api = api
    random.seed(time.clock())
    self.request_id = "".join([random.choice(string.letters+string.digits) for x in xrange(32)])
    self.pars = {}
    for i in self.request.arguments:
      self.pars[i] = self.request.arguments[i][0]
    print ' |self.request_id: '+str(self.request_id)
    print ' |self.query_parameters: '+str(self.pars)
    output_buffer = self.connections[self.api].make_api_request(self.request_id,self.out,self.pars)
    if output_buffer is not None and len(output_buffer) > 0:
      self.out(output_buffer)
  
  def on_connection_close(self):
    print '-views.api.api.on_connection_close'
    print ' |self.request_id: '+str(self.request_id)
    print ''
    self.connections[self.api].end_request(self.request_id)
  
  def out(self,data):
    print '-views.api.api.out'
    print ' |api: '+str(self.api)
    print ' |self.request_id: '+str(self.request_id)
    #print ' |data: '+str(data)
    output = {
      'request_id':self.request_id,
      'data':data
    }
    self.connections[self.api].end_request(self.request_id)
    self.write(json.dumps(output,default=pymongo.json_util.default))
    self.finish()
  