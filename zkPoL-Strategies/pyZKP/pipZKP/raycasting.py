from math import sqrt

'''
Given a certain polygon, check if a point lies within.
[ A study on code by Vikas Chitturi ]
'''

# Define a constant to get out abstract INFINITE
INFINITE = 1000

'''
METHODS: 
- distance2points(point p, point q)
- distance3points(point p, point q, point r)
- onSegment(point p, point q, point r)
- orientation(point p, point q, point r)
- doIntersect(p1, q1, p2, q2)
- is_inside_polygon(polygon, point)
'''
def distance2points(p: tuple, q: tuple):
  return sqrt(pow((q[0] - p[0]), 2) + pow((q[1] - p[1]), 2))

def distance3points(p: tuple, q: tuple, r: tuple):
  num = abs(((q[0] - p[0])*(p[1] - r[1])) - ((p[0] - r[0])*(q[1] - p[1])))
  den = distance2points(p, q)
  return num/den

# Given three collinear points p, q, r, 
# the function checks if point q lies
# on line segment 'pr'
def onSegment(p: tuple, q: tuple, r: tuple) -> bool:
    if((q[0] <= max(p[0], r[0])) &
       (q[0] >= min(p[0], r[0])) &
       (q[1] <= max(p[1], r[1])) &
       (q[1] >= min(p[1], r[1]))):
       return True
    return False

# To find orientation of ordered triplet (p, q, r).
# The function returns following values
# 0 --> p, q and r are collinear
# 1 --> Clockwise
# 2 --> Counterclockwise
def orientation(p: tuple, q: tuple, r: tuple) -> int:
    val = (((q[1] - p[1]) * (r[0] - q[0])) - ((q[0] - p[0]) * (r[1] - q[1])))
    if val == 0: return 0 # Collinear
    if val > 0:  return 1 # Clock
    else:  return 2 # Counterclock

def doIntersect(p1, q1, p2, q2):
    # Find the four orientations needed for 
    # general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if (o1 != o2) and (o3 != o4):
        return True

    # Special Cases

    # p1, q1 and p2 are collinear and
    # p2 lies on segment p1q1
    if (o1 == 0) and (onSegment(p1, p2, q1)):
        return True

    # p1, q1 and p2 are collinear and
    # q2 lies on segment p1q1
    if (o2 == 0) and (onSegment(p1, q2, q1)):
        return True
 
    # p2, q2 and p1 are collinear and
    # p1 lies on segment p2q2
    if (o3 == 0) and (onSegment(p2, p1, q2)):
        return True
 
    # p2, q2 and q1 are collinear and
    # q1 lies on segment p2q2
    if (o4 == 0) and (onSegment(p2, q1, q2)):
        return True
 
    return False

# Returns true if the point p lies 
# inside the polygon[] with n vertices
def is_inside_polygon(points: list, p: tuple) -> bool:
    n = len(points)
     
    # There must be at least 3 vertices
    # in polygon
    if n < 3:
        return False
         
    # Create a point for line segment
    # from p to infinite
    extreme = (INFINITE, p[1])
    count = i = 0
     
    while True:
        next = (i + 1) % n
        # Check if the line segment from 'p' to 
        # 'extreme' intersects with the line 
        # segment from 'polygon[i]' to 'polygon[next]'
        if (doIntersect(points[i],
                        points[next],
                        p, extreme)):             
            # If the point 'p' is collinear with line 
            # segment 'i-next', then check if it lies 
            # on segment. If it lies, return true, otherwise false
            if orientation(points[i], p,
                           points[next]) == 0:
                return onSegment(points[i], p,
                                 points[next])               
            count += 1
        i = next
        if (i == 0): 
            break
    # Return true if count is odd, false otherwise
    return (count % 2 == 1)