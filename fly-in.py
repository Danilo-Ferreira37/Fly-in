from parser.parsing import ConfigParser
from map.struct import Map, Drone
import os


def main():
    os.system("clear")
    config = ConfigParser("config.txt")
    info = config.parse()
    info: dict

    struct = Map(info)
    #for h in struct.hubs:
    #    print(h)
    #print(struct.connections)
    turn = 0
    while (True):
        print(struct.drones[0].current_hub)
        struct.drones[0].advance_my_drone()
        turn += 1
        if struct.drones[0].delivered:
            print(struct.drones[0].current_hub)
            print(f"Drone delivered with {turn} turns!!!!")
            break


if __name__ == "__main__":
    main()
