from strategy import Strategy, History


class Calculator(Strategy):
    """
    Track the resulting scores and adjust itself accordingly.
    Start by cooperation.
    If we're losing, defect to raise its score, cooperate otherwise.
    This usually ends up behaving like Tit for Tat,
    but is more self-aware of it's own status.
    """
    def __init__(self):
        self.own_score = 0
        self.opponent_score = 0

    def play(self, history: History):
        if not history:
            return 1
        own, opn = history[-1]
        self.own_score += self.OUTCOMES[own][opn]
        self.opponent_score += self.OUTCOMES[opn][own]
        if self.own_score < self.opponent_score:
            return 0
        return 1
