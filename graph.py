'''Graph'''

import copy

def read_csv(file_name: str):
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

def components_of_connectivity(graph: dict) -> list:
    '''
    Finds the connectivity components of an unoriented graph and returns a list of them.
    >>> components_of_connectivity({0: [1, 2], 1: [0, 2], 2: [0, 1], 3: [4], 4: [3]})
    'Graph contains 2 connectivity components: [{0: [1, 2], 1: [0, 2], 2: [0, 1]}, {3: [4], 4: [3]}]'
    >>> components_of_connectivity({0: [1, 2, 4], 1: [0, 2, 3], 2: [0, 1, 3], 3: [1, 2, 4], 4: [0, 3]})
    'Graph contains 1 connectivity component: \
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
    if num >=2:
        return f'Graph contains {num} connectivity components: {connectivity_components}'
    return f'Graph contains {num} connectivity component: {connectivity_components}'

def strong_connectivity(graph: dict) -> list:
    '''
    Finds the components of the strong connectivity
    of an oriented graph and returns a list of them.
    >>> strong_connectivity({0: [1, 2], 1: [2], 2: [0, 1], 3: [4], 4: [3, 5], 6: [7], 7: [6]})
    Graph contains 3 strong connectivity components:
    [{0: [1, 2], 1: [2], 2: [0, 1]}, {6: [7], 7: [6]}]
    >>> strong_connectivity({0: [1, 2], 1: [2], 2: [3], 3: [], 4: [3], 5: [4]})
    Graph doesn`t contain any strong connectivity components.
    '''

def connection_points(graph: dict) -> list:
    '''
    Finds the connection points of an unoriented graph and returns a list of them.
    >>> connection_points({0: [1], 1: [0, 2], 2: [1, 3, 4], 3: [2], \
4: [2, 5, 6, 7], 5: [4, 6], 6: [4, 5], 7: [4, 8], 8: [7]})
    There is a list of connection points of the graph: [1, 2, 4, 7]
    '''
    pass

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
        graph=copy.deepcopy(graph_origin)
    
    if bridges_result:
        bridges_sorted = sorted(bridges_result, key=lambda bridge: bridge[0])
        bridges_sorted = sorted(bridges_result, key=lambda bridge: bridge[1])
        print('There is a list of bridges of the graph:')
        return bridges_sorted
    return 'There are no bridges in the graph.'

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
