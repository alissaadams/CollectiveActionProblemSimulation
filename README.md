# CollectiveActionProblemSimulation
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
    * U^D = utility for building arms 
    * U^C = utility for not building arms

### **Utility for Building Arms:**

$$
U^D = A - (X * ln(n_{b} + 1))
$$

    * A is the utility gained for building arms, a fixed value
    * X is a constant that represents the scaling factor of the cost for building
    * ln(n_b + 1) is the logarithm of the number of countries building arms

>The idea for a logarithmic function is that the tensions will eventually plateau as more nations are added or contribute to their nuclear arms. The incremental impact on each nation’s utility will decrease. (+ 1 for the case where 0 countries build arms as ln(0) is undefined)


### **Utility for Not Building Arms:**

$$ 
U^C = B - (Y * ln(n_{b} + 1))
$$ 

    * B is the utilty that a nation gets for not building arms (like peace points), a fixed value
    * Y is a constant that represents the scaling factor of the cost for not building

### Dominant Strategy Game
We chose a dominant strategy game in order to simulate a more realistic environment, where countries are faced with uncertainties of other nations' actions but still choose what's in their best interest. In this game, each country has a clear best strategy(defecting) regardless of what other nations choose to do. We wanted to incorporate more factors playing a role in the decision making process to express the complexity of strategic considerations countries have to make. Each country would consider things like international relationships, reputation, and previous choices to calculate the probability that other countries would cooperate or defect, and base their own decision off of that probability. 

To make the decision each round, we formulated utility functions for predicted utility for both if a country cooperates or deviates. The utility differs depending on the choice they make, but in both cases they need to consider:
  * Probability of all countries cooperating
  * Probability of all countries defecting
  * All probabilities of all combinations (2 ^ N-1) of each country either cooperating or defecting

### Predicted Utilities:
These functions calculate a predicted utility using our base utilities from above. We consider the probabilities of all players cooperating or defecting based on player 𝐴's decision to cooperate or defect, factoring in both the best-case scenario (where all cooperate) and worst-case scenarios (where some or all defect). This reflects the uncertainty and strategic complexity in international relations.

#### Predicted Utility if Country A Cooperates:

$$
U_A \mid A \text{ cooperates} = \sum_{S \subset \{1, 2, \ldots, N\}, S \neq A} U_A^{C} \cdot \prod_{i \in S} p_i^{i_r, iA, 0} \cdot \prod_{i \in \bar{S}} (1 - p_i^{i_r, iA, 0})
$$

- **$$\sum_{S \subset \{1, 2, \ldots, N\}, S \neq A}$$**: This terms sums over all subsets of players excluding A
- **$$U_A^{C}$$**: Represents the utility for Player A given a specific subset 𝑆 of players cooperate while the others do not
- **$$i_r, iA, 0$$**: Reputation of i is **$$i_r$$**, i's relationship with A is **$$iA$$**, and 0 is i's choice (0 meaning defection, 1 meaning cooperation) 
- **$$\prod_{i \in S} p_i^{i_r, iA, 0}$$**: Gives probability that all players in subset 𝑆 will cooperate, $$p_i$$ represents the probability that player $$i$$ cooperates
- **$$\prod_{i \in \bar{S}} (1 - p_i^{i_r, iA, 0})$$**: Gives probability that all players not in 𝑆 will defect, $$1 - p_i$$ represents the probability that player $$i$$ defects 


#### Predicted Utility if Country A Does NOT Coooperate:

$$
U_A \mid A \text{ defects} = \sum_{S \subset \{1, 2, \ldots, N\}, S \neq A} U_A^{D} \cdot \prod_{i \in S} p_i^{i_r, iA, 1} \cdot \prod_{i \in \bar{S}} (1 - p_i^{i_r, iA, 1})
$$

- **$$\sum_{S \subset \{1, 2, \ldots, N\}, S \neq A}$$**: This terms sums over all subsets of players excluding A
- **$$U_A^{D}$$**: Represents the utility for Player A given a specific subset 𝑆 of players cooperate while the others do not
- **$$i_r, iA, 1$$**: Reputation of i is **$$i_r$$**, i's relationship with A is **$$iA$$**, and 1 is i's choice (1 meaning cooperation, 0 meaning defection
- **$$\prod_{i \in S} p_i^{i_r, iA, 1}$$**: Gives probability that all players in subset 𝑆 will cooperate, $$p_i$$ represents the probability that player $$i$$ cooperates 
- **$$\prod_{i \in \bar{S}} (1 - p_i^{i_r, iA, 1})$$**: Gives probability that all players not in 𝑆 will defect, $$1 - p_i$$ represents the probability that player $$i$$ defects 

### Probability Function:

$$
P_i = \frac{1}{1 + e^{-(w_1 \cdot i_{choice} + w_2 \cdot iN_{relationship} + w_3 \cdot i_{reputation})}}
$$

* $$P_i$$ shows the probabilty that player i decides to cooperate based on:
  *  player i's previous choice
  *  player i's relationship with N and,
  *  player i's reputation for defecting/cooperating 
> The relationship value varies with each calculation, enabling each country to evaluate probabilities based on its unique relationships with others. In this example, the relationship value represents the connection between the current player, N, and another country, $$i$$. Player N  calculates the probability of cooperation by considering $$i$$'s reputation,  N's relationship with $$i$$, and $$i$$'s previous decision to cooperate or defect. This process is repeated for all players $$i$$. Once player N  completes their calculations, the process moves to player N+1, who performs the same evaluation. This continues sequentially for all N players.
* In this implementation, w1, w2, and w3 are fixed weights that determine the relative influence of each factor on the probability of cooperation.
* We're using an exponential function because it will always output a value between 0 and 1, where 0 means an event will never occur, and 1 means it will certainly occur.

## Simulation Description

Simulation V2 uses our new utility functions for an n player game. We coded this simulation so that it represents a realistic real world outcome. We recommend running the simulation with around 4-5 players for readability to get a clear evaluation of each player's choices.

In this simulation, the user selects the number of players. Each nation compares its utility when cooperating to their utility when defecting which are both dependent upon three variables: reputation, relationship with another nation, and the nations choice (defecting or cooperating). Each nation then chooses the maximum between the two. We broke up our simulation into four parts to demonstrate how players will behave with and without our mechanisms.

#### Part 1

This is the part where mechanisms have not been implemented, resulting in defection being the dominant strategy each round. This is because in the real world, most nations are skeptical of each other and will assume that every other nation is very likely to defect and build arms. Thus, it's in every nation's best interest to also defect and build arms. To represent real world conditions, we set the reputation of each nation to range from 0 to 0.3 to show the initial cautious outlook nations have on one another. 

#### Part 2

In part two we implement our first mechanism. In this simulation, one important factor is the “reputation” of each nation, as mentioned above. This is a number from 0 to 1. Zero means that a nation will always defect and one means a nation will always cooperate. This reputation is used in the probability function and is weighed heavier than the other parameters because it represents the level of trust and their expectation for the other player's actions. We adjusted each country's reputation to range from 0.7 to 1.0, showing more developed and trustworthy relationships between nations. The output should be most if not all cooperating. 

#### Part 3

Our second mechanism is through our relationships variable. We decided to implement something like a peace treaty to improve relationship values to incentivize cooperation. We set them to range between -1 and 1, with 1 being a purely positive and -1 being purely negative. In our simulation each nation will have a mixed relationship with every other nation, ranging from -0.5 and 0.2 to represent that some nations have somewhat positive relations while others
have somewhat negative ones. The output should be most if not all cooperating.

#### Part 4

In our final part we introduce our last mechanism representing a global organization providing incentives to cooperate through things like economic advantages(financial assistance or trade), security assurances, etc. This is a value that adds to our utility function to influence players to cooperate, which is what will be seen once the simulation is run. 

Parts 2-4 show that with the proper mechanisms, we can reach a globally optimal Nash, where no nations defect! 

Simulation V1 represents an older, simpler model which achieves the same results. However, simulation V1 does not use our new utility functions.

## Analysis & Theorems

* Since players are maximizing utility based on probabilities of what other countries will do, the nash occurs when:
  * All countries’ best responses are in equilibrium meaning no country has incentive to change its strategy.
* The Nash Equilibrium is gauranteed because each player is choosing their best response.
* Countries may find defecting as a dominant strategy, leading to a *suboptimal outcome* but, with mechanisms, the outcome can become the social optimum where everyone's best strategy is to cooperate.
* Our utility functions are convex meaning:
  * As players increase their investment in arms (defection), the marginal utility gained decreases.
  * Players may be risk-averse, preferring strategies that ensure a more stable and predictable outcome.

## Implemented Mechanisms
* If we recognize that players will prefer strategies that mitigate risk due to the convexity of our function, we choose mechanisms that are aimed more toward incentivizing cooperation, and disincentivizing defection to achieve a more optimal outcome.
* The three we decided on are:
  * Global Support: It is an arbitrary value large enough to persuade players to cooperate that adds to the utility function when the player chooses to cooperate. Some examples are:
     * Security assurances between countries
     * Financial aid from one country to another
  * Reputation: With a higher value(better reputation) the probability of them defecting decreases, which will result in a smaller likelihood of other nations defecting. Some examples as shown in the simulation are:
    * Choosing to commit to reducing the spread of nuclear arsenals through peace treaties
    * Engaging in peace talks and diplomacy with other countries
    * Providing transparency to other nations about their current arsenal to avoid misunderstandings

  * Relationship: With a higher value (better relationship) the probability of nations defecting decreases, which will result in a smaller likelihood of other nations defecting. Some examples as shown in the simulation are:
    * Engage in trade agreements or economic partnerships
    * Participate in joint military exercises or alliances
    * Offer humanitarian aid during crises or disasters

 
  
 








