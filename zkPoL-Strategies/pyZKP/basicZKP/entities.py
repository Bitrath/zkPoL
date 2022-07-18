from random import randint, random
from math import sqrt

'''
 Entity: a basic communication entity
'''
class Entity:
    # Has an address, a prime, a secret and a statement
    # --> consider passing an encrypted secret at init
    def __init__(self, a, n, m: int):
        self._address = a
        self._name = n
        self._modulo = m
        self._secret = None
        self._statement = None

    def __str__(self):
        return '\nEntity (' + str(self._name) + '):' + '\n--address: ' + str(self._address) + '\n--modulo: ' + str(self._modulo) + '\n--secret: ' + str(self._secret) + '\n--statement: ' + str(self._statement) + '\n'

    # --- GETTERS --- 
    # Get Address
    def getAddress(self):
        return self._address

    # Get Name
    def getName(self):
        return self._name

    # Get Prime
    def getModulo(self):
        return self._modulo

    # Get Secret (USED FOR TESTING)
    def getSecret(self):
        return self._secret 

    # Get Statement
    def getStatement(self):
        return self._statement

    # --- SETTERS ---
    # Set Address
    # - ad : new address value
    def setAddress(self, ad):
        self._address = ad

    # Set Name 
    # - nn : new name value
    def setName(self, nn):
        self._name = nn

    # Set Modulo
    # - mod : new modulo value
    def setModulo(self, mod):
        self._modulo = mod

    # Set Secret USED FOR TESTING
    # - s : new secret value
    def setSecret(self, s):
        self._secret = s

    # Set Statement
    # - st : new statement value
    def setStatement(self, st):
        self._statement = st

    # --- METHODS ---
    # Generate a random secret
    def setRandomSecret(self):
        # self.prime is not yet set, return
        self._secret = randint(int(sqrt(self._modulo)), self._modulo - 1) # Between sqrt(n) and n-1

    # Set a statement from a personal secret
    def setStatememtFromSecret(self):
        self._statement = pow(self._secret, 2) % self._modulo # v = (s^2) modn

'''
Prover: an Entity which can compute a proof
'''
class Prover(Entity):
    def __init__(self, a, n, p: int):
        super().__init__(a, n, p)
        self._R = None

    def __str__(self):
        return '\nProver (' + str(self._name) + '):' + '\n--address: ' + str(self._address) + '\n--modulo: ' + str(self._modulo) + '\n--secret: ' + str(self._secret) + '\n--v statement: ' + str(self._statement) + '\n--r statement: ' + str(self._R) + '\n'

    # --- GETTERS Prover ---
    # Get Personal Statement
    def getR(self):
        return self._R

    # --- SETTERS Prover ---
    # Set a personal statement, the verifier won't be able to.
    def setR(self):
        self._R = randint(1, self._modulo - 1)

    # --- METHODS Prover ---
    # Compute a send-statement
    def computeSendStatement(self):
        if self._R == None : self.setR()
        return pow(self._R, 2) % self._modulo # x = (r^2) modn

    # Compute a Proof from a challenge
    # - a : challenge chosen by Verifier
    def proof(self, a):
        if a == 0:
            return self._R                                     # proof = r
        elif a == 1:
            return (self._R * self._secret)%(self._modulo)   # proof = (r*s) modn


'''
Verifier: an Entity which can verify a proof
'''
class Verifier(Entity):
    def __init__(self, a, n, p: int):
        super().__init__(a, n, p)
        self._satisfaction = True   # True : execute new cycle || False : Verifier satisfied, ends ZKP algorithm
        self._percentage = None 

    def __str__(self):
        return '\nVerifier (' + str(self._name) + '):' + '\n--address: ' + str(self._address) + '\n--modulo: ' + str(self._modulo) + '\n--secret: ' + str(self._secret) + '\n--v statement: ' + str(self._statement) + '\n--percentage: ' + str(self._percentage) + '%\n'

    # --- GETTERS Verifier ---
    # Get Satisfaction 
    def getSatisfaction(self):
        return self._satisfaction

    # Get Percentage 
    def getPercentage(self):
        return self._percentage

    # --- SETTERS Verifier ---
    # Set Satisfaction 
    # - s : new satisfaction value
    def setSatisfaction(self, s):
        self._satisfaction = s

    # Set Percentage 
    # - p : new percentage value
    def setPercentage(self, p):
        self._percentage = p

    # --- METHODS Verifier ---
    # Challenge assigner
    def challenge(self):
        randChoice = random()
        if randChoice < 0.7 : return 0
        return 1

    # Compute Percentage
    # - ev : number of favorable events
    # - cy : number of cycles executed
    def computePercentage(self, ev, cy):
        if not cy : return
        p = 100 * float(ev)/float(cy)
        self.setPercentage(p)

    # Compute Satisfaction
    # - cy : number of cycles executed
    def isSatisfied(self, cy):
        if cy < 10: return 
        if self._percentage < 95.0 and cy < 30: return 
        self.setSatisfaction(False)
        

    # Verifies a proof received
    # - proof : proof received from Prover
    # - x : pulic statement received from Prover
    # - a : challenge used by Prover to compute proof
    def verify(self, proof, x, a):
        received = pow(proof, 2) % self._modulo # (proof^2) modn
        if a == 0:
            # x [the Prover could trick the Verifier]
            personal = x
        elif a == 1: 
            # (x)*(v^a) modn [the Prover cannot trick the Verifier]
            personal = (x * (pow(self._statement, a))) % self._modulo 
        #print("\n--- (Verification Phase) ---\n " + self.getName() + " computes:\n * Statement from Proof -> "+ str(received) + "\n * Personal statement based on the challenge -> " + str(personal))

        # validation
        if received == personal: return True # proof^2 == x*(v^a) modn
        return False


'''
Point: a class that describes a simple point in space
'''
class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    # GETTERS
    def getX(self):
        return self._x

    def getY(self):
        return self._y

    # SETTERS
    def setX(self, nX):
        self._x = nX
        
    def setY(self, nY):
        self._y = nY

'''
Polygon: a class that describes a simple point in space
'''
class Polygon:
    def __init__(self, numVertexes):
        self._numVertexes = numVertexes
        self._points = []