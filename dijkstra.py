import sys

def dijkstra(graph, start):
    # Initialize distances and visited nodes
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited = set()
    
    while len(visited) < len(graph):
        # Find the unvisited node with the smallest distance
        current_node = min(set(distances.keys()) - visited, key=distances.get)
        
        # Update the distances of neighbors of the current node
        for neighbor, distance in graph[current_node].items():
            new_distance = distances[current_node] + distance
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                
    # Mark the current node as visited
    visited.add(current_node)
    return distances
