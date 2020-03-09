# Student Name: Maxwell Brown
# Student ID: 000933363

from time import sleep

from wgups.utils.application import Application
from wgups.utils.spinner import Spinner

if __name__ == "__main__":
    # Display a spinner in the console while we load in external data and setup the application
    with Spinner('Preparing WGUPS Package Router ...'):
        application = Application()
        sleep(2)
    application.start()
