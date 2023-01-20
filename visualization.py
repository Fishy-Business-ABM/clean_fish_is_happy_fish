from p5 import *
from fish import Fish
import model
from random import uniform
from shark import Shark
from copy import copy

dimension = 150
perception = 75
n_fish = 50
initial_max_speed = 10
width = 800
height = 800
sea = model.Model(width,height)

for _ in range(n_fish):
    pos = (uniform(width/2 - dimension, width/2 + dimension),uniform(height/2 - dimension, height/2 + dimension))
    vel = (uniform(-initial_max_speed,initial_max_speed), uniform(-initial_max_speed,initial_max_speed))
    fish = Fish(sea, pos, perception, vel, 15, 0, 0, 0)

shark = Shark(model=sea,
              pos=(0.7 * width, 0.3 * height),
              perception=100,
              nb_seeable_fish=5,
              nb_deep_neurons=1,
              weights=range(36),
              eat_radius=100,
              energy=20,
              metabolism=0.2)

def setup():
    size(width, height)


def draw():
    background(30,30,47)

    sharks = copy(sea.sharks)
    for shark in sharks:
        shark.show()
        prey = shark.seeable_prey()
        shark.eat(prey)
        shark.metabolize()
        #shark.step()

    fishes = copy(sea.entities)
    for fish in fishes:
        fish.show()
        fish.step()

if __name__ == '__main__':
    run()

