import math
import sys

class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __cmp__(self, other):
        xcmp = cmp(self.x,other.x)
        if xcmp != 0:
            return xcmp
        else:
            return cmp(self.y,other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def distance(self, other):
        x1 = float(self.x)
        x2 = float(other.x)
        y1 = float(self.y)
        y2 = float(other.y)

        xdist = math.pow(abs(x1-x2),2)
        ydist = math.pow(abs(y1-y2),2)
        return math.sqrt(xdist + ydist)

    #Return the point out of points closest to this one
    def find_closest_point(self,points):
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

    @staticmethod
    def average(points):
        if (len(points) == 0):
            return None

        xsum = 0.0
        ysum = 0.0
        for point in points:
            xsum += point.x
            ysum += point.y

        return Point(float(xsum)/float(len(points)), float(ysum)/float(len(points)))
