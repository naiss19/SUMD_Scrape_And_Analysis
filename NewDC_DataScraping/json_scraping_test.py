import requests
import pickle
import datetime
import time
import json
import csv
import os
import math
import multiprocessing as mp
import re
import requests
import urllib.request as urllib2
import glob


def writer(file, directory):
    url = urllib2.urlopen(file)
    wjson = url.read()
    wdata = json.loads(wjson.decode('utf-8'))
    ndata = str(wdata)
    match = ndata.count('}, {')
    length = re.sub('}, {', '},\n{', ndata)
    for x in range(0, match):
        n = x + 1
        print(wdata['data']['bikes'][n]['bike_id'])
    # fn = datetime.datetime.now().strftime('{}_%m%d%Y-%H:%M:%S.csv'.format('bird'))
    if os.path.exists(directory + 'bird.csv'):
        with open(os.path.join(directory, 'bird.csv'), 'a') as cf:
            writer = csv.writer(cf)
            for x in range(0, match):
                n = x + 1
                csvID = wdata['data']['bikes'][n]['bike_id']
                csvLat = wdata['data']['bikes'][n]['lat']
                csvLon = wdata['data']['bikes'][n]['lon']
                csvDateTime = datetime.datetime.now().strftime('%m%d%Y-%H:%M:%S')
                writer.writerow([csvID, csvLat, csvLon, csvDateTime])
    else:
        with open(os.path.join(directory, 'bird.csv'), 'w') as cf:
            writer = csv.writer(cf)
            for x in range(0, match):
                n = x + 1
                csvID = wdata['data']['bikes'][n]['bike_id']
                csvLat = wdata['data']['bikes'][n]['lat']
                csvLon = wdata['data']['bikes'][n]['lon']
                csvDateTime = datetime.datetime.now().strftime('%m%d%Y-%H:%M:%S')
                writer.writerow([csvID, csvLat, csvLon, csvDateTime])

for x in range (0, 4):
    writer('https://gbfs.bird.co/dc', '/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/New_DC_Data')
# scooter_data = {'data': [
#     {
#         'bikes': [
#             {
#                 'bike_id': x['data']['bikes']['bike_id'],
#                 'coordinates': [
#                     {
#                         'lat': x['data']['bikes'][float('lat')],
#                         'lon': x['data']['bikes'][float('lon')]
#                     }
#                 ],
#                 'battery_level': x['data']['bikes'][int('battery_level')],
#                 'vehicle_type': x['data']['bikes']['vehicle_type'],
#                 'disabled': x['data']['bikes']['is_disabled'],
#                 'reserved': x['data']['bikes']['is_reserved']
#             }
#         ]
#     }
# ]
#     for x in wdata}