from typing import List

from wgups.data.distance_table import DistanceTable
from wgups.routing.package import Package
from wgups.structures.clock import Clock


class Truck:
    """A class which represents a truck delivering packages for the WGUPS.

    Attributes
    ----------
        id : int
            The identifier for the truck.
        capacity : int
            The total number of possible packages that can be carried by the truck.
        mph : int
            The speed of the truck.
        departure_time : Clock
            The earliest time that the truck can leave the hub.
        packages : List[Package]
            The packages that have been loaded onto the truck.
    """

    id: int
    capacity: int
    mph: int
    departure_time: Clock
    packages: List[Package]

    def __init__(self, id: int) -> None:
        self.id = id
        self.capacity = 16
        self.mph = 18
        # Initialize the truck departure time to the start of the delivery day
        self.departure_time = Clock(8)
        self.current_time = Clock()
        self.packages: List[Package] = []

    def is_full(self) -> bool:
        """Determines if the truck is full.

        Returns
        -------
            bool
                Returns `True` if the truck is full, otherwise returns `False`.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        return len(self.packages) >= self.capacity

    def depart_at(self, time: Clock) -> None:
        """Sets the departure time of the truck.

        Parameters
        ----------
            time : Clock
                The departure time to set.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        self.departure_time = time
        self.current_time = self.departure_time if self.departure_time > self.current_time else self.current_time

    def destinations(self) -> List[str]:
        """Gets the list of destinations that will be visited by the truck.

        Returns
        -------
            List[str]
                The list of destinations that will be visited by the truck.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        return [package.street for package in self.packages]

    def can_load(self, n: int) -> bool:
        """Determines if the truck can accept `n` number of packages without
        exceeding its capacity.

        Parameters
        ----------
            n : int
                The number of packages.

        Returns
        -------
            bool
                Returns `True` if the truck can accept all `n` packages, otherwise
                returns `False`.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        return len(self.packages) + n <= self.capacity

    def load_package(self, package: Package) -> None:
        """Loads a package onto the truck.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        package.pickup(self.departure_time.clone())
        self.packages.append(package)

    def load_packages(self, packages: List[Package]) -> None:
        """Loads several packages onto the truck.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        for package in packages:
            self.load_package(package)

    def unload_package(self, package: Package) -> None:
        """Unloads a package from the truck.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        if package in self.packages:
            self.packages.remove(package)

    def unload_packages(self, packages: List[Package]) -> None:
        """Unloads several packages from the truck.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        for package in packages:
            if package in self.packages:
                self.packages.remove(package)

    def has_package(self, package: Package) -> bool:
        """Determines if the truck contains the specified package.

        Returns
        -------
            bool
                True if the truck contains the specified package, otherwise False

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        return package in self.packages

    def can_deliver(self, package: Package) -> bool:
        """Determines if the truck can deliver the specified package.

        Parameters
        ----------
            package : Package
                The package to check.

        Returns
        -------
            bool
                Returns `True` if the truck can deliver the package, otherwise returns
                `False`.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        return self.id in package.deliverable_by and self.departure_time >= package.arrival_time

    def deliver_packages(self, distance_table: DistanceTable, return_to_depot: bool) -> None:
        """Delivers all packages currently loaded on the truck.

        Parameters
        ----------
            distance_table : DistanceTable
                A table of addresses and the distances between them.
            return_to_depot : bool
                Whether or not the truck should return to the depot after finishing
                its deliveries.

        Space Complexity
        ---------------
            O(n^2)

        Time Complexity
        ---------------
            O(n^2*log(n))
        """
        current_location = distance_table.depot_address
        destinations = self.destinations()
        total_time = self.departure_time
        total_distance = 0

        while self.packages:
            destinations = sorted(destinations,
                                  key=lambda x: distance_table.distance(current_location, x))
            closest = destinations.pop(0)

            distance = distance_table.distance(current_location, closest)
            travel_time = self.travel_time(distance)
            total_time.add_minutes(travel_time)

            deliveries = [package for package in self.packages
                          if package.street == closest]

            for package in deliveries:
                self.packages.remove(package)
                package.deliver(total_time.clone())

            current_location = closest
            total_distance += distance

        if return_to_depot:
            distance = distance_table.to_depot(current_location)
            travel_time = self.travel_time(distance)

            total_distance += distance
            total_time.add_minutes(travel_time)

        self.current_time = Clock(self.current_time.hours + total_time.hours,
                                  self.current_time.minutes + total_time.minutes)
        return total_distance

    def travel_time(self, miles: int) -> int:
        """Returns the time in minutes that it will take the truck to travel the
        specified number of miles.

        Parameters
        ----------
            miles : int
                The number of miles that will be traveled.

        Returns
        -------
            int
                The time in minutes that it takes to travel the specified number
                of miles.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        return round((miles / self.mph) * 60)
