from model import Model
from fish import Fish
from food import Food
from shark import Shark
from random import random, normalvariate
from math import trunc
import numpy as np

# Model parameters
width = 800
height = 800

# Fish parameters
perception_fish = 75
gene_means = [1, 1, 1, 2, 5]
gene_stds = [gene / 10 for gene in gene_means]

# Shark parameters
perception_shark = 200
nb_seeable_fish = 5
nb_deep_neurons = 3
weights = [random() - 0.5 for _ in range(42)]
eat_radius = 20
initial_energy = 100000
mass = 0.2

def execute(nb_food, nb_initial_fish, nb_sharks, mass_fish, food_regrowth_rate, max_runtime):
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
                genes=random_genes
            )
    
    for _ in range(nb_sharks):
        Shark(model=sea,
            pos=(random() * width, random() * height),
            perception=perception_shark,
            nb_seeable_fish=nb_seeable_fish,
            nb_deep_neurons=nb_deep_neurons,
            weights=weights,
            eat_radius=eat_radius,
            energy=initial_energy,
            mass=mass
        )
    
    out_food = []
    out_fish = []
    out_shark = []

    for time in range(max_runtime):
        out = sea.step()
        out_food.append(out[0])
        out_fish.append(out[1])
        out_shark.append(out[2])

        print("Progress: %i/%i" %(time+1,max_runtime))

        if len(sea.sharks) == 0:
            break

    return (out_food, out_fish, out_shark)
