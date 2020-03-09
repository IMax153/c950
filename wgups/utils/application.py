from re import match

from wgups.data.data_loader import DataLoader
from wgups.data.distance_table import DistanceTable
from wgups.data.package_table import PackageTable
from wgups.routing.depot import Depot
from wgups.structures.clock import Clock
from wgups.structures.hash_set import HashSet
from wgups.utils.commander import Commander
from wgups.utils.prompter import Prompter


class Application:
    """A class which represents the WGUPS application. Handles starting and stopping the
    application program as well as delegating responses to user input.

    Attributes
    ----------
        running : bool
            A flag indicating if the application is currently running.
        depot : Depot
            The WGUPS depot.
        commander : Commander
            An instance of Commander which handles program response to user input.
        prompter : Prompter
            An instance of Prompter which handles obtaining user input.
    """

    running: bool
    depot: Depot
    commander: Commander
    prompter: Prompter

    def __init__(self) -> None:
        # Initially set the `running` flag to False
        self.running = False

        # Load in external data
        distance_table = DistanceTable(DataLoader.get_distances())
        package_table = PackageTable(DataLoader.get_packages())
        prompt_table = DataLoader.get_prompts()

        # Create the depot
        self.depot = Depot(distance_table, package_table)
        # Deliver the packages
        self.depot.deliver_packages()

        # Initialize the application Commander and Prompter
        self.commander = Commander()
        self.prompter = Prompter()

        # Set up the application commands and prompts
        self.register_commands()
        self.register_prompts(prompt_table)

    def register_commands(self) -> None:
        """Registers all available application commands.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(n)
        """
        self.commander.register('distance', self.route_distance)
        self.commander.register('package', self.package_report)
        self.commander.register('all', self.packages_report)
        self.commander.register('clear', self.prompter.clear)
        self.commander.register('exit', self.stop)

    def register_prompts(self, prompts: HashSet[str, str]) -> None:
        """Registers all available application prompts.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(n)
        """
        for name, prompt in prompts:
            self.prompter.register(name, prompt)

    def route_distance(self) -> None:
        """Prints the total distance traveled by the WGUPS.

        Space Complexity
        ---------------
            O(n^3)

        Time Complexity
        ---------------
            O(n^3*log(n))
        """
        miles = self.depot.deliver_packages()
        print('\nThe total distance traveled by the WGUPS was '
              f'{miles:.2f} miles.\n')

    def packages_report(self) -> None:
        """Prints a report of the status of all packages at a specific time.

        Time Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n*log(n))
        """
        time = self.prompter.prompt('time')
        if match(r'^\d{2}:\d{2}:\d{2}$', time) is None:
            print('\nInvalid time format\n')
            return

        (hours, minutes, seconds) = map(int, time.split(':'))
        packages = sorted(self.depot.package_table.all(), key=lambda p: p.id)

        reports = [package.delivery_report(Clock(hours, minutes))
                   for package in packages]
        col_width = max(len(item)
                        for report in reports for item in report) + 2  # Padding

        print('\nWGUPS Comprehensive Package Report\n')
        print(f'Time: {time}\n')
        for report in reports:
            print(''.join(item.ljust(col_width) for item in report))
        print('\n')

    def package_report(self) -> None:
        """Prints a report of a single package at a specific time.

        Space Complexity
        ---------------
            O(n)

        Time Complexity
        ---------------
            O(n)
        """
        package_id = self.prompter.prompt('package')
        try:
            package_id = int(package_id)
        except:
            print('\nInvalid package identifier\n')
            return

        if package_id not in self.depot.package_table.packages:
            print('\nInvalid package identifier\n')
            return

        time = self.prompter.prompt('time')
        if match(r'^\d{2}:\d{2}:\d{2}$', time) is None:
            print('\nInvalid time format\n')
            return

        (hours, minutes, seconds) = map(int, time.split(':'))
        package = self.depot.package_table.get(package_id)

        print('\nWGUPS Individual Package Report\n')
        print(f'Package: {package_id}')
        print(f'Time: {time}')
        print(package.inline_report(Clock(hours, minutes)))
        print('\n')

    def prompt(self) -> None:
        """Prompts the user for an application command.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        command = self.prompter.prompt('options')
        self.execute_command(command)

    def execute_command(self, command) -> None:
        """Executes an application command.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        self.commander.execute(command)

    def stop(self) -> None:
        """Handles stopping the application.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(1)
        """
        self.running = False

    def start(self) -> None:
        """Handles starting the application.

        Space Complexity
        ---------------
            O(1)

        Time Complexity
        ---------------
            O(n)
        """
        self.running = True
        while self.running:
            self.prompt()
