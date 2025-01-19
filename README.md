# Degrees
A program that determines how many “degrees of separation” apart two actors are.  
Implementation of the shortest_path function such that returns the shortest path from the person with id source to the person with the id target.  
**States** are people, **actions** are movies, which take from one actor to another.  
The initial state and goal state are defined by the two people we’re trying to connect.  
By using breadth-first search, find the shortest path from one actor to another. 

## Implementation 

The shortest_path function should return the shortest path from the person with id source to the person with the id target.

- Assuming there is a path from the source to the target, the function should return a list, where each list item is the next (movie_id, person_id) pair in the path from the source to the target. Each pair should be a tuple of two strings.
- If there are multiple paths of minimum length from the source to the target, the function can return any of them.
- If there is no possible path between two actors, the function should return None.
- Call the neighbors_for_person function, which accepts a person’s id as input, and returns a set of (movie_id, person_id) pairs for all people who starred in a movie with a given person.
