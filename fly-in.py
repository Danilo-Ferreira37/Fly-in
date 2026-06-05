from parser.parsing import ConfigParser
from output.visualizer import Visualizer
from fly_struct.map import Map
import os
import sys


def main():
    os.system("clear")
    config = ConfigParser(sys.argv[1])
    info = config.load_file()
    info: dict

    map = Map(info)
    vizu = Visualizer(map, 1300, 500)
    vizu.run()

if __name__ == "__main__":
    main()
