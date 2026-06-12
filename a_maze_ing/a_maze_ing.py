import sys
import random
import mazegen.colors as colors
from mazegen.classes import Grid, RecursiveBacktracker
from mazegen.parsing import config_parser, AnyError
from mazegen.mazedata import MazeData, grid_to_mazegen


def add_cycles(grid: Grid, count: int) -> None:
    added = 0

    while added < count:
        cell = grid.random_cell()
        neighbors = [
            neighbor for neighbor in cell.neighbors()
            if not neighbor.is_42 and not cell.linked(neighbor)
        ]
        if not neighbors:
            continue
        neighbor = random.choice(neighbors)
        cell.link(neighbor)
        added += 1


def create_grid(vals: list):
    grid = Grid(vals[1], vals[0])
    create_pattern(grid, vals[0], vals[1])
    grid.entry = vals[2]
    grid.exit = vals[3]
    # random.seed(22)
    RecursiveBacktracker.on(grid)
    if not vals[5]:
        add_cycles(grid, grid.size() // 20)
    mg = grid_to_mazegen(grid, vals[0], vals[1])
    mg.write_output_file(vals[4], vals[2], vals[3])
    return (grid, mg)


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
    show_path = False
    warning = ""
    if vals[1] < 7 or vals[0] < 9:
        warning += (f"{colors.YELLOW}⚠ The maze is too small to show "
                   f"42 pattern {colors.RESET}\n")

    grid, maze = create_grid(vals)

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
            grid, maze = create_grid(vals)
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
