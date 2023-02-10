from model import Model
from fish import Fish
from food import Food
from shark import Shark
from random import random, normalvariate, uniform
from math import trunc
import numpy as np
from flocking_index import flocking_index
from shark_automaton import SharkAutomaton
from gene_distribution import plot_gene_distribution, normalize
import matplotlib.pyplot as plt

from statistics import mean

# Model parameters
width = 1000
height = 1000

# Fish parameters
PERCEPTION_FISH = 75

# Shark parameters
PERCEPTION_SHARK = 75
EAT_RADIUS = 15
MASS = 0.000002
MAX_EXPLORATION_SPEED = 10
MAX_HUNTING_SPEED = 15


def output_data(
    nb_food: int, 
    reproduction_rate: float, 
    nb_sharks: int, 
    mass_fish: float, 
    food_regrowth_rate: float, 
    runtime: int, 
    output_genes:bool =True, 
    output_flocking:bool =True) -> List[float]:
    '''Runs the experiment and returns the results

        The results are: 
            float flocking index,
            float Gene0_avg,
            float Gene0_std,
            float Gene1_avg,
            float Gene1_std,
            float Gene2_avg,
            float Gene2_std,
            float Gene3_avg,
            float Gene3_std,
            float Gene4_avg,
            float Gene4_std,
            int number_fish
    '''

    # init model
    sea = Model(width, height)

    # init food sources
    for _ in range(nb_food):
        Food(sea, (random() * width, random() * height), food_regrowth_rate)
    
    # init fish at random positions with random genes
    for _ in range(50):
        pos = (random() * width, random() * height)
        random_genes = [uniform(0, 1) for _ in range(5)]
        Fish(
                model=sea,
                pos=pos,
                perception=PERCEPTION_FISH,
                mass=mass_fish,
                reproduction_rate=reproduction_rate,
                genes=random_genes
            )
    
    # init sharks at random positions
    for _ in range(nb_sharks):
        SharkAutomaton(
                model=sea,
                pos=(random() * width, random() * height),
                perception=PERCEPTION_SHARK,
                eat_radius=EAT_RADIUS,
                mass=MASS,
                MAX_EXPLORATION_SPEED=10,
                MAX_HUNTING_SPEED=15
            )

    # out will store the result metrics
    out = []

    # will store the flocking over time
    flocking_over_time = []
    
    # running the experiment for `runtime` timesteps, if we asked to, measures flocking index ever 100 iterations
    for time in range(runtime):
        sea.step()
        if output_flocking:
            if time % 100 == 0:
                index = flocking_index(sea)
                if index is not None:
                    flocking_over_time.append(index)
    
    # if asked to measure flocking, computes average flocking
    if output_flocking:
        if flocking_over_time == [None] * len(flocking_over_time):
            flocking = None
        else:
            flocking = mean(flocking_over_time)
        out.append(flocking)
    
    # asked to measure genes, computes average and standard deviation of each gene
    if output_genes:
        for gene_nr in range(5):
            gene_values = []
            for fish in sea.entities:
                gene_values.append(fish.genes[gene_nr])
            if len(gene_values) == 0:
                out.append(0)
                out.append(0)
            else:
                out.append(mean(gene_values))
                out.append(np.std(gene_values))

    out.append(len(sea.entities))
    
    return out
