'''Graph'''

import copy

def read_csv(file_name: str) -> dict:
    '''
    Reads graph from csv file returns a dictionary.
    >>> import tempfile
    >>> with tempfile.NamedTemporaryFile(mode = 'w', delete=False, encoding = 'UTF-8') as tempfile:
    ...     _ = tempfile.write('0,1\\n0,2\\n1,0\\n1,2\\n2,0\\n2,1\\n3,4\\n4,3')
    >>> read_csv(tempfile.name)
    {0: [1, 2], 1: [0, 2], 2: [0, 1], 3: [4], 4: [3]}
    '''
    graph = {}
    with open(file_name, 'r', encoding = 'UTF-8') as file:
        for line in file:
            line = line.strip().split(',')
            if int(line[0]) not in graph:
                graph[int(line[0])] = [int(line[1])]
            else:
                graph[int(line[0])].append(int(line[1]))
    return graph

def write_csv(graph: dict, file_name: str) -> None:
    '''
    Writes graph to csv file.
    >>> import tempfile
    >>> write_csv({0: [1, 2], 1: [0, 2], 2: [0, 1], 3: [4], 4: [3]}, 'temp.csv')
    >>> with open('temp.csv', 'r', encoding = 'UTF-8') as file:
    ...     file.read()
    '0,1\\n0,2\\n1,0\\n1,2\\n2,0\\n2,1\\n3,4\\n4,3\\n'
    '''
    with open(file_name, 'w', encoding = 'UTF-8') as file:
        for vertex in graph:
            for neighbor in graph[vertex]:
                file.write(f'{vertex},{neighbor}\n')

def components_of_connectivity(graph: dict) -> list:
    '''
    Finds the connectivity components of an unoriented graph and returns a list of them.
    >>> components_of_connectivity({0: [1, 2], 1: [0, 2], 2: [0, 1], 3: [4], 4: [3]})
    'Graph contains 2 connectivity component(s): [{0: [1, 2], 1: [0, 2], 2: [0, 1]}, {3: [4], 4: [3]}]'
    >>> components_of_connectivity({0: [1, 2, 4], 1: [0, 2, 3], 2: [0, 1, 3], 3: [1, 2, 4], 4: [0, 3]})
    'Graph contains 1 connectivity component(s): \
[{0: [1, 2, 4], 1: [0, 2, 3], 2: [0, 1, 3], 3: [1, 2, 4], 4: [0, 3]}]'
    '''
    def dfs(node, visited, component):
        visited[node] = True
        component[node] = graph[node]

        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor, visited, component)

    visited = {node: False for node in graph}
    connectivity_components = []

    for node in graph:
        if not visited[node]:
            component = {}
            dfs(node, visited, component)
            connectivity_components.append(component)

    num = len(connectivity_components)
    if num > 0:
        return f'Graph contains {num} connectivity component(s): {connectivity_components}'
    return 'Graph doesn`t contains any connectivity component.'

def strong_connectivity(graph: dict) -> list:
    '''
    Finds the components of the strong connectivity
    of an oriented graph and returns a list of them.
    >>> strong_connectivity({0: [1], 1: [2], 2: [0]})
    'Graph contains 1 strong connectivity component(s): [[0, 2, 1]]'
    >>> strong_connectivity({0: [1], 1: [2], 2: [0, 3], 3: [4], 4: [5], 5: [3]})
    'Graph contains 2 strong connectivity component(s): [[0, 2, 1], [3, 5, 4]]'
    >>> strong_connectivity({0: [1, 2], 1: [2], 2: [0, 1], 3: [4], 4: [3, 5], 6: [7], 7: [6]})
    'Graph contains 3 strong connectivity component(s): [[0, 2, 1], [3, 4], [6, 7]]'
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
    result_components = sorted(strongly_connected_components, key=lambda component: component[0])
    num = len(result_components)
    if num > 0:
        return f'Graph contains {num} strong connectivity component(s): {result_components}'
    return 'Graph doesn`t contain any strong connectivity components.'

def connection_points(graph: dict) -> list:
    '''
    Finds the connection points of an unoriented graph and returns a list of them.
    >>> connection_points({0: [1], 1: [0, 2], 2: [1, 3, 4], 3: [2], \
4: [2, 5, 6, 7], 5: [4, 6], 6: [4, 5], 7: [4, 8], 8: [7]})
    'There is a list of connection points of the graph: [1, 2, 4, 7]'
    '''
    def dfs(vertex, parent, visited, disc, low, time, ap):
        children = 0
        visited[vertex] = True
        disc[vertex] = low[vertex] = time[0]
        time[0] += 1

        for adj_vertex in graph[vertex]:
            if not visited[adj_vertex]:
                children += 1
                dfs(adj_vertex, vertex, visited, disc, low, time, ap)
                low[vertex] = min(low[vertex], low[adj_vertex])

                if parent is None and children > 1:
                    ap.add(vertex)
                elif parent is not None and low[adj_vertex] >= disc[vertex]:
                    ap.add(vertex)
            elif adj_vertex != parent:
                low[vertex] = min(low[vertex], disc[adj_vertex])

    visited = {v: False for v in graph}
    disc = {v: float('inf') for v in graph}
    low = {v: float('inf') for v in graph}
    ap = set()
    time = [0]

    for vertex in graph:
        if not visited[vertex]:
            dfs(vertex, None, visited, disc, low, time, ap)
    return (f'There is a list of connection points of the graph: {sorted(list(ap))}')

def bridges(graph: dict) -> list:
    '''
    Finds the bridges of an unoriented graph and returns a list of them.
    >>> bridges({0: [1], 1: [0, 2], 2: [1, 3, 4], 3: [2], \
4: [2, 5, 6, 7], 5: [4, 6], 6: [4, 5], 7: [4, 8], 8: [7]})
    There is a list of bridges of the graph:
    [(0, 1), (1, 2), (2, 3), (2, 4), (4, 7), (7, 8)]
    >>> bridges({1: [5, 2], 2: [1, 4, 5], 4: [2, 6, 7], 5: [1, 2], 6: [4, 7], 7: [3, 4, 6], 3: [7]})
    There is a list of bridges of the graph:
    [(2, 4), (3, 7)]
    >>> bridges({1: [5, 2], 2: [1, 4, 5], 4: [2, 6, 7], 5: [1, 2], 6: [4, 7, 8], 7: [3, 4, 6], \
3: [7], 8:{6, 9, 10}, 9:{8, 10, 11}, 10:{8, 9}, 11:{9}})
    There is a list of bridges of the graph:
    [(2, 4), (3, 7), (6, 8), (9, 11)]
    '''
    graph_origin=copy.deepcopy(graph)
    edges = set()
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            edge = tuple(sorted([vertex, neighbor]))
            edges.add(edge)
    edges = list(edges)
    bridges_result=[]
    def is_connected(graph: dict) -> bool:
        '''
        Checks if a graph is connected.
        '''
        def dfs(node, visited):
            visited[node] = True

            for neighbor in graph[node]:
                if not visited[neighbor]:
                    dfs(neighbor, visited)

        visited = {node: False for node in graph}
        start_node = next(iter(graph))

        dfs(start_node, visited)

        return all(visited.values())

    for edge in edges:
        graph[edge[0]].remove(edge[1])
        graph[edge[1]].remove(edge[0])
        if not is_connected(graph):
            bridges_result.append(edge)
        graph = copy.deepcopy(graph_origin)
    
    if bridges_result:
        bridges_sorted = sorted(bridges_result, key=lambda bridge: bridge[0])
        bridges_sorted = sorted(bridges_result, key=lambda bridge: bridge[1])
        print('There is a list of bridges of the graph:')
        return bridges_sorted
    return 'There are no bridges in the graph.'

# def main():
#     '''
#     Main function to interact with program.
#     '''
#     file = input('Enter the file name: ')
#     graph = read_csv(file)
#     def is_oriented(graph: dict) -> bool:
#         '''
#         Checks if a graph is oriented.
#         '''
#         for vertex in graph:
#             for neighbor in graph[vertex]:
#                 if neighbor not in graph or vertex not in graph[neighbor]:
#                     return True
#         return False
    
#     if is_oriented(graph):
#         choice = input('Enter the number of the task you want to solve:\n\
#         1. Components of the strong connectivity of an oriented graph.\n')
#         if '1' in choice:
#             print(strong_connectivity(graph))
#     else:
#         choice = input('Enter the number of the task you want to solve:\n\
#         1. Components of the connectivity of an unoriented graph.\n\
#         2. Components of the strong connectivity of an oriented graph.\n\
#         3. Connection points of an unoriented graph.\n\
#         4. Bridges of an unoriented graph.\n')
#         if '1' in choice:
#             print(components_of_connectivity(graph))
#         if '2' in choice:
#             print(strong_connectivity(graph))
#         if '3' in choice:
#             print(connection_points(graph))
#         if '4' in choice:
#             print(bridges(graph))

# if __name__ == '__main__':
#     main()

if __name__ == '__main__':
    import doctest
    print(doctest.testmod(verbose=False))
