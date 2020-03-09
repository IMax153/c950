from enum import Enum
from typing import Callable, List

from wgups.structures.clock import Clock


class PackageStatus(Enum):
    """A class representing the delivery status of a package.

    Attributes
    ----------
    AWAITING_DELIVERY : int
        The package is awaiting delivery.
    ON_TRUCK : int
        The package has been loaded onto a truck.
    DELIVERED : int
        The package has been delivered.
    """
    AWAITING_DELIVERY = 1
    ON_TRUCK = 2
    DELIVERED = 3


class Package:
    """A class representing a package within the WGUPS.

    Attributes
    ----------
        id : int
            The package identifier.
        street : str
            The destination street for the package.
        city : str
            The destination city for the package.
        state : str
            The destination state for the package.
        zip_code : str
            The destination zip code for the package.
        weight : int
            The weight of the package.
        deadline : Clock
            The delivery deadline for the package.
        status : PackageStatus
            The delivery status of the package.
        linked : bool
            Determines if the package is linked to other packages.
        deliverable_by : int
            Determines which trucks can deliver the package.
        is_priority : bool
            Determines if the package should be given priority during delivery.
        arrival_time : Clock
            The time that the package will arrive at the depot. Defaults to the start of the day (i.e. 08:00:00).
        pickup_time : Clock
            The time that the package was picked up from the depot.
        delivery_time : Clock
            The time that the package was delivered.
    """

    id: int
    street: str
    city: str
    state: str
    zip_code: str
    weight: int
    deadline: Clock
    status: PackageStatus
    linked: bool
    deliverable_by: int
    is_priority: bool
    arrival_time: Clock
    pickup_time: Clock
    delivery_time: Clock

    def __init__(self, id: int, street: str, city: str, state: str, zip_code: str,
                 weight: int, deadline: Clock, arrival_time: Clock = Clock(8)) -> None:
        self.id = id
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.weight = weight
        self.deadline = deadline
        self.status = PackageStatus.AWAITING_DELIVERY
        self.linked = False
        self.deliverable_by = [1, 2]
        self.is_priority = False
        self.arrival_time = Clock(8)
        self.pickup_time = None
        self.delivery_time = None

    def pickup(self, time: Clock) -> None:
        """Simulates picking up a package for delivery. Sets the package status
        to `ON_TRUCK` and the pickup time to the specified time.

        Parameters
        ----------
        time : Clock
            The time at which the package was picked up.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        self.status = PackageStatus.ON_TRUCK
        self.pickup_time = time

    def deliver(self, time: Clock) -> None:
        """Simulates delivering a package. Sets the package status to `DELIVERED`
        and the delivery time to the specified time.

        Parameters
        ----------
        time : Clock
            The time at which the package was delivered.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        self.status = PackageStatus.DELIVERED
        self.delivery_time = time

    def delivery_report(self, time: Clock) -> List[str]:
        """Returns a delivery report for the package.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        status = self.status_at(time)

        if self.delivery_time and time > self.delivery_time:
            on_time = self.delivery_time <= self.deadline if self.delivery_time else None
            return[
                f'Package={self.id}',
                f'Status={status.name}',
                f'Pickup Time={self.pickup_time}',
                f'Delivery Time={self.delivery_time}',
                f'On Time={on_time}'
            ]
        elif self.pickup_time and time > self.pickup_time:
            return [
                f'Package={self.id}',
                f'Status={status.name}',
                f'Pickup Time={self.pickup_time}',
                f'Delivery Time=N/A',
                f'On Time=N/A'
            ]
        else:
            return[
                f'Package={self.id}',
                f'Status={status.name}',
                f'Pickup Time=N/A',
                f'Delivery Time=N/A',
                f'On Time=N/A'
            ]

    def status_at(self, time: Clock) -> PackageStatus:
        """Returns the package status at the specified time.

        Parameters
        ----------
            time : Clock
                The time that the package status should be obtained for.

        Returns
        -------
            PackageStatus
                The status of the package.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        if self.delivery_time and time > self.delivery_time:
            return PackageStatus.DELIVERED
        elif self.pickup_time and time > self.pickup_time:
            return PackageStatus.ON_TRUCK
        else:
            return PackageStatus.AWAITING_DELIVERY

    def is_high_priority(self) -> bool:
        """Determines if the package is high priority or not.

        Returns
        -------
            bool
                Returns `True` if the package is high priority, otherwise returns `False`.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        return self.deadline < Clock(17) or self.is_priority

    def inline_report(self, time: Clock) -> str:
        """Retrieves an inline report of the package details for the specified time.

        Parameters
        ----------
            time : Clock
                The time for which the package report should be generated.

        Returns
        -------
            str
                The package report.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        return 'Details:\n' \
            f'\tId={self.id}\n' \
            f'\tStreet={self.street}\n' \
            f'\tCity={self.city}\n' \
            f'\tState={self.state}\n' \
            f'\tZip Code={self.zip_code}\n' \
            f'\tWeight={self.weight}\n' \
            f'\tDeadline={self.deadline}\n' \
            f'\tDelivery Status={self.status_at(time).name}'

    def __repr__(self) -> str:
        return 'Package(\n' \
            f'\tid={self.id},\n' \
            f'\tstreet="{self.street}",\n' \
            f'\tcity="{self.city}",\n' \
            f'\tstate="{self.state}",\n' \
            f'\tzip_code="{self.zip_code}",\n' \
            f'\tweight={self.weight},\n' \
            f'\tdeadline={self.deadline},\n' \
            f'\tstatus={self.status.name}\n)'

    def __str__(self) -> str:
        return self.__repr__()
