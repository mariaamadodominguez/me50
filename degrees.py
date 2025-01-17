import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # If source and target are the same, returns an empty list 
    if source == target:
        return []

    # Keep track of number of states explored
    num_explored = 0

    # Initialize frontier to just the starting position
    start = Node(state=source, parent=None, action=None)
    goal = Node(state=target, parent=None, action=None)    
    frontier = QueueFrontier()    
    
    # print(
    #    f"***start:{start.state}[{people[start.state]["name"]}] and goal:{goal.state}[{people[goal.state]["name"]}]***")    
    
    frontier.add(start)

    # Initialize an empty explored set
    explored = set()
    
    # Keep looping until solution found
    while True:

        # If nothing left in frontier, then no path
        if frontier.empty():
            return None

        # Choose a node from the frontier
        node = frontier.remove()
        num_explored += 1            
        # print(f"node state {node.state} [{people[node.state]["name"]}] - action {node.action}")    
        
        # Mark node as explored
        explored.add(node.state)
            
        # Add neighbors to frontier
        node_name = people[node.state]["name"]  
        # print(
        #    f"people starring with {node_name} in movies {people[node.state]["movies"]} ")              
            
        for movie, person in neighbors_for_person(node.state):
                
            person_name = people[person]["name"]
            movie_title = movies[movie]["title"]
            # if person != node.state:
            # print(f"movie {movie_title} : person  {person_name}")                                     

            if not frontier.contains_state(person) and person not in explored:
                child = Node(state=person, parent=node, action=movie)                    
                frontier.add(child)
                # print(
                #    f"### {movies[child.action]["title"]} - {people[child.state]["name"]}")

                if child.state == goal.state:
                    # If node is the goal, then we have a solution
                    path = []
                    node = child
                    while node.parent is not None:
                        # print(f"[action {node.action} parent.state {node.parent.state}, state {node.state}]")    
                        # path.append([node.action, node.state])
                        path.append((node.action, node.state))
                        
                        node = node.parent
                    path.reverse()
                    # print(f"path {path}")
                    return path            
                
        # print(f"-----------------{num_explored}: {explored}---")
    # 
    return None


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
