import sys

class DNAPoint():

    dna = []

    def __init__(self, dnaList):
        self.dna = dnaList

    def __len__(self):
        return len(self.dna)

    def __getitem__(self, i):
        return self.dna[i]

    def __cmp__(self, other):
	if(len(self) != len(other)):
            return False
        for i in range (len(other)):
            if(self[i] != other[i]):
                return False
        return True

    def __hash__(self):
        return hash(tuple(self.dna))

    def distance(self, other):
        if (len(self) != len(other)):
            return None
        dist = len(self)
        for i in range(0, len(self)):
            if (self[i] != other[i]):
                dist-= 1
        return dist

    # check the deal with max int
    def find_closest_point(self, points):
	
        if (len(points) == 0):
            return None
        max_dist = -sys.maxint - 1
        cur_centroid = 0
        for i in xrange(len(points)):
            icentroid_dist = self.distance(points[i])
            if (icentroid_dist > max_dist):
                max_dist = icentroid_dist
                cur_centroid = i
        return cur_centroid


