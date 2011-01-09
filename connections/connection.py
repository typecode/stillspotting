import sys
import urllib
import datetime
import hashlib

sys.path.append("lib")
import tornado.httpclient

class Connection:
  
  listeners = {}
  default_pars = {}
  
  def __init__(self,settings):
    self.settings = settings
    self.database = self.settings['database']
    print str(self)
    
  def __repr__(self):
    return 'connection.Connection()_____________________________________________\n\r\
 | connection.Connection Starting\n\r\
 |   This class defines the interface for an API Connection.\n\r\
 |\n\r\
 | connection.Connection Settings:\n\r\
 |  '+str(self.settings)+'\n\r\
 |__________________________________________________________________\n\r'
  
  def make_api_request(self,req_id,handler,pars=None):
    print 'connections.Connection.make_api_request'
    self.listeners[req_id] = handler
    self.process_request(req_id,pars)
    return []
    
  def emit_api_response(self,req_id,data):
    print 'connections.Connection.emit_api_response'
    if req_id in self.listeners and self.listeners[req_id] is not None:
      self.listeners[req_id]({'articles':data})
    
  def end_request(self,req_id):
    print 'connections.Connection.end_request\n\r'
    if req_id in self.listeners:
      self.listeners[req_id] = None
      del self.listeners[req_id]
      
  def process_request(self,req_id,pars):
    print 'connections.Connection.process_request'
    self.emit_api_response(req_id,{'Generic Output':123456789})
  