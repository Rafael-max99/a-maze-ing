*This project has been created as part of the 42 curriculum by rlaurean [, davimar3].*

# A-Maze-ing

## Description

A-Maze-ing is a maze generation project developed in Python. The objective is to generate valid mazes from a configuration file, display them visually in the terminal, and export their structure in a format suitable for automated validation.

The project is based on graph theory concepts, where each cell of the maze is represented as a node and the passages between cells are represented as edges. A perfect maze is generated using the Recursive Backtracker algorithm, which produces a spanning tree over the grid and guarantees a unique path between any two reachable cells.

The program supports:

* Random maze generation with optional seed-based reproducibility.
* Perfect and non-perfect maze generation.
* Terminal visualization using ASCII characters.
* Configurable wall colors.
* Entry and exit points defined in a configuration file.
* Display of the shortest path between the entry and the exit.
* Automatic insertion of the required "42" pattern when the maze dimensions allow it.

The codebase has been organized to separate maze generation, rendering, parsing, and interaction logic, allowing the generation module to be reused independently of the user interface.

---

## Instructions

### Requirements

* Python 3.10 or later

### Installation

Clone the repository and enter the project directory:

```bash
git clone <repository_url>
cd a-maze-ing
```

Install any required dependencies:

```bash
make install
```

### Running the Program

The program must be executed with a configuration file:

```bash
python3 a_maze_ing.py config.txt
```

Example:

```bash
python3 a_maze_ing.py default_config.txt
```

### Configuration File

The configuration file uses one `KEY=VALUE` pair per line.

Example:

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

### Interactive Controls

Once the maze is displayed, the following options are available:

1. Generate a new maze.
2. Show or hide the shortest path between the entry and exit.
3. Change wall colors.
4. Quit the application.

---

## Resources

### Maze Generation

* Jamis Buck, *Mazes for Programmers*.
* Jamis Buck's maze generation articles: https://weblog.jamisbuck.org
* Recursive Backtracker algorithm documentation.
* Depth-First Search (DFS) traversal algorithms.
* Spanning Tree concepts from graph theory.

### Python Documentation

* Python Official Documentation: https://docs.python.org/3/
* Python `random` module documentation.
* Python type hints and `mypy` documentation.

### Additional References

* VisuAlgo Graph Traversal Visualizations: https://visualgo.net
* GeeksforGeeks articles on graph traversal and spanning trees.

### Use of AI

Artificial Intelligence tools were used as learning aids and technical references throughout the project.

AI assistance was primarily used for:

* Understanding graph theory concepts related to maze generation.
* Studying spanning trees and the Recursive Backtracker algorithm.
* Translating algorithm examples originally written in Ruby into Python.
* Clarifying Python language features, including generators, special methods (`__getitem__`, `__str__`), type hints, and object-oriented design.
* Reviewing implementation ideas and discussing alternative approaches.
* Assisting with documentation structure and project presentation.

All generated code, architectural decisions, and final implementations were reviewed, adapted, tested, and integrated manually. AI-generated content was used only when fully understood and validated.

## Config File

We decided to use the Config file with the configuration proposed by the subject:

contain one ‘KEY=VALUE‘ pair per line

We also only made use of the Mandatory keys:

* Width - A number containing the amount of columns on the grid
* Height - A number containing the amount of rows in the grid
* Entry - The coordinates for the start point in the maze
* Exit - The coordinates for the exit point in the maze
* Output_file - The name of the file to be used for placing the output values
* Perfect - A boolean who tells us of the maze is perfcet, as having one path between the entry and the exit

## Algorithm

### Name

For the maze gennerator algorith we chose to use the Recursive BackTracker 

### Reasons

* It is simple to understand and implement
* It is good for those learning to create mazes, without any experience
* It was one of the algorith recommended in the book Mazes for Programmers

### Logic

Recieve a grid of closed off cells
Create a list to save the history of each visited cell we visit
Choose a specif or random cell to start, doesn't matter which
Add the cell to the visited list
Create a loop that takes the last member of the list
Check all neighbor cells of our current cell, creating a list with the unvisited ones
Randomly choose a neighbor to be the next visited, and continue on the loop until all cells are visited

## Reusable

