import sys
import os
import hashlib
import datetime

sys.path.append("lib")
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web
import pymongo
import pymongo.json_util
import json

import nyt.newswire
import nyt.article
import nyt.comments

class NewsWireToday(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  def get(self):
    print 'NewsWireToday.get'
    todays_wires = newswire.get_todays_wires()
    self.write(json.dumps(todays_wires,default=pymongo.json_util.default))
    self.finish()

class NewsWireLive(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  def get(self):
    print 'NewsWireLive.get'
    newswire.watch(self.on_response)

  def on_response(self, data):
    print 'NewsWireLive.on_response'
    self.write(tornado.escape.json_encode(data))
    self.finish()

class ArticleComments(tornado.web.RequestHandler):
  @tornado.web.asynchronous
  def get(self):
    print 'ArticleComments.get'
    now = datetime.datetime(2010,1,1)
    if self.get_argument('url') is not None:
      req_id = hashlib.md5(str(self.request.remote_ip)+str(now.now())).hexdigest()
      article.getArticleByUrl(req_id,self.get_argument('url'))
      comments.getCommentsForUrl(req_id,self.get_argument('url'))
      self.write(tornado.escape.json_encode({'req_id':req_id}))
      self.finish()
  
  def fetch_comments(self,article_data):
    print 'ArticleComments.fetch_comments'
    print str(article_data)
    
class ArticleUpdates(tornado.web.RequestHandler):
  
  @tornado.web.asynchronous
  def get(self):
    self.get_argument('req_id')
    article_buffer = article.listen(self.get_argument('req_id'),self.out)
    if len(article_buffer) > 0:
      self.out(article_buffer)
    comment_buffer = comments.listen(self.get_argument('req_id'),self.out)
    if len(comment_buffer) > 0:
      self.out(comment_buffer)
  
  def out(self,data):
    print 'ArticleUpdates.out'
    article.stopListening(self.get_argument('req_id'))
    comments.stopListening(self.get_argument('req_id'))
    self.write(json.dumps(data,default=pymongo.json_util.default))
    self.finish()

settings = {
  "static_path": os.path.join(os.path.dirname(__file__), "ui")
}

application = tornado.web.Application([
  (r"/article/comments", ArticleComments),
  (r"/article/updates", ArticleUpdates),
  (r"/newswire/today", NewsWireToday),
  (r"/newswire/live", NewsWireLive),
],**settings)

if __name__ == "__main__":
  newswire = nyt.newswire.Newswire()
  article = nyt.article.Article()
  comments = nyt.comments.Comments()
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8888)
  tornado.ioloop.IOLoop.instance().start()