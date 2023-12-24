import os
import inspect
import importlib
from itertools import combinations
from math import floor, log10, comb
from typing import Optional, List, DefaultDict, Type

from strategy import Strategy, History
from constants import OUTCOMES, LETTERS, ROUNDS, ROUND_LEN


# Select the strategy to compare
# This one will be ran first, before all others
# Use an empty string to disable
compare: str = ""
with_stochastic: bool = True

# Select strategies to exclude
# Useful if you don't want to test all strategies, without moving files out of the folder
exclude: List[str] = []


# load all strategies
compare_strategy: Optional[Type[Strategy]] = None
strategies: List[Type[Strategy]] = []

strat_names: List[str] = []
for name in os.listdir("./strategies"):
    if not name.endswith(".py"):
        continue
    module = importlib.import_module(f"strategies.{name[:-3]}")
    for obj in module.__dict__.values():
        if inspect.isclass(obj) and obj is not Strategy and issubclass(obj, Strategy):
            name = obj.name
            if name in strat_names:
                raise RuntimeError(f"{name} strategy already exists!")
            strat_names.append(name)
            if compare and name == compare and compare_strategy is None:
                compare_strategy = obj
            elif name in exclude:
                # skip'em
                pass
            else:
                strategies.append(obj)
del strat_names
# Run the compare strategy first
if compare_strategy is not None:
    strategies.insert(0, compare_strategy)
elif compare:
    # If we defined a strategy to compare with, but it wasn't found - let the user know about it
    raise RuntimeError(f"Strategy {compare} set to compare, but doesn't exist!")


def match(strat1_cls: Type[Strategy], strat2_cls: Type[Strategy]) -> History:
    """
    Match two strategies against each other.

    Returns the match history as seen from the point of view of the first strategy.
    """
    # init the strategies
    strat1: Strategy = strat1_cls()
    strat2: Strategy = strat2_cls()
    # simulate
    history1: History = []
    history2: History = []
    for i in range(ROUND_LEN):
        result1: int = strat1.play(history1)
        if isinstance(result1, bool):
            result1 = int(result1)
        if not (isinstance(result1, int) and 0 <= result1 <= 1):
            raise RuntimeError(
                f"Strategy {strat1_cls.name} returned an invalid move: {result1}"
            )
        result2: int = strat2.play(history2)
        if isinstance(result2, bool):
            result2 = int(result2)
        if not (isinstance(result2, int) and 0 <= result2 <= 1):
            raise RuntimeError(
                f"Strategy {strat2_cls.name} returned an invalid move: {result2}"
            )
        history1.append((result1, result2))
        history2.append((result2, result1))
    return history1


# run each strategy against one another
scores: DefaultDict[str, float] = DefaultDict(float)
with open("results.txt", "w", encoding="utf8") as file:
    file.write(f"Round length: {ROUND_LEN}\n\n\n")
    if not with_stochastic:
        strategies = [s for s in strategies if not s.stochastic]
    total_matches = comb(len(strategies), 2)
    for i, (strat1_cls, strat2_cls) in enumerate(combinations(strategies, 2), start=1):
        print(f"{i}/{total_matches}")
        strat1_name = strat1_cls.name
        strat2_name = strat2_cls.name
        file.write(f"{strat1_name}  VS  {strat2_name}\n")
        stochastic = strat1_cls.stochastic or strat2_cls.stochastic
        # stochastic strategies are averaged over multiple rounds
        # non-stochastic strategies are matched only once
        round_score1 = round_score2 = 0.0
        for round in range(ROUNDS if stochastic else 1):
            # simulate
            history = match(strat1_cls, strat2_cls)
            # total up the score
            score1 = score2 = 0
            line1 = []
            line2 = []
            for move1, move2 in history:
                line1.append(LETTERS[move1])
                line2.append(LETTERS[move2])
                score1 += OUTCOMES[move1][move2]
                score2 += OUTCOMES[move2][move1]
            if round == 0:
                file.write(''.join(line1) + '\n')
                file.write(''.join(line2) + '\n')
            round_score1 += score1 / ROUND_LEN
            round_score2 += score2 / ROUND_LEN
        if stochastic:
            round_score1 /= ROUNDS
            round_score2 /= ROUNDS
        scores[strat1_name] += round_score1
        scores[strat2_name] += round_score2
        nl = max(len(strat1_name), len(strat2_name))
        file.write(f"{strat1_name:>{nl}} score: {round_score1}\n")
        file.write(f"{strat2_name:>{nl}} score: {round_score2}\n\n\n")
    file.write('\n')


# Display the average of each strategy
with open("results.txt", "a", encoding="utf8") as file:
    file.write("AVERAGE SCORES\n")
    nw = floor(log10(len(scores))) + 1
    nl = max(len(name) for name in scores) + 1
    div = len(scores) - 1
    for i, (name, score) in enumerate(
        sorted(scores.items(), key=lambda i: i[1], reverse=True), start=1
    ):
        file.write(f"#{i:{nw}} {f'{name}:':{nl}} {score / div}\n")
