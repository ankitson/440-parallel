from DNA_Point import DNAPoint

import random
import copy
import sys
import time

def get_centroid (points):
    strandLength = len(points[0])
    centroid = []

    for dim in xrange(strandLength):
        bases = {'a':0, 'c':0, 'g':0, 't':0}
        for point in points:
            bases[point[dim]] += 1

        highest_base = 'a'
        highest_count = bases['a']
        for base in bases:
            if (bases[base] >= highest_count):
                highest_base = base
                highest_count = bases[base]
        centroid.append(highest_base)
    return DNAPoint(centroid)

def k_means_clustering (points, k, centroids):
    iterations = 0
    while (True):
        recalculatedCentroids = []
        iterations += 1

        # make k clusters with dna_points in each cluster
        clusters = [[]] * k
        for point in points:
            new_clusterPoints = point.find_closest_point(centroids)
            clusters[new_clusterPoints].append(point)

            # recalculate the new centroids
            for cluster in clusters:
                recalculatedCentroids.append(get_centroid(cluster))

            # check if centroids match
            if (set(centroids) == set(recalculatedCentroids)):
                print "Clustering completed in " + str(iterations) + " iterations"
                return recalculatedCentroids

            # re-iterate if new and old centroids do not match
            centroids = copy.deepcopy(recalculatedCentroids)

if __name__ == "__main__":
    if (len(sys.argv) != 3):
            print "Usage: python sequential_dna_clustering.py <k> <DNA_Points_filepath>"
            sys.exit(0)
    k = int(sys.argv[1])
    if (k <= 0):
            print "Cluster size can't be less than 1"
            sys.exit(0)

    # Read data points
    strPoints = [line.strip() for line in open(sys.argv[2])]
    if (len(strPoints) == 0):
        print "Empty file!"
        sys.exit(0)
    points = []
    for s in strPoints:
        points.append(DNAPoint(s))

    if (k > len(points)):
            print "ERROR: k must be at most the number of data points"
            sys.exit(0)

    # Read centroids from file
    centroids = random.sample(points, k)

    if (len(centroids) != k):
            print "ERROR: k must be equal to number of centroids"
            sys.exit(0)

    # Start k means algorithm
    start_time = time.time()
    result = k_means_clustering(points, k, centroids)
    end_time = time.time()
    print "Centroids: ", result
    print "Sequential Kmeans on DNA data set took " + str(end_time - start_time) + " second(s)"



