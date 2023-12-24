from strategy import Strategy, History


class TitForTat(Strategy):
    """
    Classic Tit for Tat. Start by cooperating, then mimic the last opponent's move.
    """
    def play(self, history: History):
        if not history:
            return 1
        return history[-1][1]


class SuspiciousTitForTat(Strategy):
    """
    Tit for Tat, but starts by defecting, then mimics the last opponent's move.
    """
    def play(self, history: History):
        if not history:
            return 0
        return history[-1][1]


class ReverseTitForTat(Strategy):
    """
    Tit for Tat, but starts by defecting, then mimics the reversed last opponent's move.
    """
    def play(self, history: History):
        if not history:
            return 0
        return 1 - history[-1][1]


class TitFor2Tats(Strategy):
    """
    Tit for Tat, but requires two defections before retaliating.
    Also known as Tit for Two Tats.
    """
    def play(self, history: History):
        if len(history) < 2:
            return 1
        return history[-1][1] + history[-2][1] > 0


class DelayedTitForTat(Strategy):
    """
    Tit for Tat, but start by cooperating twice, then mimic the 2nd last opponent's move.
    """
    def play(self, history: History):
        if len(history) < 2:
            return 1
        return history[-2][1]


class GrimmTitForTat(Strategy):
    """
    Grimm Tit for Tat. Start by cooperating, then mimic the last opponent's move.

    If at any point your opponent defects twice in a row,
    get angry and switch to defecting for the rest of the round.
    """
    def __init__(self):
        self.angry = False

    def play(self, history: History):
        if self.angry:
            return 0
        if not history:
            return 1
        elif len(history) >= 2 and history[-1][1] + history[-2][1] == 0:
            self.angry = True
            return 0
        return history[-1][1]


class NiceTitForTat(Strategy):
    """
    Start by cooperating, then mimic the last opponent's move.

    If at any point your opponent defects twice in a row,
    cooperate on the next move to get out of deadlock.
    """
    def play(self, history: History):
        if not history:
            return 1
        if len(history) >= 2 and history[-1][1] + history[-2][1] == 0:
            return 1
        return history[-1][1]


class OmegaTitForTat(Strategy):
    """
    Start by cooperating, then mimic the last opponent's move.
    Repeat this for 3 rounds.

    Then, assuming you're facing another version of TFT (possibly modified),
    based on opponent's moves, apply these interactions:

    Define 2 stages of opponent's moves:
    • 1st: alternating: CDCDCD...
    • 2nd: repeated: DDDDDD...

    1st occurence:
    • DDD -> switch to always defect
    • CCC -> consider offering help again (clears flags)
    • DCD -> offer 1st stage help by cooperating
    • CDD -> offer 2nd stage help by cooperating

    2nd occurence:
    • DCD -> switch to always defect
    • CDD -> switch to always defect

    For any move not covered by these rules, use classic TFT rules.
    """
    def __init__(self):
        self.offer_help_1 = True
        self.offer_help_2 = True
        self.always_defect = False

    def play(self, history: History):
        if not history:
            return 1
        if self.always_defect:
            return 0
        if len(history) >= 3:
            if history[-1][1] == 0:
                # opponent defected
                if history[-2][1] == 0:
                    # second defection in a row
                    if history[-3][1] == 0:
                        # third defection in a row - they can't be trusted
                        self.always_defect = True
                        return 0
                    elif self.offer_help_2:
                        # offer 2nd stage help by cooperating
                        self.offer_help_2 = False
                        return 1
                    else:
                        # they can't be helped: switch to always defect
                        self.always_defect = True
                        return 0
                elif history[-3][1] == 0:
                    # second defection in the last 3 moves
                    if self.offer_help_1:
                        # offer 1st stage help by cooperating
                        self.offer_help_1 = False
                        return 1
                    else:
                        # they aren't reacting to it - exploit by always defecting
                        self.always_defect = True
                        return 0
            elif (
                (not self.offer_help_1 or not self.offer_help_2)
                and history[-1][1] + history[-2][1] + history[-3][1] == 3
            ):
                # last 3 moves were cooperative
                self.offer_help_1 = True
                self.offer_help_2 = True
        return history[-1][1]
