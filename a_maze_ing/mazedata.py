#!/usr/bin/python3

from collections import deque
from classes import Grid, Cell

class MazeData:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.maze = []

        for _ in range(height):
            line = [0] *width
            self.maze.append(line)

    def set_wall(self, x: int, y: int, direction: int, make_wall: bool = True):
        if 0 <= x < self.width and 0 <= y < self.height:
            if make_wall:
                # ativa o bit
                self.maze[y][x] |= (1 << direction)
            else:
                # desativa o bit
                self.maze[y][x] &= ~(1 << direction)

    def is_wall_closed(self, x: int, y: int, direction: int) -> bool:
         if 0 <= x < self.width and 0 <= y < self.height:
             return bool((self.maze[y][x] >> direction) & 1)
         return True

    def can_move(self, x: int, y: int, direction: int) -> bool:
        if self.is_wall_closed(x, y, direction):
            return False
        
        directions = {
            0: (0, -1), # North
            1: (1, 0), # East
            2: (0, 1), # South
            3: (-1, 0) # West
            }
        
        dx, dy = directions[direction]
        nx, ny = x + dx, y + dy

        return 0 <= nx < self.width and 0 <= ny < self.height

    def find_shortest_path(self, start: tuple[int, int], end: tuple[int, int]) -> str:
        if start == end:
            return ""
        
        queue = deque([(start[0], start[1], "")])
        visited = {start}
        
        directions = {
                0: ('N', 0, -1), # North
                1: ('E', 1, 0), # East
                2: ('S', 0, 1), # South
                3: ('W', -1, 0) # West
                }
        
        while queue:
            x, y, path = queue.popleft()
            if (x, y) == end:
                return path
            
            for direction, (letter, dx, dy) in directions.items():
                if self.can_move(x, y, direction):
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny, path + letter))

        return ""

    def to_hex_string(self) -> str:
        result = ""

        for row in self.maze:
            line = ""
            for cell in row:
                hex_value = format(cell, 'X')
                line += hex_value
            result += line + "\n"

        return result.strip()

    def write_output_file(self, filename: str, entry: tuple[int, int], exit_pos: tuple[int, int]) -> None:
        path = self.find_shortest_path(entry, exit_pos)

        with open(filename, "w") as f:
            f.write(self.to_hex_string())
            f.write("\n\n")
            f.write(f"{entry[0]}, {entry[1]}\n")
            f.write(f"{exit_pos[0]}, {exit_pos[1]}\n")
            f.write(f"{path}\n")

def grid_to_mazegen(grid: Grid, width: int, height: int) -> MazeData:
    
    mg = MazeData(width, height)
    
    for cell in grid.each_cell():
        x = cell.column
        y = cell.row
        
        # se nao esta linkado, tem parede
        if not cell.linked(cell.north):
            mg.set_wall(x, y, 0)  # North
        if not cell.linked(cell.east):
            mg.set_wall(x, y, 1)  # East
        if not cell.linked(cell.south):
            mg.set_wall(x, y, 2)  # South
        if not cell.linked(cell.west):
            mg.set_wall(x, y, 3)  # West
    
    return mg