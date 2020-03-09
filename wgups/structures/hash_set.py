from typing import Generic, List, MutableMapping, Optional, Tuple, TypeVar, Union


class EmptySlot:
    """A class which serves as a marker of empty slots within the hash table.

    Attributes
    ----------
        tag : str
            A tag which marks the empty slot.
    """

    def __init__(self, tag: str) -> None:
        self.tag = tag

    def __repr__(self) -> str:
        return self.tag

    def __str__(self) -> str:
        return self.__repr__()


K = TypeVar('K')
V = TypeVar('V')
Table = List[Union[EmptySlot, V]]


class HashSet(Generic[K, V], MutableMapping[K, V]):
    """Implementation of a hash table using linear probing to search for suitable addresses.

    Attributes
    ----------
        EMPTY_SINCE_START : EmptySlot
            A marker for hash table slots that have been empty since initialization.
        EMPTY_AFTER_REMOVAL : EmptySlot
            A marker for hash table slots that only became empty after removing an item.
        capacity : int
            The capacity of the hash table.
        table : List[Union[EmptySlot, V]]
            The internal represenation of the hash table.
    """

    EMPTY_SINCE_START: EmptySlot
    EMPTY_AFTER_REMOVAL: EmptySlot
    capacity: int
    table: Table

    def __init__(self, initial_capacity: int = 10) -> None:
        # Create tags for the two types of empty slots
        self.EMPTY_SINCE_START = EmptySlot('EMPTY_SINCE_START')
        self.EMPTY_AFTER_REMOVAL = EmptySlot('EMPTY_AFTER_REMOVAL')

        # Set the initial capacity of the hash table
        self.capacity = initial_capacity

        # Create the array of slots
        self.table = [self.EMPTY_SINCE_START] * self.capacity

    def set(self, key: K, value: V) -> bool:
        """Inserts an item into the table.

        Parameters
        ----------
            key : K
                The key of the value to insert.
            value : V
                The value to insert.

        Returns
        -------
            bool
                A flag indicating if the (key, value) pair was successfully set.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """

        # Determine if the table should be rehashed
        if self.should_rehash():
            # Double the capacity of the table
            self.resize(self.capacity * 2)
            # Rehash the table
            self.rehash()

        # Determine the initial slot
        slot = hash(key) % len(self.table)

        # Initialize the number of slots probed to 0
        slots_probed = 0

        # Continue probing while the number of slots probed is less than the table length
        while slots_probed < len(self.table):
            # If the current slot is empty then assign the item to that slot
            # In this case, it does not matter if the slot is EMPTY_SINCE START
            # or EMPTY_AFTER_REMOVAL
            if type(self.table[slot]) is EmptySlot:
                self.table[slot] = (key, value)
                return True

            # Determine the next slot using linear probing
            slot = (slot + 1) % len(self.table)

            # Increment the number of slots probed
            slots_probed += 1

        # Table is full
        return False

    def get(self, key: K) -> Optional[V]:
        """Searches for an item within the table that matches the specified key.

        Parameters
        ----------
            key : K
                The key of the value to obtain.

        Returns
        -------
            Optional[V]
                Returns the value if found, otherwise returns `None`.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(n)
        """
        # Determine the initial slot
        slot = hash(key) % len(self.table)

        # Initialize the number of slots probed to 0
        slots_probed = 0

        # Continue probing while the number of slots probed is less than the table length
        # Probing should cease if an `EMPTY_SINCE_START` slot is reached given that
        # this indicates that a corresponding item for the key does not exist in the table
        while self.table[slot] is not self.EMPTY_SINCE_START and slots_probed < len(self.table):
            # Return the matching item, if found
            if self.table[slot][0] == key:
                return self.table[slot][1]

            # Determine the next slot using linear probing
            slot = (slot + 1) % len(self.table)

            # Increment the number of slots probed
            slots_probed += 1

        # No matching item was found
        return None

    def delete(self, key: K) -> bool:
        """Deletes an (key, value) pair from the table.

        Parameters
        ----------
            key : K
                The key of the value to delete.

        Returns
        -------
            bool
                A flag indicating if the (key, value) pair was successfully deleted.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(n)
        """
        # Determine the initial slot
        slot = hash(key) % len(self.table)

        # Initialize the number of slots probed to 0
        slots_probed = 0

        # Continue probing while the number of slots probed is less than the table length
        # Probing should cease if an `EMPTY_SINCE_START` slot is reached given that
        # this indicates that a corresponding item for the key does not exist in the table
        while self.table[slot] is not self.EMPTY_SINCE_START and slots_probed < len(self.table):
            # Mark the slot as `EMPTY_AFTER_REMOVAL` if a matching item is found
            if self.table[slot][0] == key:
                self.table[slot] = self.EMPTY_AFTER_REMOVAL
                return True

            # Determine the next slot using linear probing
            slot = (slot + 1) % len(self.table)

            # Increment the number of slots probed
            slots_probed += 1

        # No matching item was found
        return False

    def keys(self) -> List[K]:
        """Returns a list of all keys present in the table.

        Returns
        -------
            List[K]
                The list of keys present in the table.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        return [entry[0] for entry in self.__iter__() if entry is not None]

    def values(self) -> List[V]:
        """Returns a list of all values present in the table.

        Returns
        -------
            List[V]
                The list of values present in the table.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        return [entry[1] for entry in self.__iter__() if entry is not None]

    def resize(self, capacity: int) -> None:
        """Resizes the table to the specified capacity.

        Parameters
        ----------
            capacity : int
                The new capacity to set.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        self.capacity = capacity

    def rehash(self) -> None:
        """Rehashes the entire hash table.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        # Copy the previous table
        prev_table = self.table[:]

        # Create a new array of slots
        self.table = [self.EMPTY_SINCE_START] * self.capacity

        for entry in prev_table:
            # Ensure we do not try to unpack `EmptySlot`s
            if isinstance(entry, tuple):
                self.set(entry[0], entry[1])

    def should_rehash(self) -> bool:
        """Determines if the table should be rehashed. The table should only be rehashed if
        attempting to add additional (key, value) pairs after the table has reached its capacity.

        Returns
        -------
            bool
                `True` if the table should be rehashed, otherwise `False`.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        # Calculate how many values have been inserted into the table
        values = [value for value in self.values()
                  if not isinstance(value, EmptySlot)]
        return len(values) >= self.capacity

    def __getitem__(self, key: K) -> Optional[V]:
        return self.get(key)

    def __setitem__(self, key: K, value: V) -> bool:
        return self.set(key, value)

    def __delitem__(self, key: K) -> bool:
        return self.delete(key)

    def __len__(self) -> int:
        return len(self.table)

    def __contains__(self, key: K) -> bool:
        return self.get(key) != None

    def __iter__(self) -> Tuple[K, V]:
        for entry in self.table:
            if isinstance(entry, tuple):
                yield (entry[0], entry[1])
            else:
                yield None

    def __repr__(self) -> str:
        return f'HashTable {str(self.table)}'

    def __str__(self) -> str:
        return self.__repr__()
