import sys
import colors
from classes import Grid, RecursiveBacktracker
from parsing import config_parser, AnyError


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
    height = vals[1]
    width = vals[0]

    grid = Grid(height, width)

    warning = ""

    if height >= 7 and width >= 9:
        p_h = ((height - 5) // 2) + 4
        p_w = ((width - 7) // 2) + 6
        moves = [(0, -1), (0, -1), (-1, 0), (-1, 0), (0, 1), (0, 1), (-1, 0),
                 (-1, 0), (0, -1), (0, -1), (0, -4), (1, 0), (1, 0), (0, 1),
                 (0, 1), (1, 0), (1, 0)]

        grid[p_h, p_w].is_42 = True
        for h, w in moves:
            p_h += h
            p_w += w
            grid[p_h, p_w].is_42 = True
    else:
        warning += f"{colors.YELLOW}⚠ The maze is too small to show 42 pattern {colors.RESET}\n"

    RecursiveBacktracker.on(grid)
    while True:
        print(grid)
        print(warning)

        print("=== A-Maze-ing ===")
        print("1. Regenerate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        choice = int(input("Choice? (1-4): "))

        if choice == 1:
            grid = Grid(vals[1], vals[0])
            RecursiveBacktracker.on(grid)
            continue
        elif choice == 2:
            print("answer showed")
            break
        elif choice == 3:
            current_color += 1

            if current_color >= len(colors.all_colors):
                current_color = 0
            grid.wall_color = colors.all_colors[current_color]
        elif choice == 4:
            break
        else:
            print("None of the above")
            break


if __name__ == "__main__":
    main()
