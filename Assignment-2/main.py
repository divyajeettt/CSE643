from geopy.distance import geodesic
from typing import Callable
import pandas as pd
import csv


def read_csv(filename: str) -> dict[str, dict[str, float]]:
    """
    Reads the given CSV and preprocesses it into an adjacency matrix.
    """

    with open(filename, "r") as file:
        reader = csv.reader(file)
        data = list(reader)

    df = pd.DataFrame(data[1:], columns=data[0], index=[data[1:][i][0] for i in range(len(data[1:]))])
    df.drop(columns=["Distance in Kilometres"], inplace=True)

    df_dict = df.to_dict()
    index_places = df.index.values.tolist()
    column_places = df.columns.values.tolist()
    all_places = sorted(set(index_places).union(set(column_places)))

    df = pd.DataFrame(columns=all_places, dtype=float)

    for i in range(len(all_places)):
        df.loc[all_places[i]] = float("inf")
    for i in range(len(all_places)):
        df.loc[all_places[i], all_places[i]] = 0

    for place_key in df_dict:
        for place_value in df_dict[place_key]:
            df.loc[place_key, place_value] = df_dict[place_key][place_value]
            df.loc[place_value, place_key] = df_dict[place_key][place_value]

    df_dict = df.to_dict()
    for place_key in df_dict:
        for place_value in df_dict[place_key]:
            df_dict[place_key][place_value] = float(df_dict[place_key][place_value])

    return df_dict


def H1(node: str, destination: str) -> float:
    """
    Defines the first heuristic function. This heuristic is admissible.
    """
    return geodesic(COORDINATES[node], COORDINATES[destination]).km


def H2(node: str, destination: str) -> float:
    """
    Defines the second heuristic function. This heuristic is not admissible.
    """
    return 5 * H1(node, destination)


def A_star(
        adj: dict[str, dict[str, float]], source: str, destination: str, heuristic: Callable[[str], float]
    ) -> tuple[list[str], float, int]:
    """
    Returns the shortest path between the source and destination using A* Search.
    :return: A tuple containing the path, its cost, and the number of nodes expanded.
    """

    cost = {source: 0}
    parent = {source: None}
    frontier = {source}
    expanded = set()
    expanded_count = 0

    while frontier:
        node = None
        for node_v in frontier:
            if node is None or cost[node_v] + heuristic(node_v) < cost[node] + heuristic(node):
                node = node_v

        if node is None:
            print("No path found!")
            return []

        if node == destination:
            path, cost = [], 0
            while node:
                path.append(node)
                cost += adj.get(parent[node], dict()).get(node, 0)
                node = parent[node]
            return path[::-1], cost, expanded_count

        for neighbour in adj[node]:
            if neighbour not in frontier and neighbour not in expanded:
                frontier.add(neighbour)
                parent[neighbour] = node
                cost[neighbour] = cost[node] + adj[node][neighbour]
            else:
                if cost[neighbour] > cost[node] + adj[node][neighbour]:
                    cost[neighbour] = cost[node] + adj[node][neighbour]
                    parent[neighbour] = node
                    if neighbour in expanded:
                        expanded.remove(neighbour)
                        frontier.add(neighbour)

        frontier.remove(node)
        expanded.add(node)
        expanded_count += 1

    print("No path found!")
    return [], float("inf"), 0


def load_coordinates() -> dict[str, tuple[float, float]]:
    """
    Loads the coordinates of all places from the given CSV.
    https://simplemaps.com/data/in-cities
    """

    with open("Locations.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)
        data = list(reader)

    coordinates = {}
    for row in data:
        coordinates[row[0]] = (float(row[1]), float(row[2]))
    return coordinates


def main() -> None:
    """__main__ function"""

    global COORDINATES

    ADJ = read_csv("Road_Distance.csv")
    PLACES = list(ADJ.keys())
    COORDINATES = load_coordinates()

    while True:
        print("Enter 1. to find the shortest path between two places")
        print("Enter 2. to view the list of all places")
        print("Enter 3. to exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            source = input("Enter the source: ")
            destination = input("Enter the destination: ")
            if source not in PLACES:
                print("Source not found! Try again.")
                continue

            if destination not in PLACES:
                print("Destination not found! Try again.")
                continue

            print(f"Shortest path between {source} and {destination} is:")

            ucs_path, ucs_cost, ucs_expanded = A_star(ADJ, source, destination, heuristic=lambda *_: 0)
            if not ucs_path:
                print("Path not Found by UCS!")
            else:
                print("UCS:", ucs_path)
                print("Cost:", ucs_cost)
                print("Nodes expanded:", ucs_expanded)

            h1_path, h1_cost, h1_expanded = A_star(ADJ, source, destination, heuristic=lambda node: H1(node, destination))
            if not h1_path:
                print("Path not Found by A* (admissible heuristic)!")
            else:
                print("A* (admissible heuristic):", h1_path)
                print("Cost:", h1_cost)
                print("Nodes expanded:", h1_expanded)

            h2_path, h2_cost, h2_expanded = A_star(ADJ, source, destination, heuristic=lambda node: H2(node, destination))
            if not h2_path:
                print("Path not Found by A* (unadmissible heuristic)!")
            else:
                print("A* (unadmissible heuristic):", h2_path)
                print("Cost:", h2_cost)
                print("Nodes expanded:", h2_expanded)

        elif choice == "2":
            print("List of all places:", PLACES, sep="\n")
        elif choice == "3":
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()