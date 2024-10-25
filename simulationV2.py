//new changed with the addition to our neuman-morgan files
import random
import math
import itertools


if __name__ == "__main__":

    def getRelationships(n):
        relationships = dict()
        for i in range(n):
            relationships[i] = [0] * n

            for j in range(n):
                if j == i:
                    relationships[i][j] = 0
                    continue
                if j in relationships:
                    relationships[i][j] = (relationships[j][i])
                    continue

                rand = random.uniform(-1, 1)
                relationships[i][j] = rand
        return relationships
    def getReputations(n, lower, uper):
        reputation = dict()

        for i in range(n):
            reputation[i] = random.uniform(lower, uper)

        return reputation
    def cooperatingUtility(numPlayersDefecting, cooperatingUtility=15, cooperatingScalar=3):
        return cooperatingUtility - (cooperatingScalar * math.log(1 + numPlayersDefecting))
    def defectingUtility(numPlayersDefecting, defectingUtility=30, defectingScalar=2):
        return defectingUtility - (defectingScalar * math.log(1 + numPlayersDefecting))
    def probabiltiy(a, b, choice):
        w1 = 5
        w2 = 1
        w3 = 1

        x = (reputations[b] * w1) + (relationships[a][b] * w2) + (-choice * w3) - 1.1

        return 1 / (1 + math.exp(-x))
    def get_combinations(arr):
        result = []
        # Generate combinations for all possible lengths (1 to len(arr))
        for r in range(1, len(arr) + 1):
            combinations = itertools.combinations(arr, r)
            result.extend(combinations)

        # Convert tuples to lists
        return [list(comb) for comb in result]
    def getExpectedUtilityCombinations(thisNation, combinations, choice):

        # for defecting
        totalUtility = 0

        for comb in combinations:
            percentOfCooperate = 1
            percentOfDefect = 1

            for otherNation in comb:
                percentOfDefect *= (1 - probabiltiy(thisNation, otherNation, choice))

            for otherNation in players:
                if otherNation not in comb:
                    percentOfCooperate *= probabiltiy(thisNation, otherNation, choice)
            totalUtility += (percentOfCooperate * cooperatingUtility(n-len(comb))) + (percentOfDefect * defectingUtility(len(comb)))
        return totalUtility
    def getExpectedUtilityCooperating(thisCountry, n, choice=True):

        totalPD = []
        totalPC = []
        combinations = []

        totalProbDefect = 1
        totalProbCooperate = 1
        temp = []
        for j in range(n):
            if thisCountry == j:
                continue

            temp.append(j)

            # prob of j cooperating when i cooperates
            probCC = probabiltiy(thisCountry, j, 0)
            # prob of j defects when i cooperates
            probCD = 1 - probCC



            totalProbDefect *= probCD
            totalProbCooperate *= probCC

        combinations.append(getExpectedUtilityCombinations(thisCountry, get_combinations(temp), 0))
        totalPD.append(totalProbDefect * defectingUtility(n-1))
        totalPC.append(totalProbCooperate * cooperatingUtility(0))

        print(f"Now nation {thisCountry} is considering what all other nations will do when nation {thisCountry} cooperates")
        print(f"If nation {thisCountry} cooperates, the total probability of all other nations cooperating is {totalProbCooperate * 100}%")
        print(f"If nation {thisCountry} cooperates, the total probability of all other nations defecting is {totalProbDefect * 100}%")


        res = totalPD[0] + totalPC[0] + combinations[0]

        return res
    def getExpectedUtilityDefecting(thisCountry, n, choice=False):
        totalPD = []
        totalPC = []
        combinations = []

        totalProbDefect = 1
        totalProbCooperate = 1
        temp = []
        for j in range(n):
            if thisCountry == j:
                continue

            temp.append(j)
            # prob of j cooperating when i defect
            probDC = probabiltiy(thisCountry, j, 1)
            # prob of j defecting when i defect
            probDD = 1 - probDC

            # prob of j cooperating when i cooperates
            probCC = probabiltiy(thisCountry, j, 0)
            # prob of j defects when i cooperates
            probCD = 1 - probCC

            totalProbDefect *= probDD
            # totalProbDefect *= probCD

            totalProbCooperate *= probDC
            # totalProbCooperate *= probCC

        combinations.append(getExpectedUtilityCombinations(thisCountry, get_combinations(temp), 1))
        totalPD.append(totalProbDefect * defectingUtility(n-1))
        totalPC.append(totalProbCooperate * cooperatingUtility(0))


        print(f"Now nation {thisCountry} is considering what all other nations will do when nation {thisCountry} defects")
        print(f"If nation {thisCountry} defects, the total probability of all other nations cooperating is {totalProbCooperate * 100}%")
        print(f"If nation {thisCountry} defects, the total probability of all other nations defecting is {totalProbDefect * 100}%")

        res = (totalPD[0] + totalPC[0] + combinations[0])
        return res


    n = int(input("How Many Players Do You Want? "))
    players = [0, 1, 2, 3, 4]
    relationships = getRelationships(n)
    reputations = getReputations(n, 0, 0.3)

    for i in range(n):
        print(f"Nation {i}'s turn...")
        expCop = getExpectedUtilityCooperating(i, n)
        expDef = getExpectedUtilityDefecting(i, n)
        print(f"Nation {i}'s expected utility for cooperating is {expCop} ")
        print(f"Nation {i}'s expected utility for defecting is {expDef} ")
        if expCop > expDef:
            print(f'{i} choose to cooperate')
        else:
            print(f'{i} chooses to defect')
        print("")
        print("")

    print("Each nation has a reputation from 0-1.  0 means that nation is very likely to defect and 1 means that nation is very likley to cooperate.")
    print("For this first simulation, every nation had a bad reputation (each nation's reputation ranged from 0 -> 0.3). Meaning that they were all likley to defect")
    print("Lets see what happens when all nations want to cooperate!")
    print("Lets change the reputation of each nation to range from 0.7 -> 1")

    reputations = getReputations(n, 0.7, 1)
    print("")

    for i in range(n):
        print(f"Nation {i}'s turn...")
        expCop = getExpectedUtilityCooperating(i, n)
        expDef = getExpectedUtilityDefecting(i, n)
        print(f"Nation {i}'s expected utility for cooperating is {expCop} ")
        print(f"Nation {i}'s expected utility for defecting is {expDef} ")
        if expCop > expDef:
            print(f'{i} choose to cooperate')
        else:
            print(f'{i} chooses to defect')
        print("")
        print("")

    print("As we can see, if all other nations are more likely to cooperate, everyone else will cooperate")






















