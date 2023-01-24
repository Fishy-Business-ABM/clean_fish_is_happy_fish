from p5 import *
from fish import Fish
import model
from random import random, uniform, normalvariate
from shark import Shark
from copy import copy
from food import Food

dimension = 150
perception = 75
n_fish = 30
initial_max_speed = 10
width = 800
height = 800
sea = model.Model(width,height)

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
    pos = (uniform(width/2 - dimension, width/2 + dimension),uniform(height/2 - dimension, height/2 + dimension))
    vel = (uniform(-initial_max_speed,initial_max_speed), uniform(-initial_max_speed,initial_max_speed))
    fish = Fish(sea, pos, perception, vel, 0.0001, 0.001, 1, 15, [1,1,1,10])

Shark(model=sea,
      pos=(0.5 * width, 0.5 * height),
      perception=200,
      nb_seeable_fish=5,
      nb_deep_neurons=3,
      weights=[random() - 0.5 for _ in range(42)],
      eat_radius=0,
      energy=100000,
      mass=0.2)

def setup():
    size(width, height)


def draw():
    background(30,30,47)
    stroke(255)

    regrowing_foods = copy(sea.regrowing_foods)
    for food in regrowing_foods:
        food.step()
    
    for food in sea.foods:
        circle(food.pos, 3*food.available_fraction)

    sharks = copy(sea.sharks)
    for shark in sharks:
        rect(shark.pos, 5, 5)
        #prey = shark.seeable_prey()
        #shark.eat(prey)
        #shark.metabolize()
        shark.step()

    fishes = copy(sea.entities)
    for fish in fishes:
        circle(fish.pos,10*fish.energy)
        fish.step()

if __name__ == '__main__':
    run()

