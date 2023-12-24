"""
If it uses the `random` library, it belongs here.
"""

import random

from strategy import Strategy


class Random(Strategy):
    """
    50/50 on whether it cooperates or defects.
    """
    def play(self, history):
        return random.randint(0, 1)


class CooperateSometimesDefect(Strategy):
    """
    Usually cooperates, but sometimes defects.
    """
    def play(self, history):
        return random.choices((0, 1), weights=(0.1, 0.9), k=1)[0]


class DefectSometimesCooperate(Strategy):
    """
    Usually defects, but sometimes cooperates.
    """
    def play(self, history):
        return random.choices((0, 1), weights=(0.9, 0.1), k=1)[0]


class SelfishTFT(Strategy):
    """
    Classic Tit for Tat, but it defects 10% of the time, even when the opponent cooperates.
    """
    def play(self, history):
        if not history:
            return 1
        if history[-1][1] == 0:
            return 0
        if random.random() <= 0.1:
            # 10% chance to defect for cooperation, once in a while
            return 0
        return 1


class GenerousTFT(Strategy):
    """
    Classic Tit for Tat, but it cooperates 10% of the time, even when the opponent defects.
    """
    def play(self, history):
        if not history:
            return 1
        if history[-1][1] == 1:
            return 1
        if random.random() <= 0.1:
            # 10% chance to cooperate for defection, once in a while
            return 1
        return 0
