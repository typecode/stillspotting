import sys

import models.user

import views.handler

sys.path.append("lib")
import tornado.httpclient
import json
import pymongo
import pymongo.json_util

class register(views.handler.handler):
  def post(self):
    user = models.user.User(email=self.get_argument("email"), password=self.get_argument("password"), password2=self.get_argument("password"))
    self.set_secure_cookie("session_data", user.get_session_data())
    self.redirect("/")

class login(views.handler.handler):
  def get(self):
    self.clear_cookie("session_data")
    self.write('<html><body>\
      LOGIN:\
      <form action="/login/" method="post">'
      'email: <input type="text" name="email">'
      'pw: <input type="password" name="password">'
      '<input type="submit" value="Sign in">'
      '</form><br/><br/>\
      REGISTER:\
      <form action="/register/" method="post">'
      'email: <input type="text" name="email">'
      'pw: <input type="password" name="password">'
      'pw2: <input type="password" name="password2">'
      '<input type="submit" value="Register">'
      '</form></body></html>')
      
  def post(self):
    self.clear_cookie("session_data")
    if 'email' not in self.request.arguments or 'password' not in self.request.arguments:
      self.redirect("/login/")
      return
    user = models.user.User(email=self.get_argument("email"), password=self.get_argument("password"))
    self.set_secure_cookie("session_data", user.get_session_data())
    self.redirect("/")

class logout(views.handler.handler):
  @tornado.web.authenticated
  def get(self):
    self.clear_cookie("session_data")
    self.redirect("/")

class current(views.handler.handler):
  @tornado.web.authenticated
  def post(self):
    print '-views.user.current.post'
    self.write(json.dumps(self.current_user.session_data,default=pymongo.json_util.default))
    