import os

from sys import stdout
from threading import Thread
from time import sleep
from typing import Any, Generator, Union

SpinnerGenerator = Generator[str, None, None]


class Spinner:
    """A class that creates a spinning loader in the console.

    Attributes
    ----------
        busy : bool
            A flag indicating if the spinner is currently busy.
        delay : float
            Indicates the delay between displaying the different loader animation sprites.
        generator : Generator[str, None, None]
            A generator function which yields the different loader animation sprites.
        message : str
            A message to display alongside the loader.
    """

    busy: bool
    delay: float
    generator: SpinnerGenerator
    message: str

    def __init__(self, message: str = '', delay: float = 0.1) -> None:
        self.busy = False
        self.delay = delay
        self.generator = self.spinning_cursor()
        self.message = message

    def spinner_task(self) -> None:
        """Sequentially writes the loader sprites to the console and then clears
        the console for the subsequent sprite.

        Time Complexity
        ---------------
            O(n)
        """
        while self.busy:
            stdout.write(f'{next(self.generator)} {self.message}')
            stdout.flush()
            sleep(self.delay)
            self.clear()
            stdout.flush()

    def spinning_cursor(self) -> SpinnerGenerator:
        """Generator function which yields the different loader animation sprites.

        Time Complexity
        ---------------
            O(n)
        """
        while True:
            for cursor in '|/-\\':
                yield cursor

    def clear(self) -> None:
        """Clears the console.

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

    def __enter__(self) -> None:
        self.busy = True
        Thread(target=self.spinner_task).start()

    def __exit__(self, exception: Exception, value: Any, tb: Any) -> Union[bool, None]:
        self.busy = False
        sleep(self.delay)
        if exception is not None:
            return False
