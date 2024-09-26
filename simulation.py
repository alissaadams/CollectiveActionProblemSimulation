import random

# Constants
n_countries = 7  # Total number of countries (US, Russia, China, North Korea, India, Pakistan, France)
A = 10  # Base utility for building arms
B = 8   # Base utility for not building arms
X = 2   # Cost scaling factor for building arms
Y = 3   # Cost scaling factor for not building arms

# Countries and strategies
countries = ['US', 'Russia', 'China', 'North Korea', 'India', 'Pakistan', 'France']
strategies = ['cooperate', 'defect']

# Let the user input the initial strategy for each country
def choose_initial_strategies():
    country_strategies = {}
    print("Choose strategies for each country: cooperate (reduce arms) or defect (build arms).")
    for country in countries:
        while True:
            strategy = input(f"{country}'s strategy (cooperate/defect): ").strip().lower()
            if strategy in strategies:
                country_strategies[country] = strategy
                break
            else:
                print("Invalid input, please enter 'cooperate' or 'defect'.")
    return country_strategies

# Calculate payoffs based on the current strategies
def calculate_payoffs(country_strategies):
    n_b = sum([1 for strategy in country_strategies.values() if strategy == 'defect'])
    n_nb = n_countries - n_b

    payoffs = {}
    for country, strategy in country_strategies.items():
        if strategy == 'defect':
            Ub = A - X * n_b
            payoffs[country] = Ub
        else:
            Unb = B - Y * n_b
            payoffs[country] = Unb
    return payoffs

# Best response logic (adjust strategy based on payoff)
def best_response(current_strategy, payoff_cooperate, payoff_defect):
    if payoff_cooperate > payoff_defect:
        return 'cooperate'
    else:
        return 'defect'

# Simulate a round with the ability for user to see results
def simulate_rounds(rounds, country_strategies):
    for round in range(rounds):
        print(f"\nRound {round + 1}:")
        payoffs = calculate_payoffs(country_strategies)
        print(f"Payoffs: {payoffs}")

        # Adjust strategies based on payoffs
        new_strategies = {}
        for country, current_strategy in country_strategies.items():
            payoff_cooperate = B - Y * (n_countries - 1)  # Payoff if cooperating
            payoff_defect = A - X * (n_countries - 1)     # Payoff if defecting
            new_strategy = best_response(current_strategy, payoff_cooperate, payoff_defect)
            new_strategies[country] = new_strategy

        country_strategies = new_strategies
        print(f"New strategies: {country_strategies}")

# Main simulation flow
def main():
    # Get the initial strategies from the user
    country_strategies = choose_initial_strategies()

    # Run the simulation for a given number of rounds
    rounds = int(input("How many rounds would you like to simulate? "))
    simulate_rounds(rounds, country_strategies)

if __name__ == "__main__":
    main()
