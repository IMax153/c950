from __future__ import annotations
from typing import Union


class Clock:
    """A class which represents a time in minutes since the start of the
    delivery period.

    Attributes
    ----------
        total_minutes : int
            The number of total minutes on the clock.

    Properties
    ----------
        hours : int
            The number of hours on the clock.
        minutes : int
            The number of minutes on the clock.
    """

    total_minutes: int

    def __init__(self, hours: int = 0, minutes: int = 0) -> None:
        self.total_minutes = 0
        self.add_minutes(hours * 60 + minutes)

    @property
    def hours(self) -> int:
        """Determines the number of hours on the clock.

        Returns
        -------
            int
                The number of hours on the clock.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        return self.total_minutes // 60

    @property
    def minutes(self) -> int:
        """Determines the number of minutes on the clock.

        Returns
        -------
            int
                The number of minutes on the clock.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        return self.total_minutes % 60

    def add_minutes(self, minutes: int) -> None:
        """Adds the specified number of minutes to the clock.

        Parameters
        ----------
            minutes : int
                The number of minutes to add.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        self.total_minutes += minutes
        self.total_minutes = self.total_minutes % (60 * 24)

    def add_hours(self, hours: int) -> None:
        """Adds the specified number of hours to the clock.

        Parameters
        ----------
            hours : int
                The number of hours to add.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        self.add_minutes(hours * 60)

    def clone(self) -> Clock:
        """Creates a clone of the clock.

        Returns
        -------
            Clock
                The clone of the clock.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        return Clock(self.hours, self.minutes)

    def __eq__(self, other: Clock) -> bool:
        return self.total_minutes == other.total_minutes

    def __lt__(self, other: Clock) -> bool:
        return self.total_minutes < other.total_minutes

    def __gt__(self, other: Clock) -> bool:
        return self.total_minutes > other.total_minutes

    def __le__(self, other: Clock) -> bool:
        return self.__eq__(other) or self.__lt__(other)

    def __ge__(self, other: Clock) -> bool:
        return self.__eq__(other) or self.__gt__(other)

    def __repr__(self):
        return f'{self.hours:02d}:{self.minutes:02d}'

    def __str__(self):
        return self.__repr__()
