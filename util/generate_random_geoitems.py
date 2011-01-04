import sys
import urllib
import math
import random

sys.path.append('./')
import tc.geoitem

for i in range(10000):
  gi = tc.geoitem.geoitem(random.uniform(-90, 90),random.uniform(-180, 180))
  print gi.get_id()