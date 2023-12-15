# Purpose: Strong connectivity components

def strong_connectivity(graph: dict) -> list:
    '''
    Finds the components of the strong connectivity
    of an oriented graph and returns a list of them.
    >>> strong_connectivity({0: [1], 1: [2], 2: [0]})
    'Graph contains 1 strong connectivity component: [{0: [1], 1: [2], 2: [0]}]'
    >>> strong_connectivity({0: [1], 1: [2], 2: [0, 3], 3: [4], 4: [5], 5: [3]})
    'Graph contains 2 strong connectivity components: [{0: [1], 1: [2], 2: [0, 3], 3: [4], 4: [5], 5: [3]}, {6: [7], 7: [6]}]'
    '''
    def fill_order(v, graph, visited, stack):
        visited[v] = True
        if v in graph:
            for i in graph[v]:
                if i not in visited or not visited[i]:
                    fill_order(i, graph, visited, stack)
        stack.append(v)

    def dfs(v, graph, visited, result):
        visited[v] = True
        result.append(v)
        if v in graph:
            for i in graph[v]:
                if i not in visited or not visited[i]:
                    dfs(i, graph, visited, result)

    stack = []
    visited = {}
    
    for node in graph:
        visited[node] = False

    for node in graph:
        if not visited[node]:
            fill_order(node, graph, visited, stack)

    transposed_graph = {j: [i for i in graph if j in graph[i]] for j in graph}
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

components = strong_connectivity(graph_dict)
print("Компоненти сильної зв'язності:")
print(components)
