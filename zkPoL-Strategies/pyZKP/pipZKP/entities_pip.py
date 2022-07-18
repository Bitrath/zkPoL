from email import generator
from random import randint, random
from math import sqrt

from sympy import per, true
from raycasting import is_inside_polygon, distance3points, distance2points

'''
Polygon: a class that describes a simple point in space
'''
class Polygon:
    def __init__(self, nVertexes):
        self.nVertexes = nVertexes
        self._points = []
    
    def __str__(self):
        return f'<Polygon - Vertex: {self.nVertexes} - List of Points: {self._points} >'
    
    # --- GETTERS ---
    # Get number of Vertixes
    def getNumberOfVertexes(self):
        return self.nVertexes

    def getListOfPoints(self):
        return self._points

    # --- METHODS ---
    def addPoint(self, point: tuple):
        if(len(self._points) == self.nVertexes): return
        self._points.append(point)

'''
 Entity: a basic communication entity
'''
class Entity:
    def __init__(self, a, n, p: int, g, poly: Polygon, point: tuple):
        self._address = a
        self._name = n
        self._prime = p
        self._generator = g
        self._polygon = poly
        self._point = point
        self._secret = None

    def __str__(self):
        return f'\n--Entity--\n name: {self._address}\n address: {self._name}\n prime: {self._prime}\n generator: {self._generator}\n polygon: {self._polygon}\n point: {self._point}'

    # --- GETTERS ---
    # Get Address
    def getAddress(self):
        return self._address

    # Get Name
    def getName(self):
        return self._name

    # Get Prime
    def getPrime(self):
        return self._prime

    # Get Generator
    def getGenerator(self):
        return self._generator

    # Get Polygon
    def getPolygon(self):
        return self._polygon

    # Get Point
    def getPoint(self):
        return self._point

    # Get Secret
    def getSecret(self):
        return self._secret

    # --- SETTERS ---
    # Set Prime
    def setPrime(self, p):
        self._prime = p

    # Set Polygon
    def setPolygon(self, poly: Polygon):
        self._polygon = poly

    # Set Point
    def setPoint(self, p: tuple):
        self._point = p

    # Set Generator
    def setGenerator(self, g: int):
        self._generator = g

    # Set Secret
    def setSecret(self, s: int):
        self._secret = s


'''
Prover: an Entity which can compute a proof
'''
class Prover(Entity):
    # consider passing a point cyphertext and decypher it inside obj
    def __init__(self, a, n, p: int, g, poly: Polygon, point: tuple):
        super().__init__(a, n, p, g, poly, point)
        self._r = None

    def __str__(self):
        return f'\n--Prover--\n name: {self._address}\n address: {self._name}\n prime: {self._prime}\n generator: {self._generator}\n polygon: {self._polygon}\n point: {self._point}\n secret: {self._secret}'
    
    # --- METHODS ---
    # Computes an X value.
    # The right value is computable only upon the knowledge of such parameters:
    # - a Polygon
    # - a Point inside a polygon
    # - a Prime number
    # - a Number of the Zp field
    def computeX(self):
        sum = 0
        perimeter = 0
        vertexes = self._polygon.getListOfPoints()
        lenght = len(vertexes)
        # 1: Sum of distances
        # 2: Perimeter
        for i in range(0, lenght):
            inc1 = 0
            inc2 = 0
            if i+1 == lenght: # last tuple
                # From Point to side: distance((poly i 0, poly i 1), (poly 0 0, poly 1 0), self._point)
                inc1 = distance3points((vertexes[i][0], vertexes[i][1]), (vertexes[0][0], vertexes[0][1]), self._point)
                # Perimeter increment
                inc2 = distance2points((vertexes[i][0], vertexes[i][1]), (vertexes[0][0], vertexes[0][1]))
            else:
                # From Point to side: distance((poly i 0, poly i 1), (poly i+1 0, poly i+1 0), self._point)
                inc1 = distance3points((vertexes[i][0], vertexes[i][1]), (vertexes[i+1][0], vertexes[i+1][1]), self._point)
                # Perimeter increment
                inc2 = distance2points((vertexes[i][0], vertexes[i][1]), (vertexes[i+1][0], vertexes[i+1][1]))
            sum += inc1
            print(f"\nSUM: {sum}")
            perimeter += inc2
        
        # 3: prime 
        # 4: generator 
        self.setSecret(int(sum + perimeter + self._prime + self._generator))

    def pointInsidePolygon(self) -> bool:
        return is_inside_polygon(self._polygon.getListOfPoints(), self._point)
    
    def proof(self):
        return (pow(self._generator, self._secret) % self._prime) # y = g^x modp

    def chooseR(self):
        self._r = randint(0, self._prime - 2)

    def cStatement(self):
        return (pow(self._generator, self._r) % self._prime) # c = g^r modp

    def challengeStatement(self, challenge):
        if challenge == 0:
            return ((self._secret + self._r) % (self._prime - 1)) # (x + r) modp 
        return self._r


'''
Verifier: an Entity which can verify a proof
'''
class Verifier(Entity):
    def __init__(self, a, n, p: int, g, poly: Polygon, point: tuple):
        super().__init__(a, n, p, g, poly, point)
        self._challenge = None
        self._received = []

    def __str__(self):
        return f'\n--Verifier--\n name: {self._address}\n address: {self._name}\n prime: {self._prime}\n generator: {self._generator}\n polygon: {self._polygon}\n point: {self._point}\n received: {self._received}\n secret: {self._secret}'
    
    # --- GETTER --- 
    def getChallenge(self):
        return self._challenge

    # --- SETTERS ---
    def setChallenge(self, c):
        self._challenge = c
    
    def setReceivedValue(self, value):
        self._received.append(value)

    # --- METHODS ---
    def challenge(self):
        choice = randint(0, 1)
        self.setChallenge(choice) 
    
    def verify(self):
        value1 = 0
        value2 = 0
        if self._challenge == 0: 
            value1 = (self._received[1] * self._received[0]) % self._prime
            value2 = pow(self._generator, self._received[2]) % self._prime
            if value1 == value2: return True
            return False
        value1 = self._received[1]
        value2 = pow(self._generator, self._received[2]) % self._prime
        if value1 == value2: return True
        return False

