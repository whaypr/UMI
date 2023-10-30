import networkx as nx
import copy


class Heuristics:
    
    def __init__(self, maze_graph, trashes):
        self.maze_graph = maze_graph
        self.trashes = trashes

        # create trashes graph for MST heuristic
        self.trashes_graph = nx.Graph()

        for i in range(0, len(self.trashes)):
            for j in range(i+1, len(self.trashes)):
                weig = len(nx.shortest_path(self.maze_graph, self.trashes[i], self.trashes[j])) - 1
                self.trashes_graph.add_edge(self.trashes[i], self.trashes[j], weight=weig)


    # ------------------------------------------------------------------------

    def MST(self, start_node, end_nodes):
        """
        Returns a weight of a minimum spanning tree of a complete graph of
        the remaining trashes and the robot,
        where edge weights are lengths of the shortests path between corresponding pairs. 
        """

        heur_graph = copy.deepcopy(self.trashes_graph)

        for to_delete in set(self.trashes).difference(set(end_nodes)):
            heur_graph.remove_node(to_delete)
        
        for n in end_nodes:
            weig = len(nx.shortest_path(self.maze_graph, start_node, n)) - 1
            heur_graph.add_edge(start_node, n, weight=weig)
        
        MST = nx.minimum_spanning_tree(heur_graph)

        MST_weight = sum([MST.edges[e]["weight"] for e in MST.edges])
        return MST_weight


    def furthest_and_remaining(self, start_node, end_nodes):
        """
        Returns a distance to the furthest remaining trash
        plus number of remaining trashes.
        """
        
        furthest = len(nx.shortest_path(self.maze_graph, start_node, end_nodes[0])) - 1
        for n in end_nodes[1:]:
            l = len(nx.shortest_path(self.maze_graph, start_node, n)) - 1
            if l > furthest:
                furthest = l

        return furthest + len(end_nodes)


    def nearest(self, start_node, end_nodes):
        """
        Returns a distance to the nearest remaining trash.
        """
        
        nearest = len(nx.shortest_path(self.maze_graph, start_node, end_nodes[0])) - 1
        for n in end_nodes[1:]:
            l = len(nx.shortest_path(self.maze_graph, start_node, n)) - 1
            if l < nearest:
                nearest = l

        return nearest


    def remaining(self, start_node, end_nodes):
        """
        Returns a number of remaining trashes.
        """
        
        return len(end_nodes)


    def zero(self, start_node, end_nodes):
        """
        Returns zero.
        """
        
        return 0
