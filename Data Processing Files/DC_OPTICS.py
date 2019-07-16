from sklearn.cluster import OPTICS
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from shapely.geometry import shape
import numpy as np
import pickle
from DC_parking_processing import open_csvfile, point_within_boundary, validate_time
from osgeo import ogr
import json


def compute_optics(scooter_data, facil_bndry):
    with open('/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/DC_Outlines/DCboundCoords.pkl', 'rb') as f:
        facilities = pickle.load(f)
    xext = (-76.00, -77.20)
    yext = (38.7, 39.00)
    X = np.array([[trip['xy'].x, trip['xy'].y] for trip in scooter_data])
    print("Shape of X", X.shape)
    clust = OPTICS(min_samples=50, xi=.005, max_eps=.1, min_cluster_size=.005)
# Run the fit
    labels = clust.fit_predict(X)
    unique_labels = set(labels)
    print('there are ' + str(len(unique_labels)-1) + ' clusters')
    # graph clusters
    plt.figure(figsize=(7, 7))
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    plt.fill(*facil_bndry.exterior.xy, c='gold', alpha=0.3)
    plt.plot(*facil_bndry.exterior.xy)
    plt.plot(*facilities.exterior.xy)
    # G = gridspec.GridSpec(1, 1)
    # ax = plt.subplot(G[0, 0])
    # ax.set_title('Automatic Clustering\nOPTICS')

    for klass, color in zip(range(0, len(unique_labels)), colors):
        Xk = X[clust.labels_ == klass]
        plt.plot(Xk[:, 0], Xk[:, 1], alpha=0.9)
    plt.plot(X[clust.labels_ == -1, 0], X[clust.labels_ == -1, 1], 'k+', alpha=0.5)

    plt.axis('equal')
    plt.show()


def main():
    scooter_data = open_csvfile("/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/New_DC_Data copy"
                                "/lyft_07122019-104944.csvmerged_data.csv")
    print("Data points in csv: " + str(len(scooter_data)))
    file_path_0 = '/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/DC_Outlines' \
                  '/Washington_DC_Boundary/Washington_DC_Boundary.shp'
    file_path_1 = '/Users/BrandonHall/Documents/GitHub/SUMDScrapeAndAnalysis/DC_Outlines/' \
                  'Building_Footprints/Building_Footprints.shp'
    # file_path_0 = '/Users/BrandonHall/PycharmProjects/city_bike_trips/data/spatial/ofo_boundary.shp'
    # file_path_1 = '/Users/BrandonHall/PycharmProjects/city_bike_trips/data/spatial/vu_neighborhoods.shp'
    scooter_data, facil_bndry = point_within_boundary(file_path_0, file_path_1, scooter_data)
    compute_optics(scooter_data, facil_bndry)

if __name__ == "__main__":
    main()
