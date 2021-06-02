from strategy import Strategy


class Detective(Strategy):
    """
    DETECTIVE: First: I analyze you. I start:
    Cooperate, Cheat, Cooperate, Cooperate.
    If you cheat back, I'll act like Tit for Tat.
    If you never cheat back, I'll act like Always Defect,
    to exploit you. Elementary, my dear Watson.
    """
    def __init__(self):
        self.moves = (1, 0, 1, 1)
        self.exploit = False

    def play(self, history):
        if self.exploit:
            return 0
        l = len(history)
        if l < 4:
            return self.moves[l]
        if l == 4 and all(m[1] == 1 for m in history):
            # opponent never cheated back - exploit them
            self.exploit = True
            return 0
        return history[-1][1]
