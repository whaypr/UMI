# For given graph G passed on stdin:
#   - creates a CNF SAT representation of the problem of existence of Hamiltonian cycle in G
#   - solves the SAT instance using a SAT solver
#   - reinterprets results from the SAT solver back in G
#   - saves various information into created files
#
# The transformation to SAT is inspired by
# https://discuss.codechef.com/t/how-to-solve-hamiltonian-path-using-sat-solver-for-undirected-graph/13261/3.

import networkx as nx

import sys
sys.path.append('../utils')
import solve_SAT


# LOAD INPUT GRAPH

# Helper class to ensure that nodes always always have names 1,2,3,...
class Node_mapper:
    def __init__(self):
        self.n = 0
        self.node_mapping = {}

    def map(self, key):
        if key not in self.node_mapping:
            self.n += 1
            self.node_mapping[key] = self.n
        return self.node_mapping[key]

    def inverse_map(self, val):
        return list(self.node_mapping.keys())[list(self.node_mapping.values()).index(val)]


mapper = Node_mapper()
graph = nx.Graph()

n_nodes, n_edges = map(int, input().split())
for _ in range(n_edges):
    u, v = map(mapper.map, map(int, input().split()))
    graph.add_edge(u, v)


# TRANSFORM TO SAT INSTANCE

# Helper function to map states (node+position_in_the_cycle) to SAT variables 
def state2var(node, position):
    return node + (position - 1) * n_nodes


clauses = set()

# Nodes that are not neighbors in the graph cannot be neighbors in the cycle
# For each such pair, ban them from being neighbors on any position in the cycle
for u in graph.nodes:
    for v in graph.nodes:
        if u != v and v not in list(graph.neighbors(u)):
            for pos in range(1, n_nodes):
                clauses.add(f"-{state2var(u, pos)} -{state2var(v, pos+1)}")
            clauses.add(f"-{state2var(u, 1)} -{state2var(v, n_nodes)}")

# On each position in the cycle, there must be some node
for pos in graph.nodes:
    clause = ""
    for node in graph.nodes:
        clause = clause + str(state2var(node, pos)) + " "
    clause = clause.removesuffix(" ")
    clauses.add(clause)

# Each node must be on some position
for node in graph.nodes:
    clause = ""
    for pos in graph.nodes:
        clause = clause + str(state2var(node, pos)) + " "
    clause = clause.removesuffix(" ")
    clauses.add(clause)

# On no position in the cycle, there can be more than one node
for pos in graph.nodes:
    for node1 in range(1, n_nodes):
        for node2 in range(node1+1, n_nodes+1):
            clauses.add(f"-{state2var(node1, pos)} -{state2var(node2, pos)}")

# No node can be on more than one position
for node in graph.nodes:
    for pos1 in range(1, n_nodes):
        for pos2 in range(pos1+1, n_nodes+1):
            clauses.add(f"-{state2var(node, pos1)} -{state2var(node, pos2)}")



# CREATE DIMACS AND CALL SAT SOLVER ON IT

no_vars = max(set(abs(int(item)) for c in clauses for item in c.split(" ")))
dimacs = f"p cnf {no_vars} {len(clauses)}\n"

for c in clauses:
    dimacs = dimacs + f"{c} 0\n"

sat_result = solve_SAT.solve(dimacs)

if sat_result == None:
    raise Exception("The input graph is not Hamiltonian!")


# REINTERPRET RESULTS BACK IN THE INPUT GRAPH

cycle = [
    mapper.inverse_map(x % n_nodes) if (x % n_nodes) != 0 else mapper.inverse_map(n_nodes)
    for x in sat_result
    if x > 0
]


# SAVE ALL THE INFORMATION TO FILES

directory = "outputs/"
filename = "custom_graph"

# store SAT representation in the DIMACS format
with open(f"{directory}/{filename}.sat", "w") as f:
    f.writelines(dimacs)

# store the Hamiltonian cycle as the output of the SAT solver
with open(f"{directory}/{filename}.solution_sat", "w") as f:
    f.writelines(" - ".join(map(str, cycle)) + "\n")

# store the Hamiltonian cycle as a sequence of nodes in the input graph
with open(f"{directory}/{filename}.solution_graph", "w") as f:
    for x in sat_result:
        f.writelines(str(x) + "\n")

# visualize the graph with the cycle
G_agraph = nx.nx_agraph.to_agraph(graph)

G_agraph.node_attr.update(style="filled")

for node in G_agraph.nodes_iter():
    node.attr.update(color="red")

cycle_edges = [(str(cycle[i]), str(cycle[(i+1)%len(cycle)])) for i in range(len(cycle))]
for edge in G_agraph.edges_iter():
    if edge in cycle_edges or (edge[1], edge[0]) in cycle_edges:
        edge.attr.update(color="red")

G_agraph.draw(f"{directory}/{filename}.png", prog="sfdp", args="-x -Goverlap=scale -Tpng")
