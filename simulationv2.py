import random
import math
import itertools

def getRelationships(n, upper, lower):
    '''
    :param n: the number of players/nations
    :param upper: an upper bound for relationships (between -1 and 1)
    :param lower: a lower bound for relationships (between -1 and 1)
    :return: map of relationships

    The key in the map we return will be a nation, and the value will be an array
    Each index of the array will represent the relationship with that key

    So if there are 5 players. And we do relationships[3], this will give us an array for nation 3, call it relations. Then
    if we do relations[4] this gives us nation 3's relationship with nation 4.

    Note that if we do relations[3] for nation 3, this will be a zero, because nation 3's relationship with itself is neutral.
    And note that relationships[3][4] == relationships[4][3] because nation 3's relationship with nation 4 is assumed to be the same as nation
    4's relationship with nation 3.
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
    This utility function has an additional mechanism to encourage cooperation. It provides 50 extra util points!
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
    w1 = 5 # for reputations
    w2 = 3 # for relationships
    w3 = 1 # for choice

    x = (reputations[b] * w1) + (relationships[a][b] * w2) + (-choice * w3)

    return 1 / (1 + math.exp(-x))

def get_combinations(arr):
    '''
    :param arr: An array of all (n-1) nations. EX: If there are 5 nations, and we want all combinations
    for nation 3, arr = [0,1,2,4]. It will not include the nation that uses this helper function. This is because
    in our predicted utility functions, we iterate over all nations except itself (S != A in the readMe)
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
    :param combinations: a 2D array of nations. We assume that each nation in the subarrays will defect. Any nation
    not in this subarray will cooperate
    :param choice: if currNation is cooperating or defecting
    :return: total utility for all possible combinations

    This function sums the utility over all subsets of players excluding the current nation based on the probability of each player
    cooperating and defecting

    '''
    totalUtility = 0

    # for each array in combinations
    for combo in combinations:
        percentOfCooperate = 1
        percentOfDefect = 1

        for otherNation in combo:
            # all players in combo assumed to defect
            percentOfDefect *= (1 - probabiltiy(currNation, otherNation, choice))

        for otherNation in players:
            if otherNation not in combo:
                # all players NOT in combo assumed to cooperate
                percentOfCooperate *= probabiltiy(currNation, otherNation, choice)
        # get total utility
        totalUtility += (percentOfCooperate * cooperatingUtility(n - len(combo))) + (
                    percentOfDefect * defectingUtility(len(combo)))
    # round to two decimal points
    return round(totalUtility, 2)

def getExpectedUtilityCombinationsMech(currNation, combinations, choice):
    '''
    :param currNation: represents the nation that is making the choice to either defect or cooperate
    :param combinations:  a 2D array of nations. We assume that each nation in the subarrays will defect. Any nation
    not in this subarray will cooperate
    :param choice: if currNation is cooperating or defecting
    :return: total utility for all possible combinations

    This represents the complex summation part of the equation in readMe

    This function sums the utility over all subsets of players excluding the current nation based on the probability of each player
    cooperating and defecting

    Same as getExpectedUtilityCombinations, except this uses the global support mechanism (uses cooperatingUtilityMech function instead
    of the cooperatingUtility function)
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
        # skip thisCountry
        if thisCountry == j:
            continue

        otherNations.append(j)
        # prob of j cooperating when i cooperates
        probCC = probabiltiy(thisCountry, j, 0)
        # prob of j defects when i cooperates
        probCD = 1 - probCC

        totalProbDefect *= probCD
        totalProbCooperate *= probCC

    # Gets total utility for all combinations
    combinations = getExpectedUtilityCombinations(thisCountry, get_combinations(otherNations), 0)
    # Gets total utility when everyone defects
    totalPDUtility = totalProbDefect * defectingUtility(n - 1)
    # Gets total utility when everyone cooperates
    totalPCUtility = totalProbCooperate * cooperatingUtility(0)

    print(f"Now nation {thisCountry + 1} is considering what all other nations will do when nation {thisCountry + 1} cooperates")
    print(f"If nation {thisCountry + 1} cooperates, the total probability of all other nations cooperating is {round(totalProbCooperate * 100, 2)}%, and")
    print(f"the total probability of all other nations defecting is {round(totalProbDefect * 100, 2)}%")

    res = totalPDUtility + totalPCUtility + combinations
    return round(res, 2)

def getExpectedUtilityCooperatingMech(thisCountry, n, choice=True):
    '''
    :param thisCountry: represents the nation that is making the choice to either defect or cooperate
    :param n: number of players / nations
    :param choice: if thisCountry is cooperating or defecting. Always set to True ( 1 ).
    :return: total utility assuming that thisCountry is cooperating

    Same as above but with global support mechanism!
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

    # Gets total utility for all combinations
    combinations = getExpectedUtilityCombinationsMech(thisCountry, get_combinations(otherNations), 0)
    # Gets total utility when everyone defects
    totalPD = totalProbDefect * defectingUtility(n - 1)
    # Gets total utility when everyone cooperates
    totalPC = totalProbCooperate * cooperatingUtilityMech(0)

    print(f"Now nation {thisCountry + 1} is considering what all other nations will do when nation {thisCountry + 1} cooperates")
    print(f"If nation {thisCountry + 1} cooperates, the total probability of all other nations cooperating is {round(totalProbCooperate * 100, 2)}%")
    print(f"If nation {thisCountry + 1} cooperates, the total probability of all other nations defecting is {round(totalProbDefect * 100, 2)}%")

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

    # Gets total utility for all combinations
    combinationsUtility = getExpectedUtilityCombinations(thisCountry, get_combinations(otherNations), 1)
    # Gets total utility when everyone defects
    totalPDUtility = totalProbDefect * defectingUtility(n - 1)
    # Gets total utility when everyone cooperates
    totalPCUtility = totalProbCooperate * cooperatingUtility(0)

    print(f"Now nation {thisCountry + 1} is considering what all other nations will do when nation {thisCountry + 1} defects")
    print(
        f"If nation {thisCountry + 1} defects, the total probability of all other nations cooperating is {round(totalProbCooperate * 100, 2)}%, and")
    print(
        f"the total probability of all other nations defecting is {round(totalProbDefect * 100, 2)}%")

    res = totalPDUtility + totalPCUtility + combinationsUtility
    return round(res, 2)

if __name__ == "__main__":

    # basic set up
    n = int(input("How Many Players Do You Want? "))
    players = [i for i in range(n)]
    relationships = getRelationships(n, -0.5, 0.2)
    reputations = getReputations(n, 0, 0.3)

    print("")
    print("")

    print("Part 1:")
    print("Each nation can have a reputation from 0 -> 1. 0 means that a nation is very likely to defect and 1 means that a nation is very likely to cooperate.")
    print("Also, each nation can have a relationship from -1 -> 1 with every other nation. -1 represents a purely negative relationship. 1 represent a purely possitive one.")
    print("For this first simulation, every nation has a \"bad\" reputation (each nation's reputation ranges from 0 -> 0.3), meaning that they are all likely to defect")
    print("Also, each nation has mixed relationships with every other nation (currently ranging between -0.2 -> 0.5), meaning some nations have somewhat positive relations while others")
    print("have somewhat negative ones.")
    print("The results of these factors can be seen below.")
    print("")

    for i in range(n):
        print(f"Nation {i+1}'s turn...")
        expCop = getExpectedUtilityCooperating(i, n)
        expDef = getExpectedUtilityDefecting(i, n)
        print(f"Nation {i+1}'s expected utility for cooperating is {expCop} ")
        print(f"Nation {i+1}'s expected utility for defecting is {expDef} ")
        if expCop > expDef:
            print(f'{i} chooses to cooperate')
        else:
            print(f'{i+1} chooses to defect')
        print("")
        print("")


    print("Part 2:")
    print("Lets change the reputation of each nation to range from 0.7 -> 1")
    print("This will be our first mechanism. A nation has incentive to have a higher reputation because they know ")
    print("other nations also consider their reputation when determining if they will cooperate or defect.")
    print("Ways to increase reputations: ")
    print("Choosing to commit to reducing the spread of nuclear arsenals through peace treaties")
    print("Engaging in peace talks and diplomacy with other countries")
    print("Providing transparency to other nations about their current arsenal to avoid misunderstandings")


    # change reputation as part of our first mechanism
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
            print(f'{i+1} chooses to cooperate')
        else:
            print(f'{i+1} chooses to defect')
        print("")
        print("")

    print("As we can see, if all other nations have higher reputations, everyone else will cooperate")

    print("")
    print("")

    print("Part 3:")
    print("Now we will set the reputation back to range from 0 -> 0.3")
    print("Relationships between each nation can also help other nations to cooperate.")
    print("If we change the relationships from -0.5 -> 0.2 to 0 -> 1, we should see more nations cooperating.")
    print("Ways to increase relationships: ")
    print("1. Engage in trade agreements or economic partnerships.")
    print("2. Participate in joint military exercises or alliances.")
    print("3. Offer humanitarian aid during crises or disasters.")


    print("")
    print("")

    # set reputation back to normal
    reputations = getReputations(n, 0, 0.3)
    # change relationship as part of our second mechanism
    relationships = getRelationships(n, 0, 1)

    for i in range(n):
        print(f"Nation {i+1}'s turn...")
        expCop = getExpectedUtilityCooperating(i, n)
        expDef = getExpectedUtilityDefecting(i, n)
        print(f"Nation {i+1}'s expected utility for cooperating is {expCop} ")
        print(f"Nation {i+1}'s expected utility for defecting is {expDef} ")
        if expCop > expDef:
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
    print("With this mechanism, we should see countries are more likely to cooperate.")
    print("")
    print("")

    # Set relationships back to normal
    relationships = getRelationships(n, -0.5, 0.2)

    for i in range(n):
        print(f"Nation {i+1}'s turn...")
        expCop = getExpectedUtilityCooperatingMech(i, n)
        expDef = getExpectedUtilityDefecting(i, n)
        print(f"Nation {i+1}'s expected utility for cooperating is {expCop} ")
        print(f"Nation {i+1}'s expected utility for defecting is {expDef} ")
        if expCop > expDef:
            print(f'{i+1} chooses to cooperate')
        else:
            print(f'{i+1} chooses to defect')
        print("")
        print("")

    print("As we can see, the global support mechanism increases cooperation")
