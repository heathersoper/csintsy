import heapq
import time
from typing import List, Tuple

# Constants
WALKABLE = 0
BLOCKED = 1
EATERY = 2

Grid = List[List[int]]
Position = Tuple[int, int]

class BlindSearch:
    def __init__(self):
        self.grid = self.initialize_grid()
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.landmarks = self.define_landmarks()

    def initialize_grid(self) -> Grid:
        return [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 2, 1, 1, 1, 1, 1, 2, 0, 1, 2, 2, 0, 1, 2, 1, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 2, 2, 2, 0, 2, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 2, 2],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
            [1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

    def define_landmarks(self):
        return {
            "University Mall": (7, 19),
            "McDonald's": (7, 18),
            "Perico's": (8, 17),
            "Bloemen Hall": (9, 11),
            "WH Taft Residence": (7, 10),
            "EGI Taft": (7, 9),
            "Castro Street": (7, 7),
            "Agno Food Court": (9, 7),
            "One Archer's": (7, 5),
            "La Casita 1": (7, 4),
            "La Casita 2": (9, 4),
            "Green Mall": (7, 3),
            "Green Court": (9, 5),
            "Sherwood": (1, 3),
            "Jollibee": (1, 4),
            "Dagonoy Street": (1, 10),
            "Burgundy": (1, 13),
            "Estrada Street": (1, 14),
            "D'Student's Place": (1, 17),
            "Leon Guinto Street": (0, 13),
            "P. Ocampo Street": (1, 19),
            "Fidel A. Reyes Street": (8, 1),
        }

    def is_valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y] != BLOCKED

    def uniform_cost_search(self, start: Position, goal: Position) -> Tuple[List[Position], int]:
        visited = set()
        queue = [(0, start, [start])]
        heapq.heapify(queue)
        nodes_expanded = 0

        while queue:
            cost, current, path = heapq.heappop(queue)
            if current in visited:
                continue
            visited.add(current)
            nodes_expanded += 1

            if current == goal:
                return path, nodes_expanded

            x, y = current
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if self.is_valid(nx, ny) and (nx, ny) not in visited:
                    heapq.heappush(queue, (cost + 1, (nx, ny), path + [(nx, ny)]))

        return [], nodes_expanded

    def print_grid_with_path(self, path: List[Position], start: Position, goal: Position):
        print("\nGrid View:")
        for i in range(self.rows):
            row = ""
            for j in range(self.cols):
                if (i, j) == start:
                    row += "S "
                elif (i, j) == goal:
                    row += "G "
                elif (i, j) in path:
                    row += "* "
                elif self.grid[i][j] == BLOCKED:
                    row += "X "
                elif self.grid[i][j] == EATERY:
                    row += "E "
                else:
                    row += ". "
            print(row)

    def print_path_summary(self, path: List[Position], start: Position, goal: Position, nodes_expanded: int):
        print("\nRunning Uniform Cost Search . . .")
        start_name = next((name for name, pos in self.landmarks.items() if pos == start), f"{start}")
        goal_name = next((name for name, pos in self.landmarks.items() if pos == goal), f"{goal}")

        print(f"From: {start_name} ➜ {goal_name}")
        print("------------------------------------")

        if not path:
            print("PATH NOT FOUND.")
            return

        readable_path = []
        for pos in path:
            name = next((label for label, location in self.landmarks.items() if location == pos), None)
            readable_path.append(name if name else f"{pos}")

        print("\nPATH FOUND!")
        print("Nodes Visited: " + " ➜ ".join(readable_path))
        print(f"Total Cost: {len(path) - 1}")
        print(f"Nodes Expanded: {nodes_expanded}")

    def show_landmark_menu(self):
        print("\nDLSU FOOD MAP:")
        for i, name in enumerate(self.landmarks.keys()):
            print(f"  [{i}] {name}")
        print()

    def get_landmark_by_index(self, index: int) -> Tuple[str, Position]:
        key = list(self.landmarks.keys())[index]
        return key, self.landmarks[key]

    def run(self):
        while True:
            print("\n========================")
            print("     Blind Search")
            print("========================")
            print(" 1. Run Uniform Cost Search")
            print(" 2. Add new eatery (node)")
            print(" 3. Remove existing eatery")
            print(" 4. Add edge (connect eateries)")
            print(" 5. Exit")

            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                if len(self.landmarks) < 1:
                    print("No landmarks available.")
                    continue

                self.show_landmark_menu()
                try:
                    sx = int(input("Enter START row (0-9): "))
                    sy = int(input("Enter START column (0-19): "))
                    goal_index = int(input("Choose GOAL eatery index: "))
                    goal_name, goal = self.get_landmark_by_index(goal_index)
                    start = (sx, sy)

                    if not (self.is_valid(*start) and self.is_valid(*goal)):
                        print("Invalid start or goal position. Must not be BLOCKED.")
                        continue

                    start_time = time.time()
                    path, nodes = self.uniform_cost_search(start, goal)
                    end_time = time.time()

                    self.print_path_summary(path, start, goal, nodes)
                    print(f"Time taken: {end_time - start_time:.4f}s")
                    self.print_grid_with_path(path, start, goal)
                except (ValueError, IndexError):
                    print("Invalid input. Please enter correct coordinates and valid eatery index.")

            elif choice == '2':
                try:
                    name = input("Enter new eatery name: ").strip()
                    x = int(input("Enter row (0-9): "))
                    y = int(input("Enter column (0-19): "))
                    if not (0 <= x < self.rows and 0 <= y < self.cols):
                        print("Invalid position.")
                    else:
                        self.grid[x][y] = EATERY
                        self.landmarks[name] = (x, y)
                        print(f"Added '{name}' at position ({x}, {y}) as an eatery.")
                except ValueError:
                    print("Invalid input.")

            elif choice == '3':
                self.show_landmark_menu()
                try:
                    index = int(input("Enter index of eatery to remove: "))
                    name = list(self.landmarks.keys())[index]
                    del self.landmarks[name]
                    print(f"Removed '{name}' from landmarks.")
                except (ValueError, IndexError):
                    print("Invalid selection.")

            elif choice == '4':
                try:
                    x = int(input("Enter row (0-9): "))
                    y = int(input("Enter column (0-19): "))
                    if self.grid[x][y] == BLOCKED:
                        self.grid[x][y] = WALKABLE
                        print(f"Tile at ({x}, {y}) is now walkable.")
                    else:
                        print("Tile is already walkable or special.")
                except ValueError:
                    print("Invalid input.")

            elif choice == '5':
                print("Returning to main menu...")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
