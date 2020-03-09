from typing import Any, Callable, List, Union

from wgups.structures.hash_set import HashSet

Command = Union[int, str]


class Commander:
    """A class which handles mapping commands to their associated actions.

    Attributes
    ----------
        commands : HashSet[Union[int, str], Callable]
            A mapping of valid commands to their associated actions.
    """

    commands: HashSet[Command, Callable]

    def __init__(self) -> None:
        self.commands = HashSet[Command, Callable]()

    def options(self) -> List[str]:
        """Returns a list of all available commands.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        return [command for command in self.commands.keys()]

    def register(self, command: Command, action: Callable) -> None:
        """Registers a new command with the commander.

        Parameters
        ----------
            command : Union[int, str]
                The command to register.
            action : Callable)
                The action to execute for the specified command.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(n)
        """
        self.commands[command] = action

    def execute(self, command: Command) -> None:
        """Executes the action associated with the specified command.

        Parameters
        ----------
            command : Union[int, str]
                The command input by the user.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(n)
        """
        if command in self.commands:
            action = self.commands[command]
            action()
        else:
            print(f'\nInvalid Command: "{command}"\n'
                  f'Available commands: {self.options()}\n')

    def __repr__(self) -> str:
        return f'{self.options()}'

    def __str__(self) -> str:
        return self.__repr__()
