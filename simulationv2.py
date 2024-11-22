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
    popularity points as they were not the first nations to cooperate. We chose 200 to give nations enough incentive to change
    their decision when the mechanism is implemented

    '''
    return 200 / (numCooperated + 1)

def cooperatingUtility(numPlayersDefecting, cooperatingUtility=15, cooperatingScalar=2):
    '''

    :param numPlayersDefecting: number of players defecting
    :param cooperatingUtility: A constant that represents the base utility for cooperating
    :param cooperatingScalar: A constant that represents the base cost for cooperating
    :return: utility that represent cooperating

    This models our cooperating utility function found in the readMe.

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
    '''
    return cooperatingUtility - (cooperatingScalar * math.log(1 + numPlayersDefecting)) + 50

def defectingUtility(numPlayersDefecting, defectingUtility=30, defectingScalar=3):
    '''

    :param numPlayersDefecting: number of players defecting
    :param defectingUtility: A constant that represents the base utility for defecting
    :param defectingScalar: A constant that represents the base cost for defecting
    :return: utility that represent defecting

    This models our defecting utility function found in the readMe.
    '''
    return defectingUtility - (defectingScalar * math.log(1 + numPlayersDefecting))

def probabiltiy(a, b, choice):
    '''

    :param a: nation that is making the choice to either defect or cooperate
    :param b: this is the "other" nation that nation a is considering
    :param choice: if a is cooperating or defecting
    :return: the probability that nation b will cooperate

    this represents our probability function found on the readMe

    weights were chosen to represent the amount of importance each value has in calculating
    the probability

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
    return [list(combo) for combo in result]

def getExpectedUtilityCombinations(currNation, combinations, choice):
    '''
    :param currNation: represents the nation that is making the choice to either defect or cooperate
    :param combinations: an array of nations. We assume that each nation in this array will defect. Any nation
    not in this array will cooperate
    :param choice: if currNation is cooperating or defecting
    :return: total utility for all possible combinations

    This function sums the utility over all subsets of players excluding the current nation based on the probability of each player
    cooperating and defecting

    '''
    # for defecting
    totalUtility = 0

    for combo in combinations:
        percentOfCooperate = 1
        percentOfDefect = 1

        for otherNation in combo:
            percentOfDefect *= (1 - probabiltiy(currNation, otherNation, choice))

        for otherNation in players:
            if otherNation not in combo:
                percentOfCooperate *= probabiltiy(currNation, otherNation, choice)
        totalUtility += (percentOfCooperate * cooperatingUtility(n - len(combo))) + (
                    percentOfDefect * defectingUtility(len(combo)))
    return round(totalUtility, 2)

def getExpectedUtilityCombinationsMech(currNation, combinations, choice):
    '''
    :param currNation: represents the nation that is making the choice to either defect or cooperate
    :param combinations: an array of nations. We assume that each nation in this array will defect.Any nation
    not in this array will cooperate
    :param choice: if currNation is cooperating or defecting
    :return: total utility for all possible combinations

    This represents the complex summation part of the equation in readMe

    This function sums the utility over all subsets of players excluding the current nation based on the probability of each player
    cooperating and defecting, and factors in the mechanism to update the utility if the player cooperates
    '''
    # for defecting
    totalUtility = 0

    for combo in combinations:
        percentOfCooperate = 1
        percentOfDefect = 1

        for otherNation in combo:
            percentOfDefect *= (1 - probabiltiy(currNation, otherNation, choice))

        for otherNation in players:
            if otherNation not in combo:
                percentOfCooperate *= probabiltiy(currNation, otherNation, choice)
        totalUtility += (percentOfCooperate * cooperatingUtilityMech(n - len(combo))) + (
                    percentOfDefect * defectingUtility(len(combo)))
    return round(totalUtility, 2)

def getExpectedUtilityCooperating(thisCountry, n, choice=True):
    '''
    :param thisCountry: represents the nation that is making the choice to either defect or cooperate
    :param n: number of players / nations
    :param choice: if thisCountry is cooperating or defecting. Always set to True ( 1 ).
    :return: total utility assuming that thisCountry is cooperating

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
    print(f"If nation {thisCountry} cooperates, the total probability of all other nations cooperating is {round(totalProbCooperate * 100, 2)}%, and")
    print(f"the total probability of all other nations defecting is {round(totalProbDefect * 100, 2)}%")
    # If nation {thisCountry} cooperates,
    res = totalPD + totalPC + combinations
    return round(res, 2)

def getExpectedUtilityCooperatingMech(thisCountry, n, choice=True):
    '''
    :param thisCountry: represents the nation that is making the choice to either defect or cooperate
    :param n: number of players / nations
    :param choice: if thisCountry is cooperating or defecting. Always set to True ( 1 ).
    :return: total utility assuming that thisCountry is cooperating
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
    print(f"If nation {thisCountry} cooperates, the total probability of all other nations cooperating is {round(totalProbCooperate * 100, 2)}%")
    print(f"If nation {thisCountry} cooperates, the total probability of all other nations defecting is {round(totalProbDefect * 100, 2)}%")

    res = totalPD + totalPC + combinations
    return round(res, 2)

def getExpectedUtilityDefecting(thisCountry, n, choice=False):
    '''
    :param thisCountry: represents the nation that is making the choice to either defect or cooperate
    :param n: number of players / nations
    :param choice: if thisCountry is cooperating or defecting. Always set to False ( 0 ).
    :return: total utility assuming that thisCountry is defecting

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
        f"If nation {thisCountry} defects, the total probability of all other nations cooperating is {round(totalProbCooperate * 100, 2)}%, and")
    print(
        f"the total probability of all other nations defecting is {round(totalProbDefect * 100, 2)}%")

    res = (totalPDUtility + totalPCUtility + combinationsUtility)
    return round(res, 2)

if __name__ == "__main__":

    # basic set up
    n = int(input("How Many Players Do You Want? "))
    rounds = int(input("How many rounds? "))
    players = [i for i in range(n)]
    relationships = getRelationships(n, -0.5, 0.2)
    reputations = getReputations(n, 0, 0.3)
    numCooperated = 0

    print("")
    print("")

    print("Part 1:")
    print("Each nation has a reputation from 0-1. 0 means that nation is very likely to defect and 1 means that nation is very likely to cooperate.")
    print("For this first simulation, every nation has a bad reputation (each nation's reputation ranges from 0 -> 0.3), meaning that they are all likely to defect")
    print("This will be seen below.")
    print("")

    for k in range(rounds):
        print(f"Round {k+1}: ")
        for i in range(n):
            print(f"Nation {i+1}'s turn...")
            expCop = getExpectedUtilityCooperating(i, n)
            expDef = getExpectedUtilityDefecting(i, n)
            print(f"Nation {i+1}'s expected utility for cooperating is {expCop} ")
            print(f"Nation {i+1}'s expected utility for defecting is {expDef} ")
            if expCop > expDef:
                print(f'{i} chooses to cooperate')
                numCooperated += 1
            else:
                print(f'{i+1} chooses to defect')
            print("")
            print("")


    print("Part 2:")
    print("Lets change the reputation of each nation to range from 0.7 -> 1")
    print("This will be our first mechanism. A nation has incentive to have a higher reputation because they know ")
    print("other nations also consider their reputation when determining if they will cooperate or defect.")


    reputations = getReputations(n, 0.7, 1)
    numCooperated = 0
    print("")

    for i in range(n):
        print(f"Nation {i+1}'s turn...")
        expCop = getExpectedUtilityCooperating(i, n)
        expDef = getExpectedUtilityDefecting(i, n)
        print(f"Nation {i+1}'s expected utility for cooperating is {expCop} ")
        print(f"Nation {i+1}'s expected utility for defecting is {expDef} ")
        if expCop > expDef:
            numCooperated += 1
            print(f'{i+1} chooses to cooperate')
        else:
            print(f'{i+1} chooses to defect')
        print("")
        print("")

    print("As we can see, if all other nations have higher reputations, everyone else will cooperate")

    print("")
    print("")

    print("Part 3:")
    print("Now we will set the reputation back to range to 0 -> 0.3")

    # Not sure what u mean :p
    print("Relationships between each nation can also help other nations to cooperate. We can improve them through something ")
    print("like a global peace treaty to stop building arms. Currently, they range from -1 to 1 with -1 being a purely negative")
    print("relationship and 1 being a purely positive relationship.")
    print("We set them to range between -0.5 and 0.2 to represent that some nations have somewhat positive relations while others")
    print("have somewhat negative ones")
    print("If we change the relationships from -0.5 -> 0.2 to 0 -> 1, we should see more nations cooperating as well.")

    print("")
    print("")

    reputations = getReputations(n, 0, 0.3)
    relationships = getRelationships(n, 0, 1)

    for i in range(n):
        print(f"Nation {i+1}'s turn...")
        expCop = getExpectedUtilityCooperating(i, n)
        expDef = getExpectedUtilityDefecting(i, n)
        print(f"Nation {i+1}'s expected utility for cooperating is {expCop} ")
        print(f"Nation {i+1}'s expected utility for defecting is {expDef} ")
        if expCop > expDef:
            numCooperated += 1
            print(f'{i+1} chooses to cooperate')
        else:
            print(f'{i+1} chooses to defect')
        print("")
        print("")

    print("As we can see, if all other nations have better relationships, everyone else will cooperate")

    print("")
    print("")

    print("Part 4:")
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
        print(f"Nation {i+1}'s turn...")
        expCop = getExpectedUtilityCooperatingMech(i, n)
        expDef = getExpectedUtilityDefecting(i, n)
        print(f"Nation {i+1}'s expected utility for cooperating is {expCop} ")
        print(f"Nation {i+1}'s expected utility for defecting is {expDef} ")
        if expCop > expDef:
            numCooperated += 1
            print(f'{i+1} chooses to cooperate')
        else:
            print(f'{i+1} chooses to defect')
        print("")
        print("")

    print("As we can see, the global support mechanism increases cooperation")



















