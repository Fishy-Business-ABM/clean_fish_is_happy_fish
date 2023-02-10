import matplotlib.pyplot as plt
from copy import copy
from statistics import mean
from typing import List, Set


def normalize(genes: List[float]) -> float:
    '''Normalizes genes so that they can be compared
    '''

    tot = sum(genes)
    if tot == 0:
        normalized = copy(genes)
        return normalized
    normalized = []
    for gene in genes:
        normalized.append(gene/tot)
    return normalized


def plot_gene_distribution(entities: Set['Fish']) -> None:
    '''computes and plots normalized gene distribution 
    '''
    genes = []
    for fish in entities:
        genes.append(normalize(fish.genes))
    genes.sort(key=lambda g: g[0])
    fish_nrs = range(len(genes))
    to_plot = []
    for gene_nr in range(len(genes[0])):
        gene_list = []
        for gene in genes:
            gene_list.append(gene[gene_nr])
        to_plot.append(gene_list)

    avgs = []
    for list in to_plot:
        avg = mean(list)
        avgs.append(avg)
    print(avgs)

    plt.close()
    bottoms = [0 for _ in to_plot[0]]
    for i in range(len(to_plot)):
        plt.bar(fish_nrs, to_plot[i], bottom=bottoms)
        for j in range(len(bottoms)):
            bottoms[j] += to_plot[i][j]
    plt.draw()
    plt.pause(0.1)
