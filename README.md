# CollectiveActionProblemSImulation
# Nuclear Arms - A Security Dilemma 

**Note: We have two versions of the simulation, our original and our newest version. This readME describes the updated version(V2), and our original is there for our reference.*

## Scenario
There are N countries who have the ability to build nuclear arms. Each country has incentive to build arms for protection based on the perceived threat of other countries also building/owning nuclear arms. However, it's in all countries' best interest to participate in disarmament to reduce the risk of nuclear conflict. Collectively they benefit, but individual incentive promotes defection. This project simulates the Security Dilemma in game theory, where multiple players(countries) choose between two strategies: to defect(build arms) or cooperate(disarmament).
This simulation explores how individual decisions affect utility and outcomes for other players. 



## Game Definitions & Concepts
* N player game
* Two Strategies:
  * Build Arms
  * Disarmament

### Variables 
    * Let n_b = number of countries that build arms
    * Let n_nb = number of countries that do NOT build arms
    * Ub = utility for building arms 
    * Unb = utility for not building arms

### **Utility for Building Arms:**

$$
U^D = A - C(n_B)
$$

    * A is the utility gained for building arms, a fixed value
    * C(n_b) is the cost function shown below:


  $$
  C(n_B) = X * ln(n_B + 1)
  $$

*where:*

    * ln (n_B + 1) is the logarithm of the number of countries building arms
>The idea for a logarithmic function is that the tensions will eventually plateau as more nations are added or contribute to their nuclear arms. The incremental impact on each nation’s utility will decrease. (+ 1 for the case where 0 countries build arms as ln(0) is undefined)


### **Utility for Not Building Arms:**

$$ 
U^C = B - Y*ln(n_B + 1)
$$ 

    * B is the utilty that a nation gets for not building arms (like peace points), a fixed value
    * G(n_b) is the cost function for not building arms shown below:

$$
G(n_b) = Y * ln(n_B + 1)
$$

*where:*

    * Y is the constant representing the scale of the cost
    * n_B is the number of countries not building arms

### Dominant Strategy Game
We chose a dominant strategy game in order to simulate a more realistic environment, where countries are faced with uncertainties of other nations' actions but still choose what's in their best interest. In this game, each country has a clear best strategy(defecting) regardless of what other nations choose to do. We wanted to incorporate more factors playing a role in the decision making process to express the complexity of strategic considerations countries have to make. Each country would consider things like international relationships, reputation, and previous choices to calculate the probability that other countries would cooperate or defect, and base their own decision off of that probability. 

To make the decision each round, we formulated expected utility functions for both if a country cooperates or deviates. The utility differs depending on the choice they make, but in both cases they need to consider:
  * Probability of all countries cooperating
  * Probability of all countries defecting
  * All probabilities of all combinations (2 ^ N-1) of each country either cooperating or defecting

### Utilities:
These functions calculate the utility considering the probabilities of all players cooperating or defecting based on player 𝐴's decision to cooperate or defect, factoring in both the best-case scenario (where all cooperate) and worst-case scenarios (where some or all defect). This reflects the uncertainty and strategic complexity in international relations.

#### Utility if Country A Cooperates:

$$
U_A \mid A \text{ cooperates} = U_A^{C} \cdot \prod_{i \neq A} p_i^{i_r, iA, 0} + U_A^{D} \cdot \prod_{i \neq A} (1 - p_i^{i_r, iA, 0}) + \sum_{S \subset \{1, 2, \ldots, N\}, S \neq A} U_A^{C} \cdot \prod_{i \in S} p_i^{i_r, iA, 0} \cdot \prod_{i \in \bar{S}} (1 - p_i^{i_r, iA, 0})
$$

- $$U_A^{C}$$: This is the utility for player A if they cooperate while others also cooperate
- $$U_A^{D}$$: This is the utility for player A if they cooperate while others defect

- **$$i_r, iA, 0$$**: Reputation of i is **$$i_r$$**, i's relationship with A is **$$iA$$**, and 0 is i's choice (0 meaning defection, 1 meaning cooperation) 

- **$$\prod_{i \neq A} p_i^{i_r, iA, 0}$$**: This notation means we're multiplying the probabilities of the other players (all players except A) cooperating. Each $$p_i$$ represents the probability that player $$i$$ cooperates 

- **$$\prod_{i \neq A} (1 - p_i^{i_r, iA, 0})$$**: This notation indicates the product of the probabilities that the other players do not cooperate. $$1 - p_i$$ represents the probability that player $$i$$ defects
  
- **$$\sum_{S \subset \{1, 2, \ldots, N\}, S \neq A}$$**: This terms sums over all subsets of players excluding A
- **$$U_A^{C}$$**: Represents the utility for Player A given a specific subset 𝑆 of players cooperate while the others do not
- **$$\prod_{i \in S} p_i^{i_r, iA, 0}$$**: Gives probability that all players in subset 𝑆 will cooperate
- **$$\prod_{i \in \bar{S}} (1 - p_i^{i_r, iA, 0})$$**: Gives probability that all players not in 𝑆 will defect


#### Utility if Country A Does NOT Coooperate:

$$
U_A \mid A \text{ defects} = U_A^{C} \cdot \prod_{i \neq A} p_i^{i_r, iA, 1} + U_A^{D} \cdot \prod_{i \neq A} (1 - p_i^{i_r, iA, 1}) + \sum_{S \subset \{1, 2, \ldots, N\}, S \neq A} U_A^{D} \cdot \prod_{i \in S} p_i^{i_r, iA, 1} \cdot \prod_{i \in \bar{S}} (1 - p_i^{i_r, iA, 1})
$$

- $$U_A^{C}$$:: This is the utility for player A if they cooperate while others defect

- $$U_A^{D}$$: This is the utility for player A if they defect while others also defect

- **$$i_r, iA, 1$$**: Reputation of i is **$$i_r$$**, i's relationship with A is **$$iA$$**, and 1 is i's choice (1 meaning cooperation, 0 meaning defection)

- **$$\\prod_{i \neq A} p_i^{i_r, iA, 1}\$$**: This notation means we're multiplying the probabilities of the other players (all players except A) cooperating. Each $$p_i$$ represents the probability that player $$i$$ cooperates 

- **\$$\prod_{i \neq A} (1 - p_i^{i_r, iA, 1})\$$**: This notation indicates the product of the probabilities that the other players do not cooperate. $$p_i$$ represents the probability that player $$i$$ defects.

- **$$\sum_{S \subset \{1, 2, \ldots, N\}, S \neq A}$$**: This terms sums over all subsets of players excluding A
  
- **$$U_A^{D}$$**: Represents the utility for Player A given a specific subset 𝑆 of players cooperate while the others do not
- **$$\prod_{i \in S} p_i^{i_r, iA, 1}$$**: Gives probability that all players in subset 𝑆 will cooperate
- **$$\prod_{i \in \bar{S}} (1 - p_i^{i_r, iA, 1})$$**: Gives probability that all players not in 𝑆 will defect

### Probability Function:

$$
P_i = \frac{1}{1 + e^{-(w_1 \cdot i_{choice} + w_2 \cdot iN_{relationship} + w_3 \cdot i_{reputation})}}
$$

* $$P_i$$ shows the probabilty that player i decides to cooperate based on:
  *  player i's previous choice
  *  player i's relationship with N and,
  *  player i's reputation for defecting/cooperating 
> The idea is the relationship value varies for each calculation, allowing each country to assess the probabilities based on its unique relationships with other countries. In this example the relationship value is between current player N and another country $$i$$. Player N is going to calculate the probability based on $$i$$'s reputation, N's relationship with $$i$$, and $$i$$'s previous decision to defect or cooperate. They will calculate this for all players $$i$$. We will then move to player N+1, and N+1 will do the same. This will continue for N players.
* w1, w2, and w3 are weights that determine the influence of each factor on the probability of cooperation and are fixed values in this implementation
* We're using an exponential function because it will always output a value between 0 and 1, where 0 means an event will never occur, and 1 means it will certainly occur

## Simulation Description

Simulation V2 uses our new utility functions for an n player game. We coded this simulation so that it represents a realistic real world outcome. 

In this simulation, there are two rounds. In both rounds, each nation compares its expected utility when cooperating to their expected utility when defecting. Each nation then chooses the maximum between the two. 

In this simulation, one important factor is the “reputation” of each nation. This is a number from 0 to 1. Zero means that a nation will always defect and one means a nation will always cooperate. This reputation is used in the probability function and is weighed much heavier than all other parameters. 

In the first round, all n players should defect. This is because in the real world, most nations are skeptical of each other and will assume that every other nation is very likely to defect and build arms. Thus, it's in every nation's best interest to also defect and build arms. To represent real world conditions, we set the reputation of each nation to range from 0 to 0.3 to show the initial cautious outlook nations have on one another. 

In our second round, we want to show what could be possible with future mechanisms. We change each country's reputation to range from 0.7 to 1.0, showing more developed and trustworthy relationships between nations. Thus, each nation should now cooperate. This is because, if everyone is willing to cooperate, every nation gets more utility compared to when they defect. 

Therefore, this second round shows that with the proper mechanisms, we can reach a globally optimal Nash, where no nations defect! 

Simulation V1 represents an older, simpler model which achieves the same results. However, simulation V1 does not use our new utility functions.

## Analysis & Theorems

* Since players are maximizing utility based on probabilities of what other countries will do, the nash occurs when:
  * All countries’ best responses are in equilibrium meaning no country has incentive to change its strategy
* The Nash Equilibrium is gauranteed because each player is choosing their best response 
* Countries may find defecting as a dominant strategy, leading to a *suboptimal outcome*
* Our utility functions are convex meaning:
  * As players increase their investment in arms (defection), the marginal utility gained decreases
  * players may be risk-averse, preferring strategies that ensure a more stable and predictable outcome

## Implemented Mechanisms
* If we recognize that players will prefer strategies that mitigate risk due to the convexity of our function, we choose mechanisms that are aimed more toward incentivizing cooperation, and disincentivizing defection to achieve a more optimal outcome
* The three we decided on are:
  * Global Support: It is an arbitrary value large enough to persuade players to cooperate that adds to the utility function when the player chooses to cooperate.(Ex. security assurances, financial aid) 
  * Reputation: With a higher value(better reputation) the probability of them defecting decreases, which will result in a smaller likelihood of other nations defecting
  * Relationship: With a higher value (better relationship) the probability of nations defecting decreases, which will result in a smaller likelihood of other nations defecting

 
  
 








