import sys
import urllib
import datetime
import hashlib

import connections.connection

import tornado.httpclient
import pymongo

class NoiseComplaints(connections.connection.Connection):
  
#### START CONNECTION-SPECIFIC MEMBERS
  name = 'NYC 311 Noise Complaints'
  description = 'Provides Access to NYC 311 Noise Complaints. This connection uses a MongoDB query interface.'
  default_pars = {
    "2000_Census_Block":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "2000_Census_Tract":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Civil_Court_District":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Congressional_District":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Fire_Battalion":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Fire_Company_Number":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Fire_Division":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Health_Area":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Health_Center_District":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Instructional_Region":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Sanitation_Collection_Scheduling_Section_and_Subsection":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "State_Senatorial_District":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Vacant_Lot_Flag":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Assembly_District":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Election_District":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "X_Coordinate":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Y_Coordinate":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Pseudo_Address_Flag":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "BBL":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "City_Council_District":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "School_District_(Confirmed)":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Building_Classification_Code":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Complaint_Type":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Descriptor_1":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Incident_Address":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Incident_City":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Borough":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Incident_Zip_Code":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Created_Date":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Police_Precinct":{'accepted':'','default':None,'required':False,'more_info':'None'},
    "Borough_Command":{'accepted':'','default':None,'required':False,'more_info':'None'}
  }
  example_query = {
    "Incident_Zip_Code":10009,
    "Descriptor_1":"Loud Music/Party"
  }
#### END CONNECTION-SPECIFIC MEMBERS

  mongo_conn = pymongo.Connection('localhost', 27017)
  db = mongo_conn['tc']
  
  def process_request(self,user,req_id,pars):
    print 'connections.nyc311.noiseComplaint.NoiseComplaint.process_request'
    
    results = self.db.noiseComplaints.find(pars)
    
    if results is not None:
      out = []
      for row in results:
        out.append(row)
      self.emit_api_response(req_id,out)
    else:
      self.emit_api_response(req_id,[])
    
    