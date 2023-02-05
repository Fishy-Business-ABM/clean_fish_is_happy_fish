from model import Model
from fish import Fish
from food import Food
from shark import Shark
from random import random, normalvariate
from math import trunc
import numpy as np
from flocking_index import flocking_index
from shark_automaton import SharkAutomaton

from statistics import mean


# Model parameters
width = 1000
height = 1000

# Fish parameters
perception_fish = 75
gene_means = [5, 5, 5, 5, 5]
gene_stds = [5, 5, 5, 5, 5]

# Shark parameters
perception_shark = 200
nb_seeable_fish = 5
nb_deep_neurons = 3
weights = [random() - 0.5 for _ in range(42)]
eat_radius = 20
initial_energy = 100000
mass = 0.2

def execute(nb_food, nb_initial_fish, nb_sharks, mass_fish, food_regrowth_rate, runtime):
    sea = Model(width, height)

    for _ in range(nb_food):
        Food(sea, (random() * width, random() * height), food_regrowth_rate)
    
    for _ in range(nb_initial_fish):
        pos = (random() * width, random() * height)
        random_genes = [normalvariate(gene_means[i], gene_stds[i]) for i in range(len(gene_means))]
        Fish(
                model=sea,
                pos=pos,
                perception=perception_fish,
                mass=mass_fish,
                reproduction_rate=0.01,
                genes=random_genes
            )
    
    for _ in range(nb_sharks):
        SharkAutomaton(
                model=sea,
                pos=(0.5 * width, 0.5 * height),
                perception=75,
                eat_radius=15,
                mass=0.000002,
                max_exploration_speed=5,
                max_hunting_speed=15
            )
#        Shark(model=sea,
#            pos=(random() * width, random() * height),
#            perception=perception_shark,
#            nb_seeable_fish=nb_seeable_fish,
#            nb_deep_neurons=nb_deep_neurons,
#            weights=weights,
#            eat_radius=eat_radius,
#            energy=initial_energy,
#            mass=mass
#        )
    
    out_food = []
    out_fish = []
    out_shark = []

    for time in range(runtime):
        out = sea.step()
        out_food.append(out[0])
        out_fish.append(out[1])
        out_shark.append(out[2])


        print("Progress: %i/%i" %(time+1,runtime))

        if len(sea.sharks) == 0:
            break

    return (out_food, out_fish, out_shark)

def output_data(nb_food, reproduction_rate, nb_sharks, mass_fish, food_regrowth_rate, runtime):
    sea = Model(width, height)

    for _ in range(nb_food):
        Food(sea, (random() * width, random() * height), food_regrowth_rate)
    
    for _ in range(50):
        pos = (random() * width, random() * height)
        random_genes = [normalvariate(gene_means[i], gene_stds[i]) for i in range(len(gene_means))]
        Fish(
                model=sea,
                pos=pos,
                perception=perception_fish,
                mass=mass_fish,
                reproduction_rate=reproduction_rate,
                genes=random_genes
            )
    
    for _ in range(nb_sharks):
        SharkAutomaton(
                model=sea,
                pos=(random() * width, random() * height),
                perception=75,
                eat_radius=15,
                mass=0.000002,
                max_exploration_speed=5,
                max_hunting_speed=15
            )

    flocking_over_time = []

    for time in range(runtime):
        sea.step()

        if time % 10 == 0:
            index = flocking_index(sea)
            if index != None:
                flocking_over_time.append(index)
    
    if flocking_over_time == [None] * len(flocking_over_time):
        flocking = None
    else:
        flocking = mean(flocking_over_time)
    print(flocking)
    
    # genes = []
    # for gene_nr in range(5):
    #     gene_values = ["Gene %i" %(gene_nr)]
    #     for fish in sea.entities:
    #         gene_values.append(fish.genes[gene_nr])
    #     genes.append(gene_values)

        #print("Progress: %i/%i" %(time+1,runtime))

    return [flocking]

