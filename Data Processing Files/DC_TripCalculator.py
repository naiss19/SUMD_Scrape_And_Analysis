import numpy as np
from DC_parking_processing import open_csvfile, validate_time


def TripPlotting(scooter_data):
    '''min_lat, max_lat, min_lon, max_lon = \
        min(scooter_data[1]), max(scooter_data[1]), \
        min(scooter_data[0]), max(scooter_data[0])
    mymap = gmplot.GoogleMapPlotter(
        min_lat + (max_lat - min_lat) / 2,
        min_lon + (max_lon - min_lon) / 2,
        16)'''
    X = np.array([(trip['geometry'].x, trip['geometry'].y) for trip in scooter_data])
    print(X)
    #mymap.plot(X, 'blue', edge_width=1)
    #mymap.draw('my_gm_plot.html')
def main():
    scooter_data = open_csvfile("/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/DC_TripData/Bird_Datav6.csv")
    scooter_data = validate_time(scooter_data)
    print(len(scooter_data))
    #file_path_0 = 'C:/Users/sandovrj/Documents/GitHub/city_bike_trips/data/spatial/ofo_boundary.shp'
    #file_path_1 = 'C:/Users/sandovrj/Documents/GitHub/city_bike_trips/data/spatial/vu_neighborhoods.shp'
    TripPlotting(scooter_data)

if __name__ == "__main__":
    main()
