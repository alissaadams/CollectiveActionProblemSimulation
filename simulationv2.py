import random
import math
import itertools

def getRelationships(n, upper, lower):
    '''
    :param n: the number of players/nations
    :return: map of relationships

    Key will be a nation, and the value will be an array
    each index of the array will represent the relationship with the key

    So if there are 5 players. And we do relationships[3], this will give us an array for nation 3, call it relations. Then
    if we do relations[4] this gives us nations 3 relationship with nation 4.

    Note that if we deo relations[3], this will be a zero, because nations 3 relationship with itself is neutral.
    And not that relationships[3][4] == relationships[4][3] because nations 3 relationship with nation 4 is the same as nation's
    4 relationship with nation 3.
    '''
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
            rand = random.uniform(lower, upper)
            relationships[i][j] = rand
    return relationships

def getReputations(n, lower, upper):
    '''
    :param n: number of players/nations
    :param lower: lower range for reputation (between 0 - 1)
    :param upper: upper range for reputation (between 0 - 1)
    :return: hash map of reputations, where the key is a nation and the value is their reputation. Size of hashmap is n

    Assigns each nation a random reputation that falls between the lower and upper bounds
    '''
    reputation = dict()

    for i in range(n):
        reputation[i] = random.uniform(lower, upper)

    return reputation

def populatiryPoints(numCooperated):
    '''
    :param numCooperated:
    :return: peacePoints

    This is a mechanism that will increase utility for cooperation. Basically, the first nation that cooperates will get
    lots of popularity points as they will gain social respect. Later, as more nations cooperate, they receive lets
    popularity points as they were not the first nations to cooperate.

    TODO
        Find an optimal number for populatiryPoints. Right now its just 200, is there a better number?
        Also can we make this equation more realistic to model the real world?
    '''
    return 200 / (numCooperated + 1)

def cooperatingUtility(numPlayersDefecting, cooperatingUtility=15, cooperatingScalar=2):
    '''

    :param numPlayersDefecting: number of players defecting
    :param cooperatingUtility: A constant that represents the base utility for cooperating
    :param cooperatingScalar: A constant that represents the base cost for cooperating
    :return: utility that represent cooperating

    This models our cooperating utility function found in the readMe.

    TODO
        Verify that this utility function makes sense based on readMe and code
    '''
    return cooperatingUtility - (cooperatingScalar * math.log(1 + numPlayersDefecting))

def cooperatingUtilityMech(numPlayersDefecting, cooperatingUtility=15, cooperatingScalar=2):
    '''

    :param numPlayersDefecting: number of players defecting
    :param cooperatingUtility: A constant that represents the base utility for cooperating
    :param cooperatingScalar: A constant that represents the base cost for cooperating
    :return: utility that represent cooperating

    This models our cooperating utility function found in the readMe.
    This utility function has an additional mechanism to encourage cooperation. It provides 175 extra util points

    TODO
        Verify that this utility function makes sense based on readMe and code
    '''
    return cooperatingUtility - (cooperatingScalar * math.log(1 + numPlayersDefecting)) + 50

def defectingUtility(numPlayersDefecting, defectingUtility=30, defectingScalar=3):
    '''

    :param numPlayersDefecting: number of players defecting
    :param defectingUtility: A constant that represents the base utility for defecting
    :param defectingScalar: A constant that represents the base cost for defecting
    :return: utility that represent defecting

    This models our defecting utility function found in the readMe.

    TODO
        Verify that this utility function makes sense based on readMe and code
    '''
    return defectingUtility - (defectingScalar * math.log(1 + numPlayersDefecting))

def probabiltiy(a, b, choice):
    '''

    :param a: nation that is making the choice to either defect or cooperate
    :param b: this is the "other" nation that nation a is considering
    :param choice: if a is cooperating or defecting
    :return: the probability that nation b will cooperate

    this represents our probability function found on the readMe

    TODO
        Modify the weights and see which work best. We want reputation to be weighed the highest!
        I had trouble with the weights. When increasing w2 and w3 I got weird results. Try them out and
        see if anything weird happens for you (look at nations choices).
    '''
    w1 = 5
    w2 = 3
    w3 = 1

    x = (reputations[b] * w1) + (relationships[a][b] * w2) + (-choice * w3)

    return 1 / (1 + math.exp(-x))

def get_combinations(arr):
    '''

    :param arr: An array of all n nations. EX: If there are 5 nations, arr = [0,1,2,3,4]
    :return: An array of all possible combinations for players

    used for getExpectedUtilityCombinations
    '''
    result = []
    # Generate combinations for all possible lengths (1 to len(arr))
    for r in range(1, len(arr) + 1):
        combinations = itertools.combinations(arr, r)
        result.extend(combinations)

    # Convert tuples to lists
    return [list(comb) for comb in result]

def getExpectedUtilityCombinations(thisNation, combinations, choice):
    '''
    :param thisNation: represents the nation that is making the choice to either defect or cooperate
    :param combinations: an array of nations. We assume that each nation in this array will defect.Any nation
    not in this array will cooperate
    :param choice: if thisNation is cooperating or defecting
    :return: total utility for all possible combinations

    This represents the complex summation part of the equation in readMe

    TODO
        Word the description better. Fix variable names to make it less confusing.
    '''
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
        totalUtility += (percentOfCooperate * cooperatingUtility(n - len(comb))) + (
                    percentOfDefect * defectingUtility(len(comb)))
    return totalUtility

def getExpectedUtilityCombinationsMech(thisNation, combinations, choice):
    '''
    :param thisNation: represents the nation that is making the choice to either defect or cooperate
    :param combinations: an array of nations. We assume that each nation in this array will defect.Any nation
    not in this array will cooperate
    :param choice: if thisNation is cooperating or defecting
    :return: total utility for all possible combinations

    This represents the complex summation part of the equation in readMe

    TODO
        Word the description better. Fix variable names to make it less confusing.
    '''
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
        totalUtility += (percentOfCooperate * cooperatingUtilityMech(n - len(comb))) + (
                    percentOfDefect * defectingUtility(len(comb)))
    return totalUtility

def getExpectedUtilityCooperating(thisCountry, n, choice=True):
    '''
    :param thisCountry: represents the nation that is making the choice to either defect or cooperate
    :param n: number of players / nations
    :param choice: if thisCountry is cooperating or defecting. Always set to True ( 1 ).
    :return: total utility assuming that thisCountry is cooperating

    TODO
        Fix varaible names so it makes more sense. Verify everything works as should... no logical errors
    '''

    # total probability of all nations defecting
    totalProbDefect = 1
    # total probability of all nations cooperating
    totalProbCooperate = 1
    otherNations = []
    for j in range(n):
        if thisCountry == j:
            continue

        otherNations.append(j)
        # prob of j cooperating when i cooperates
        probCC = probabiltiy(thisCountry, j, 0)
        # prob of j defects when i cooperates
        probCD = 1 - probCC

        totalProbDefect *= probCD
        totalProbCooperate *= probCC

    combinations = getExpectedUtilityCombinations(thisCountry, get_combinations(otherNations), 0)
    totalPD = totalProbDefect * defectingUtility(n - 1)
    totalPC = totalProbCooperate * cooperatingUtility(0)

    print(f"Now nation {thisCountry} is considering what all other nations will do when nation {thisCountry} cooperates")
    print(f"If nation {thisCountry} cooperates, the total probability of all other nations cooperating is {totalProbCooperate * 100}%")
    print(f"If nation {thisCountry} cooperates, the total probability of all other nations defecting is {totalProbDefect * 100}%")

    res = totalPD + totalPC + combinations
    return res

def getExpectedUtilityCooperatingMech(thisCountry, n, choice=True):
    '''
    :param thisCountry: represents the nation that is making the choice to either defect or cooperate
    :param n: number of players / nations
    :param choice: if thisCountry is cooperating or defecting. Always set to True ( 1 ).
    :return: total utility assuming that thisCountry is cooperating

    TODO
        Fix varaible names so it makes more sense. Verify everything works as should... no logical errors
    '''

    # total probability of all nations defecting
    totalProbDefect = 1
    # total probability of all nations cooperating
    totalProbCooperate = 1
    otherNations = []
    for j in range(n):
        if thisCountry == j:
            continue

        otherNations.append(j)
        # prob of j cooperating when i cooperates
        probCC = probabiltiy(thisCountry, j, 0)
        # prob of j defects when i cooperates
        probCD = 1 - probCC

        totalProbDefect *= probCD
        totalProbCooperate *= probCC

    combinations = getExpectedUtilityCombinationsMech(thisCountry, get_combinations(otherNations), 0)
    totalPD = totalProbDefect * defectingUtility(n - 1)
    totalPC = totalProbCooperate * cooperatingUtilityMech(0)

    print(f"Now nation {thisCountry} is considering what all other nations will do when nation {thisCountry} cooperates")
    print(f"If nation {thisCountry} cooperates, the total probability of all other nations cooperating is {totalProbCooperate * 100}%")
    print(f"If nation {thisCountry} cooperates, the total probability of all other nations defecting is {totalProbDefect * 100}%")

    res = totalPD + totalPC + combinations
    return res

def getExpectedUtilityDefecting(thisCountry, n, choice=False):
    '''
    :param thisCountry: represents the nation that is making the choice to either defect or cooperate
    :param n: number of players / nations
    :param choice: if thisCountry is cooperating or defecting. Always set to False ( 0 ).
    :return: total utility assuming that thisCountry is defecting

    TODO
        Fix varaible names so it makes more sense. Verify everything works as should... no logical errors
    '''

    # total probability of all nations defecting
    totalProbDefect = 1
    # total probability of all nations cooperating
    totalProbCooperate = 1
    otherNations = []
    for j in range(n):
        if thisCountry == j:
            continue

        otherNations.append(j)
        # prob of j cooperating when i defect
        probDC = probabiltiy(thisCountry, j, 1)
        # prob of j defecting when i defect
        probDD = 1 - probDC

        totalProbDefect *= probDD
        totalProbCooperate *= probDC

    combinationsUtility = getExpectedUtilityCombinations(thisCountry, get_combinations(otherNations), 1)
    totalPDUtility = totalProbDefect * defectingUtility(n - 1)
    totalPCUtility = totalProbCooperate * cooperatingUtility(0)

    print(f"Now nation {thisCountry} is considering what all other nations will do when nation {thisCountry} defects")
    print(
        f"If nation {thisCountry} defects, the total probability of all other nations cooperating is {totalProbCooperate * 100}%")
    print(
        f"If nation {thisCountry} defects, the total probability of all other nations defecting is {totalProbDefect * 100}%")

    res = (totalPDUtility + totalPCUtility + combinationsUtility)
    return res

if __name__ == "__main__":

    # basic set up
    n = int(input("How Many Players Do You Want? "))
    rounds = int(input("How many rounds?"))
    players = [i for i in range(n)]
    relationships = getRelationships(n, -0.5, 0.2)
    reputations = getReputations(n, 0, 0.3)
    numCooperated = 0

    print("")
    print("")


    for k in range(rounds):
        for i in range(n):
            print(f"Nation {i}'s turn...")
            expCop = getExpectedUtilityCooperating(i, n)
            expDef = getExpectedUtilityDefecting(i, n)
            print(f"Nation {i}'s expected utility for cooperating is {expCop} ")
            print(f"Nation {i}'s expected utility for defecting is {expDef} ")
            if expCop > expDef:
                print(f'{i} choose to cooperate')
                numCooperated += 1
            else:
                print(f'{i} chooses to defect')
            print("")
            print("")

    print("Each nation has a reputation from 0-1.  0 means that nation is very likely to defect and 1 means that nation is very likley to cooperate.")
    print("For this first simulation, every nation had a bad reputation (each nation's reputation ranged from 0 -> 0.3). Meaning that they were all likley to defect")
    print("Lets change the reputation of each nation to range from 0.7 -> 1")
    print("This will be our first mechanism.Reputations for each nation can be improved via a global peace treaty to stop building arms")


    reputations = getReputations(n, 0.7, 1)
    numCooperated = 0
    print("")

    for i in range(n):
        print(f"Nation {i}'s turn...")
        expCop = getExpectedUtilityCooperating(i, n)
        expDef = getExpectedUtilityDefecting(i, n)
        print(f"Nation {i}'s expected utility for cooperating is {expCop} ")
        print(f"Nation {i}'s expected utility for defecting is {expDef} ")
        if expCop > expDef:
            numCooperated += 1
            print(f'{i} choose to cooperate')
        else:
            print(f'{i} chooses to defect')
        print("")
        print("")

    print("As we can see, if all other nations have higher reputations, everyone else will cooperate")

    print("")
    print("")

    print("Now we will set the reputation back to range to 0 -> 0.3")
    print("Relationships between each nation can also help other nations to cooperate. Currently, they range from -0.5 to 0... -1 being a purley negative relationship and 1 being a purley positive relationship")
    print("We set them to range between -0.5 and 0.2 to represent that some nations have somewhat positive relations while others have somewhat negative ones")
    print("So if we change the relationships from -0.5 -> 0.2 to 0 -> 1, we should see more nations cooperating as well")

    print("")
    print("")

    reputations = getReputations(n, 0, 0.3)
    relationships = getRelationships(n, 0, 1)

    for i in range(n):
        print(f"Nation {i}'s turn...")
        expCop = getExpectedUtilityCooperating(i, n)
        expDef = getExpectedUtilityDefecting(i, n)
        print(f"Nation {i}'s expected utility for cooperating is {expCop} ")
        print(f"Nation {i}'s expected utility for defecting is {expDef} ")
        if expCop > expDef:
            numCooperated += 1
            print(f'{i} choose to cooperate')
        else:
            print(f'{i} chooses to defect')
        print("")
        print("")

    print("As we can see, if all other nations have better relationships, everyone else will cooperate")

    print("")
    print("")

    print("Now we will add a global support mechanism")
    print("This is when some global force or organization comes and helps each nation to cooperate")
    print("This is done by giving each nation some extra cooperating utility. With this mechansim, we are giving an extra 50 util points if a nation cooperates")
    print("Util points can correlate to things like money, social praise, increased trading rights, etc.")
    print("With this mechanism, we should see countries more likely to cooperate.")
    print("")
    print("")

    reputations = getReputations(n, 0, 0.3)
    relationships = getRelationships(n, -0.5, 0.2)



    for i in range(n):
        print(f"Nation {i}'s turn...")
        expCop = getExpectedUtilityCooperatingMech(i, n)
        expDef = getExpectedUtilityDefecting(i, n)
        print(f"Nation {i}'s expected utility for cooperating is {expCop} ")
        print(f"Nation {i}'s expected utility for defecting is {expDef} ")
        if expCop > expDef:
            numCooperated += 1
            print(f'{i} choose to cooperate')
        else:
            print(f'{i} chooses to defect')
        print("")
        print("")

    print("As we can see, the global support mechanism increases cooperating")



















