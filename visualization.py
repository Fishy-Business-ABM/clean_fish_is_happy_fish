from p5 import *
from fish import Fish
import model
from random import uniform

sea = model.Model()
dimension = 150
perception = 100
n_fish = 30
initial_max_speed = 10
width = 200
height = 150

for _ in range(n_fish):
    pos = (uniform(960 -dimension,960 +dimension),uniform(540-dimension, 540+ dimension))
    vel = (uniform(-initial_max_speed,initial_max_speed), uniform(-initial_max_speed,initial_max_speed))
    fish = Fish(sea, pos, perception, vel, 5, 1)

def setup():
    size(width, height)


def draw():
    background(30,30,47)
    for fish in sea.entities:
        fish.show()
        fish.step()

if __name__ == '__main__':
    run()
