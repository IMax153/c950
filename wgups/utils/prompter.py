import os

from typing import List

from wgups.structures.hash_set import HashSet


class Prompter:
    """A class which handles obtaining input based upon specific prompts.

    Attributes
    ----------
        prompts : HashSet[str, str]
            A mapping of valid prompt names to their associated display.
    """

    prompts: HashSet[str, str]

    def __init__(self) -> None:
        self.prompts = HashSet[str, str]()

    def options(self) -> List[str]:
        """Returns a list of all available prompts.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        return [name for name in self.prompts.keys()]

    def register(self, name: str, prompt: str) -> None:
        """Registers a new prompt with the prompter.

        Parameters
        ----------
            name : str
                The name of the prompt to register.
            prompt : str
                The prompt to execute for the specified prompt name.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(n)
        """
        self.prompts[name] = prompt

    def prompt(self, name: str) -> str:
        """Executes the action associated with the specified command.

        Parameters
        ----------
            name (str): The name of the prompt to display.

        Returns
        -------
            str
                The response to the prompt.

        Raises
        ------
            KeyError
                No valid prompt found for name.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(n)
        """
        if name in self.prompts:
            return input(self.prompts[name])
        else:
            raise KeyError(f'No valid prompt found for name {name}')

    def clear(self):
        """Clears the console.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        # Windows
        if os.name == 'nt':
            os.system('cls')
        # OSX and Linux (`os.name` here is 'posix')
        else:
            os.system('clear')

    def __repr__(self) -> str:
        return f'{self.options()}'

    def __str__(self) -> str:
        return self.__repr__()
