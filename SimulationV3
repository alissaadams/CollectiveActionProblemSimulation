import random
import math
import itertools
import matplotlib.pyplot as plt

# Function to generate random relationships
def get_relationships(n):
    relationships = {i: [0] * n for i in range(n)}
    for i in range(n):
        for j in range(n):
            if j != i and relationships[i][j] == 0:
                relationships[i][j] = random.uniform(-1, 1)
                relationships[j][i] = relationships[i][j]  # Ensure symmetry
    return relationships

# Function to generate random reputations
def get_reputations(n, lower, upper):
    return {i: random.uniform(lower, upper) for i in range(n)}

# Utility functions for cooperating and defecting
def cooperating_utility(num_players_defecting, cooperating_utility=15, cooperating_scalar=3):
    return cooperating_utility - (cooperating_scalar * math.log(1 + num_players_defecting))

def defecting_utility(num_players_defecting, defecting_utility=30, defecting_scalar=2):
    return defecting_utility - (defecting_scalar * math.log(1 + num_players_defecting))

# Probability calculation function
def probability(a, b, choice, reputations, relationships):
    w1, w2, w3 = 5, 1, 1
    x = (reputations[b] * w1) + (relationships[a][b] * w2) + (-choice * w3) - 1.1
    return 1 / (1 + math.exp(-x))

# Function to get all combinations of players
def get_combinations(arr):
    return [list(comb) for r in range(1, len(arr) + 1) for comb in itertools.combinations(arr, r)]

# Function to calculate expected utility based on the player's action
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

# Function to update reputation based on actions
def update_reputation(reputations, action_taken, other_nation, learning_rate=0.05):
    if action_taken == 'cooperate':
        reputations[other_nation] = min(1, reputations[other_nation] + learning_rate)
    elif action_taken == 'defect':
        reputations[other_nation] = max(0, reputations[other_nation] - learning_rate)
    return reputations

# Function to simulate the decision-making process for multiple rounds
def run_multiple_rounds(n, players, relationships, reputations, num_rounds=10):
    cooperation_history = []
    for round_num in range(num_rounds):
        print(f"\nRound {round_num + 1}")
        cooperation_count = 0

        for i in range(n):
            exp_coop = get_expected_utility(i, 'cooperate', n, relationships, reputations, players)
            exp_def = get_expected_utility(i, 'defect', n, relationships, reputations, players)

            print(f"Nation {i}'s expected utility for cooperating is {exp_coop}")
            print(f"Nation {i}'s expected utility for defecting is {exp_def}")

            if exp_coop > exp_def:
                action = 'cooperate'
                print(f'{i} chooses to cooperate')
                cooperation_count += 1
            else:
                action = 'defect'
                print(f'{i} chooses to defect')

            # Update reputation based on the action chosen
            for other_nation in players:
                if other_nation != i:
                    reputations = update_reputation(reputations, action, other_nation)

        # Record cooperation percentage for this round
        cooperation_percentage = cooperation_count / n * 100
        cooperation_history.append(cooperation_percentage)

        print("\nEnd of round", round_num + 1)
        print("Updated Reputations:", reputations)
        print("===================================")

    return reputations, cooperation_history

# Function to plot cooperation history over rounds
def plot_cooperation_history(cooperation_history):
    plt.plot(cooperation_history)
    plt.xlabel('Round')
    plt.ylabel('Percentage of Cooperation')
    plt.title('Cooperation Over Time')
    plt.show()

# Main function to initiate the simulation
def main():
    n = int(input("How Many Players Do You Want? "))
    players = list(range(n))
    relationships = get_relationships(n)
    reputations = get_reputations(n, 0, 0.3)

    print("Initial Reputation Range: 0 to 0.3 (Players more likely to defect)")

    # Run the simulation for multiple rounds
    num_rounds = int(input("How many rounds do you want to simulate? "))
    reputations, cooperation_history = run_multiple_rounds(n, players, relationships, reputations, num_rounds)

    # Visualize the cooperation over time
    plot_cooperation_history(cooperation_history)

    print("Now let's change the reputation of each nation to range from 0.7 -> 1")
    reputations = get_reputations(n, 0.7, 1)

    print("Reputation Range: 0.7 to 1 (Players more likely to cooperate)")

    # Run the simulation again with updated reputations
    reputations, cooperation_history = run_multiple_rounds(n, players, relationships, reputations, num_rounds)

    # Visualize the cooperation over time again
    plot_cooperation_history(cooperation_history)

if __name__ == "__main__":
    main()
