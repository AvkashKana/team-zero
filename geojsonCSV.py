# !/usr/bin/env python2.7
#
# geojsonCSV.py -- Convert the 'neighbourhoods.geojson' to
# a CSV file for Dom

# 07/25/2016, Georgetown Data Science Cohort 6

import csv, json

json_parsed = json.loads('neighbourhoods.geojson')

print json_parsed['features']
