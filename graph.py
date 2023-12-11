'''Graph'''

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
    Graph contains 2 connectivity components: [{0: [1, 2], 1: [0, 2], 2: [0, 1]}, {3: [4], 4: [3]}]
    >>> components_of_connectivity({0: [1, 2, 4], 1: [0, 2, 3], 2: [0, 1, 3], 3: [1, 2, 4], 4: [0, 3]})
    Graph contains 1 connectivity component:
    [{0: [1, 2, 4], 1: [0, 2, 3], 2: [0, 1, 3], 3: [1, 2, 4], 4: [0, 3]}]
    '''
    pass

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

    visited = {v: False for v in graph} #відстежує, чи була кожна вершина відвідана. 
    disc = {v: float('inf') for v in graph} #містить час відкриття (або відвідування) кожної вершини. 
    low = {v: float('inf') for v in graph} #зберігає найнижчий індекс вершини, який можна досягти з даної вершини.
    ap = set() #зберігає всі точки сполучення графу.
    time = [0] #Список з одного елемента, що використовується для збереження поточного часу під час DFS.
    #Цей час збільшується під час відвідування кожної нової вершини.

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
    [[0, 1], [2, 3], [2, 4], [4, 5], [4, 6], [4, 7], [7, 8]]
    '''
    pass

if __name__ == '__main__':
    import doctest
    print(doctest.testmod(verbose=True))
