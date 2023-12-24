from strategy import Strategy


class Detective(Strategy):
    """
    First: I analyze you. I start:
    Cooperate, Defect, Cooperate, Cooperate.
    If you defect back, I'll act like Tit for Tat.
    If you never defect back, I'll act like AlwaysDefect,
    to exploit you.

    - "Elementary, my dear Watson."

    """
    def __init__(self):
        self.moves = (1, 0, 1, 1)
        self.exploit = False

    def play(self, history):
        if self.exploit:
            return 0
        l = len(history)
        if l < len(self.moves):
            return self.moves[l]
        if l == len(self.moves) and all(m[1] == 1 for m in history):
            # opponent never cheated back - exploit them
            self.exploit = True
            return 0
        return history[-1][1]
