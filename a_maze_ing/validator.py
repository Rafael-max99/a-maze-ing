#!/usr/bin/python3

import re
from typing import Optional


class MazeValidator:
    def __init__(self, filename: str):
        self.filename = filename
        self.errors = []
        self.warnings = []

    def validate(self) -> bool:
        try:
            with open(self.filename, "r") as f:
                content = f.read()
        except FileNotFoundError:
            self.errors.append(f"Arquivo não encontrado: {self.filename}")
            return False

        parts = content.split("\n\n")
        if len(parts) < 2:
            self.errors.append("Arquivo não contém linha vazia de separação")
            return False

        maze_lines = parts[0].strip().split('\n')
        metadata_lines = parts[1].strip().split('\n')

        if not self.validate_maze(maze_lines):
            return False
        if not self._validate_metadata(metadata_lines, maze_lines):
            return False

        return len(self.errors) == 0

    def validate_maze(self, lines: list) -> bool:
        if not lines:
            self.errors.append("Maze vazio")
            return False

        width = len(lines[0])
        for i, line in enumerate(lines):

            if not re.match(r'^[0-9A-Fa-f]+$', line):
                self.errors.append(f"Linha {i}: caracteres "
                                   f"hexadecimais inválidos")
                return False

            if len(line) != width:
                self.errors.append(f"Linha {i}: largura inconsistente "
                                   f"({len(line)} vs {width})")
                return False

            for j, char in enumerate(line):
                val = int(char, 16)

                if val > 0xF:
                    self.errors.append(f"Linha {i}, coluna {j}: valor > 0xF")
                    return False

        print(f"Maze válido: {len(lines)} linhas x {width} colunas")
        return True

    def _validate_metadata(self, lines: list, maze_lines: list) -> bool:
        if len(lines) < 3:
            self.errors.append("Metadados incompletos "
                               "(esperado: entrada, saída, caminho)")
            return False

        entry_str, exit_str, path_str = lines[0], lines[1], lines[2]
        entry = self._parse_coordinates(entry_str)

        if entry is None:
            self.errors.append(f"Entrada inválida: {entry_str}")
            return False

        exit_pos = self._parse_coordinates(exit_str)
        if exit_pos is None:
            self.errors.append(f"Saída inválida: {exit_str}")
            return False

        height = len(maze_lines)
        width = len(maze_lines[0]) if maze_lines else 0

        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            self.errors.append(f"Entrada fora dos limites: {entry}")
            return False

        if not (0 <= exit_pos[0] < width and 0 <= exit_pos[1] < height):
            self.errors.append(f"Saída fora dos limites: {exit_pos}")
            return False

        print(f"Entrada válida: {entry}")
        print(f"Saída válida: {exit_pos}")

        if not re.match(r'^[NESW]*$', path_str):
            self.errors.append(f"Caminho inválido: {path_str}")
            return False

        print(f"Caminho válido: {path_str} ({len(path_str)} passos)")
        return True

    def _parse_coordinates(self, coord_str: str) -> Optional[tuple[int, int]]:
        try:
            parts = coord_str.strip().split(',')
            if len(parts) != 2:
                return None
            x, y = int(parts[0]), int(parts[1])
            return (x, y)
        except (ValueError, IndexError):
            return None
