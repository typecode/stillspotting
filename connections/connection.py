import sys
import urllib
import datetime
import hashlib
import pprint
import time
import datetime

sys.path.append("lib")
import tornado.httpclient
import json
import pymongo
import pymongo.json_util

class Connection:
  
#### START CONNECTION-SPECIFIC MEMBERS
  name = 'Generic Connection'
  description = 'This class defines the interface for an API Connection.'
  source = None
  default_pars = {
    'min_lat':{'accepted':'-90,90','default':None},
    'max_lat':{'accepted':'-90,90','default':None},
    'min_lng':{'accepted':'-180,180','default':None},
    'max_lng':{'accepted':'-180,180','default':None}
  }
  example_query = {}
#### END CONNECTION-SPECIFIC MEMBERS
  
#### START STANDARD CONNECTION MEMBERS
  buffers = {}
  listeners = {}
  settings = None
#### END STANDARD CONNECTION MEMBERS
  
  def __init__(self,settings):
    self.settings = settings
    #print str(self)
    
  def __repr__(self):
    pp = pprint.PrettyPrinter(indent=1)
    return str(self.name)+'()_____________________________________________\n\r\
 | '+str(self.name)+' Starting\n\r\
 |   '+str(self.description)+'\n\r\
 |\n\r\
 | '+str(self.name)+' Query Parameters:\n\r\
'+pp.pformat(self.default_pars)+'\n\r\
 |\n\r\
 | '+str(self.name)+' Settings:\n\r\
'+pp.pformat(self.settings)+'\n\r\
 |__________________________________________________________________\n\r'
  
  def get_info(self,user=None):
    print 'connections.Connection.get_info'
    if 'disabled' in self.settings and self.settings['disabled']:
      return None
    info = {}
    info['name'] = self.name
    info['description'] = self.description
    info['source'] = self.source
    info['default_pars'] = self.default_pars
    info['example_query'] = self.example_query
    return info
  
  def process_request(self,apirequest):
    print 'connections.Connection.process_request'
    data = {'Generic Output':123456789}
    apirequest.handle_data(data)
  
  def make_api_request(self,apirequest):
    print 'connections.Connection.make_api_request'
    if apirequest.requestid in self.buffers and len(self.buffers[apirequest.requestid]) > 0:
      return self.buffers[apirequest.requestid]
    self.listeners[apirequest.requestid] = apirequest.handle_data
    self.process_request(apirequest)
    
  def handle_pars(self,pars):
    print 'connections.Connection.handle_pars'
    for i in self.default_pars:
      if self.default_pars[i]['required'] is True and i not in pars:
        if self.default_pars[i]['default'] is not None:
          pars[i] = self.default_pars[i]['default']
        else:
          raise tornado.web.HTTPError(400)
    for i in pars:
      try:
        mytime = time.strptime(pars[i],'%m/%d/%y %H:%M')
        pars[i] = datetime(*mytime[:5])
      except (ValueError,TypeError):
        try:
          pars[i] = int(pars[i])
        except ValueError:
          pass
    return pars
    
  def emit_api_response(self,req_id,data):
    print 'connections.Connection.emit_api_response'
    if req_id in self.listeners and self.listeners[req_id] is not None:
      self.listeners[req_id](data)
    else:
      if req_id not in self.buffers:
        self.buffers[req_id] = []
      self.buffers[req_id].append(data)
      
  def end_request(self,req_id):
    print 'connections.Connection.end_request\n\r'
    if req_id in self.listeners:
      self.listeners[req_id] = None
      del self.listeners[req_id]
      
  @staticmethod
  def json(data):
    print 'connections.Connection.json'
    return data