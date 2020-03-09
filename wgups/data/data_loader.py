from __future__ import annotations
from datetime import timedelta
from json import load
from os import path
from typing import Any, Mapping

from wgups.structures.clock import Clock
from wgups.structures.hash_set import HashSet
from wgups.routing.package import Package

Distances = HashSet[str, HashSet[str, str]]
Packages = HashSet[int, Package]
Prompts = HashSet[str, str]


class DataLoader:
    """A class for loading external data into the application. Utilizes a cache to ensure
    that data is ever only loaded once.

    Class Attributes
    ----------------
        cache : HashSet[str, Any]
            The cache which handles storing file data.
    """

    cache = HashSet[str, Any]()

    @classmethod
    def load_json(cls, filename) -> Mapping[Any, Any]:
        """Attempts to retrieve the file from the cache. Loads the file data if it is not
        present in the cache.

        Returns
        -------
            Mapping[Any, Any]
                The JSON file data.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        file_path = path.join(path.dirname(__file__), filename)

        with open(file_path, 'r') as file:
            return load(file)

    @classmethod
    def get_packages(cls) -> Packages:
        """Attempts to retrieve the packages from the cache. Loads the package data from a file
        if it is not present in the cache.

        Returns
        -------
            HashSet[int, str]
                The mapping of package identifiers to package objects.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        if 'packages' not in cls.cache:
            cls.cache.set('packages', cls.load_packages())

        return cls.cache.get('packages')

    @classmethod
    def load_packages(cls) -> Packages:
        """Loads the package data from a file.

        Returns
        -------
            HashSet[int, str]
                The mapping of package identifiers to package objects.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        data = cls.load_json('data/package_data.json')
        size = len(data)
        packages = HashSet(size)

        for key, value in data.items():
            identifier = int(key)

            (hours, minutes) = map(int, value['deadline'].split(':'))
            deadline = Clock(hours, minutes)

            package = Package(
                identifier,
                value['address'],
                value['city'],
                value['state'],
                value['zip'],
                value['kg'],
                deadline,
            )

            # Delayed packages - will not arrive at depot until 09:05
            if package.id in [6, 25, 28, 32]:
                package.arrival_time = Clock(9, 5)

            # Incorrect address - will be corrected at 10:20
            if package.id == 9:
                package.street = '410 S State St'
                package.arrival_time = Clock(10, 20)

            # Package must be delivered via truck two
            if package.id in [3, 18, 36, 38]:
                package.deliverable_by = [2]
                package.is_priority = True

            # Package must be delivered with linked packages
            if package.id in [13, 14, 15, 16, 19, 20]:
                package.linked = True
                package.is_priority = True

            packages.set(identifier, package)

        return packages

    @classmethod
    def get_distances(cls) -> Distances:
        """Attempts to retrieve the distances from the cache. Loads the distance data from a file
        if it is not present in the cache.

        Returns
        -------
            HashSet[str, HashSet[str, str]]
                The mapping of from and to addresses and the corresponding distance between them.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        if 'distances' not in cls.cache:
            cls.cache.set('distances', cls.load_distances())

        return cls.cache.get('distances')

    @classmethod
    def load_distances(cls) -> Distances:
        """Loads the distance data from a file.

        Returns
        -------
            HashSet[str, HashSet[str, str]]
                The mapping of from and to addresses and the corresponding distance between them.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        data = cls.load_json('data/distance_data.json')
        size = len(data)
        distances = HashSet(size)

        for from_address, destinations in data.items():
            if from_address not in distances:
                distances.set(from_address, HashSet(size))

            for to_address, miles in destinations.items():
                distances.get(from_address).set(to_address, miles)

        return distances

    @classmethod
    def get_prompts(cls) -> Prompts:
        """Attempts to retrieve the prompts from the cache. Loads the prompt data from a file
        if it is not present in the cache.

        Returns
        -------
            HashSet[str, str]
                The mapping of prompt names to prompt values.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        if 'prompts' not in cls.cache:
            cls.cache.set('prompts', cls.load_prompts())

        return cls.cache.get('prompts')

    @classmethod
    def load_prompts(cls) -> Prompts:
        """Loads the prompt data from a file.

        Returns
        -------
            HashSet[str, str]
                The mapping of prompt names to prompt values.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        data = cls.load_json('data/prompts.json')
        size = len(data)
        prompts = HashSet(size)

        for key, value in data.items():
            prompts.set(key, value)

        return prompts
