from typing import Set, List, Optional
from util import euclidian_distance
from functools import reduce
import networkx as nx

""" A clustering coefficient is a measure of how close a graph is to a clique

This file implements various utilities to compute different clustering coefficients.
"""


def convert_to_graph(fish: Set['Fish']) -> List[List[float]]:
    """Converts a set of entities to the matrix representation of a graph

        The graph is undirected ([i][j] == [j][i]) and weighted.
        The weights are the distance between each couple of entities.
    """

    entities = list(fish)
    out = [[0 for _ in range(len(entities))] for _ in range(len(entities))]
    for i in range(len(entities)):
        for j in range(i+1, len(entities)):
            dist = euclidian_distance(entities[i].pos, entities[j].pos)
            out[i][j] = dist
            out[j][i] = out[i][j]
    return out


def build_neighborhood_graph(fish: Set['Fish']) -> List[List[float]]:
    """Converts a set of fish into the matrix representation of a neighborhood graph
    
        The neighborhood graph is caracterized by having an infinite distance between two fish that are not within perception reach of each other.
        The graph is undirected ([i][j] == [j][i]) and weighted.
        The weights are the distance between each couple of entities if not infinity.
    """

    entities = list(fish)
    out = [[None for _ in range(len(entities))] for _ in range(len(entities))]
    for i in range(len(entities)):
        for j in range(i+1, len(entities)):
            dist = euclidian_distance(entities[i].pos, entities[j].pos)
            are_paired = dist < entities[i].perception and dist < entities[j].perception
            out[i][j] = dist if are_paired else float('inf')
            out[j][i] = out[i][j]
    return out

def split_disjoint_graphs(graph: List[List[float]]) -> List[List[int]]:
    """Returns the list of disjoint subgraphs within input graph
    
        Two graphs are disjoint if they share no edge that is not None and not infinitely-weighted.
        A disjoint subgraph is represented a list of node indices within the input graph.
    """

    clusters = []
    visited = set()

    for i in range(len(graph)):
        if i in visited:
            continue
        visited.add(i)

        current_cluster = []
        current_cluster.append(i)

        for j in range(i+1, len(graph)):
            if j in visited or graph[i][j] is None or graph[i][j] == float("inf"):
                continue

            visited.add(j)
            current_cluster.append(j)

        clusters.append(current_cluster)
    return clusters

def get_perception_clusters(entities: Set['Fish']) -> (List[List[int]], List[List[float]]):
    '''Converts a set of Fish into a list of disjoint neighborhood graphs

        Each neighborhood graph is a graph of fish within perception range of each other.

        We can use the output values of this to count the number of clusters
        and the number of nodes in them if we want, it also returns the graph
        to read the distances if needed
    '''

    neighborhood_graph = build_neighborhood_graph(entities)
    clusters = split_disjoint_graphs(neighborhood_graph)
    return (clusters, neighborhood_graph)

def get_perception_clusters_w_clustering_coefficient(entities: Set['Fish']) -> List[Tuple[List[int], float]]:
    '''Converts a set of Fish into a list of disjoint neighborhood graphs and computes the clustering coefficient of each

        Each neighborhood graph is a graph of fish within perception range of each other.

        We can use the output values of this to count the number of clusters
        and the number of nodes in them if we want, it also returns the graph
        to read the distances if needed
    '''
    def __convert_cluster_to_nx_graph(cluster, og_graph):
        '''Auxiliary function to convert a graph into its Networkx representation
        '''
        edge_pairs = []
        for i in cluster:
            for j in cluster:
                if i == j:
                    continue
                ep = (i, j, {'weight': og_graph[i][j]})
                edge_pairs.append(ep)

        G = nx.Graph()
        G.add_edges_from(edge_pairs)
        return G

    clusters, neighborhood_graph = get_perception_clusters(entities)
    clusters_w_nx_graphs = [(c, __convert_cluster_to_nx_graph(c, neighborhood_graph)) for c in clusters]
    clusters_w_clustering_k = [
        (c[0], nx.average_clustering(c[1], weight='weight')) for c in clusters_w_nx_graphs
    ]

    return clusters_w_clustering_k

def get_average_clustering(entity: Set['Fish']) -> float:
    '''returns clustering coefficient of entire graph
    '''

    if len(entity) == 0:
        return 0
    graph = convert_to_graph(entity)
    edge_pairs = [
        [(i, j, {'weight': graph[i][j]}) for j in range(len(graph[i]))]
        for i in range(len(graph))
    ]
    flat_edge_pairs = reduce(lambda val, acc: val + acc, edge_pairs, [])

    G = nx.Graph()
    G.add_edges_from(flat_edge_pairs)
    return nx.average_clustering(G, weight='weight')


from fish import Fish
from model import Model
import random

test_genes = [0., 0., 0., 0., 0., 0.]

def naive_test_clustering():
    # create random model
    # test that each graph is non empty
    sea = Model(100, 100)
    for _ in range(4):
        Fish(
                model=sea,
                pos=(1 + random.random(), 1 + random.random()),
                perception=1,
                velocity=(0, 0),
                energy=0,
                eat_radius=0,
                genes=test_genes
            )

        Fish(
                model=sea,
                pos=(99 - random.random(), 99 - random.random()),
                perception=1,
                velocity=(0, 0),
                energy=0,
                eat_radius=0,
                genes=test_genes
            )
    ng = build_neighborhood_graph(sea.entities)
    clusters = split_disjoint_graphs(ng)

    assert isinstance(clusters, type([]))
    assert len(clusters) == 2
    assert len(clusters[0]) == len(clusters[1]) and len(clusters[0]) == 4

    assert get_average_clustering(sea.entities) < 0.2

    clusters_w_coeffs = get_perception_clusters_w_clustering_coefficient(sea.entities)
    for i in range(len(clusters_w_coeffs)):
        for j in range(len(clusters_w_coeffs[i][0])):
            assert clusters_w_coeffs[i][0][j] == clusters[i][j]
            assert clusters_w_coeffs[i][1] > 0.4

if __name__ == '__main__':
    naive_test_clustering()
    print("PASSED CLUSTERING")