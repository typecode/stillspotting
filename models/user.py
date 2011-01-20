import sys
import urllib
import math
import hashlib
import datetime
import pickle

sys.path.append("lib")
import tornado.httpclient
import json
import pymongo
import pymongo.json_util

class User():
  
  user_data = None
  session_data = None
  db = pymongo.Connection('localhost', 27017)['tc']
  
  def __init__(self,session_data=None,email=None,password=None,password2=None):
    print '#models.user.User()'
    if session_data is not None:
      self.revive_from_session(session_data)
      return
    if email is not None and password is not None and password2 is not None:
      self.register(email,password,password2)
      return
    if email is not None and password is not None:
      self.start_session(email,password)
      return
  
  def register(self,email,password,password2):
    print '#models.user.User.register'
    if password != password2:
      return False
    existing = self.db.users.find({'email':email})
    if existing.count() > 0:
      return False
    new = {
      'email':email,
      'passhash':hashlib.md5(password).hexdigest()
    }
    self.session_data = {
      'email':email,
      'authenticated':True
    }
    _id = self.db.users.insert(new)
    new['_id'] = _id
    self.user_data = new
  
  def update(self,key,value):
    print '#models.user.User().update'
    if value is None:
      if self.user_data[key]:
        self.user_data.remove(key)
    else:
      self.user_data[key] = value
    self.db.users.update({'email':self.user_data['email']},{'$set':{key:value}})
  
  def revive_from_session(self,session_data):
    print '#models.user.User.revive_from_session'
    self.session_data = pickle.loads(session_data)
    if self.session_data is None:
      return
    records = self.db.users.find({'email':self.session_data['email']})
    if records.count() == 0:
      return False
    else:
      self.user_data = records[0]
      print str(self.user_data)
    
  def start_session(self,email,password):
    print '#models.user.User.start_session'
    records = self.db.users.find({'email':email,'passhash':hashlib.md5(password).hexdigest()})
    if records.count() == 0:
      return False
    else:
      self.user_data = records[0]
      self.session_data = {
        'email':records[0]['email'],
        'authenticated':True
      }
    
  def get_session_data(self):
    print '#models.user.User.get_session_data'
    return pickle.dumps(self.session_data)
    
  def end_session(self):
    print '#models.user.User.end_session'
    self.session_data = None