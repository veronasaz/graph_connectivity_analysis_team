def add_edge(graph, u, v):
    if u in graph:
        graph[u].append(v)
    else:
        graph[u] = [v]

def fill_order(v, graph, visited, stack):
    visited[v] = True
    if v in graph:
        for i in graph[v]:
            if i not in visited or not visited[i]:
                fill_order(i, graph, visited, stack)
    stack.append(v)

def transpose(graph):
    transposed_graph = {}
    for i in graph:
        if i in graph:
            for j in graph[i]:
                if j in transposed_graph:
                    transposed_graph[j].append(i)
                else:
                    transposed_graph[j] = [i]
    return transposed_graph

def dfs(v, graph, visited, result):
    visited[v] = True
    result.append(v)
    if v in graph:
        for i in graph[v]:
            if i not in visited or not visited[i]:
                dfs(i, graph, visited, result)

def kosaraju(graph):
    stack = []
    visited = {}
    
    for node in graph:
        visited[node] = False

    for node in graph:
        if not visited[node]:
            fill_order(node, graph, visited, stack)

    transposed_graph = transpose(graph)
    for node in graph:
        visited[node] = False
    
    strongly_connected_components = []

    while stack:
        node = stack.pop()
        if not visited[node]:
            component = []
            dfs(node, transposed_graph, visited, component)
            strongly_connected_components.append(component)

    return strongly_connected_components

graph_dict = {0: [1, 2], 1: [2], 2: [0, 1], 3: [4], 4: [3, 5], 6: [7], 7: [6]}

components = kosaraju(graph_dict)
print("Компоненти сильної зв'язності:")
print(components)
