from parser.parsing import ConfigParser
from map.struct import Map
import os


def main():
    os.system("clear")
    config = ConfigParser("config.txt")
    info = config.parse()
    info: dict

    struct = Map(info)
    print(struct.start_hub)
    for h in struct.hubs:
        print(h)


if __name__ == "__main__":
    main()
