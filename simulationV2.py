import random
import math
import itertools

def get_relationships(n):
    relationships = {i: [0] * n for i in range(n)}
    for i in range(n):
        for j in range(n):
            if j != i and relationships[i][j] == 0:
                relationships[i][j] = random.uniform(-1, 1)
                relationships[j][i] = relationships[i][j]  # Ensure symmetry
    return relationships

def get_reputations(n, lower, upper):
    return {i: random.uniform(lower, upper) for i in range(n)}

def cooperating_utility(num_players_defecting, cooperating_utility=15, cooperating_scalar=3):
    return cooperating_utility - (cooperating_scalar * math.log(1 + num_players_defecting))

def defecting_utility(num_players_defecting, defecting_utility=30, defecting_scalar=2):
    return defecting_utility - (defecting_scalar * math.log(1 + num_players_defecting))

def probability(a, b, choice, reputations, relationships):
    w1, w2, w3 = 5, 1, 1
    x = (reputations[b] * w1) + (relationships[a][b] * w2) + (-choice * w3) - 1.1
    return 1 / (1 + math.exp(-x))

def get_combinations(arr):
    return [list(comb) for r in range(1, len(arr) + 1) for comb in itertools.combinations(arr, r)]

def get_expected_utility(this_nation, action, n, relationships, reputations, players):
    total_utility = 0
    total_prob_defect = 1
    total_prob_cooperate = 1
    temp = [j for j in range(n) if j != this_nation]

    for other_nation in temp:
        prob_c = probability(this_nation, other_nation, 0 if action == 'cooperate' else 1, reputations, relationships)
        prob_d = 1 - prob_c
        total_prob_cooperate *= prob_c
        total_prob_defect *= prob_d

    # Consider all possible combinations of players cooperating/defecting
    combinations = get_combinations(temp)
    total_utility += sum(prob * cooperating_utility(len(comb)) if action == 'cooperate' else defecting_utility(len(comb))
                         for comb in combinations for prob in [total_prob_cooperate if action == 'cooperate' else total_prob_defect])

    # Additional utilities based on the action
    if action == 'cooperate':
        total_utility += total_prob_cooperate * cooperating_utility(0)
        total_utility += total_prob_defect * defecting_utility(n-1)
    else:
        total_utility += total_prob_cooperate * cooperating_utility(0)
        total_utility += total_prob_defect * defecting_utility(n-1)

    return total_utility

def decision(n, players, relationships, reputations):
    for i in range(n):
        print(f"Nation {i}'s turn...")

        exp_coop = get_expected_utility(i, 'cooperate', n, relationships, reputations, players)
        exp_def = get_expected_utility(i, 'defect', n, relationships, reputations, players)

        print(f"Nation {i}'s expected utility for cooperating is {exp_coop}")
        print(f"Nation {i}'s expected utility for defecting is {exp_def}")

        if exp_coop > exp_def:
            print(f'{i} chooses to cooperate')
        else:
            print(f'{i} chooses to defect')
        print("\n")

def main():
    n = int(input("How Many Players Do You Want? "))
    players = list(range(n))
    relationships = get_relationships(n)
    reputations = get_reputations(n, 0, 0.3)

    decision(n, players, relationships, reputations)

    print("Now let's change the reputation of each nation to range from 0.7 -> 1")
    reputations = get_reputations(n, 0.7, 1)

    decision(n, players, relationships, reputations)

if __name__ == "__main__":
    main()
