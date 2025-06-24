import heapq
from typing import Dict, List, Tuple

# Define type aliases for clarity
Path = List[str]
Graph = Dict[str, List[Tuple[str, int]]]

GRAPH_UCS = {
    'A': [('B', 33)],
    'B': [('A', 33), ('C', 57)],
    'C': [('B', 57), ('D', 350)],
    'D': [('C', 350), ('E', 140)],
    'E': [('D', 140), ('F', 27)],
    'F': [('E', 27), ('G', 130)],
    'G': [('F', 130), ('H', 26), ('I', 16)],
    'H': [('G', 26), ('J1', 98), ('J2', 110), ('L', 81)],
    'I': [('G', 16), ('J1', 8)],
    'J1': [('I', 8), ('H', 160), ('K', 12)],
    'J2': [('H', 110), ('L', 45)],
    'K': [('J1', 12), ('U', 47)],
    'L': [('H', 81), ('J2', 45), ('M', 250), ('N', 190)],
    'M': [('L', 250), ('N', 57)],
    'N': [('M', 57), ('O', 210)],
    'O': [('N', 210), ('P', 250)],
    'P': [('O', 250), ('Q', 100)],
    'Q': [('P', 100), ('R', 24)],
    'R': [('Q', 24), ('S', 80)],
    'S': [('R', 80), ('T', 300)],
    'T': [('S', 300)],
    'U': [('K', 47)],
}

def add_node(graph: Graph, name: str):
    if name in graph:
        print(f"Node '{name}' already exists.")
        return
    graph[name] = []
    print(f"Node '{name}' added.")

def add_edge(graph: Graph, from_node: str, to_node: str, cost: int):
    if from_node not in graph or to_node not in graph:
        print("Both nodes must exist to add an edge.")
        return
    graph[from_node].append((to_node, cost))
    graph[to_node].append((from_node, cost))  # Because it's undirected

def remove_node(graph: Graph, name: str):
    if name not in graph:
        print(f"Node '{name}' doesn't exist.")
        return
    del graph[name]
    for node in graph:
        graph[node] = [edge for edge in graph[node] if edge[0] != name]
    print(f"Node '{name}' removed.")


def uniform_cost_search(graph: Graph, start: str, goal: str) -> Tuple[Path | None, int, int]:
    """
    Uniform Cost Search algorithm.

    Returns:
        - optimal path (list of node names) or None if no path
        - number of nodes expanded
        - total cost (sum of edge distances in meters)
    """
    
    # Priority queue of (total_cost, path)
    frontier = [(0, [start])]
    explored = set()
    nodes_expanded = 0

    while frontier:
        cost, path = heapq.heappop(frontier)
        current = path[-1]

        if current == goal:
            return path, nodes_expanded, cost

        if current in explored:
            continue

        explored.add(current)
        nodes_expanded += 1

        for neighbor, edge_cost in graph.get(current, []):
            if neighbor not in explored:
                new_path = path + [neighbor]
                heapq.heappush(frontier, (cost + edge_cost, new_path))

    return None, nodes_expanded, 0

def main():
    graph = GRAPH_UCS.copy()  # Work on a copy so original remains safe

    while True:
        print("\n========================")
        print("     Available Nodes")
        print("========================")
        print(", ".join(sorted(graph.keys())))

        print("\n========================")
        print("        Main Menu")
        print("========================")
        print(" 1. Run Uniform Cost Search")
        print(" 2. Add new eatery (node)")
        print(" 3. Remove existing eatery")
        print(" 4. Add edge (connect eateries)")
        print(" 5. Exit")

        choice = input("\nEnter your choice (1–5): ").strip()


        if choice == '1':
            start = input("Enter start node: ").strip()
            goal = input("Enter goal node: ").strip()

            if start not in graph or goal not in graph:
                print("Invalid start or goal.")
                continue

            path, expanded, cost = uniform_cost_search(graph, start, goal)
            if path:
                print("\n========== Search Result ==========")
                print("Shortest path      :", " → ".join(path))
                print("Nodes expanded     :", expanded)
                print("Total distance     :", cost, "meters")
                print("===================================\n")

            else:
                print("No path found.")

        elif choice == '2':
            new_node = input("Enter new node name (e.g., V): ").strip()
            add_node(graph, new_node)

        elif choice == '3':
            node_to_remove = input("Enter node to remove: ").strip()
            remove_node(graph, node_to_remove)

        elif choice == '4':
            from_node = input("From node: ").strip()
            to_node = input("To node: ").strip()
            try:
                cost = int(input("Distance between them (in meters): ").strip())
            except ValueError:
                print("Distance must be a number.")
                continue
            add_edge(graph, from_node, to_node, cost)

        elif choice == '5':
            print("Exiting.")
            break

        else:
            print("Invalid option.")
            
if __name__ == "__main__":
    main()

