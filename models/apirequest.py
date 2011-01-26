import sys
import urllib
import math
import hashlib
import datetime
import pickle
import random
import time
import string

sys.path.append("lib")
import tornado.httpclient
import json
import pymongo
import pymongo.json_util

class APIRequest():
  
  requestid = None
  user = None
  api = None
  pars = None
  run = None
  output = None
  emitter = None
  error = None
  
  def __init__(self,user,api,pars,emitter,error):
    print '#models.apirequest.APIRequest()'
    random.seed(time.clock())
    self.user = user
    self.requestid = "".join([random.choice(string.letters+string.digits) for x in xrange(32)])
    self.api = api
    self.pars = pars
    self.run = {
      'n_requests':1,
      'n_requests_received':0
    }
    self.output = []
    self.emitter = emitter
    self.error = error
    
  def start(self):
    print '#models.apirequest.start'
    self.api.make_api_request(self)
    
  def handle_data(self,data):
    print '#models.apirequest.handle_data'
    self.run['n_requests_received'] = self.run['n_requests_received'] + 1
    self.output.append(data)
    
    if self.run['n_requests_received'] == self.run['n_requests']:
      self.finish()
  
  def finish(self):
    print '#models.apirequest.finish'
    format = 'json'
    output = self.output
    if 'output' in self.pars:
      format = self.pars['output']
    if hasattr(self.api,format):
      print 'we have it'
      output = getattr(self.api,format)(self.output)
    self.api.end_request(self.requestid)
    self.emitter(output)
  
  def handle_error(self,msg):
    print '#models.apirequest.handle_error'
    self.api.end_request(self.requestid)
    self.error(data)