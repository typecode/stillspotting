import sys

import models.user

sys.path.append("lib")
import tornado.httpclient
import json
import pymongo
import pymongo.json_util

class handler(tornado.web.RequestHandler):
  
  def initialize(self,connections={}):
    print '-views.handler.handler.initialize'
  
  def get(self):
    print '-views.handler.handler.get'
    if self.current_user is not None and self.current_user.session_data['authenticated'] is True:
      self.redirect('/static/index.html')
    else:
      self.redirect('/login/')
    
  def get_current_user(self):
    print '-views.handler.handler.get_current_user'
    user = models.user.User(session_data=self.get_secure_cookie("session_data"))
    if user.session_data is None:
      return None
    return user
    