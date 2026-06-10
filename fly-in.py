from parser.parsing import ConfigParser
from output import Visualizer, choose_map
from fly_struct.map import Map
import os
import sys


def main() -> None:
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
        # map.vizu = Visualizer(map, 3700, 2500, theme)
        map.vizu = Visualizer(map, 1700, 1100, theme)
        map.run_simulation()
    except FileNotFoundError:
        print("Error: Image to the vizualization not found!")
        exit(1)


if __name__ == "__main__":
    main()
