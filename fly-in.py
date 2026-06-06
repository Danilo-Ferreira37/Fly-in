from parser.parsing import ConfigParser
from output.visualizer import Visualizer
from fly_struct.map import Map
import os, sys

def choose_map() -> str:
    maps = {"easy" : {
                "1": "01_linear_path.txt",
                "2": "02_simple_fork.txt",
                "3": "03_basic_capacity.txt"},
            "medium": {
                "1": "01_dead_end_trap.txt",
                "2": "02_circular_loop.txt",
                "3": "03_priority_puzzle.txt"
            },
            "hard": {
                "1": "01_maze_nightmare.txt",
                "2": "02_capacity_hell.txt",
                "3": "03_ultimate_challenge.txt"
            }}
    
    while(True):
        print("1. Easy\n2. Medium\n3. Hard\n4. Challenger\n5. Customized\n6. Quit")
        option = input("\nChoose the map difficulty: ")
        if option not in {"1", "2", "3", "4", "5", "6"}:
            os.system("clear")
            print("Error: Choose a number from 1 to 6.")
            continue

        elif option == "1":
            os.system("clear")
            print(maps["easy"].get("1"))
            print(maps["easy"].get("2"))
            print(maps["easy"].get("3"))
            mp = input("\nChoose a map: ")
            if mp not in {"01","02", "03", "1", "2", "3"}:
                os.system("clear")
                print("To the easy maps choose a number from 1 to 3.")
                continue
            return f'maps/easy/{maps["easy"].get(mp.replace("0", ""))}'

        elif option == "2":
            os.system("clear")
            print(maps["medium"].get("1"))
            print(maps["medium"].get("2"))
            print(maps["medium"].get("3"))
            mp = input("\nChoose a map: ")
            if mp not in {"01","02", "03", "1", "2", "3"}:
                os.system("clear")
                print("To the medium maps choose a number from 1 to 3.")
                continue
            return f'maps/medium/{maps["medium"].get(mp.replace("0", ""))}'

        elif option == "3":
            os.system("clear")
            print(maps["hard"].get("1"))
            print(maps["hard"].get("2"))
            print(maps["hard"].get("3"))
            mp = input("\nChoose a map: ")
            if mp not in {"01","02", "03", "1", "2", "3"}:
                os.system("clear")
                print("To the hard maps choose a number from 1 to 3.")
                continue
            return f'maps/hard/{maps["hard"].get(mp.replace("0", ""))}'
        elif option == "4":
            return "maps/challenger/01_the_impossible_dream.txt"
        elif option == "5":
            os.system("clear")
            mp = input("Enter your customized map (Ex:. config.txt) or 'q' to return:\n")
            if mp == 'q':
                os.system("clear")
                continue
            return mp
        
        elif option == "6":
            os.system("clear")
            print("Exit the program!!")
            exit(0)

def main():
    os.system("clear")
    if len(sys.argv) > 1:
        if len(sys.argv) > 2: 
            print("Error: The program only can be "
                  "executes with a config file or alone!")
            exit(1)
        config = ConfigParser(sys.argv[1])
    else:
        config = ConfigParser(choose_map())
    info = config.load_file()
    map = Map(info, Visualizer)

if __name__ == "__main__":
    main()
