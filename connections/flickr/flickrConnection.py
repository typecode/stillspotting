import sys
import urllib
import datetime
import hashlib

import connections.connection
import connections.flickr.flickrConnection

import tornado.httpclient
import pymongo

class FlickrConnection(connections.connection.Connection):
  
  pass