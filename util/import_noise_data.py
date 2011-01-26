#!/usr/bin/env python2.7

import sys
import argparse
import csv
import string
import time
from datetime import datetime

sys.path.append("lib")
import tornado
import pymongo

database = pymongo.Connection('localhost', 27017).tc.noiseComplaints

def check_args():
  if hasattr(args, "filename") is False:
    print 'Must provide filename!'
    return False
  return True

def create_model(model_row):
  model = []
  for i in model_row:
    model.append(string.replace(i,' ','_'))
  return model

def process():
  
  open(args.filename[0], 'rb')
  data_reader = csv.reader(open(args.filename[0], 'rb'))
  
  model = create_model(data_reader.next())
  
  print model
  
  for row in data_reader:
    record = {}
    for i in range(0,len(row)):
      try:
        mytime = time.strptime(row[i],'%m/%d/%y %H:%M')
        record[model[i]] = datetime(*mytime[:5])
      except ValueError:
        try:
          record[model[i]] = int(row[i])
        except ValueError:
          record[model[i]] = row[i]
    
    record['_id'] = string.replace(str(record['X_Coordinate']) + ',' + str(record['Y_Coordinate']) + ',' + str(record['Created_Date']),' ',"_")
    #existing_record = database.find_one({"_id": record['_id']})
    #if existing_record is not None:
    #  print 'ERROR ALREADY INSERTED ('+record['_id']+')'
    #  continue
    _id = database.insert(record)
    if _id is None:
      print 'ERROR INSERTING ('+record['_id']+')'
    
  
  
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Import Guggenheim Noise Data.')
  parser.add_argument('--filename', metavar='f', type=str, nargs='+',help='path to data file')
  args = parser.parse_args()
  if check_args() is True:
    process()