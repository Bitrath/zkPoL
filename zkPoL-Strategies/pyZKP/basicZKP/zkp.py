from math import sqrt
from random import randint
from sympy import randprime
from Crypto.Random import get_random_bytes
from entities import Prover, Verifier

'''
Generate n = p*q from two large private primes
'''
def generateModulo():
    p = randprime(0, 20) # Between 0 and 19
    q = randprime(0, 20) # Between 0 and 19
    return p*q

'''
Generate two random secrets
- p : Prover entity
- v : Verifier entity
- same : True (outputs the same secret) || False (randomized secrets)
'''
def generateSecrets(p: Prover, v: Verifier, same: bool):
    if same :
        # Generates an equal secret to both
        s = randint(int(sqrt(p.getModulo())), v.getModulo() - 1)
        p.setSecret(s)
        v.setSecret(s)
        return 
    p.setRandomSecret()
    v.setRandomSecret()

'''
Execute a zkp verification algorithm.
- p: Prover entity
- v: Verifier entity
'''
def zero_knowledge_proof(p: Prover, v: Verifier):
    # Generic Variables Setup
    n_p = 0
    n_e = 0

    # Witness Phase: 
        # Prover computes V & X, sends X to the Verifier
    p.setStatememtFromSecret() # V, Prover
    x = p.computeSendStatement() # X
    print("--- (Witness Phase) ---\n " + p.getName() + " computes: \n v = " + str(p.getStatement()) + "\n x = " + str(x))
    print("\n ...sends x to " + v.getName() + "...")
    print("\n ...At each cycle the following phases are being executed:\n(Challenge Phase) -> (Response Phase) -> (Verification Phase)...")

    while(v.getSatisfaction()):
        # New Cycle
        n_p += 1

        # Challenge Phase:
            # Verifier randomly chooses between 0 and 1, sends it to the Prover
        alpha = v.challenge()
            #print("\n--- (Challenge Phase) ---\n " + v.getName() + " chooses the challenge: " + str(alpha))
            #print("\n ...sends the challenge to " + p.getName() + "...")

        # Response Phase:
            # Prover computes a Proof from the Challenge received, sends the result to the Verifer
        phi = p.proof(alpha)
            #print("\n--- (Response Phase) ---\n" + p.getName() + " computes the proof: " + str(phi))
            #print("\n ...sends the proof to " + v.getName() + "...")

        # Verification Phase:
            # Verifier validates the Proof, takes a decision
        v.setStatememtFromSecret() # V, Verifier
        cycle_validation = v.verify(phi, x, alpha)
            # Number of favorable events (Trues)
        if cycle_validation: n_e += 1
            # Compute new percentage of proof satisfaction
        v.computePercentage(n_e, n_p)
            # Checks its personal satisfaction criteria
        v.isSatisfied(n_p)

        #Current Cycle Results
        print("\n--- CYCLE " + str(n_p) + " ---\n" + "* Challenge: " + str(alpha) + "\n* Validation: " + str(cycle_validation) + "\n* Percentage of Trust: " + str(v.getPercentage()) +"%\n")

    # Setup of the RETURN statement
    validation = True
    if v.getPercentage() < 95.0: validation = False
    print("\nAfter " + str(n_p) + " cycles " + v.getName() + " validates the proof as " + str(validation) + "\n")
    return validation


'''
Setup a verification zkp process between two entities.
'''
if __name__ == '__main__':
    # --- PROMPT INTRO ---
    print("------------------ \n----- Z K P ------ \n------------------ \nCopyright @Bitrath\n")

    # --- SETUP ZKP ---
        # Generate a random modulo m
    m = generateModulo() # Between 0 and 19

        # Create Prover
    address_p = get_random_bytes(16)
    name_p = "Bob"
    pr = Prover(address_p, name_p, m)

        # Create Verifier
    address_v = get_random_bytes(16)
    name_v = "Alice"
    vr = Verifier(address_v, name_v, m)

        # Set random secrets to Verify
    generateSecrets(pr, vr, True)

        # Prompt setupm styling
    print("*** SETUP ***\n")
    print(str(pr.getName()) + " wants to prove to " + str(vr.getName()) + " that he knows a certain secret number.\n")
    print("They decide that the shared modulo used by their algorithms will be: ", m)

    # --- RUN ZKP ---
    print("\n*** ZKP ALGORITHM ***\n")

        # Call Verification Algorithm 
    result = zero_knowledge_proof(pr, vr)

    # --- RESULTS PRINTxs ---
    print("\n*** RESULTS *** \nDoes " + pr.getName() + " really know the secret? \n(" + vr.getName() + " says) " + str(result) + "\n")
    print("\n*** ENTITIES *** " + pr.__str__() + vr.__str__())

    # --- TESTING PRINT ---
    #vr.computePercentage(30, 50)
    #print("\n*** Percentages *** \n " + str(vr.getPercentage()))