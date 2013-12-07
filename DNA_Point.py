import sys

class DNAPoint():

    dna = []

    def __str__(self):
        return "DNA(" + ''.join(self.dna) + ")"

    def __repr__(self):
        return self.__str__()

    def __init__(self, dnaList):
        self.dna = dnaList

    def __len__(self):
        return len(self.dna)

    def __getitem__(self, i):
        return self.dna[i]

    def __cmp__(self, other):
        if(len(self) != len(other)):
            return TypeError

        for i in xrange(len(other)):
            if (cmp(self[i],other[i]) != 0):
                return cmp(self[i],other[i])

        return 0

    def __hash__(self):
        return hash(tuple(self.dna))

    def distance(self, other):
        if (len(self) != len(other)):
            return None

        dist = 0
        for i in xrange(len(self)):
            if (self[i] != other[i]):
                dist += 1
        return dist

    def find_closest_point(self, points):
        if (len(points) == 0):
            return None
        pts_idxs = enumerate(points)
        pts_indxs = [(idx,self.distance(pt)) for (idx,pt) in pts_idxs]

        mindist = sys.maxint
        minptidx = 0
        for (idx,dist) in pts_indxs:
            if dist < mindist:
                mindist = dist
                minptidx = idx

        return minptidx
