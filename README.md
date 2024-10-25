# Nuclear Arms - A Security Dilemma 

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
U_b = A - C(n_B)
$$

    * A is the utility gained for building arms
    * C(n_b) is the cost function shown below:


  $$
  C(n_B) = X * ln(n_B + 1)
  $$

*where:*

    * ln (n_B + 1) is the logarithm of the number of countries building arms
>The idea for a logarithmic function is that the tensions will eventually plateau as more nations are added or contribute to their nuclear arms. The incremental impact on each nation’s utility will decrease. (+ 1 for the case where 0 countries build arms as ln(0) is undefined)


### **Utility for Not Building Arms:**

$$ 
U_{nb} = B - Y*ln(n_B + 1)
$$ 

    * B is the utilty that a nation gets for not building arms (like peace points)
    * G(n_b) is the cost function for not building arms shown below:

$$
G(n_b) = Y * ln(n_B + 1)
$$

*where:*

    * Y is the constant representing the scale of the cost
    * n_B is the number of countries not building arms

### Mixed Strategy Game
We chose a mixed strategy game in order to simulate a more realistic environment, where countries are faced with uncertainties of other nations' actions. Since a mixed strategy game allows for randomized choices from players, this will better show the unpredictability in how nations might choose to build arms or cooperate. We wanted to incorporate more factors playing a role in the decision making process. Each country would consider things like international relationships, reputation, and previous choices to calculate the probability that other countries would cooperate or defect, and base their own decision off of that probability. 

To make the decision each round, we formulated expected utility functions for both if a country cooperates or deviates. The utility differs depending on the choice they make, but in both cases they need to consider:
  * Probability of all countries cooperating (C)
  * Probability of all countries defecting (B)
  * All probabilities of all combinations (2 ^ N-1) of each country either cooperating or defecting (D) 

### Expected Utilities:

#### Expected Utility if Country A Cooperates:

$$
E[U_A \mid A \text{ cooperates}] = U_A^{CC} \cdot \prod_{i \neq A} p_i^{i_r, iA, 0} + U_A^{CD} \cdot \prod_{i \neq A} (1 - p_i^{i_r, iA, 0}) + \sum_{S \subset \{1, 2, \ldots, N\}, S \neq A} U_A^{C,S} \cdot \prod_{i \in S} p_i^{i_r, iA, 0} \cdot \prod_{i \in \bar{S}} (1 - p_i^{i_r, iA, 0})
$$

- $$U_A^{CC}$$: This is the utility for player A if they cooperate while others also cooperate
- $$U_A^{CD}$$: This is the utility for player A if they cooperate while others defect


- **$$\prod_{i \neq A} p_i$$**: This notation means we're multiplying the probabilities of the other players (all players except A) cooperating. Each $$p_i$$ represents the probability that player $$i$$ cooperates

- **$$\prod_{i \neq A} (1 - p_i)$$**: This notation indicates the product of the probabilities that the other players do not cooperate. $$1 - p_i$$ represents the probability that player $$i$$ defects
!!!! Add explanation for summation



#### Expected Utility if Country A Does NOT Coooperate:

$$
E[U_A \mid A \text{ defects}] = U_A^{DC} \cdot \prod_{i \neq A} p_i^{i_r, iA, 1} + U_A^{DD} \cdot \prod_{i \neq A} (1 - p_i^{i_r, iA, 1}) + \sum_{S \subset \{1, 2, \ldots, N\}, S \neq A} U_A^{D,S} \cdot \prod_{i \in S} p_i^{i_r, iA, 1} \cdot \prod_{i \in \bar{S}} (1 - p_i^{i_r, iA, 1})
$$

- $$U_A^{DC}$$:: This is the utility for player A if they cooperate while others defect

- $$U_A^{DD}$$: This is the utility for player A if they defect while others also defect

- **$$\\prod_{i \neq A} p_i\$$**: This notation means we're multiplying the probabilities of the other players (all players except A) cooperating. Each $$p_i$$ represents the probability that player $$i$$ cooperates.

- **\$$\prod_{i \neq A} (1 - p_i)\$$**: This notation indicates the product of the probabilities that the other players do not cooperate. $$p_i$$ represents the probability that player $$i$$ defects.

!!!! Add explanation for summation

### Probability Function:

$$
P_i = \frac{1}{1 + e^{-(w_1 \cdot A_{choice} + w_2 \cdot iA_{relationship} + w_3 \cdot i_{reputation})}}
$$

* $$P_i$$ shows the probabilty that player i decides to cooperate based on:
  *  player A's choice
  *  player i's relationship with A and,
  *  player i's reputation for defecting/cooperating
* player A represents some "other" player. So, if we had nations A-Z, we would need to call this function using player A on nations B-Z with both choices, cooperating and defecting. Then i would represent each nation, B-Z. Then, we would call this function using player B on nations A and C-Z. In this case, all the A's would be changed to Bs. And the i would represent nations A and C-Z. Thus, A is not really a "fixed" nation as it changes depending on which country we are looking at. 
> The idea is the relationship value varies for each calculation, allowing each country to assess the probabilities based on its unique interactions with other countries. In this example the relationship value is between current player A and another country $$i$$. A is going to sum all of the probabilities of all other players ($$i$$) to use in its calculation for its own expected utility, then we'll move to player B and they'll do the same. This will continue for N players.
* w1, w2, and w3 are weights that determine the influence of each factor on the probability of cooperation and can be adjusted based on strategical importance, or fixed values
* We're using an exponential function because it will always output a value between 0 and 1, where 0 means an event will never occur, and 1 means it will certainly occur


## Analysis & Theorems

* The Nash Equilibrium Theorem guarantees that any mixed strategy game with a finite number of strategies has at least one Nash equilibrium
  * Our game has two strategies, therefore finite, influenced by the number of other countries who build arms
* Since players are maximizing utility based on probabilities of what other countries will do, the nash occurs when:
  * All countries’ best responses are in equilibrium meaning no country has incentive to change its strategy
* Countries may find defecting as a dominant strategy, leading to a *suboptimal outcome*
* Our utility functions are convex meaning:
  * As players increase their investment in arms (defection), the marginal utility gained decreases
  * players may be risk-averse, preferring strategies that ensure a more stable and predictable outcome

## Mechanisms
* If we recognize that players may prefer strategies that mitigate risk due to the convexity of our function, our mechanisms can be aimed more toward incentivizing cooperation, and disincentivizing defection to achieve a more optimal outcome
* Some ideas for incentives include:
  * Mutual alliances - if a country defects, their cost could increase(losing alliance benefits/points)
  * Providing nations with anti-nuclear arms - adding peace points to utility function, and decreasing the perceived threat making cooperation more attractive
  * Reputation costs - damaged reputation increases the cost by losing ability to form alliances, or influences other countries to defect when considering the probability of defection
  * Peace points - gain utility for cooperation
  * Security gaurantee from other countries - reduces perceived threat, reduces cost in utility function
  * Economic advantages - countries involved in disarmament are rewarded with economic/trade advantages increasing utility 
 








