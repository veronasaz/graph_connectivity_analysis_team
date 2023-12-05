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
    [[0, 1, 2], [3, 4]]
    '''
    pass

def strong_connectivity(graph: dict) -> list:
    '''
    Finds the components of the strong connectivity
    of an oriented graph and returns a list of them.
    >>> strong_connectivity({0: [1, 2], 1: [2], 2: [0, 1], 3: [4], 4: [3, 5], 6: [7], 7: [6]})
    [[0, 1, 2], [6, 7]]
    '''

def connection_points(graph: dict) -> list:
    '''
    Finds the connection points of an unoriented graph and returns a list of them.
    >>> connection_points({0: [1], 1: [0, 2], 2: [1, 3, 4], 3: [2], \
4: [2, 5, 6, 7], 5: [4, 6], 6: [4, 5], 7: [4, 8], 8: [7]})
    [1, 2, 4, 7]
    '''
    pass

def bridges(graph: dict) -> list:
    '''
    Finds the bridges of an unoriented graph and returns a list of them.
    >>> bridges({0: [1], 1: [0, 2], 2: [1, 3, 4], 3: [2], \
4: [2, 5, 6, 7], 5: [4, 6], 6: [4, 5], 7: [4, 8], 8: [7]})
    [[0, 1], [1, 2], [2, 3], [2, 4], [4, 7], [7, 8]]
    '''
    pass

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
