from strategy import Strategy


class GrimmTrigger(Strategy):
    """
    Start by cooperating, and repeat it until the opponent defects, at which point you get "angry"
    and defect for the rest of the round.
    """
    def __init__(self):
        self.angry = False

    def play(self, history):
        if self.angry:
            return 0
        if not history:
            return 1
        if history[-1][1] == 0:
            # our opponent defected - RAGE!
            self.angry = True
            return 0
        return 1


class DelayedGrimmTrigger(Strategy):
    """
    Same as GrimmTrigger, but requires two defections - forgives the first one.
    """
    def __init__(self):
        self.defections = 0

    def play(self, history):
        if not history:
            return 1
        if history[-1][1] == 0:
            # our opponent defected
            self.defections += 1
        if self.defections >= 2:
            return 0
        return 1


class NiceTrigger(Strategy):
    """
    Start by defecting, and repeat it until the opponent cooperates, at which point you get "nice"
    and cooperate for the rest of the round.
    """
    def __init__(self):
        self.nice = False

    def play(self, history):
        if self.nice:
            return 1
        if not history:
            return 0
        if history[-1][1] == 1:
            # our opponent cooperated
            self.nice = True
            return 1
        return 0


class Grumpy(Strategy):
    """
    Start by cooperating and continue to do so, but watch out for defections.
    After enough of them, get "grumpy" and switch to defecting.
    If your opponent decided to cooperate enough times, switch to cooperating again too.
    """
    def __init__(self):
        self.count = 0

    def play(self, history):
        if not history:
            return 1
        if history[-1][1] == 0:
            self.count += 1
        elif history[-1][1] == 1 and self.count > 0:
            # don't let them build up trust with a bunch of cooperations
            self.count -= 1
        return self.count < 5
