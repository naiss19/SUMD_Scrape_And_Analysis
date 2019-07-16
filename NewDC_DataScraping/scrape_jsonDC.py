import requests
import pickle
import datetime
import time
import json
import csv
import os
import math
import multiprocessing as mp
import urllib.request as urllib2


class scraper:
    """

    """
    def __init__(self, data_name, url, params=None):
        self.name = data_name
        self.url = url
        self.params = params
        self.current_data = {}

    def scrape(self, interval_seconds, duration_minutes):
        duration_seconds = duration_minutes * 60
        num_requests = math.ceil(duration_seconds / interval_seconds)
        for i in range(num_requests):
            r = requests.get(self.url, params=self.params)
            if r.status_code == 200:
                self.current_data[datetime.datetime.now()] = r.json()
            else:
                self.current_data[datetime.datetime.now()] = None
            time.sleep(interval_seconds)
        return

    def write(self, directory):
        url = urllib2.urlopen(self.url)
        wjson = url.read()
        wdata = json.loads(wjson.decode('utf-8'))
        ndata = str(wdata)
        match = ndata.count('}, {')
        print('Scraping complete at: ' + datetime.datetime.now().strftime('%m/%d/%Y-%H:%M:%S'))
        fn = datetime.datetime.now().strftime('{}_%m%d%Y-%H%M%S.csv'.format(self.name))
        with open(os.path.join(directory, fn), 'w') as cf:
            writer = csv.writer(cf)
            for x in range(0, match):
                n = x + 1
                # to add more items for the csv, format each variable as:
                # variable = wdata['data']['bikes'][n]['index name']
                # index names are: 'bike_id', 'lat', lon', 'vehicle_type', 'disabled', 'reserved'
                csvID = wdata['data']['bikes'][n]['bike_id']
                csvLat = wdata['data']['bikes'][n]['lat']
                csvLon = wdata['data']['bikes'][n]['lon']
                csvDateTime = datetime.datetime.now().strftime('%m%d%Y-%H:%M:%S')
                writer.writerow([csvID, csvLat, csvLon, csvDateTime])
        self.current_data = {}
        return


def run_scraper(scraper_name, scraper_url):
    s = scraper(data_name=scraper_name, url=scraper_url)
    while True:
        s.scrape(interval_seconds=30, duration_minutes=2)
        # make sure to write this to a directory that ends in 'New_DC_Data' or the code will create one
        s.write(directory='/Volumes/Elements/New_DC_Data')


if __name__ == '__main__':
    # load up list of URL's
    # format the list of URL's as: company name;URL
    with open('/Users/BrandonHall/Documents/GitHub/SUMD_Scrape_And_Analysis'
              '/NewDC_DataScraping/DC_Scrape_Files/urls.txt', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        urls = list(reader)
# initialize data directory at ./data if directory is not already found
    if 'New_DC_Data' not in os.listdir('./'):
        print('Make a folder named "New_DC_Data"')

    p = mp.Pool(len(urls))
    p.starmap(run_scraper, urls)

