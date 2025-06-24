from astar import run_astar
from blindsearch import BlindSearch

def main_menu():
    print("\nDLSU EATERY PATHFINDER")
    print("-" * 30)
    print("1 - Use Uniform Cost Search (UCS)")
    print("2 - Use A* Search")
    print("3 - Exit")
    return input("Choose an option: ").strip()

if __name__ == "__main__":
    while True:
        choice = main_menu()

        if choice == "1":
            BlindSearch().run()
        elif choice == "2":
            run_astar()
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")
