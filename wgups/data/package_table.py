from typing import List, Optional

from wgups.structures.hash_set import HashSet
from wgups.routing.package import Package


class PackageTable:
    """A class which handles storing, updating, and retrieving packages to be delivered
    by the WGUPS.

    Attributes
    ----------
        packages : HashSet[int, Package]
            The underlying data structure which stores packages. Maps package ids to package data.
    """

    packages: HashSet[int, Package]

    def __init__(self, packages: HashSet[int, Package]) -> None:
        self.packages = packages

    def get(self, identifier: int) -> Optional[Package]:
        """Finds a package by its identifier.

        Parameters
        ----------
            identifier : int
                The identifier of the package to find.

        Returns
        -------
            Optional[Package]
                The package if it exists, otherwise `None`.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        return self.packages.get(identifier)

    def all(self) -> List[Package]:
        """Returns a list of all packages.

        Returns
        -------
            List[Package]
                The list of all packages.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        return [package for _, package in self.packages]
