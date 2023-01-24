from fish import Fish
from model import Model
from random import uniform
import matplotlib.pyplot as plt
from copy import copy

dimension = 10
initial_max_speed = 1
max_speed = 1
metabolism = 0.02
initial_energy = 1
eat_radius = 0
perception = 6
n_fish = 100
zoom = 10

tester = Model()

for _ in range(n_fish):
    pos = (uniform(-dimension, dimension), uniform(-dimension, dimension))
    vel = (uniform(-initial_max_speed,initial_max_speed), uniform(-initial_max_speed,initial_max_speed))
    fish = Fish(tester, pos, perception, vel, max_speed, metabolism, initial_energy, eat_radius)
    tester.add_entity(fish)

for _ in range(100):
    entities = copy(tester.entities)
    for entity in entities:
        entity.step()
        plt.plot([entity.pos[0]], [entity.pos[1]], 'bo')
    
    plt.axis('square')
    plt.grid(True)
    plt.draw()
    plt.pause(0.1)
    plt.close()