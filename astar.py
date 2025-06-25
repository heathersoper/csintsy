import heapq
import string

class Node:
    def __init__(self, position, parent, g, h):
        self.cell_position = position
        self.parent_cell = parent                   # the cell that it visited before the current cell
        self.eateries_data = []                     
        self.g = g
        self.h = h
        self.f = g + h
        
    def __lt__(self, other):                        # less than method - compares f values for priority queue
        return self.f < other.f
    
    def __eq__(self, other):                        # equal method - compares cell positions to determine if it is the same cell
        return self.cell_position == other.cell_position
    
    def __hash__(self):                             # hash method - if equal according to __eq__, then hash should be equal
        return hash(self.cell_position)
        
class Eatery:
    def __init__(self, name: str, row: int, col: int, cuisine: str):
        self.name = name
        self.row = row
        self.col = col
        self.cuisine = cuisine
        
    def __repr__(self):                             # repr method - string representation of the object
        return f"{self.name}: {self.row}, {self.col}"

class Pathfinder:                                   # class for the pathfinder which uses the A* search algorithm
    def __init__(self):
        self.no_of_rows = 10
        self.no_of_cols = 20
    
        self.grid = self.initialize_grid()
        self.eateries = {}
        self.initialize_dlsu_eateries()         
    
    def initialize_grid(self):                      # 0 - walkable, 1 - blocked, 2 - eatery
        grid = [
            #0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0], # row 0
            [0, 0, 0, 2, 2, 1, 1, 1, 1, 1, 2, 0, 1, 2, 2, 0, 1, 2, 1, 2], # row 1
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # row 2
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1], # row 3
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1], # row 4
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1], # row 5
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # row 6
            [1, 1, 1, 2, 2, 2, 0, 2, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0, 2, 2], # row 7
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0], # row 8
            [1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0]  # row 9
        ]
        
        return grid
        
    def initialize_dlsu_eateries(self):
        self.eateries_data = [ 
            # Name, Row, Col, Cuisine
            ("University Mall", 7, 19, "Fast Food"),
            ("McDonald's", 7, 18, "Fast Food"),
            ("Perico's", 8, 17, "Filipino"),
            ("Bloemen Hall", 9, 11, "Fast Food, Filipino, Japanese"),
            ("W.H. Taft Residence", 7, 10, "American"),
            ("EGI Taft", 7, 9, "Chinese, Korean, Vietnamese"),
            ("Castro St.", 7, 7, "American, Fast Food"),
            ("Agno Food Court", 9, 7, "Chinese, Filipino, Italian"),
            ("One Archers'", 7, 5, "Filipino, Japanese, Korean"),
            ("La Casita (Br. Andrew Gonzalez Hall)", 7, 4, "Filipino"),
            ("La Casita (Enrique Razon Sports Center)", 9, 4, "Filipino"),
            ("Green Mall", 7, 3, "American, Fast Food"),
            ("Green Court", 9, 5, "Fast Food"),
            ("Sherwood", 1, 3, "Chinese, Korean, Middle Eastern"),
            ("Jollibee", 1, 4, "Fast Food"),
            ("Dagonoy St.", 1, 10, "Filipino"),
            ("Burgundy", 1, 13, "American"),
            ("Estrada St.", 1, 14, "Filipino, Mexican"),
            ("D'Student's Place", 1, 17, "American, Korean"),
            ("Leon Guinto St.", 0, 13, "Filipino, Korean"),
            ("P. Ocampo St.", 1, 19, "Filipino, Japanese"),
            ("Fidel A. Reyes St.", 8, 1, "Filipino")
        ]
        
        letters = string.ascii_uppercase
        for i, (name, row, col, cuisine) in enumerate(self.eateries_data):
            eatery = Eatery(name, row, col, cuisine)
            letter_key = letters[i] if i < len(letters) else f"{letters[i//26-1]}{letters[i%26]}"
            self.eateries[letter_key] = eatery
            # self.grid[row][col] = 2      
    
    def is_valid(self, row, col):                   # checks if the coordinates are within the grid
        return (row >= 0) and (row < self.no_of_rows) and (col >= 0) and (col < self.no_of_cols)
    
    def is_walkable(self, row, col):                
        return self.grid[row][col] == 0 or self.grid[row][col] == 2
    
    def is_destination(self, row, col, dest):             # where dest[0] is the x-coordinate and dest[1] is the y-coordinate
        return row == dest[0] and col == dest[1]
    
    def calculate_heuristic(self, x, y):                  # uses manhattan distance for the heuristic value
        return abs(x[0] - y[0]) + abs(x[1] - y[1])      
    
    def get_neighbors(self, position):
        row, col = position
        neighbors = []
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for x, y in directions:
            new_row, new_col = row + x, col + y
            if self.is_valid(new_row, new_col) and self.is_walkable(new_row, new_col):
                neighbors.append((new_row, new_col))
                
        return neighbors
    
    def trace_path(self, node):
        path = []
        current = node
        while current:
            path.append(current.cell_position)
            current = current.parent_cell
        return path[::-1]                           # reverses the path to get the start -> goal path
    
    def astar_search(self, start, goal):
        discovered_nodes = []
        visited_nodes = set()
        g_cost = {}  
        
        start_node = Node(start, None, 0, self.calculate_heuristic(start, goal))
        heapq.heappush(discovered_nodes, start_node)
        g_cost[start] = 0                                                       # cumulative cost (actual cost)  
        
        while discovered_nodes:
            current_node = heapq.heappop(discovered_nodes)                     
            
            if current_node.cell_position in visited_nodes:
                continue
            
            visited_nodes.add(current_node.cell_position)
            
            if self.is_destination(current_node.cell_position[0], current_node.cell_position[1], goal):
                return self.trace_path(current_node), current_node.g            # returns both the path and the total cost (current value of g_cost)
            
            for neighbor_pos in self.get_neighbors(current_node.cell_position):
                if neighbor_pos in visited_nodes:
                    continue
                
                tentative_g = current_node.g + 1
                
                if neighbor_pos not in g_cost or tentative_g < g_cost[neighbor_pos]:
                    g_cost[neighbor_pos] = tentative_g
                    h_cost = self.calculate_heuristic(neighbor_pos, goal)
                    neighbor_node = Node(neighbor_pos, current_node, tentative_g, h_cost)
                    heapq.heappush(discovered_nodes, neighbor_node)
        
        return None
        
    def input_eatery(self, input_str):
        input_str = input_str.strip().upper()
        
        if input_str in self.eateries:
            return self.eateries[input_str]
        
        for key, eatery in self.eateries.items():
            if input_str.lower() in eatery.name.lower():
                return eatery
            
        return None
    
    def list_eateries(self):
        print("\nList of Eateries:")
        print("-" * 60)
            
        # Get only letter keys (exclude name duplicates)
        letter_keys = {k: v for k, v in self.eateries.items() if len(k) <= 2 and k.isalpha()}
            
        for letter, eatery in sorted(letter_keys.items()):
            print(f"{letter.upper()} - {eatery}")
            
    def print_path_on_grid(self, path, start, goal):
        # creates a copy of the grid for display
        display_grid = [row[:] for row in self.grid]
        
        for i, (row, col) in enumerate(path):
            if (row, col) == start:
                display_grid[row][col] = 'S'  # start node
            elif (row, col) == goal:
                display_grid[row][col] = 'G'  # goal node
            else:
                display_grid[row][col] = '*'  # path taken
        
        print("\nGrid with path:")
        print("S = Start, G = Goal, * = Path, 0 = Walkable, 1 = Blocked, 2 = Eatery")
        print("-" * 60)
        
        for i, row in enumerate(display_grid):
            print(f"Row {i:2d}: ", end="")
            for cell in row:
                print(f"{str(cell):>2}", end=" ")
            print()
        
    def find_eatery(self):
        while True:
            try:
                print("\nEnter your starting position")
                start_row = int(input("Row (0 - 9): "))
                start_col = int(input("Column (0 - 19): "))
                
                if not self.is_valid(start_row, start_col):
                    print("Error: Starting position out of bounds! Try again.")
                    continue
                
                if not self.is_walkable(start_row, start_col):
                    print("Error: Starting position is blocked! Try again.")
                    continue
                
                break
            
            except ValueError:
                print("Error: Invalid number! Try again.")
                continue
                
        start = (start_row, start_col)
        
        while True:
            print("\nSelect destination eatery:")
            self.list_eateries()
            eatery_input = input("\nEnter eatery letter or name: ")
            
            destination_eatery = self.input_eatery(eatery_input)
            if destination_eatery:
                break
            else:
                print("Error: Eatery not found! Try again.")
                
        goal = (destination_eatery.row, destination_eatery.col)
        print(f"\nFinding path from {start} to {destination_eatery.name} at {goal}...")
        
        result = self.astar_search(start, goal)
        
        if result:
            path, total_cost = result
            print(f"\nPath found! Length: {len(path)} steps")
            print("Path:", " -> ".join([f"({r},{c})" for r, c in path]))
            print(f"Total cost: {total_cost}")
            self.print_path_on_grid(path, start, goal)
        else:
            print("No path found!")
                
    def print_grid(self):
        print("\nCurrent Grid:")
        print("0 = Walkable, 1 = Blocked, 2 = Eatery")
        print("-" * 60)
        for i, row in enumerate(self.grid):
            print(f"Row {i:2d}: ", end="")
            for cell in row:
                print(f"{cell:>2}", end=" ")
            print()

    def add_new_eatery(self):
        print("\nAdd New Eatery")
        print("-" * 30)

        name = input("Enter eatery name: ").strip()
        cuisine = input("Enter cuisine type(s): ").strip()

        try:
            row = int(input("Enter row (0–9): "))
            col = int(input("Enter column (0–19): "))
        except ValueError:
            print("Error: Row and column must be numbers.")
            return

        if not self.is_valid(row, col):
            print("Error: Coordinates out of grid bounds.")
            return
        
        if self.grid[row][col] == 1:
            print("Error: Cannot place eatery on a blocked cell (1).")
            return

        # Mark cell as eatery
        self.grid[row][col] = 2

        # Automatically appoint a letter to the new eatery
        existing_keys = set(self.eateries.keys())
        next_letter = None

        for letter in string.ascii_uppercase:
            if letter not in existing_keys:
                next_letter = letter
                break

        # If all single letters are taken, try AA–ZZ
        if next_letter is None:
            for first in string.ascii_uppercase:
                for second in string.ascii_uppercase:
                    combo = first + second
                    if combo not in existing_keys:
                        next_letter = combo
                        break
                if next_letter:
                    break

        if next_letter is None:
            print("Error: All letter keys from A to ZZ are used up.")
            return
        
        new_eatery = Eatery(name, row, col, cuisine)
        self.eateries[next_letter] = new_eatery
        self.eateries_data.append((name, row, col, cuisine))

        print(f"Successfully added {name} at ({row}, {col}) as {next_letter}.")

    def remove_eatery(self):
        print("\nRemove Eatery")
        print("-" * 30)
        
        if not self.eateries:
            print("No eateries available to remove.")
            return

        self.list_eateries()
        eatery_input = input("\nEnter the letter key or name of the eatery to remove: ").strip()

        target_key = None
        target_eatery = None

        # Check if eatery exist by for key input
        if eatery_input.upper() in self.eateries:
            target_key = eatery_input.upper()
            target_eatery = self.eateries[target_key]
        else:
            # Else check if eatery exist for name input
            for key, eatery in self.eateries.items():
                if eatery_input.lower() in eatery.name.lower():
                    target_key = key
                    target_eatery = eatery
                    break

        if not target_eatery:
            print("Error: Eatery not found!")
            return

        # Confirm deletion
        confirm = input(f"Are you sure you want to remove '{target_eatery.name}' at ({target_eatery.row}, {target_eatery.col})? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            return

        # Remove from grid
        self.grid[target_eatery.row][target_eatery.col] = 0

        # Remove from dictionary
        del self.eateries[target_key]

        # Remove from eateries_data
        self.eateries_data = [
            data for data in self.eateries_data
            if not (data[0] == target_eatery.name and data[1] == target_eatery.row and data[2] == target_eatery.col)
        ]

        print(f"'{target_eatery.name}' has been removed successfully.")

def print_menu():
    print("-" * 15)
    print("1 - Eatery pathfinder")
    print("2 - Show grid")
    print("3 - List all eateries")
    print("4 - Add new eatery")
    print("5 - Remove eatery")
    print("6 - Back")
    print("7 - Exit")
    print("-" * 15)
    
    choice = input("\nEnter a number from 1-7: ").strip()
    
    return choice

#if __name__ == "__main__":
def run_astar():
    print("-" * 50)
    print("DLSU EATERY PATHFINDER (A* SEARCH ALGORITHM)")
    print("-" * 50)
    
    pathfinder = Pathfinder()
    
    while True:
        user_choice = print_menu()
        
        if user_choice == "1":
            pathfinder.find_eatery()
        elif user_choice == "2":
            pathfinder.print_grid()
        elif user_choice == "3":
            pathfinder.list_eateries()
        elif user_choice == "4":
            pathfinder.add_new_eatery()
        elif user_choice == "5":
            pathfinder.remove_eatery()
        elif user_choice == "6":
            print("Returning to main menu...")
            break
        else:
            print("Invalid choice! Please enter a number from 1-7.")
