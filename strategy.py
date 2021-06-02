from __future__ import annotations

import importlib
from abc import ABC, abstractmethod
from typing import Union, List, Tuple, Literal, Callable


History = List[Tuple[int, int]]


class classproperty(property):
    def __get__(self, instance, owner=None):
        if owner is None and instance is not None:
            owner = type(instance)
        return super().__get__(owner, owner)


class Strategy(ABC):
    """
    The base strategy class. Subclass it to implement your own strategy.

    You have access to some helpful read-only attributes:

    • Strategy.name - the name of your strategy, matching the name of the class.
    • Strategy.stochastic - set to `True` if your strategy is non-deterministic.
    • Strategy.OUTCOMES - the possible outcomes of the dillema as a tuple of 2-item tuples:
    (
        (both_defected, opponent_cooperated_you_defected),
        (opponent_defected_you_cooperated, both_cooperateed),
    )
    • Strategy.play - this is where you should implement your strategy.

    It's recomended to utilize only Python's standard library, like `math` and `random`.
    No 3rd party libraries should be required to construct successful strategies.
    """
    # tell MyPy this is okay to be overwritten with just bool
    stochastic: Union[bool, Callable[[Strategy], bool]]
    # provides access to the game's outcomes
    from constants import OUTCOMES

    @classproperty
    def name(cls) -> str:
        """
        Returns the strategy's name.

        :type: str
        """
        return cls.__name__  # type: ignore[attr-defined]

    @classproperty  # type: ignore[no-redef]
    def stochastic(cls) -> bool:
        """
        Returns `True` if the `random` module is imported (and presumably used
        within the strategy), `False` otherwise.
        This is checked by looking into the module's disctionary where the strategy is defined,
        and checking for the `random` variable name.

        Strategies that are non-deterministic (their next move can be different
        between instances, despite given identical history), but don't import the `random` module
        (or import it under a different name), should manually set this to `True`
        in their body like so:

        .. codeblock:: py

            class MyStrategy(Strategy):
                stochastic = True

        .. warning::

            Because this checks for the import alone, subclasses defined in modules that
            do import the `random` module, bot don't use it, will end up
            having this set incorrectly. To avoid this, please keep stochastic
            and non-stochastic strategies in separate modules:
            one module which does import `random`, and one which does not.

        :type: bool
        """
        module = importlib.import_module(cls.__module__)
        return "random" in module.__dict__

    @abstractmethod
    def play(self, history: History) -> Literal[0, 1, False, True]:
        """
        The main Strategy's function. Here, you can implement your strategy.

        Subclasses should overwrite this method accordingly.

        Helpful history recipes:

        .. codeblock:: py

            if not history:
                print("This signifies it's the first round, thus there's no history.")
            if history:
                # make sure to check for the history being there, before getting items out of it.
                last = history[-1]
                print(
                    "This gives you the outcome of the last round.\n"
                    "`last[0]` is the move you did, and `last[1]` is the move your opponent did."
                )
                last_opponent = history[-1][1]
                print("This gives you the last move of your opponent.")

        Arguments
        ---------
        history : List[Tuple[int, int]]
            The past history of the current round.
            Each tuple contains (self, other) scores of the past rounds
            against the same strategy player.
            The list will be empty during the first round.
        """
        raise NotImplementedError
