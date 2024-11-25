def dfs_recursive(graph, vertex, visited, component):
    visited.add(vertex)
    component.append(vertex)
    
    for neighbor in graph[vertex]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited, component)

def find_connected_components_recursive(graph):
    visited = set()
    components = []

    for vertex in graph:
        if vertex not in visited:
            component = []
            dfs_recursive(graph, vertex, visited, component)
            components.append(component)

    return components

def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    component = []

    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            component.append(vertex)
            stack.extend(neighbor for neighbor in graph[vertex] if neighbor not in visited)
    
    return component

def find_connected_components_iterative(graph):
    visited = set()
    components = []

    for vertex in graph:
        if vertex not in visited:
            component = dfs_iterative(graph, vertex)
            components.append(component)
            visited.update(component)

    return components

graph = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1],
    3: [4],
    4: [3],
    5: []
}

components_recursive = find_connected_components_recursive(graph)
print("Компоненты связности (рекурсивно):", components_recursive)

components_iterative = find_connected_components_iterative(graph)
print("Компоненты связности (нерекурсивно):", components_iterative)
