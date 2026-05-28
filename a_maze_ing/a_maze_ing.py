import sys
from classes import Cell, Grid, RecursiveBacktracker
from parsing import config_parser, AnyError
from mazedata import MazeData, grid_to_mazegen


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
    # Marca a entrada e a saída no grid
    grid[vals[2][1], vals[2][0]].body = f"{GREEN} E {RESET}" # Entrada (ENTRY HEIGHT, ENTRY WIDTH)
    grid[vals[3][1], vals[3][0]].body = f"{RED} X {RESET}" # Saída (EXIT HEIGHT, EXIT WIDTH)

    RecursiveBacktracker.on(grid)
    print(grid)
    # Converte o grid para MazeGenerator e escreve o arquivo de saída
    mg = grid_to_mazegen(grid, vals[0], vals[1])
    mg.write_output_file(vals[4], vals[2], vals[3])


if __name__ == "__main__":
    main()