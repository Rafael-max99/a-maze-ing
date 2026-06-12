import sys
import random
import mazegen.colors as colors
from mazegen.classes import Grid, RecursiveBacktracker
from mazegen.parsing import config_parser, AnyError
from mazegen.mazedata import MazeData, grid_to_mazegen


def create_pattern(grid: Grid, width: int, height: int) -> None:
    if height >= 7 and width >= 9:
        p_h = ((height - 5) // 2) + 4
        p_w = ((width - 7) // 2) + 6
        moves = [(0, -1), (0, -1), (-1, 0), (-1, 0), (0, 1), (0, 1), (-1, 0),
                 (-1, 0), (0, -1), (0, -1), (0, -4), (1, 0), (1, 0), (0, 1),
                 (0, 1), (1, 0), (1, 0)
                 ]

        grid[p_h, p_w].is_42 = True
        for h, w in moves:
            p_h += h
            p_w += w
            grid[p_h, p_w].is_42 = True
    else:
        warning += f"{colors.YELLOW}⚠ The maze is too small to show 42 pattern {colors.RESET}\n"

    # random.seed(22)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    try:
        vals = config_parser(sys.argv[1])
    except AnyError as e:
        print(e)
        return

    current_color = 0
    warning = ""
    height = vals[1]
    width = vals[0]

    grid = Grid(height, width)
    create_pattern(grid, width, height)
    RecursiveBacktracker.on(grid)
    mg = grid_to_mazegen(grid, vals[0], vals[1])
    mg.write_output_file(vals[4], vals[2], vals[3])
    maze = mg
    show_path = False

    while True:
        print(grid)
        print(warning)

        print("=== A-Maze-ing ===")
        print("1. Regenerate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        try:
            choice = int(input("Choice? (1-4): "))
        except ValueError:
            print("It needs to be an integer between 1 and 4")
            continue

        if choice == 1:
            grid = Grid(width, height, current_color)
            create_pattern(grid, width, height)
            RecursiveBacktracker.on(grid)
            mg = grid_to_mazegen(grid, vals[0], vals[1])
            mg.write_output_file(vals[4], vals[2], vals[3])
            maze = mg
            show_path = False
            continue

        elif choice == 2:
            if not show_path:
                for cell in grid.each_cell():
                    cell.is_path = False

                path = maze.find_shortest_path_cells(vals[2], vals[3])

                for x, y in path:
                    grid[y, x].is_path = True
                show_path = True

            else:
                for cell in grid.each_cell():
                    cell.is_path = False
                show_path = False
            continue

        elif choice == 3:
            current_color += 1

            if current_color >= len(colors.all_colors):
                current_color = 0
            grid.wall_color = colors.all_colors[current_color]

        elif choice == 4:
            break
        else:
            print("Choose between 1-4")
            continue


if __name__ == "__main__":
    main()
