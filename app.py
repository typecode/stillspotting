import sys
import os
import datetime
import hashlib

sys.path.append("lib")
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.web

import views.article
import views.newswire

settings = {
  "static_path": os.path.join(os.path.dirname(__file__), "ui")
}

application = tornado.web.Application([
  (r"/article/comments", views.article.comments),
  (r"/article/updates", views.article.updates),
  (r"/newswire/today", views.newswire.today),
  (r"/newswire/live", views.newswire.live),
],**settings)

if __name__ == "__main__":
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8888)
  tornado.ioloop.IOLoop.instance().start()