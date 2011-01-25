import sys
import urllib
import math
import hashlib
import datetime
import random
import string
import time

import models.apirequest

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
  
  @tornado.web.authenticated
  @tornado.web.asynchronous
  def get(self):
    print '-views.api.info.get'
    output = {}
    for i in self.connections:
      info = self.connections[i].get_info(self.current_user)
      if info is not None:
        output[i] = info
    self.write(json.dumps(output,default=pymongo.json_util.default))
    self.finish()

class auth(views.handler.handler):
  def initialize(self,connections={}):
    print '-views.api.auth.init'
    self.connections = connections
  
  @tornado.web.authenticated
  @tornado.web.asynchronous
  def get(self,api):
    print '-views.api.auth.get'
    print ' |api: '+str(api)
    if not api or api not in self.connections:
      raise tornado.web.HTTPError(404)
    self.redirect(self.connections[api].generate_auth_url())
    
    
class authenticated(views.handler.handler):
  def initialize(self,connections={}):
    print '-views.api.auth.init'
    self.connections = connections
  
  @tornado.web.authenticated
  @tornado.web.asynchronous
  def get(self,api):
    print '-views.api.authenticated.get'
    print ' |api: '+str(api)
    print ' |pars: '+str(self.request.arguments)
    if not api or api not in self.connections:
      raise tornado.web.HTTPError(404)
    def finish():
      self.redirect('/')
    self.connections[api].handle_auth_response(self.request.arguments,self.current_user,finish)

class api(views.handler.handler):
  
  def initialize(self,connections={}):
    print '-views.api.api.init'
    self.apirequest = None
    self.connections = connections
  
  @tornado.web.authenticated
  @tornado.web.asynchronous
  def get(self,api):
    print '-views.api.api.get'
    print ' |api: '+str(api)
    if not api or api not in self.connections:
      raise tornado.web.HTTPError(404)
    pars = {}
    for i in self.request.arguments:
      pars[i] = self.request.arguments[i][0]
    self.apirequest = models.apirequest.APIRequest(self.current_user,self.connections[api],pars,self.out,self.error)
    print ' |self.request_id: '+str(self.apirequest.requestid)
    print ' |self.query_parameters: '+str(self.apirequest.pars)
    print ''
    self.apirequest.start()
  
  def on_connection_close(self):
    print '-views.api.api.on_connection_close'
    print ' |self.request_id: '+str(self.apirequest.requestid)
    print ''
    self.connections[self.apirequest.api].end_request(self.apirequest.requestid)
  
  def out(self,data):
    print '-views.api.api.out'
    print ' |api: '+str(self.apirequest.api.name)
    print ' |self.request_id: '+str(self.apirequest.requestid)
    print ''
    output = {
      'format':self.apirequest.pars['output'],
      'request_id':self.apirequest.requestid,
      'data':data
    }
    self.write(json.dumps(output,default=pymongo.json_util.default))
    self.finish()
  
  def error(self,error):
    print '-views.api.api.error'
    print ' |api: '+str(self.apirequest.api.name)
    print ' |self.request_id: '+str(self.apirequest.requestid)
    print ''
    output = {
      'error':True,
      'request_id':self.apirequest.requestid,
      'message':error
    }
    self.write(json.dumps(output,default=pymongo.json_util.default))
    self.finish()