import random
# constant
A = 10 # Base utility for building arms
B = 8 # Base utility for not building arms (favors cooperation)
X = 2 # Cost scaling factor for building arms (^ for discourage defecting)
Y = 3 # Cost scaling factor for not building arms (^ to increase penalty)
T = 0.2

def defect(n_b):
    return A - (X * n_b)

def cooperate(n_b):
    return B - (Y * n_b)

def greedyApproach(players):
        n_build = 0
        storePayoffs = []
        messages = []

        for i in range(players):
            c = cooperate(n_build)
            d = defect(n_build)

            if d > c:
                n_build += 1
                messages.append(f"Player {i + 1} defected. Util: {d}")
                storePayoffs.append(d)
            else:
                n_build += 1
                messages.append(f"Player {i + 1} defected. Util: {c}")
                storePayoffs.append(c)

        for message in messages:
            print(message)

        print(f"The total utils for all the players: {sum(storePayoffs)}\n")
        print("Each nation will always choose to defect when taking a greedy approach. \n"
              "This is because in the short run, every nation's best bet is to defect as "
              "it gives them the highest util.")
        return sum(storePayoffs)
def randomApproach(players):
    messages = []
    storePayoffs = []
    n_build = 0

    for i in range(players):
        random_number = random.choice([0, 1])
        c = cooperate(n_build)
        d = defect(n_build)
        if random_number == 0:
            n_build +=1
            messages.append(f"Player {i + 1} defected. Util: {d}")
            storePayoffs.append(d)
        else:
            messages.append(f"Player {i + 1} cooperated. Util: {c}")
            storePayoffs.append(c)

    for message in messages:
        print(message)

    print("The total utils for all the players: ", sum(storePayoffs))
    print(" ")
    return sum(storePayoffs)

def runSimulation():
    print("Simulation of the Security Dilemma")
    print("----------------------------------\n")

    print("In this first simulation, each player will pick the best option for themselves. This is a greedy approach.")
    players = int(input("Enter a number of players: "))
    print("")
    greed = greedyApproach(players)

    print("\nIn this next simulation, each player will randomly choose to defect or cooperate.")
    rand = randomApproach(players)

    if greed > rand:
        print("In this case, the greedy approach resulted in a higher total util for all the nations. \n"
              "However, this is not always the case! Please run the simulation again!")
    elif greed < rand:
        print("As we can see, when more players decide to cooperate, we get a higher total util!")
        print("Each nation's best bet is to defect. But if they cooperated, it would result in more total util!")
    else:
        print("In this case, the random strategy has allowed for just the right number of cooperators,\n"
              "offsetting the defectors domination!")

if __name__ == "__main__":
    runSimulation()














