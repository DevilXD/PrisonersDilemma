from strategy import Strategy, History


class TitForTat(Strategy):
    """
    Classic Tit for Tat. Start by cooperating, then mimic the last opponent's move.
    """
    def play(self, history: History):
        if not history:
            return 1
        return history[-1][1]


class ReverseTitForTat(Strategy):
    """
    Classic Tit for Tat, but starts by defecting, then mimics the reversed last opponent's move.
    """
    def play(self, history: History):
        if not history:
            return 0
        return 1 - history[-1][1]


class TitFor2Tats(Strategy):
    """
    Classic Tit for Tat, but requires two defections before retaliating.
    Also known as Tit for Two Tats.
    """
    def play(self, history: History):
        if len(history) < 2:
            return 1
        return history[-1][1] + history[-2][1] > 0


class GrimmTitForTat(Strategy):
    """
    Grimm Tit for Tat. Start by cooperating, then mimic the last opponent's move.

    If at any point, your opponent defects twice in a row,
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
