import networkx as nx
from queue import PriorityQueue

def A_star(graph, heuristic, start_node, end_nodes):
    opened = set()
    closed = set()

    start_dist = {}
    preds = {}

    state = (start_node, *end_nodes)

    start_dist[state] = 0
    preds[state] = tuple()

    pq = PriorityQueue()

    entry_count = 0
    pq.put((0 + heuristic(start_node, end_nodes), entry_count, state))
    entry_count += 1
    opened.add(state)

    while not pq.empty():
        _, _, state = pq.get()
        node = state[0]
        nodes_to_visit = list(state[1:])

        # solution found
        if len(nodes_to_visit) == 0:
            res = []
            pred = preds[state]
            while (pred != tuple()):
                res.append(pred[0])
                pred = preds[pred]

            res = list(reversed(res))
            res.append(node)
            return res, len(opened)
        
        neig_states = set()
        for neig_node in graph.neighbors(node):
            if neig_node in nodes_to_visit:
                nodes_to_visit_updated = [x for x in nodes_to_visit if x != neig_node]
                neig_states.add((neig_node, *nodes_to_visit_updated),)
            else:
                neig_states.add((neig_node, *nodes_to_visit),)

        for neig_state in neig_states:
            if neig_state in closed:
                continue
            
            if neig_state not in start_dist:
                start_dist[neig_state] = 999_999_999_999

            if neig_state not in opened or start_dist[neig_state] > start_dist[state] + 1:
                preds[neig_state] = state

                start_dist[neig_state] = start_dist[state] + 1
                
                if neig_state not in opened:
                    heur_val = start_dist[neig_state] + heuristic(node, nodes_to_visit)
                    pq.put((heur_val, entry_count, neig_state))
                    entry_count += 1
                opened.add(neig_state)
            
        closed.add(state)

    raise Exception("NOT FOUND!")
