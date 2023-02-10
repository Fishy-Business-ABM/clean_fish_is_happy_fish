from p5 import *
from fish import Fish
from flocking_index import flocking_index
import model
from random import random, uniform, normalvariate
from shark_automaton import SharkAutomaton
from copy import copy
from food import Food
from gene_distribution import plot_gene_distribution

dimension = 150
perception = 75
n_fish = 30
initial_max_speed = 10

width = 800
height = 800

sea = model.Model(width, height)

# for w in range(round(width/4),round(3*width/8),50):
#     for h in range(round(width/4),round(3*width/8),40):
#         food = Food(sea, (w,h), 0.005)
# for w in range(round(5*width/8),round(3*width/4),50):
#     for h in range(round(5*width/8),round(3*width/4),40):
#         food = Food(sea, (w,h), 0.005)

Food(sea, (0.2 * width, 0.2 * height), 0.005)
Food(sea, (0.2 * width, 0.8 * height), 0.005)
Food(sea, (0.8 * width, 0.2 * height), 0.005)
Food(sea, (0.8 * width, 0.8 * height), 0.005)
Food(sea, (0.4 * width, 0.4 * height), 0.005)
Food(sea, (0.4 * width, 0.6 * height), 0.005)
Food(sea, (0.6 * width, 0.4 * height), 0.005)
Food(sea, (0.4 * width, 0.4 * height), 0.005)

for _ in range(n_fish):
    pos = (uniform(0, width), uniform(0, height))
    vel = (uniform(-initial_max_speed, initial_max_speed),
           uniform(-initial_max_speed, initial_max_speed))
    fish = Fish(
        model=sea,
        pos=pos,
        perception=perception,
        mass=0.0001,
        genes=[1, 1, 1, 1, 1],
        reproduction_rate=0.01,
    )

SharkAutomaton(
    model=sea,
    pos=(0.5 * width, 0.5 * height),
    perception=75,
    eat_radius=15,
    mass=0.000002,
    max_exploration_speed=5,
    max_hunting_speed=15
)


def setup():
    size(width, height)


def draw():
    background(30, 30, 47)
    stroke(255)

    for food in sea.foods:
        circle(food.pos, 3*food.available_fraction)

    fishes = copy(sea.entities)
    for fish in fishes:
        fill(0, 255, 0)
        circle(fish.pos, 10*fish.energy)
        fish.step()
    regrowing_foods = copy(sea.regrowing_foods)
    for food in regrowing_foods:
        food.step()

    sharks = copy(sea.sharks)
    for shark in sharks:
        fill(255, 0, 0)
        rect(shark.pos, 10, 10)
        # prey = shark.seeable_prey()
        # shark.eat(prey)
        # shark.metabolize()
        shark.step()
    print(flocking_index(sea))

    # plot_gene_distribution(sea.entities, 0)


if __name__ == '__main__':
    run()
