import os
import glob
import re
import csv
import pandas as pd
def CSVconcatenate():
    os.chdir('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/New_DC_Data copy')
    with open('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis'
            '/NewDC_DataScraping/DC_Scrape_Files/urls.txt', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        urls = list(reader)
    #     for x in urls:
    #         print(x)
    listing = glob.glob('lyft*.csv')
    print(type(listing))
    finder = (glob.glob('lyft*.csv'))
    for url in listing:
        out = open('lyft_merged_data.csv', "a")
        for num in range(0, 20):
            n = num + 1
            f = open(listing[n], "r")
            for line in f:
                out.write(line)

CSVconcatenate()
# os.chdir('/Volumes/Elements/New_DC_Data')
# extension = 'csv'
# all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
# combine all files in the list
# combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
# export to csv
# combined_csv.to_csv("/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Clean_DC_CSVs/combined_csv.csv", encoding='utf-8')
