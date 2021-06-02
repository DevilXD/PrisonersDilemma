from strategy import Strategy


class Pavlov(Strategy):
    """
    Start by cooperating.

    If your opponent cooperates, just repeat your last move.
    If your opponent defects, do the opposite move of your last.
    """
    def play(self, history):
        if not history:
            return 1
        last = history[-1]
        if last[1] == 1:
            # repeat
            return last[0]
        else:
            # opposite
            return 1 - last[0]
