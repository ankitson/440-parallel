import math
import sys

class Point:

    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __cmp__(self, other):
        return cmp(self.x, other.x) and cmp(self.y, other.y)

    def __hash__(self):
	return hash((self.x, self.y))

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'
    
    def distance(self, other):
        dx = math.fabs(self.x - other.x)
        dy = math.fabs(self.y - other.y)
        return math.sqrt(dx * dx + dy * dy)


    # todo
    def find_closest_point(self, points):
      
        if (len(points) == 0):
            return None
        min_dist = sys.maxint
        cur_centroid = 0
        for i in xrange(len(points)):
            icentroid_dist = self.distance(points[i])
            if (icentroid_dist <= min_dist):
                min_dist = icentroid_dist
                cur_centroid = i
        return cur_centroid

    @staticmethod
    def getAverage(points):
	    
        if (len(points) == 0):
            return None
        sum_x = 0
        sum_y = 0
        for point in points:
            sum_x += point.x
            sum_y += point.y
        return Point(float(sum_x)/len(points), float(sum_y)/len(points))



