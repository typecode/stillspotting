import sys
import urllib
import datetime
import hashlib
import pprint

sys.path.append("lib")
import tornado.httpclient

class Connection:
  
#### START CONNECTION-SPECIFIC MEMBERS
  name = 'Generic Connection'
  description = 'This class defines the interface for an API Connection.'
  default_pars = {
    'min_lat':{'accepted':'-90,90','default':None},
    'max_lat':{'accepted':'-90,90','default':None},
    'min_lng':{'accepted':'-180,180','default':None},
    'max_lng':{'accepted':'-180,180','default':None}
  }
#### END CONNECTION-SPECIFIC MEMBERS
  
#### START STANDARD CONNECTION MEMBERS
  listeners = {}
  settings = None
#### END STANDARD CONNECTION MEMBERS
  
  def __init__(self,settings):
    self.settings = settings
    print str(self)
    
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
  
  def get_info(self):
    info = {}
    info['name'] = self.name
    info['description'] = self.description
    info['default_pars'] = self.default_pars
    return info
  
  def process_request(self,req_id,pars):
    print 'connections.Connection.process_request'
    self.emit_api_response(req_id,{'Generic Output':123456789})
  
  def make_api_request(self,req_id,handler,pars=None):
    print 'connections.Connection.make_api_request'
    self.listeners[req_id] = handler
    self.process_request(req_id,pars)
    return []
    
  def emit_api_response(self,req_id,data):
    print 'connections.Connection.emit_api_response'
    if req_id in self.listeners and self.listeners[req_id] is not None:
      self.listeners[req_id](data)
    
  def end_request(self,req_id):
    print 'connections.Connection.end_request\n\r'
    if req_id in self.listeners:
      self.listeners[req_id] = None
      del self.listeners[req_id]