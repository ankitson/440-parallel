import copy
import sys
import random
import time
import csv

from Point import Point

'''
Algorithm for clustering based on the template given in handout
'''
def k_means_clustering (k, centroids, points):
    iterations = 0
    while (True):
        recalculatedCentroids = []
        iterations += 1

        # This is a 2-d list where each inner list is a list of points
        # associated with the corresponding centroid/cluster
        clusters = [[]] * k
        for point in points:
            new_clusterPoints = point.find_closest_point(centroids)
            clusters[new_clusterPoints].append(point)
            
        # recalculate the new centroids
        for cluster in clusters:
            recalculatedCentroids.append(Point.getAverage(cluster))

        # check if centroids match
        if (set(centroids) == set(recalculatedCentroids)):
            print "Clustering completed in " + str(iterations) + " iterations"
            return recalculatedCentroids

	# re-iterate if new and old centroids do not match
	centroids = copy.deepcopy(recalculatedCentroids)
	
# Command line arguments
if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print "Usage : python sequential_2DPoints_clustering.py <k> <pointsFilePath>"
        sys.exit(0)

    # number of clusters
    k = int(sys.argv[1])
    if (k <= 0):
        print "There needs to be at least one cluster! (k >= 1)"
        sys.exit(0)
    
    # get the points from generated file
    points = []
    csv_reader = csv.reader(open(sys.argv[2], 'r'))
    for row in csv_reader:
        x = float(row[0])
        y = float(row[1])
        points.append(Point(x,y))

    # choose centroids to start with
    centroids = random.sample(points,k)

    # Run the clustering algorithm
    start_time = time.time()
    result = k_means_clustering(k, centroids, points)
    end_time = time.time()
    centroids_str = '|'.join([str(pt) for pt in result])

    print "Sequential clustering of 2D points took " + str(end_time - start_time) + " seconds"
    print "Centroids: " + centroids_str

        
