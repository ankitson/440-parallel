from mpi4py import *

if __name__ == '__main__':
    rank = MPI.COMM_WORLD.Get_rank()
    if rank == 0:
        server()
    else:
        slave()

def generate_new_centroids(centroids,pts,k):
    size = [] * k
    for i in xrange(k):
        for node in pts:
            size[i] += node[i]
    
    new_centroids = [Point(0,0)] * k
    for i in xrange(k):
        for j in xrange(len(centroids)):
            if (size[i] != 0):
                centroid = centroids[j][i]
                if centroid == None:
                    continue
                scale_factor = float(pts[j][i])/float(size[i])
                newptx = centroid.x * scale_factor
                newpty = centroid.y * scale_factor
                oldptx = new_centroids[i].x
                oldpty = new_centroids[i].y
                new_centroids[i] = Point(newptx+oldptx,newpty+oldpty)
    return new_centroids

def parallel_kmeans(k,centroids,points):
    
    comm = MPI.COMM_WORLD

    #number of slave nodes
    s = comm.Get_size() - 1

    #distribute points across nodes
    points_for_node = [[]] * s
    for (i,point) in enumerate(points):
        points_for_node[i % s].append(point)
    
    for i in xrange(s):
        comm.send(k,dest=i+1)
        comm.send(points_for_node[i],dest=i+1)
    
    slave_centroids = [[]] * s
    slave_pts = [[]] * s
    
    iters = 0
    while True:
        iters += 1
        comm.bcast(centroids)
        for i in xrange(s):
            (slave_centroids[i],slave_pts[i]) = comm.recv(source=i+1)

        updated = generate_new_centroids(slave_centroids,slave_pts,k)

        if (set(centroids) == set(updated)):
            comm.bcast([],root=0)
            print "Converged in %d iterations" % (iters)
            return centroids

        centroids = copy.deepcopy(updated)

def server():
    if (len(sys.argv) != 3):
        print "Usage : python parallel_kmeans.py <k> <pointsFilePath>"
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
    result = parallel_kmeans(k, centroids, points)
    end_time = time.time()
    centroids_str = '|'.join([str(pt) for pt in result])

    print "Sequential clustering of 2D points took " + str(end_time - start_time) + " seconds"
    print "Centroids: " + centroids_str

def cluster(points,centroids,k):
    clusters = [[]] * k
    for point in points:
        idx = point.find_closest_point(centroids)
        clusters[idx].append(point)
    return clusters
    
def slave():
    comm = MPI.COMM_WORLD

    k = comm.recv(source=0)
    points = comm.recv(source=0)

    new_centroids = [[]] * k
    cluster_sizes = [0] * k

    while True:
        centroids = comm.bcast(centroids,root=0)

        if len(centroids) == 0:
            break

        clustered_points = cluster(points,centroids,k)
        for i in xrange(k):
            new_centroids[i] = Point.average(clustered_points[i])
            cluster_sizes[i] = len(clustered_points[i])

        comm.send((new_centroids,cluster_sizes),dest=0)


