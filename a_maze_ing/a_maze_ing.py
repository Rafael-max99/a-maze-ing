import sys
from classes import Cell, Grid, RecursiveBacktracker
from errors import config_parser, AnyError


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    try:
        vals = config_parser(sys.argv[1])
    except AnyError as e:
        print(e)
        return

    grid = Grid(vals[1], vals[0])
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"
    grid[vals[2]].body = f"{GREEN} E {RESET}" 
    grid[vals[3]].body = f"{RED} X {RESET}"

    RecursiveBacktracker.on(grid)
    print(grid)


if __name__ == "__main__":
    main()
