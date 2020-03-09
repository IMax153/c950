from random import randint, sample
from typing import List, Tuple

from wgups.data.distance_table import DistanceTable
from wgups.data.package_table import PackageTable
from wgups.routing.package import Package
from wgups.routing.truck import Truck
from wgups.structures.clock import Clock
from wgups.structures.hash_set import HashSet


class Depot:
    """A class that represents the depot that handles route planning and
    distribution of packages for the WGUPS.

    Attributes
    ----------
        distance_table : DistanceTable
            A table containing the distance between destinations serviced by
            the WGUPS.
        package_table : PackageTable
            A table containing the packages that must be delivered by the WGUPS.
        trucks : HashSet[int, Truck]
            A mapping between truck identifiers and trucks.
    """

    distance_table: DistanceTable
    package_table: PackageTable
    trucks: HashSet[int, Truck]

    def __init__(self, distance_table: DistanceTable, package_table: PackageTable) -> None:
        self.distance_table = distance_table
        self.package_table = package_table

        self.trucks = HashSet(2)
        # The first truck will leave on time at 08:00
        self.trucks.set(0, Truck(1))
        # The second truck will be held at the depot until the late packages arrive at 09:05
        self.trucks.set(1, Truck(2))

    def deliver_packages(self) -> float:
        """Returns the total distance traveled by trucks during package delivery.

        Returns
        -------
            float
                The total distance.

        Space Complexity
        ---------------
            O(n^3)

        Time Complexity
        ---------------
            O(n^3*log(n))
        """
        packages = self.package_table.all()

        # Obtain separate lists of the high and low priority packages that must be delivered
        # and sort them by deadline (if applicable) and their distance to the depot
        high_priority = sorted(
            [package for package in packages
             if package.is_high_priority()],
            key=lambda x: (x.deadline, self.distance_table.to_depot(x.street))
        )
        regular_priority = sorted(
            [package for package in packages
             if not package.is_high_priority()],
            key=lambda x: self.distance_table.to_depot(x.street)
        )

        # Initialize loop parameters
        trip = 0
        truck_index = 0
        delivered = 0
        total_distance = 0
        departure_times = [Clock(8), Clock(9, 5), Clock(10, 20)]

        # Continue delivering packages while the number of packages that have been delivered
        # is less than the total number of packages that need to be delivered. The loop will
        # iterate three times in total given that our truck capacity is 16 and the trucks are
        # always loaded to capacity
        while delivered < len(packages):
            # Obtain the truck and set its departure time
            truck: Truck = self.trucks.get(truck_index)
            truck.depart_at(departure_times[trip].clone())

            # Obtain the priority packages that are deliverable by the truck
            priority_deliveries = [package for package in high_priority
                                   if truck.can_deliver(package)]

            # Obtain the regular priority packages that are deliverable by the truck
            regular_deliveries = [package for package in regular_priority
                                  if truck.can_deliver(package)]

            # First, load all priority deliveries that fit on the truck
            for package in priority_deliveries:
                if not truck.is_full() and not truck.has_package(package):
                    high_priority.remove(package)
                    truck.load_package(package)
                    delivered += 1

            # Then, load all regular priority deliveries that fit on the truck
            for package in regular_deliveries:
                if not truck.is_full() and not truck.has_package(package):
                    regular_priority.remove(package)
                    truck.load_package(package)
                    delivered += 1

            # Calculate the total distance traveled by the truck in addition to the
            # distance to return to the depot, if necessary
            remaining_packages = len(packages) - delivered
            return_to_depot = remaining_packages > 0
            total_distance += truck.deliver_packages(
                self.distance_table, return_to_depot)

            # Increment the trip index and the truck index
            trip += 1
            truck_index = trip % len(self.trucks)

        return total_distance

    def can_deliver(self, truck: Truck, package: Package) -> bool:
        """Determines if the specified truck can deliver the specified package.

        Parameters
        ----------
            truck : Truck
                The truck to check.
            package : Package
                The package to check.

        Returns
        -------
            bool
                Returns `True` if the truck can deliver the package, otherwise returns `False`.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        # Packages that must be delivered on truck two
        if package.id in [3, 18, 36, 38]:
            return truck.id == 2

        return package.arrival_time <= truck.departure_time
