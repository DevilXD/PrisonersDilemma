from strategy import Strategy


class Tester(Strategy):
    """
    Starts by defecting, but then cooperates and checks if you retaliated back.
    If not, it repeats the cycle.
    If yes, or the opponent's first move was to defect too, it becomes Tit for Tat.
    """
    def __init__(self):
        self.repeat = True

    def play(self, history):
        if self.repeat:
            l = len(history)
            if l in (1, 2):
                self.repeat = not any(m[1] == 0 for m in history[-2:])
            return l % 2
        return history[-1][1]
