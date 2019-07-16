import datetime
import csv
import json
from shapely.geometry import Point, shape, MultiPoint
from osgeo import ogr
from itertools import product
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pickle
from statistics import median
from operator import itemgetter
import hdbscan

# *****IMPORT LIBRARIES FOR YOUR CLUSTER ALGORITHMS HERE*****


# ***************************************************************

class Cluster:
    def __self__(self):
        self.scooter_data = []
        self.facil_boundary = None
        self.rides = []
        self.campus_rides = []
        self.facilities = None
        self.chronological_campus_rides = []

    def load_data(self, geofence_file, neighborhood_file):
        # open file containing scooter trips
        print("OPENING CSV FILE CONTAINING TRIPS DATA")
        with open('scooter_locations.csv', 'r') as csv_file:
            file_reader = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_ALL, quotechar='"')
            header = next(file_reader)
            self.scooter_data = [{
                'record': int(row[0]),
                'company': row[1],
                'device_ID': row[2],
                'geometry': Point(map(float, row[3].split('[')[1].split(']')[0].split(','))),
                'date_time': datetime.datetime.fromtimestamp(float(row[4]))
            } for row in file_reader]
        print("DONE LOADING CSV FILE CONTAINING TRIPS DATA\n")

        # load geofence
        print("LOADING VU GEOFENCE AND NEIGHBORHOOD FILES")
        shpfile = ogr.Open(geofence_file)
        shapes = shpfile.GetLayer(0)
        self.facil_boundary = shapes.GetFeature(1)
        self.facil_boundary = json.loads(self.facil_boundary.ExportToJson())
        self.facil_boundary = shape(self.facil_boundary['geometry'])
        shpfile = ogr.Open(neighborhood_file)
        shapes = shpfile.GetLayer(0)
        neighborhoods = [json.loads(shapes.GetFeature(fi).ExportToJson()) for fi in range(shapes.GetFeatureCount())]
        neighborhoods = {n['id']: n for n in neighborhoods}
        for n in neighborhoods.values():
            n['geometry'] = shape(n['geometry'])
        print("DONE LOADING VU GEOFENCE AND NEIGHBORHOOD FILES\n")

        # filter trips that are outside of VU's geofence and that are between the time interval 4:00am-8:00am
        print("FILTERING TRIPS BY TIME AND LOCATION")
        staging_start = 4
        staging_end = 8
        self.rides = [s for s in self.scooter_data if s['date_time'].time().hour < staging_start or s['date_time'].time(

        ).hour >=
                      staging_end]
        self.campus_rides = [s for s in self.rides if s['geometry'].within(self.facil_boundary)]
        print("DONE FILTERING TRIPS BY TIME AND LOCATION\n")

        # sort data in chronological order
        print("SORTING DATA IN CHR0NOLOGICAL ORDER")
        self.chronological_campus_rides = sorted(self.campus_rides, key=itemgetter('date_time'))
        print("DONE SORTING DATA IN CHRONOLOGICAL ORDER\n")

    def clustering(self, facilities_file, csv_file, **kwargs):
        # load pickle file with facilities
        print("OPENING VU FACILITIES FILE")
        with open(facilities_file, 'rb') as facilities:
            self.facilities = pickle.load(facilities)
            self.facilities = [fc['geom'] for fc in self.facilities[2].values()]
        print("DONE OPENING VU FACILITIES FILE\n")

        # load train data file
        print("OPENING TRAINING DATA FILE")
        with open('train_set.pickle', 'rb') as train_pickle:
            train_data = pickle.load(train_pickle)
        print("DONE OPENING TRAiNING DATA FILE\n")

        # load test data file
        print("OPENING TESTING DATA FILE")
        with open('test_set.pickle', 'rb') as test_pickle:
            test_data = pickle.load(test_pickle)
        print("DONE OPENING TRAINING DATA FILE\n")

        # results = []
        # parking_locations_list = []
        #
        # print("PERFORMING TRAINING/TESTING FOR CLUSTERING ALGORITHM")
        # # *****WILL HAVE TO CHANGE THE PARAMETERS AND FUNCTION VARIABLES DEPENDING ON YOUR CLUSTERING ALGORITHMS
        # # REQUIREMENTS*****
        # for eps, smpls in product(kwargs['epsilon'], kwargs['min_samples']):
        #     try:
        #         # perform clustering using train data
        #         # ********CHANGE THIS PART OF CODE TO BEST FIT YOUR CLUSTERING ALGORITHMS' REQUIREMENTS*****
        #         clustering_i = DBSCAN(eps=eps, min_samples=smpls, metric='euclidean', n_jobs=-1)
        #         train_labels_i = clustering_i.fit_predict(train_data)
        #         # ******************************************************************************************
        #
        #
        #         # compute the number of clusters found by the clustering algorithm
        #         train_unique_labels_i = sorted(list(set(train_labels_i)))
        #
        #         parking_location = None
        #         # for loop that computes performances for the clustering algorithms
        #         for label in train_unique_labels_i:
        #             if label == -1:
        #                 continue
        #             # declare variables that will be used to keep track of results
        #             hulls_i = []
        #             buffers_i = []
        #             sizes_i = []
        #             points_in_cluster = [point for point, cluster_label in zip(train_data, train_labels_i) if
        #                                  cluster_label == label]
        #             # compute median for x and y coordinates
        #             x_coordinates = [point[0] for point in points_in_cluster]
        #             y_coordinates = [point[1] for point in points_in_cluster]
        #             x_median = median(x_coordinates)
        #             y_median = median(y_coordinates)
        #
        #             # determine the parking location
        #             parking_location = Point(x_median, y_median)
        #             parking_locations_list.append(parking_location)
        #
        #             # compute cluster hulls and buffers
        #             class_member_mask = (train_labels_i == label)
        #             cl = train_data[class_member_mask]
        #             hull = MultiPoint(cl).convex_hull
        #             hulls_i.append(hull)
        #             sizes_i.append(hull.area)
        #             cnt = parking_location
        #             # HAVE TO CALCULATE THE VALUE THAT REPLACES 0.0004
        #             buf = cnt.buffer(0.000314858698466)
        #             buffers_i.append(buf)
        #
        #             train_hull_capture_i = 0
        #             train_buffer_capture_i = 0
        #             for r in train_data:
        #                 cur_point = Point(r)
        #                 if cur_point.within(buf):
        #                     train_buffer_capture_i += 1
        #                 if cur_point.within(hull):
        #                     train_hull_capture_i += 1
        #
        #             train_results_i = ('train', eps, smpls, train_buffer_capture_i, (parking_location.x,
        #                                 parking_location.y), len(train_data), len(train_unique_labels_i),
        #                                train_hull_capture_i)
        #
        #             results.append(train_results_i)
        #
        #             test_hull_capture_i = 0
        #             test_buffer_capture_i = 0
        #             # evaluate clustering using test data
        #             for r in test_data:
        #                 cur_point = Point(r)
        #                 if cur_point.within(buf):
        #                     test_buffer_capture_i += 1
        #                 if cur_point.within(hull):
        #                     test_hull_capture_i += 1
        #
        #             test_results_i = ('test', eps, smpls, test_buffer_capture_i, (parking_location.x,
        #                             parking_location.y), len(test_data))
        #             results.append(test_results_i)
        #
        #     except:
        #         continue

        results = []
        graph_results = []
        parking_location = None

        # *****COMMENT THIS OUT IF YOUR ALGORITHMS DOES NOT USE MIN_SAMPLES*****
        min_samples = [int(len(train_data) * 0.001), int(len(train_data) * 0.002), int(len(train_data) * 0.003), int(len(train_data) *
                       0.004), int(len(train_data) * 0.005)]
        # **********************************************************************

        print("PERFORMING TRAINING/TESTING FOR HDBSCAN ALGORITHM")
        # *****WILL HAVE TO CHANGE THE PARAMETERS AND FUNCTION VARIABLES DEPENDING ON YOUR CLUSTERING ALGORITHMS
        # REQUIREMENTS*****
        for mcs, smpls in product(kwargs['min_cluster_size'], min_samples):
            #try:
                # perform clustering using train data
                # ********CHANGE THIS PART OF CODE TO BEST FIT YOUR CLUSTERING ALGORITHMS' REQUIREMENTS*****
                clustering_i = hdbscan.HDBSCAN(min_cluster_size=mcs, min_samples=smpls)
                train_labels_i = clustering_i.fit_predict(train_data)
                # ******************************************************************************************

                # compute the number of clusters found by the clustering algorithm
                train_unique_labels_i = sorted(list(set(train_labels_i)))

                # parking_location = None
                hulls_i = []
                buffers_i = []
                sizes_i = []
                # for loop that computes performances for the clustering algorithms
                for label in train_unique_labels_i:
                    if label == -1:
                        continue
                    # declare variables that will be used to keep track of results
                    #                     hulls_i = []
                    #                     buffers_i = []
                    #                     sizes_i = []
                    points_in_cluster = [point for point, cluster_label in zip(train_data, train_labels_i) if
                                        cluster_label == label]
                    # compute median for x and y coordinates
                    x_coordinates = [point[0] for point in points_in_cluster]
                    y_coordinates = [point[1] for point in points_in_cluster]
                    x_median = median(x_coordinates)
                    y_median = median(y_coordinates)

                    # determine the parking location
                    parking_location = Point(x_median, y_median)

                    # compute cluster hulls and buffers
                    class_member_mask = (train_labels_i == label)
                    cl = train_data[class_member_mask]
                    hull = MultiPoint(cl).convex_hull
                    hulls_i.append(hull)
                    sizes_i.append(hull.area)
                    cnt = parking_location
                    # HAVE TO CALCULATE THE VALUE THAT REPLACES 0.0004
                    buf = cnt.buffer(0.000314858698466)
                    buffers_i.append(buf)

                    train_hull_capture_i = 0
                    train_buffer_capture_i = 0
                    for r in train_data:
                        cur_point = Point(r)
                        if cur_point.within(buf):
                            train_buffer_capture_i += 1
                        if cur_point.within(hull):
                            train_hull_capture_i += 1

                    train_results_i = ('train', mcs, smpls, train_buffer_capture_i, (parking_location.x,
                                        parking_location.y), len(train_data), len(train_unique_labels_i),
                                       train_hull_capture_i)

                    results.append(train_results_i)

                    test_hull_capture_i = 0
                    test_buffer_capture_i = 0
                    # evaluate clustering using test data
                    for r in test_data:
                        cur_point = Point(r)
                        if cur_point.within(buf):
                            test_buffer_capture_i += 1
                        if cur_point.within(hull):
                            test_hull_capture_i += 1

                    test_results_i = ('test', mcs, smpls, test_buffer_capture_i, (parking_location.x,
                                                                              parking_location.y), len(test_data))
                    results.append(test_results_i)

                graph_buffer_capture = 0
                for r in test_data:
                    cur_point = Point(r)
                    for b in buffers_i:
                        if cur_point.within(b):
                            graph_buffer_capture += 1
                            break
                print(graph_buffer_capture)

                test_results_graph = (mcs, smpls, graph_buffer_capture, len(train_unique_labels_i))
                graph_results.append(test_results_graph)

            #except:
                #continue

        print("DONE PERFORMING TRAINING/TESTING FOR CLUSTERING ALGORITHM\n")

        # print results into csv file
        print("PRINTING RESULTS INTO CSV FILE")
        csv_file = open(csv_file, 'w')
        csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(('Data', 'Min Cluster Size', 'Min Pts', 'Performance (buffer capture)', 'Parking Location',
                             '# of points on file', '# of Clusters', 'Hull capture'))
        for row in results:
            csv_writer.writerow(row)
        csv_file.close()
        print("DONE PRINTING RESULTS INTO CSV FILE\n")

        print("GRAPHING PERFORMANCE")
        performance = [result[2] for result in graph_results]
        x_values = [result[0] for result in graph_results]
        y_values = [result[1] for result in graph_results]
        clusters = [result[3] for result in graph_results]

        ax = plt.axes(projection='3d')
        ax.scatter(x_values, y_values, performance, c=performance, cmap='viridis')
        ax.set_xlabel('Min Cluster Size')
        ax.set_ylabel('Min Samples')
        ax.set_zlabel('Performance (points captured by the buffer)')
        ax.set_title('Cluster Performance')
        plt.savefig('HDBSCAN_cluster_performance.png')
        print("DONE GRAPHING AND SAVING PERFORMANCE")

        print("CREATING CSV GRAPH PERFORMANCE FILE")
        graph_performance_results = []
        for mcs, smpl, perf, cluster in zip(x_values, y_values, performance, clusters):
            performance_values = (mcs, smpl, perf, cluster)
            graph_performance_results.append(performance_values)
        csv_performance_file = open("graph_performance.csv", 'w', newline='')
        csv_graph_writer = csv.writer(csv_performance_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csv_graph_writer.writerow(('Min Cluster Size', 'Min Samples', 'Total Performance', 'Number of Clusters'))
        for row in graph_performance_results:
            csv_graph_writer.writerow(row)
        csv_performance_file.close()
        print("DONE CREATING CSV GRAPH PERFORMANCE FILE")


def main():

    # *****CHANGE FILE PATHS/PARAMETERS FOR FUNCTION CALLS*****
    hdbscan = Cluster()
    hdbscan.load_data(geofence_file='C:/Users/caleb/Documents/GitHub/city_bike_trips/data/spatial'
                                   '/ofo_boundary.shp',
                     neighborhood_file='C:/Users/caleb/Documents/GitHub/city_bike_trips/data/spatial'
                                       '/vu_neighborhoods.shp')
    min_cluster_size = [100, 200, 300, 400, 500]
    hdbscan.clustering(facilities_file='C:/Users/caleb/Documents/GitHub/city_bike_trips/data/spatial'
                                      '/vu_facilities.pkl',
                      csv_file='C:/Users/caleb/Documents/GitHub/city_bike_trips/parking_optimization'
                               '/hdbscan_performance.csv',
                      min_cluster_size=min_cluster_size)

    # ***********************************************************


if __name__ == "__main__":
    main()
