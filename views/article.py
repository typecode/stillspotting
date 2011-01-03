import sys
import urllib
import math
import hashlib
import datetime

import nyt.newswire
import nyt.article
import nyt.comments

sys.path.append("lib")
import tornado.httpclient
import json
import pymongo
import pymongo.json_util

class comments(tornado.web.RequestHandler):
  nytarticle = nyt.article.Article()
  nytcomments = nyt.comments.Comments()
  @tornado.web.asynchronous
  def get(self):
    print 'views.article.comments.get'
    now = datetime.datetime(2010,1,1)
    if self.get_argument('url') is not None:
      req_id = hashlib.md5(str(self.request.remote_ip)+str(now.now())).hexdigest()
      self.nytarticle.getArticleByUrl(req_id,self.get_argument('url'))
      self.nytcomments.getCommentsForUrl(req_id,self.get_argument('url'))
      self.write(tornado.escape.json_encode({'req_id':req_id}))
      self.finish()
  
  def comments(self,article_data):
    print 'views.article.comments.fetch_comments'
    print str(article_data)
    
class updates(tornado.web.RequestHandler):
  nytarticle = nyt.article.Article()
  nytcomments = nyt.comments.Comments()
  @tornado.web.asynchronous
  def get(self):
    self.get_argument('req_id')
    article_buffer = self.nytarticle.listen(self.get_argument('req_id'),self.out)
    if len(article_buffer) > 0:
      self.out(article_buffer)
    comment_buffer = self.nytcomments.listen(self.get_argument('req_id'),self.out)
    if len(comment_buffer) > 0:
      self.out(comment_buffer)
  def out(self,data):
    print 'views.article.updates.out'
    self.nytarticle.stopListening(self.get_argument('req_id'))
    self.nytcomments.stopListening(self.get_argument('req_id'))
    self.write(json.dumps(data,default=pymongo.json_util.default))
    self.finish()