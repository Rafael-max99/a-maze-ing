import random
import colors


class Cell:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.is_42 = False
        self.is_path = False

        self.north = None
        self.east = None
        self.south = None
        self.west = None

        self.links = set()

    def link(self, cell, bidi=True) -> None:
        self.links.add(cell)

        if bidi:
            cell.link(self, False)

    def unlink(self, cell, bidi=True) -> None:
        self.links.discard(cell)

        if bidi:
            cell.unlink(self, False)

    def linked(self, cell) -> bool:
        return cell in self.links

    def neighbors(self):
        return [
            neighbor for neighbor in
            [self.north, self.south, self.east, self.west]
            if neighbor is not None
        ]


class Grid:
    def __init__(self, rows: int, columns: int, cl: int = 0) -> None:
        self.rows = rows
        self.columns = columns

        self.wall_color = colors.all_colors[cl]
        self.grid = self.prepare_grid()
        self.configure_cells()

        self.entry = None
        self.exit = None

    def prepare_grid(self) -> list[list[Cell]]:
        return [
            [Cell(row, column) for column in range(self.columns)]
            for row in range(self.rows)
        ]

    def configure_cells(self) -> None:
        for cell in self.each_cell():
            row = cell.row
            col = cell.column

            cell.north = self[row - 1, col]
            cell.south = self[row + 1, col]
            cell.west = self[row, col - 1]
            cell.east = self[row, col + 1]

    def __getitem__(self, position: tuple[int, int]) -> Cell | None:
        row, column = position

        if not (0 <= row < self.rows):
            return None

        if not (0 <= column < self.columns):
            return None

        return self.grid[row][column]

    def random_cell(self) -> Cell:
        row = random.randrange(self.rows)
        column = random.randrange(self.columns)

        return self[row, column]

    def is_entry(self, cell: Cell) -> bool:
        return (cell.column, cell.row) == self.entry

    def is_exit(self, cell: Cell) -> bool:
        return (cell.column, cell.row) == self.exit

    def size(self) -> int:
        return self.rows * self.columns

    def each_row(self):
        for row in self.grid:
            yield row

    def each_cell(self):
        for row in self.each_row():
            for cell in row:
                if cell is not None:
                    yield cell

    def __str__(self) -> str:
        output = "+" + "---+" * self.columns + "\n"

        for row in self.each_row():

            top = "|"
            bottom = "+"

            for cell in row:

                if cell is None:
                    cell = Cell(-1, -1)
                if cell.is_42:
                    body = "█▇█"
                elif self.is_entry(cell):
                    body = "🚪 "
                elif self.is_exit(cell):
                    body = "🏁 "
                elif cell.is_path:
                    body = "✨ "
                else:
                    body = "   "
                east_boundary = " " if cell.linked(cell.east) else "|"
                top += body + east_boundary

                south_boundary = "   " if cell.linked(cell.south) else "---"
                corner = "+"
                bottom += south_boundary + corner

            output += top + "\n"
            output += bottom + "\n"

        return f"{self.wall_color}{output}{colors.RESET}"


class RecursiveBacktracker:

    @staticmethod
    def on(grid, start_at=None):

        if start_at is None:
            start_at = grid.random_cell()

        stack = [start_at]

        while stack:

            current = stack[-1]

            neighbors = [
                neighbor
                for neighbor in current.neighbors()
                if len(neighbor.links) == 0 and not neighbor.is_42
            ]

            if not neighbors:
                stack.pop()

            else:
                neighbor = random.choice(neighbors)
                current.link(neighbor)
                stack.append(neighbor)

        return grid
