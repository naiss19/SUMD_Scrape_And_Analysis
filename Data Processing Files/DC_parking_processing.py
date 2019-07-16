import csv
import json
import datetime
from shapely.geometry import Point, shape, MultiPoint
from osgeo import ogr
import pickle
import re
import pandas as pd

def pleaseReadInOrder(filename):
    infile = open(filename, 'rb')
    BigData = pickle.load(infile, fix_imports=True, encoding="ASCII", errors="strict")
    infile.close()
    Data = BigData
    download_dir = "csvboi.csv"
    csv = open(download_dir, "w")
    result = re.sub("}, {|{|},",'\n', str(Data))
    #result2 = "(%s)" % str(result).strip("[")
    NoApostrophe = re.sub("'",'', result)
    CleanResult = re.sub("last_updated: (.*) data:|ttl: 10|bikes:", '', NoApostrophe)
    NewResult = re.sub("is_disabled:|disabled:|is_reserved:|reserved:|lon:|lat:|vehicle_type:|bike_id:|"
                       "battery_level:|jump_ebike_battery_level:|name|jump_vehicle_type|:|type",'', CleanResult)
    row = NewResult
    #csv.write(CleanDateTime)
    csv.write(row)


def open_csvfile(filename):
    """""
    Open CSV file and converts it into a list of dictionaries. This dictionary separates the different data fields of 
    the csv file into different keys.
    :param filename, which is the name of the csv file, must be in valid format (i.e. data.csv)
    :return list of dictionaries containing data fields separated into different keys
    """""

    with open(filename, 'r') as input_file:
        reader = csv.reader(input_file, delimiter=',', quoting=csv.QUOTE_ALL, quotechar='"')
        # skip the first row of the csv file
        # populate dictionary with data fields from csv file
        scooter_data = [{
           # 'device_name': int(row[]),
            'device_ID': row[0],
            'xy': Point(float(row[2]), float(row[1]))
        }
            for row in reader]
        return scooter_data


def validate_time(scooter_data):
    """""
    Iterates over dictionary: scooter_data and verifies that the time are within the specified range (8:00am -
    3:59am) otherwise it removes the data points that don't lie within this time range
    :param scooter_data, list of dictionaries containing the data points from the csv file
    :return returns dictionary which only contains validated dates
    """""
    setup_start_time = datetime.time(4, 0, 0, 0)
    setup_end_time = datetime.time(8, 0, 0, 0)
    return_list = []
    for trip in scooter_data:
        trip_end_time = trip['date_time'].time()
        if not setup_start_time <= trip_end_time <= setup_end_time:
            return_list.append(trip)
    return return_list


def point_within_boundary(file_path_0, file_path_1, scooter_data):
    """""
    Checks for points that are within campus geofence. It adds the points within the campus geofence into a new list 
    and returns this new list.
    :param file_path_0, file path that contains first boundary
    :param file_path_1, file path that contains second boundary
    :param scooter_data, list of dictionaries that contain the trip data.
    :return returns list of dictionaries including only points within campus boundary.
    """""
    # load campus geofence
    shpfile = ogr.Open(file_path_0)
    shapes = shpfile.GetLayer(0)
    facil_bndry = shapes.GetFeature(0)
    facil_bndry = json.loads(facil_bndry.ExportToJson())
    facil_bndry = shape(facil_bndry['geometry'])
    shpfile = ogr.Open(file_path_1)
    shapes = shpfile.GetLayer(0)
    neighborhoods = [json.loads(shapes.GetFeature(fi).ExportToJson()) for fi in range(shapes.GetFeatureCount())]
    neighborhoods = {n['id']: n for n in neighborhoods}
    for n in neighborhoods.values():
        n['geometry'] = shape(n['geometry'])
    print("number of scooter dropoffs on campus:", len([True for s in scooter_data if s['xy'].within(
        facil_bndry)]))
    return_list = []

    # append data points within campus boundary to new list
    for s in scooter_data:
        if s['xy'].within(facil_bndry):
            return_list.append(s)
    # return the new list with validated data points
    return (return_list, facil_bndry)




def main():
    scooter_data = open_csvfile("/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/Clean_DC_CSVs/DC_Test.csv")
    print("Data points in csv: " + str(len(scooter_data)))
    file_path_0 = '/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/DC_Outlines' \
                  '/Washington_DC_Boundary/Washington_DC_Boundary.shp'
    file_path_1 = '/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/DC_Outlines/' \
                  'Building_Footprints/Building_Footprints.shp'
    #file_path_0 = '/Users/BrandonHall/PycharmProjects/city_bike_trips/data/spatial/ofo_boundary.shp'
    #file_path_1 = '/Users/BrandonHall/PycharmProjects/city_bike_trips/data/spatial/vu_neighborhoods.shp'
    scooter_data, facil_bndry = point_within_boundary(file_path_0, file_path_1, scooter_data)
    import matplotlib.pyplot as plt
    plt.plot(*facil_bndry.exterior.xy)
    plt.show()

if __name__ == "__main__":
    main()

