import random

if __name__ == "__main__":
    A = 10
    B = 8
    X = 2
    Y = 3
    T = 0.2
    n_b = 0
    n_nb = 0

    def defect(n_b):
        return A - (X * n_b)

    def cooperate(n_b):
        return B - (Y * n_b)

    print(" ")
    print("In this first simulation, each player will pick the best option for themselves. This is a greedy approach.")
    print(" ")
    n = int(input("Enter a number of players: "))
    messages = []
    res = []

    print("")
    for i in range(n):
        c = cooperate(n_b)
        d = defect(n_b)
        if d > c:
            n_b +=1
            messages.append(f"Player {i+1} defected, this is their util, {d}")
            res.append(d)
        else:
            n_nb += 1
            messages.append(f"Player {i+1} cooperated, this is their util, {c}")
            res.append(c)

    for message in messages:
        print(message)
        print("")

    print("The total utils for all the players: ", sum(res))
    print("")
    print("Each nation will always choose to defect when taking a greedy approach. This is because in the short run, every nation's best bet is to defect as it gives them the highest util.")
    print("")
    print("__________")
    print("")

    n_b = 0
    n_nb = 0
    print("In this next simulation, each player will randomly choose to defect or cooperate")
    print(" ")
    n = int(input("Enter a number of players: "))
    messages = []
    res1 = []

    print("")
    for i in range(n):
        random_number = random.choice([0, 1])
        c = cooperate(n_b)
        d = defect(n_b)
        if random_number == 0:
            n_b +=1
            messages.append(f"Player {i + 1} defected, this is their util, {d}")
            res1.append(d)
        else:
            messages.append(f"Player {i + 1} cooperated, this is their util, {c}")
            res1.append(c)

    for message in messages:
        print(message)
        print("")

    print("The total utils for all the players: ", sum(res1))
    print(" ")

    if sum(res) > sum(res1):
        print("In this case, the greedy approach resulted in a higher total util for all the nations. However, this is not always the case! Please run the simulation again!")

    else:
        print("As we can see, when some players decide to cooperate, we get a higher total util!")
        print("Each nation's best bet is to defect. But if they cooperated, it would result in more total util!")














