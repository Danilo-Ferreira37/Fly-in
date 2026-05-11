from parser.parsing import ConfigParser
from map.struct import Map, Drone
import os


def main():
    os.system("clear")
    config = ConfigParser("config.txt")
    info = config.load_file()
    info: dict

    struct = Map(info)
    #for h in struct.hubs:
    #    print(h.max_drones, h.zone)
    #print(struct.connections)


if __name__ == "__main__":
    main()
