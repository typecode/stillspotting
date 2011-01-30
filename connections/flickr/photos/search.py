# coding: utf-8

import sys
import urllib
import datetime
import hashlib
import string

import connections.connection
import connections.flickr.flickrConnection

import tornado.httpclient
import pymongo

class Search(connections.flickr.flickrConnection.FlickrConnection):
  
#### START CONNECTION-SPECIFIC MEMBERS
  name = 'Flickr Photo Search'
  description = 'Return a list of photos matching some criteria. Only photos visible to the calling user will be returned. To return private or semi-private photos, the caller must be authenticated with \'read\' permissions, and have permission to view the photos. Unauthenticated calls will only return public photos.'
  source = 'http://www.flickr.com/services/api/flickr.photos.search.html'
  default_pars = {
    '':{'accepted':'','default':None,'required':False},
    'user_id':{'accepted':'The NSID of the user who\'s photo to search. If this parameter isn\'t passed then everybody\'s public photos will be searched. A value of "me" will search against the calling user\'s photos for authenticated calls.','default':None,'required':False},
    'tags':{'accepted':'A comma-delimited list of tags. Photos with one or more of the tags listed will be returned. You can exclude results that match a term by prepending it with a - character.','default':None,'required':False},
    'tag_mode':{'accepted':'Either \'any\' for an OR combination of tags, or \'all\' for an AND combination. Defaults to \'any\' if not specified.','default':None,'required':False},
    'text':{'accepted':'A free text search. Photos who\'s title, description or tags contain the text will be returned. You can exclude results that match a term by prepending it with a - character.','default':None,'required':False},
    'min_upload_date':{'accepted':'Minimum upload date. Photos with an upload date greater than or equal to this value will be returned. The date can be in the form of a unix timestamp or mysql datetime.','default':None,'required':False},
    'max_upload_date':{'accepted':'Maximum upload date. Photos with an upload date less than or equal to this value will be returned. The date can be in the form of a unix timestamp or mysql datetime.','default':None,'required':False},
    'min_taken_date':{'accepted':'Minimum taken date. Photos with an taken date greater than or equal to this value will be returned. The date can be in the form of a mysql datetime or unix timestamp.','default':None,'required':False},
    'max_taken_date':{'accepted':'Maximum taken date. Photos with an taken date less than or equal to this value will be returned. The date can be in the form of a mysql datetime or unix timestamp.','default':None,'required':False},
    'license':{'accepted':'The license id for photos (for possible values see the <a target="blank" href="http://www.flickr.com/services/api/flickr.photos.licenses.getInfo.html">flickr.photos.licenses.getInfo</a> method). Multiple licenses may be comma-separated.','default':None,'required':False},
    'sort':{'accepted':'The order in which to sort returned photos. Deafults to date-posted-desc (unless you are doing a radial geo query, in which case the default sorting is by ascending distance from the point specified). The possible values are: date-posted-asc, date-posted-desc, date-taken-asc, date-taken-desc, interestingness-desc, interestingness-asc, and relevance.','default':None,'required':False},
    'privacy_filter':{'accepted':'Return photos only matching a certain privacy level. This only applies when making an authenticated call to view photos you own. Valid values are 1 (public photos), 2 (private photos visible to freinds), 3 (private photos visible to family), 4 (private photos visible to friends and family), 5 (completely private photos).','default':None,'required':False},
    'bbox':{'accepted':'A comma-delimited list of 4 values defining the Bounding Box of the area that will be searched.<br /><br />\
      The 4 values represent the bottom-left corner of the box and the top-right corner, minimum_longitude, minimum_latitude, maximum_longitude, maximum_latitude.<br /><br />\
      Longitude has a range of -180 to 180 , latitude of -90 to 90. Defaults to -180, -90, 180, 90 if not specified.<br /><br />\
      Unlike standard photo queries, geo (or bounding box) queries will only return 250 results per page.<br /><br />\
      Geo queries require some sort of limiting agent in order to prevent the database from crying. This is basically like the check against "parameterless searches" for queries without a geo component.<br /><br />\
      A tag, for instance, is considered a limiting agent as are user defined min_date_taken and min_date_upload parameters — If no limiting factor is passed we return only photos added in the last 12 hours (though we may extend the limit in the future).',
      'default':None,'required':False},
    'accuracy':{'accepted':'Recorded accuracy level of the location information. Current range is 1-16 : World level is 1, Country is ~3, Region is ~6, City is ~11, Street is ~16','default':None,'required':False},
    'safe_search':{'accepted':'Safe search setting: 1 for safe, 2 for moderate, 3 for restricted','default':None,'required':False},
    'content_type':{'accepted':'1 for photos only, 2, for screenshots only, 3 for \'other\' only 4 for photos and screenshots, 5 for screenshots and \'other\', 6 for photos and \'other\' and 7 for all.','default':None,'required':False},
    'machine_tags':{'accepted':'Aside from passing in a fully formed machine tag, there is a special syntax for searching on specific properties. Please see <a target="blank" href="http://www.flickr.com/services/api/flickr.photos.search.html">source</a> for more details.','default':None,'required':False},
    'machine_tag_mode':{'accepted':'Either \'any\' for an OR combination of tags, or \'all\' for an AND combination. Defaults to \'any\' if not specified.','default':None,'required':False},
    'group_id':{'accepted':'group_id','default':None,'required':False},
    'contacts':{'accepted':'Search your contacts. Either \'all\' or \'ff\' for just friends and family. (Experimental)','default':None,'required':False},
    'woe_id':{'accepted':'A 32-bit identifier that uniquely represents spatial entities. (not used if bbox argument is present).<br /><br />\
      Geo queries require some sort of limiting agent in order to prevent the database from crying. This is basically like the check against "parameterless searches" for queries without a geo component.<br /><br />\
      A tag, for instance, is considered a limiting agent as are user defined min_date_taken and min_date_upload parameters &emdash; If no limiting factor is passed we return only photos added in the last 12 hours (though we may extend the limit in the future).',
      'default':None,'required':False},
    'place_id':{'accepted':'A Flickr place id. (not used if bbox argument is present).<br /><br />\
      Geo queries require some sort of limiting agent in order to prevent the database from crying. This is basically like the check against "parameterless searches" for queries without a geo component.<br /><br />\
      A tag, for instance, is considered a limiting agent as are user defined min_date_taken and min_date_upload parameters &emdash; If no limiting factor is passed we return only photos added in the last 12 hours (though we may extend the limit in the future).',
      'default':None,'required':False},
    'media':{'accepted':'Filter results by media type. Possible values are all (default), photos or videos','default':None,'required':False},
    'has_geo':{'accepted':'Any photo that has been geotagged, or if the value is "0" any photo that has not been geotagged.<br /><br />\
      Geo queries require some sort of limiting agent in order to prevent the database from crying. This is basically like the check against "parameterless searches" for queries without a geo component.<br /><br />\
      A tag, for instance, is considered a limiting agent as are user defined min_date_taken and min_date_upload parameters &emdash; If no limiting factor is passed we return only photos added in the last 12 hours (though we may extend the limit in the future).','default':None,'required':False},
    'geo_context':{'accepted':'Geo context is a numeric value representing the photo\'s geotagginess beyond latitude and longitude. For example, you may wish to search for photos that were taken "indoors" or "outdoors".<br />\
      The current list of context IDs is :<br />\
        0, not defined.<br />\
        1, indoors.<br />\
        2, outdoors.<br /><br />\
      Geo queries require some sort of limiting agent in order to prevent the database from crying. This is basically like the check against "parameterless searches" for queries without a geo component.<br /><br />\
      A tag, for instance, is considered a limiting agent as are user defined min_date_taken and min_date_upload parameters &emdash; If no limiting factor is passed we return only photos added in the last 12 hours (though we may extend the limit in the future).','default':None,'required':False},
    'lat':{'accepted':'A valid latitude, in decimal format, for doing radial geo queries.<br /><br />\
      Geo queries require some sort of limiting agent in order to prevent the database from crying. This is basically like the check against "parameterless searches" for queries without a geo component.<br /><br />\
      A tag, for instance, is considered a limiting agent as are user defined min_date_taken and min_date_upload parameters &emdash; If no limiting factor is passed we return only photos added in the last 12 hours (though we may extend the limit in the future).','default':None,'required':False},
    'lon':{'accepted':'A valid longitude, in decimal format, for doing radial geo queries. <br /><br />\
      Geo queries require some sort of limiting agent in order to prevent the database from crying. This is basically like the check against "parameterless searches" for queries without a geo component. <br /><br />\
      A tag, for instance, is considered a limiting agent as are user defined min_date_taken and min_date_upload parameters &emdash; If no limiting factor is passed we return only photos added in the last 12 hours (though we may extend the limit in the future).','default':None,'required':False},
    'radius':{'accepted':'A valid radius used for geo queries, greater than zero and less than 20 miles (or 32 kilometers), for use with point-based geo queries. The default value is 5 (km).','default':None,'required':False},
    'radius_units':{'accepted':'The unit of measure when doing radial geo queries. Valid options are "mi" (miles) and "km" (kilometers). The default is "km".','default':None,'required':False},
    'is_commons':{'accepted':'Limit the scope of the search to only photos that are part of the Flickr Commons project. Default is false.','default':None,'required':False},
    'in_gallery':{'accepted':'Limit the scope of the search to only photos that are in a gallery? Default is false, search all photos.','default':None,'required':False},
    'is_getty':{'accepted':'Limit the scope of the search to only photos that are for sale on Getty. Default is false.','default':None,'required':False},
    'extras':{'accepted':'A comma-delimited list of extra information to fetch for each returned record. Currently supported fields are: description, license, date_upload, date_taken, owner_name, icon_server, original_format, last_update, geo, tags, machine_tags, o_dims, views, media, path_alias, url_sq, url_t, url_s, url_m, url_z, url_l, url_o','default':None,'required':False},
    'per_page':{'accepted':'Number of photos to return per page. If this argument is omitted, it defaults to 100. The maximum allowed value is 500.','default':None,'required':False},
    'page':{'accepted':'The page of results to return. If this argument is omitted, it defaults to 1.','default':None,'required':False}
  }
  example_query = {
    'text':'quiet still',
    'bbox':'-73.9873289,40.720113,-73.972849,40.731099',
    'extras':'geo,url_o,tags',
    'output':'csv'
  }
#### END CONNECTION-SPECIFIC MEMBERS
  
  def process_request(self,apirequest):
    print 'connections.flickr.photos.search.Search.process_request'
    #if self.is_user_authenticated(apirequest.user) is False:
    #  return
    http = tornado.httpclient.AsyncHTTPClient()
    request_pars = self.handle_pars(apirequest.pars)
    
    request_pars['api_key'] = self.settings['api_key']
    request_pars['auth_token'] = apirequest.user.user_data['flickr']['auth']['token']['_content']
    request_pars['method'] = 'flickr.photos.search'
    request_pars['format'] = 'json'
    
    request_pars['api_sig'] = self.generate_api_sig(request_pars)
    
    url = 'http://api.flickr.com/services/rest/?'
    url = url + urllib.urlencode(request_pars)
    
    def handle_response(response):
      json_string = string.lstrip(response.body,'jsonFlickrApi(')
      json_string = string.rstrip(json_string,');')
      try:
        data = tornado.escape.json_decode(json_string)
      except TypeError, ValueError:
        apirequest.handle_error('Flickr Error')
        return
      apirequest.handle_data(data)
      
    http.fetch(url,callback=handle_response)
    
  @staticmethod
  def csv(data):
    print 'connections.flickr.photos.search.Search.csv'
    header = []
    rows = []
    for i in data:
      if u'photos' in i:
        if u'photo' in i[u'photos']:
          print str(i[u'photos'][u'photo'])
          for j in i[u'photos'][u'photo']:
            row = list("" for i in range(0,100))
            for k in j:
              try:
                hi = header.index(k)
              except ValueError:
                header.append(unicode(k))
                hi = len(header) - 1
              row[hi] = u'"'+unicode(j[k])+u'"'
            rows.append(row)
    output = unicode(u'\t'.join(header))
    for i in rows:
      i = i[0:len(header)]
      output = output + '\n' + unicode(u'\t'.join(i))
    return output