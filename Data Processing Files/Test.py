import gzip
import pickle
import json
from json import JSONEncoder
import datetime
import re
import numpy as np
from shapely.geometry import Point
import csv
import ogr
import pandas as pd
import itertools
import sys


'''class NewLine:
    def __init__(self, filename):
        self.filename = filename
    def __iter__(self, row = 0, filename):
        self.row = re.findall('\n', filename)
        return self
    def __next__(self):
        if self.__iter__():'''

#LyftExtraction('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Pickle Data/lyft_04132019.pkl')
    #stringRow = re.sub("'is_reserved':|'electric_scooter'|'is_disabled':|'type':|'name':| 0|", '', str(row))


def pleaseReadInOrder(filename):
    infile = open(filename, 'rb')
    BigData = pickle.load(infile, fix_imports=True, encoding="ASCII", errors="strict")
    infile.close()
    Data = BigData
    download_dir = "csvboiLime.csv"
    csv = open(download_dir, "w")
    result = re.sub("}, {|{|},",'\n', str(Data))
    NoApostrophe = re.sub("'",'', result)
    CleanResult = re.sub("last_updated: (.*) data:|ttl: 10|bikes:", '', NoApostrophe)
    CleanestResult = re.sub(' -', '-', str(CleanResult))
    NewResult = re.sub("is_disabled: |disabled: |is_reserved: |reserved:|vehicle_type:|bike_id: |"
                       "battery_level: |jump_ebike_battery_level:|lat: |lon:|name|jump_vehicle_type |type", '', CleanestResult)
    row = NewResult
    #csv.write(CleanDateTime)
    csv.write(row)
    '''if not re.search('lon', SmallerData) or re.search('lat', SmallerData) or re.search('bike_id', SmallerData):
        re.sub(r"'name': '(.+?)'|'is_disabled':(.+?)|'type': '(.+?)'|'is_reserved':(.+?)",'', SmallerData)
    else:
        print(SmallerData)
    def printout():
        try:
            x = re.search("'lon':(.+?)'", SmallerData).group(1)
            y = re.search("'lat':(.+?)'", SmallerData).group(1)
            z = re.search("'bike_id':(.+?)'", SmallerData).group(1)
            print(z + ',' + x + ',' + y)
        except AttributeError:
            print('haha x u thought')
    for n in SmallerData:
        printout()'''


#pleaseReadInOrder('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Pickle Data/lime_04132019.pkl')
def csvFormatting(filename, outfile):  # Put your filename here
    word_delete = '"['  # Put what you want to delete here
    with open(filename, 'r') as file_text:  # Open your file
        lines = file_text.readlines()  # Read all the lines from your file, then put them in a list
        newlines = []  # Make a list to save edits in
        for line in lines:  # Loop over all the lines, each line will first go into variable line for some actions
            newline = line.replace(word_delete, '')  # Replace the text in word_delete to an empty string (aka nothing)
            if any(line):
                newlines.append(newline)  # Add the edit to the list with edits
    with open(outfile, 'w') as file_text:  # Open the file, but in write mode
        file_text.writelines(newlines)  # Write the list with edits to the new file

'''def csvFormatting2(filename):
    with open(filename, "r") as source:
        if enumerate(csv.find_index{row}) < 2:
            for row in range(4):
                header = next(source)
        rdr = csv.reader(source)
        with open('niceCSVboi', "wb") as result:
            wtr = csv.writer(result)
            for r in rdr:
                wtr.writerow(r[1], r[2])'''
def csvFormatting3(filename):
    with open(filename, 'rb') as inp, open(filename, 'wb') as out:
        writer = csv.writer(out)
        for row in csv.reader(inp):
            if row[4] != int:
                writer.writerow(row)


# csvFormatting('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Test CSVs/DC_Test3.csv',
#               '/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Test CSVs/DC_Test3.csv')
# csvFormatting('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Test CSVs/csvboiLite.csv',
#               '/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Test CSVs/csvboiLite.csv')
# csvFormatting3('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Clean_DC_CSVs/csvboiLyft_Test2.csv')


def shapefileTesting():
    source = ogr.Open('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/DC_Outlines/Washington_DC_Boundary/Washington_DC_Boundary.shp')
    pointsLayer = source.GetLayer()
    iterator = iter(pointsLayer)
    # first feature in pointsLayer
    feature = iterator.next()
    geom = feature.GetGeometryRef()
    xy = geom.GetPoint()
    print(xy)


#shapefileTesting()

import fiona
import geopandas
import pandas
# DC_gdf = geopandas.read_file("/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis"
#                              "/DC_Outlines/Washington_DC_Boundary/Washington_DC_Boundary.shp",
#                              layer='Washington_DC_Boundary')
# DC_list = list(DC_gdf)
# with open('Washington_DC_Boundary2.pkl', 'wb') as f:
#     pickle.dump(DC_list, f)



def plswork():
    with open('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Test CSVs/csvboi copy 3.csv', 'r') as in_file:
        with open('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Test CSVs/csvboiLite.csv', 'w') as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if row:
                    writer.writerow(row)

#plswork()


def plswork2():
    with open('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Clean_DC_CSVs/csvboiLyft_Test2 copy.csv', 'r') as in_file:
        with open('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Clean_DC_CSVs/csvboiLyft_Test2'
                  '.csv', 'w') as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if row[1] != 'type':
                    writer.writerow(row)


#plswork2()


def fullClean():
    with open('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Test CSVs/csvboiLite.csv', 'r') as inp,\
            open('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Test CSVs/csvboi copy 3.csv', 'w') as out:
        writer = csv.writer(out)
        for row in csv.reader(inp):
            if type(row[2]) is 'int':
                del row
            else:
                writer.writerow(row)

# fullClean()

def trainData():
    # with open('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Clean_DC_CSVs/DC_TrainingData.csv', 'r') as in_file:
    #     with open('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Clean_DC_CSVs/DC_TestingData.csv', 'w') as out_file:
    #         writer = csv.writer(out_file)
    #         for row in csv.reader(in_file):
    #                 writer.writerow(row)
    with open('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Test CSVs/DC_TestingData.csv',
              'rb') as out_file2:
        with open('Washington_DC_TestingDataSample2.pkl', 'wb') as f:
            for row in out_file2:
                pickle.dump(row, f)


trainData()
