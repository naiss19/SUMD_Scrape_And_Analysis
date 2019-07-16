import gzip
import pickle
import re
import json
from json import JSONEncoder
import datetime
import csv
from collections import Counter
from datetime import datetime
import pandas as pd

def cleanup(Data):
    for datetime in Data:
        data_datetime = datetime.strftime("%B, %d, %Y, %I: %M: %S %p")
    result = re.sub("}, {|{|},",'\n', str(Data))
    NoApostrophe = re.sub("'",'', result)
    CleanResult = re.sub("last_updated: (.*) data:|ttl: 0|bikes:", '', NoApostrophe)
    DatedResult = re.sub("datetime.datetime((.*))", data_datetime, CleanResult)
    columnTitleRow = "Disabled, Reserved, Vehicle Type, Latitude, Longitude, Bike ID"
    csv.write(columnTitleRow)

def SpinExtraction(filename):
    infile = open(filename, 'rb') # insert whatever .pkl file is needed 
    BigData = pickle.load(infile, fix_imports=True, encoding = "ASCII", errors = "strict")
    infile.close()
    Data = BigData
    download_dir = "Spin_DataTest.csv"
    csv = open(download_dir, "w")
    cleanup(Data)
    NewResult = re.sub("is_disabled:|disabled:|is_reserved:|reserved:|lon:|lat:|vehicle_type:|bike_id:|battery_level:|jump_ebike_battery_level:|name|jump_vehicle_type|:|type",'', DatedResult)
    row = NewResult
    csv.write(row)
def JumpExtraction(filename):
    infile = open(filename, 'rb') # insert whatever .pkl file is needed 
    BigData = pickle.load(infile, fix_imports=True, encoding = "ASCII", errors = "strict")
    infile.close()
    Data = BigData
    download_dir = "Jump_Datav6.csv"
    csv = open(download_dir, "w")
    for datetime in Data:
        data_datetime = datetime.strftime("%B, %d, %Y, %I: %M: %S %p")
    result = re.sub("}, {|{|},",'\n', str(Data))
    #result2 = "(%s)" % str(result).strip("[")
    NoApostrophe = re.sub("'",'', result)
    CleanResult = re.sub("last_updated: (.*) data:|ttl: 0|bikes:", '', NoApostrophe)
    DatedResult = re.sub("datetime.datetime((.*))", data_datetime, CleanResult)
    columnTitleRow = "Is disabled, Is reserved, Name, Vehicle Type, Battery Level, Latitude, Longitude, Bike ID\n"
    csv.write(columnTitleRow)
    NewResult = re.sub("is_disabled:|disabled:|is_reserved:|reserved:|lon:|lat:|vehicle_type:|bike_id:|battery_level:|jump_ebike_battery_level:|name|jump_vehicle_type|:|type",'', DatedResult)
    row = NewResult
    csv.write(row)
def BirdExtraction(filename):
    infile = open(filename, 'rb') # insert whatever .pkl file is needed 
    BigData = pickle.load(infile, fix_imports=True, encoding = "ASCII", errors = "strict")
    infile.close()
    Data = BigData
    download_dir = "Bird_Datav6.csv"
    csv = open(download_dir, "w")
    for datetime in Data:
        data_datetime = datetime.strftime("%B, %d, %Y, %I: %M: %S %p")
    result = re.sub("}, {|{|},",'\n', str(Data))
    #result2 = "(%s)" % str(result).strip("[")
    NoApostrophe = re.sub("'",'', result)
    CleanResult = re.sub("last_updated: (.*) data:|ttl: 0|bikes:", '', NoApostrophe)
    DatedResult = re.sub("datetime.datetime((.*))", data_datetime, CleanResult)
    columnTitleRow = "Vehicle Type, Longitude, Latitude, Reserved, Battery Level, Disabled, Bike ID\n"
    csv.write(columnTitleRow)
    NewResult = re.sub("is_disabled:|disabled:|is_reserved:|reserved:|lon:|lat:|vehicle_type:|bike_id:|battery_level:|jump_ebike_battery_level:|name|jump_vehicle_type|:|type",'', DatedResult)
    row = NewResult
    csv.write(row)
def LimeExtraction(filename):
    infile = open(filename, 'rb') # insert whatever .pkl file is needed 
    BigData = pickle.load(infile, fix_imports=True, encoding = "ASCII", errors = "strict")
    infile.close()
    Data = BigData
    download_dir = "Lime_Datav6.csv"
    csv = open(download_dir, "w")
    for datetime in Data:
        data_datetime = datetime.strftime("%B, %d, %Y, %I: %M: %S %p")
    result = re.sub("}, {|{|},",'\n', str(Data))
    #result2 = "(%s)" % str(result).strip("[")
    NoApostrophe = re.sub("'",'', result)
    CleanResult = re.sub("last_updated: (.*) data:|ttl: 0|bikes:", '', NoApostrophe)
    DatedResult = re.sub("datetime.datetime((.*))", data_datetime, CleanResult)
    columnTitleRow = "Disabled, Reserved, Longitude, Latitude, Vehicle Type, Bike ID\n"
    csv.write(columnTitleRow)
    NewResult = re.sub("is_disabled:|disabled:|is_reserved:|reserved:|lon:|lat:|vehicle_type:|bike_id:|battery_level:|jump_ebike_battery_level:|name|jump_vehicle_type|:|type",'', DatedResult)
    row = NewResult
    csv.write(row)
def LyftExtraction(filename):
    infile = open(filename, 'rb') # insert whatever .pkl file is needed 
    BigData = pickle.load(infile, fix_imports=True, encoding="ASCII", errors="strict")
    infile.close()
    Data = BigData
    download_dir = "Lyft_Datav6.csv"
    csv = open(download_dir, "w")
    for datetime in Data:
        data_datetime = datetime.strftime("%B, %d, %Y, %I: %M: %S %p")
    result = re.sub("}, {|{|},",'\n', str(Data))
    #result2 = "(%s)" % str(result).strip("[")
    NoApostrophe = re.sub("'",'', result)
    CleanResult = re.sub("last_updated: (.*) data:|ttl: 0|bikes:", '', NoApostrophe)
    DatedResult = re.sub("datetime.datetime((.*))", data_datetime, CleanResult)
    columnTitleRow = "Available, Disabled, Vehicle Type, Latitude, Longitude, Bike ID\n"
    csv.write(columnTitleRow)
    NewResult = re.sub("is_disabled:|disabled:|is_reserved:|reserved:|lon:|lat:|vehicle_type:|bike_id:|battery_level:|jump_ebike_battery_level:|name|jump_vehicle_type|:|type",'', DatedResult)
    row = NewResult
    #csv.write(CleanDateTime)
    csv.write(row)
def CapitalExtraction(filename):
    infile = open(filename, 'rb') # insert whatever .pkl file is needed 
    BigData = pickle.load(infile, fix_imports=True, encoding = "ASCII", errors = "strict")
    infile.close()
    Data = BigData
    download_dir = "Capital_Datav6.csv"
    csv = open(download_dir, "w")
    for datetime in Data:
        data_datetime = datetime.strftime("%B, %d, %Y, %I: %M: %S %p")
    result = re.sub("}, {|{|},",'\n', str(Data))
    #result2 = "(%s)" % str(result).strip("[")
    NoApostrophe = re.sub("'",'', result)
    CleanResult = re.sub("last_updated: (.*) data:|ttl: 10|bikes:", '', NoApostrophe)
    DatedResult = re.sub("datetime.datetime((.*))", data_datetime, CleanResult)
    columnTitleRow = "Available, Disabled, Vehicle Type, Latitude, Longitude, Bike ID\n"
    csv.write(columnTitleRow)
    NewResult = re.sub("num_docs_disabled:|num_ebikes_available:|is_returning:|num_docks_available:|is_renting:|num_bikes_available:|station_id:|eightd_has_available_keys:|is_installed:|num_bikes_disabled:|last_reported:",'', DatedResult)
    row = NewResult
    #csv.write(CleanDateTime)
    csv.write(row)
def SkipExtraction(filename):
    infile = open(filename, 'rb') # insert whatever .pkl file is needed 
    BigData = pickle.load(infile, fix_imports=True, encoding = "ASCII", errors = "strict")
    infile.close()
    Data = BigData
    download_dir = "Skip_Datav6.csv"
    csv = open(download_dir, "w")
    for datetime in Data:
        data_datetime = datetime.strftime("%B, %d, %Y, %I: %M: %S %p")
    result = re.sub("}, {|{|},",'\n', str(Data))
    #result2 = "(%s)" % str(result).strip("[")
    NoApostrophe = re.sub("'",'', result)
    CleanResult = re.sub("last_updated: (.*) data:|ttl: 0|bikes:", '', NoApostrophe)
    DatedResult = re.sub("datetime.datetime((.*))", data_datetime, CleanResult)
    columnTitleRow = "Disabled, Reserved, Longitude, Latitude, Vehicle Type, Bike ID\n"
    csv.write(columnTitleRow)
    NewResult = re.sub("is_disabled:|disabled:|is_reserved:|reserved:|lon:|lat:|vehicle_type:|bike_id:|battery_level:|jump_ebike_battery_level:|name|jump_vehicle_type|:|type",'', DatedResult)
    row = NewResult
    #csv.write(CleanDateTime)
    csv.write(row)

'''SpinExtraction("/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Pickle Data/.spin_04132019.pkl.icloud")
print("Spin complete")'''
LyftExtraction("/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Pickle Data/lyft_04132019.pkl")
print("Lyft complete")
'''JumpExtraction("jump_04132019.pkl")
print("Jump complete")
BirdExtraction("bird_04132019.pkl")
print("Bird complete")
LimeExtraction("lime_04132019.pkl")
print("Lime complete")
SkipExtraction("skip_04132019.pkl")
print("Skip complete")
CapitalExtraction("capital_04132019.pkl")
print("All done")'''