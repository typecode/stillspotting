import sys
import urllib
import datetime
import hashlib
import pprint
import time
import datetime
import threading

sys.path.append("lib")
import tornado.httpclient
import json
import pymongo
import pymongo.json_util

class Queue:
  
  request_queue = []
  request_queue_stopped = True
  request_queue_timer = None
  
  def add_to_queue(self,item):
    print 'connections.twitter.search.Search.add_to_queue'
    self.request_queue.append(item)
    if self.request_queue_stopped is True:
      self.run_queue()
      
  def run_queue(self):
    print 'connections.twitter.search.Search.process_request'
    if len(self.request_queue) == 0:
      self.request_queue_stopped = True
      print 'connections.twitter.search.Search.run_queue[Queue Stopped]'
      return
    elif self.request_queue_stopped is True:
      print 'connections.twitter.search.Searchrun_queue[Queue Started]'
      self.request_queue_stopped = False
    t = threading.Timer(1.0,self.make_request)
    t.start()
  
  def make_request(self):
    print 'connections.twitter.search.Search.make_request'
    http = tornado.httpclient.AsyncHTTPClient()
    item = self.request_queue.pop(0)
    http.fetch(item['url'],callback=item['callback'])