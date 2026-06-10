from parser.parsing import ConfigParser
from output import Visualizer, choose_map
from fly_struct.map import Map
import os
import sys


def main() -> None:
    """
    Entry point for the Fly-In simulation.

    Loads the configuration file (either from command-line arguments or from
    an interactive map selection), parses it, builds the Map object,
    initializes
    the Visualizer, and starts the simulation loop.

    Execution flow:
        1. Clear the terminal screen.
        2. Determine whether a config file was provided via command line.
        3. Parse the configuration using ConfigParser.
        4. Build the Map and initialize the Visualizer with the chosen theme.
        5. Run the simulation until all drones reach the end hub.
        6. Handle missing visualization assets gracefully.
    """
    os.system("clear")
    if len(sys.argv) > 1:
        if len(sys.argv) > 2:
            print(
                "Error: The program only can be "
                "executes with a config file or alone!"
            )
            exit(1)
        config = ConfigParser(sys.argv[1])
        theme = "Space Travel"
    else:
        mp, theme = choose_map()
        config = ConfigParser(mp)
    info = config.load_file()
    map = Map(info)
    try:
        #map.vizu = Visualizer(map, 3700, 2500, theme)
        map.vizu = Visualizer(map, 1900, 1000, theme)
        map.run_simulation()
    except FileNotFoundError:
        print("Error: Image to the vizualization not found!")
        exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        exit(1)
