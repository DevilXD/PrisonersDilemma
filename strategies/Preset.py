from strategy import Strategy


class AlwaysCooperate(Strategy):
    """
    Always cooperates.
    """
    def play(self, history):
        return 1


class AlwaysDefect(Strategy):
    """
    Always defects.
    """
    def play(self, history):
        return 0


class Alternator(Strategy):
    """
    Alternates beteween cooperating and defecting.
    Starts by cooperating.
    """
    def play(self, history):
        return 1 - len(history) % 2


class ReverseAlternator(Strategy):
    """
    Alternates beteween cooperating and defecting.
    Starts by defecting.
    """
    def play(self, history):
        return len(history) % 2
