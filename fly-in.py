from parser.parsing import ConfigParser
from map.struct import Map
import os

def main():
    os.system("clear")
    config = ConfigParser("config.txt")
    info = config.parse()
    info: dict

    struct = Map(info)
    for h in struct.hubs:
        print(h)



    #for k,v in info.items():
    #    if k == "hub":
    #        for i in info["hub"]:
    #            print("hub", i)
    #    elif k == "connection":
    #        for i in info["connection"]:
    #            print("connection", i)
    #    else:
    #        print(k, v)

if __name__ == "__main__":
    main()
