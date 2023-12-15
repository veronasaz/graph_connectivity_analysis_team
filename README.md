Звіт з проекту на тему: «Аналіз зв'язності графів»
Над проектом працювала, команда 17, а саме: Вероніка Сазонова, Марта Кійко, Софія Базилевич, Гембара Софія, Чупа Орест.

Завдання дли виконання:
1 Читання графу з файлу - функція яка вміє прочитати файл і записати дані в відповідну структуру. Формат файлу - csv, перша колонка містить перші вершини кожного ребра, друга - другі вершини (порядок вершин не грає ролі в випадку неорієнтованого графу, і є важливим коли граф орієнтований). 
2 Запис графу в файл - записує граф у файл (структура файлу описана вище) 
3 Пошук компонент зв’язності - повинен знаходити усі компоненти зв'язності 
неорієнтованого графу і повертати список компонент зв'язності (вважаємо що 
компонента ідентифікується вершиною найменшого номеру, який їй належить). 
4 Аналогічна функція пошуку компонент сильної зв'язності для орієнтованого графу. 
5 Пошук точок сполучення - знаходить усі точки сполучення неорієнтованого графу 
(повертає список вершин). 
6 Пошук мостів - знаходить усі мости неорієнтованого графу (повертає список ребер, 
кожне ребро - впорядкована пара точок). 
Розподіл обов’язків:
Функції 1, 2 розробляла Вероніка Сазонова
Функцію 3  розробляла Марта Кійко
Функцію 5  розробляла Софія Гембара
Функцію 6  розробляла Софія Базилевич
Функцію 4 розробляли Вероніка Сазонова та Орест Чупа

Опис першої функції
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

Функція «read_csv» призначена для зчитування графа з CSV-файлу та представлення його у вигляді словника.
Кроки функції:
1 Відкривається CSV-файл за допомогою конструкції «with open».
2 Проходиться по кожному рядку файлу, розділеному комами.
3 Кожен рядок вставляється в словник «graph», де ключем є перший елемент рядка, а значенням - другий елемент.
4 Повертається отриманий словник «graph», який представляє граф, зчитаний з CSV-файлу.
Для тестування функції використовується тимчасовий CSV-файл.
Опис другої функції:
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

Функція «write_csv» приймає граф у форматі словника, де кожний ключ представляє вершину, а відповідний йому список містить сусідні вершини. 
Функція записує граф у CSV-файл. 
Файл має дві колонки: перша колонка представляє вершину, а друга - її сусідів. Кожен рядок відповідає ребру у графі.
Основні етапи функції:
«graph»: Словник, який представляє граф, де ключі - це вершини, а значення - списки сусідніх вершин.
«file_name»: Рядок, який вказує назву створюваного CSV-файлу.
Функція відкриває вказаний файл у режимі запису ('w') з кодуванням UTF-8.
Вона проходить через кожну вершину графа та її сусідів.
Для кожної пари вершина-сусід записує рядок у файл у форматі "вершина,сусід\n".
Після обробки всіх вершин та їх сусідів файл закривається.





Опис третьої функції:
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
Граф називають незв’язним, якщо він складається з двох або більше зв’язних підграфів, кожна пара з яких не має спільних вершин. Назва цих зв’язних підграфів є компонентами зв’язності
Основна функція components_of_connectivity: 
1 Пошук компонент зв'язності у неорієнтованому графі та повернення їх у вигляді списку. 
2 Використовує рекурсивну функцію dfs(Depth-first search) для обходу графа у глибину та визначення кожної компоненти зв'язності. 
3 Зберігає результат у списку connectivity_components. 
4 Рекурсивна функція dfs: 
Використовується для обходу графа у глибину та визначення вершин, які належать даній компоненті зв'язності. 
5 Змінні та виведення результату: 
visited: Словник для відстеження відвіданих вершин. 
connectivity_components: Список компонент зв'язності. 
Результат виводиться на екран зазначенням кількості компонент зв'язності в графі.
Опис четвертої функції:
def strong_connectivity(graph: dict) -> list:
    '''
    Finds the components of the strong connectivity
    of an oriented graph and returns a list of them.
    >>> strong_connectivity({0: [1, 2], 1: [2], 2: [0, 1], 3: [4], 4: [3, 5], 6: [7], 7: [6]})
    'Graph contains 3 strong connectivity components: \
[{0: [1, 2], 1: [2], 2: [0, 1]}, {6: [7], 7: [6]}]'
    >>> strong_connectivity({0: [1, 2], 1: [2], 2: [3], 3: [], 4: [3], 5: [4]})
    'Graph doesn`t contain any strong connectivity components.'
    '''
    def dfs_pass_one(vertex, stack, visited):
        '''
        First pass of dfs to fill the stack with vertices
        in the order of their finishing times.
        '''
        visited.add(vertex)
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                dfs_pass_one(neighbor, stack, visited)
        stack.append(vertex)

    def dfs_pass_two(vertex, visited, scc):
        '''
        Second pass of dfs to find strongly connected components.
        '''
        visited.add(vertex)
        scc.append(vertex)
        for neighbor in reverse_g.get(vertex, []):
            if neighbor not in visited:
                dfs_pass_two(neighbor, visited, scc)

    def reverse_graph(graph):
        '''
        Function to reverse the direction of all edges in the graph.
        '''
        reversed_g = {}
        for vertex in graph:
            for neighbor in graph[vertex]:
                reversed_g.setdefault(neighbor, []).append(vertex)
        return reversed_g
    stack = []
    visited = set()

    for vertex in graph:
        if vertex not in visited:
            dfs_pass_one(vertex, stack, visited)

    reverse_g = reverse_graph(graph)

    visited.clear()
    connected_components = []
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            scc = []
            dfs_pass_two(vertex, visited, scc)
            connected_components.append(scc)

    strongly_connected_components = [component for component in connected_components if len(component) > 1]
    filtered_components = []

    for components in strongly_connected_components:
        filtered_dict = {}
        for component in components:
            if component in graph:
                filtered_dict[component] = graph[component]
        filtered_components.append(filtered_dict)
    
    result = sorted(filtered_components, key=lambda component: list(component.keys())[0])

    if strongly_connected_components:
        return f'Graph contains {len(strongly_connected_components)} strong connectivity components: {result}'
    return "Graph doesn`t contain any strong connectivity components."
Звіт про функцію «strong_connectivity»:
Функція «strong_connectivity» визначає компоненти сильної зв'язності для орієнтованого графа та повертає список цих компонент. 
Перший прохід DFS (dfs_pass_one):
Функція «dfs_pass_one» виконує перший прохід алгоритму DFS (Depth-First Search) для наповнення стеку вершинами у порядку їх завершення.
Використовується рекурсивний підхід для відвідування вершин та додавання їх до стеку.
Другий прохід DFS (dfs_pass_two):
Функція «dfs_pass_two» виконує другий прохід алгоритму DFS для знаходження сильно зв'язаних компонент.
Знову використовується рекурсивний підхід для відвідування вершин та додавання їх до поточної сильно зв'язаної компоненти.
Реверс графу (reverse_graph):
Функція «reverse_graph» реверсує всі напрямки ребер у графі, створюючи новий граф, де ребра спрямовані у зворотному напрямку.
Заповнення стеку та виклик DFS для всіх вершин:
Створюється порожній стек та множина відвіданих вершин.
Для кожної вершини графу, яка ще не відвідана, викликається функція dfs_pass_one для наповнення стеку.
Виклик DFS для вершин у порядку їх завершення (dfs_pass_two):
Граф реверсується за допомогою «reverse_graph».
Знову ініціалізується порожній набір відвіданих вершин.
Поки стек не пустий, знімається вершина зі стеку, і викликається «dfs_pass_two» для знаходження сильно зв'язаних компонент.
Сильно зв'язані компоненти сортуються за умовою, що вони мають більше однієї вершини.
Створюється новий список, де кожен елемент - словник, представляє сильно зв'язану компоненту.
Список сортується за ключем - першою вершиною кожної компоненти.
Результат:
Якщо є сильно зв'язані компоненти, повертається рядок, що містить їх кількість та відсортовані компоненти.
Якщо сильно зв'язаних компонент немає, повертається «Graph doesn`t contain any strong connectivity components».

Опис п’ятої функції:
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

Звіт до функції connection_points()
          Точкою сполучення в графі називається вершина при видаленні якої, граф розпадається на кілька компонент зв’язності графа. Відповідно після вилучення такої точки, граф перестає бути зв’язним. Алгоритм знаходження точок звʼязності базується на використанні методу пошуку вглиб(DFS). Варто відмітити, що при відсутності точок сполучення граф є двозвʼязним, тобто ця функція також підходить, як тест на те, чи є граф двозвʼязним.  
       Ідея використання DFS полягає в тому, що він дозволяє систематично відвідувати вершини та при цьому тримати інформацію про звʼязки між ними.
     Коли ми запускаємо DFS з певної вершини, алгоритм рекурсивно відвідує всі сусідні вершини тої певної вершини, які ще не були відвідані. Цей процес продовжується поки не будуть відвідані всі доступні з даної точки вершини.
     Під час виконання алгоритму DFS, будується підграф-дерево заданого графу. Кожне ребро, по якому відбувався перехід від однієї вершини до іншої, становить частину цього дерева. Тут я застосувала отримані на курсі дискретної математики знання про дерева. 
Нам відомі такі властивості дерева DFS:
Корінь дерева є точною сполучення, якщо він має дві або більше дочірніх вершин. Це означає, що існує хоча б два незалежних піддерева, і видалення кореня розірве ці два піддерева, роблячи граф менш звʼязним. 
Вершина відмінна від кореня є точкою сполучення, якщо для неї існує дочірня вершина, у якої немає зворотнього шляху до будь-якого предка цієї вершини. 

Функція dfs(vertex, parent, visited, disc, low, time, ap):
Приймає параметри:
-vertex: поточна вершина 
-parent: батько поточної вершини
-visited: масив відвіданих вершин
-disc: множина, що містить час відкриття кожної вершини (мітка), допомагає визначити у якому порядку вершина була відвідана. 
-low:  для кожної вершини  V, найраніше відвідана вершина, до якої можна дістатися від V. 
-time: загальна кількість в момент часу відвіданих вершин або яка по порядку відвідується вершина зараз
-ap: множина для зберігання точок сполучення (articulation point)
Алгоритм роботи функції dfs():

1. Проходимось по суміжним вершинам (adj_vertex),перевіряємо чи ми її відвідали, якщо ні, то добавляємо число дітей і виконуємо пошук вглиб сусідів. 
2. Починаємо рекурсивний обхід з стартової точки, перевіряємо для кожної суміжної вершини «adj_vertex» поточної вершини «vertex» чи не була вона відвідана раніше. 
3. Далі відбувається рекурсивний виклик для усіх невідвіданих вершин. Якщо adj_vertex не була відвідана, то функція  dfs викликає сама себе, вже з adj_vertex як новою стартовою вершиною. 
4. Потім ми шукаємо суміжні вершини adj_vertex і алгоритм повторюється. 
Цей процес повторюється, дозволяючи алгоритму продовжувати обхід вглибину.  Після обходу всіх суміжних вершин рекурсивний виклик завершується, і виконання повертається до попередньої вершини.  

Далі відбуваються перевірки:
1.
if parent is None and children > 1:
                    ap.add(vertex)
Ця умова перевіряє чи є поточна вершина «vertex», кореневою вершиною, тобто чи не має вона батьківської вершини і чи має вона більше ніж одну дочірню вершину. Якщо так, то вона додається до масиву з точками сполучення. 
children > 1
Ця умова, тому що видалення видалення кореневої вершини з двома або більше дочірніми вершинами розділить граф на кілька незалежних компонентів. 
2. 
elif parent is not None and low[adj_vertex] >= disc[vertex]:
                    ap.add(vertex)
Ця частина перевіряє чи є не коренева вершина, точкою сполучення. Якщо для будь-якої дочірньої вершини adj_vertex немає зворотного шляху до предків вершини vertex (тобто low[adj_vertex] більше або дорівнює disc[vertex]), то vertex є точкою сполученя і додається до множини ap.
3.
elif adj_vertex != parent:
                low[vertex] = min(low[vertex], disc[adj_vertex])
Ця умова виконується, якщо суміжна вершина adj_vertex не є батьком поточної вершини vertex. Вона оновлює low[vertex] на найменше значення між поточним low[vertex] і часом відкриття disc[adj_vertex]. Це важливо для визначення найранішої вершини, до якої можна дістатися з vertex, і використовується для виявлення зворотних шляхів у графі.

for vertex in graph:
        if not visited[vertex]:
            dfs(vertex, None, visited, disc, low, time, ap)
    return (f'There is a list of connection points of the graph: {sorted(list(ap))}')

Ця частина є завершальною у моїй функції.

I.Циклом for перебираємо всі вершини vertex у графі graph, для кожної вершини перевіряється, чи була вона вже відвідана. Це робиться через словник (або масив) visited.

II.Якщо вершина vertex не була відвідана, запускається функція dfs для цієї вершини.В якості аргументів передаються поточна вершина vertex, значення None для parent (оскільки vertex розглядається як можливий корінь DFS-дерева), а також поточні стани visited, disc, low, time, та множина ap.

III.Після завершення циклу, коли всі вершини були відвідані, алгоритм сформував множину ap, яка містить усі точки сполучення графа.

IV.Код повертає рядок із відсортованим списком точок сполучення. Функція sorted(list(ap)) конвертує множину ap у відсортований список, який легше читати та аналізувати.

Цей фрагмент коду ефективно збирає та повертає результати виконання алгоритму DFS для виявлення точок сполучення в графі, що робить його корисним для різних застосувань, таких як аналіз мережевої структури, планування та інші.



Опис шостої функції: 
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

Функція «bridges» призначена для знаходження та повернення мостів у неорієнтованому графі. Міст - це ребро, видалення якого роз'єднує граф або збільшує кількість компонентів зв'язності.
«graph»: словник, що представляє неорієнтований граф, де ключі - вершини, а значення - списки суміжних вершин.
Кроки функції:
1 Спочатку створюється копія початкового графу, оскільки функція буде змінювати структуру графу під час визначення мостів.
2 Всі ребра графу відображаються у вигляді відсортованих кортежів та зберігаються у списку «edges».
3 Визначається, чи залишений граф з'єднаним після видалення поточного ребра. Для цього використовується допоміжна функція «is_connected», яка використовує алгоритм DFS.
4 Проходиться по всіх ребрах і перевіряється, чи викликає видалення ребра зміни в з'єднаності графу. Якщо ні, то ребро вважається мостом та додається до списку «bridges_result».
5 Якщо знайдені мости, то вони сортуються та виводяться. Інакше повертається відповідне повідомлення.

Опис «main» функції:
Функція «main» призначена для запускання цілої програми. 
У ній ви вказуєте назву файлу, як «file» з якого ви хочете зчитати дані графа за допомогою функції «read_csv()».
Функція «is_oriented()» перевіряє чи граф є орієнтованим:
Використовує вкладений цикл, який проходить через всі вершини графу та їх сусідні вершини.
Для кожної вершини перевіряється, чи є її сусід у словнику графу та чи вказує цей сусід на поточну вершину.
Якщо хоча б одна з таких перевірок не виконується, функція повертає True, що свідчить про те, що граф не є орієнтованим.
Якщо жодна з перевірок не виявила неорієнтованості, функція повертає False, що вказує на те, що граф орієнтований.
