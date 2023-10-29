import sys
import networkx as nx
import copy

from A_star import A_star

# load maze data
with open(sys.argv[1], "r") as f:
        maze_data = f.readlines()

# create maze and init maze data
w = len(maze_data[0])
h = len(maze_data)
maze = [[0 for x in range(w)] for y in range(h)]
trashes = []
robot = ""

for r, row in enumerate(maze_data):
    for c, tile in enumerate(row):
        tile = tile.removesuffix("\n")

        if tile in ["R", "T"]:
            maze[r][c] = " "
        else:
            maze[r][c] = tile


        if tile == "T":
            trashes.append(f"{r}_{c}")
        elif tile == "R":
            robot = f"{r}_{c}"

# create maze graph
maze_graph = nx.Graph()

for r in range(1, h-1):
    for c in range(1, w-1):
        if maze[r][c] == "X":
            continue
        
        node = f"{r}_{c}"
        maze_graph.add_node(node)
        
        if maze[r][c-1] != "X":
            maze_graph.add_edge(node, f"{r}_{c-1}")
        if maze[r-1][c] != "X":
            maze_graph.add_edge(node, f"{r-1}_{c}")

# create trashes graph
trashes_graph = nx.Graph()

for i in range(0, len(trashes)):
    for j in range(i+1, len(trashes)):
        weig = len(nx.shortest_path(maze_graph, trashes[i], trashes[j])) - 1
        trashes_graph.add_edge(trashes[i], trashes[j], weight=weig)

# define A* heuristic
def heuristic(start_node, end_nodes):
    heur_graph = copy.deepcopy(trashes_graph)

    for to_delete in set(trashes).difference(set(end_nodes)):
        heur_graph.remove_node(to_delete)
    
    for n in end_nodes:
        weig = len(nx.shortest_path(maze_graph, start_node, n)) - 1
        heur_graph.add_edge(start_node, n, weight=weig)
    
    MST = nx.minimum_spanning_tree(heur_graph)

    MST_weight = sum([MST.edges[e]["weight"] for e in MST.edges])
    return MST_weight

# run A*
path, states_opened = A_star(maze_graph, heuristic, robot, trashes)

# print results
def print_maze(robot_curr, path_part, trash=""):
    for r in range(0, h):
        for c in range(0, w):
            rc = f"{r}_{c}"

            if rc == robot_curr:
                print("\033[1;31mR\033[0m", end="")
            elif rc == trash:
                print("\033[1;31mT\033[0m", end="")
            elif rc in trashes:
                print("\033[1;33mT\033[0m", end="")
            elif rc in path_part:
                print("\033[1;31m.\033[0m", end="")
            else:
                print("\033[1;32m"+maze[r][c]+"\033[0m", end="")
        print()
    print("Trashes remaining:", len(trashes))
    print("Traveled so far:", traveled)
    input("Press enter to continue")
    

i = 1
traveled = 0
robot_curr = robot

print_maze(robot, [])

while i < len(path):
    path_part = []
    curr = path[i]
    while curr not in trashes and i < len(path):
        path_part.append(curr)
        curr = path[i]
        i += 1
    if len(path_part) == 0:
        path_part.append(curr)
        i += 1
    
    print_maze(robot_curr, path_part, path[i-1])
    
    robot_curr = path[i-1]
    traveled += len(path_part)
    trashes.remove(path[i-1])

print_maze(robot_curr, [])
print_maze("", path)

print("--------------")
print("States_opened:", states_opened)
