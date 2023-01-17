from fish import Fish
from model import Model
from random import uniform
import matplotlib.pyplot as plt

dimension = 10
initial_max_speed = 1
perception = 2
n_fish = 100
zoom = 10

tester = Model()

for _ in range(n_fish):
    pos = (uniform(-dimension, dimension), uniform(-dimension, dimension))
    vel = (uniform(-initial_max_speed,initial_max_speed), uniform(-initial_max_speed,initial_max_speed))
    fish = Fish(tester, pos, perception, vel, 1)
    tester.add_entity(fish)

for _ in range(100):
    for entity in tester.entities:
        entity.step()
        plt.plot([entity.pos[0]], [entity.pos[1]], 'bo')
    
    plt.axis('square')
    plt.grid(True)
    plt.draw()
    plt.pause(0.1)
    plt.close()