import random

# Specification of the outcomes of the dilemma.
# Note: For the dilemma to remain valid, the values given have to meet these conditions:
# • top row values have to be greater than their corresponding bottom row values.
# • right column values have to be greater than their corresponding left column values.
# • the bottom-right value has to be greater than the top-left value.
OUTCOMES = (
    (1, 5),
    (0, 3),
)
# The letters used for `results.txt` file generation,
# specifying Defection and Cooperation respectively.
LETTERS = ('D', 'C')
# The amount of rounds played between each strategy.
# Note: This applies only to stochastic strategies, ones that utilize the `random` module
# Strategies not using that module are compared via a single round each.
ROUNDS = 10
# The length of each round. This is random, to prevent strategies from knowing when the round
# is about to end, and using this information to their advantage.
# Step of 2 guarantees the length to be even,
# to give a fair chance for each strategy to retailiate back if needed.
ROUND_LEN = random.randrange(100, 500, 2)
