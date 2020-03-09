from wgups.structures.hash_set import HashSet

Distances = HashSet[str, HashSet[str, float]]


class DistanceTable:
    """A class which represents a table of the distances between destinations
    serviced by the WGUPS.

    Attributes
    ----------
        depot_address : str
            The address of the WGUPS depot.
        distances : HashSet[str, HashSet[str, float]]
            The underlying data structure which stores the distances between all
            destinations services by the WGUPS.
    """

    depot_address = '4001 South 700 East'
    distances: Distances

    def __init__(self, distances: Distances) -> None:
        self.distances = distances

    def distance(self, from_address: str, to_address: str) -> float:
        """Determines the distances between two destinations.

        Parameters
        ----------
            from_address : str
                The starting address.
            to_address : str
                The ending address.

        Returns
        -------
            float
                The distance between the two addresses.

        Raises
        ------
            KeyError
                The `from_address` or the `to_address` were not found in the distance table.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        if from_address in self.distances:
            if to_address in self.distances[from_address]:
                return self.distances[from_address][to_address]
            else:
                raise KeyError(
                    f'The address {to_address} was not found in the city map.')
        else:
            raise KeyError(
                f'The address {from_address} was not found in the city map.')

    def to_depot(self, address: str) -> float:
        """Determines the distance between the specified address and the depot.

        Parameters
        ----------
            address : str
                The address.

        Returns
        -------
            float
                The distance between the address and the depot.

        Raises
        ------
            KeyError
                The `address` was not found in the distance table.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        return self.distance(self.depot_address, address)
