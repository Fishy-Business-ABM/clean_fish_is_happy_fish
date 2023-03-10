from functools import reduce
from math import sin, cos, exp, pi, atan
from model import Model
from agent import Agent
from typing import Tuple, List, Optional
from p5 import stroke, fill, rect
from util import compute_norm, normalize
from random import random
from fish import Fish


class SharkAutomaton(Agent):
    """Shark (Rule-based version)

        Training the neural network shark took us 26 hours and at the end it had the optimal strategy of barely moving if at all.
        So, we decided to use simple rules for our shark.

        The shark may explore around randomly until it sees a fish, in which case it tries to get as close as possible to eat it.
        It pays an energy cost at the end of each iteration.
    """

    def __init__(
        self,
        model: Model,
        pos: Tuple[float],
        perception: float,
        eat_radius: float,
        mass: float,
        max_exploration_speed: float,
        max_hunting_speed: float
    ):
        super(SharkAutomaton, self).__init__(pos)

        self.model = model
        self.model.add_shark(self)

        self.perception = perception
        self.eat_radius = eat_radius

        self.energy = 10
        self.mass = mass
        self.speed = 0
        self.angle = 0

        self.max_exploration_speed = max_exploration_speed

        self.max_hunting_speed = max_hunting_speed

    def closest_prey(self) -> Optional[Fish]:
        '''Get the closest prey
        '''

        prey = list(self.model.get_neighbors_w_distance(
            self, self.perception, False))
        if len(prey) == 0:
            return None
        prey.sort(key=lambda x: x[1])  # sort them by who is closer
        return prey[0]

    def explore(self) -> None:
        '''Moves randomly at max_exploration_speed
        '''

        d_angle = (random() - 0.5) * 0.2 * pi
        self.angle += d_angle

        dx = cos(self.angle) * self.max_exploration_speed
        dy = sin(self.angle) * self.max_exploration_speed

        new_x = self.pos[0] + dx
        new_y = self.pos[1] + dy

        self.pos = (new_x, new_y)

        return self.max_exploration_speed

    def compute_angle(self, pos1, pos2):
        '''Computes the angle between two positions
        '''
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]

        return -atan(dy/dx)

    def hunt(self, target) -> None:
        '''Tries to get as close as needed to the target fish and eat it
        '''

        dist_to_target = target[1]

        if dist_to_target < self.eat_radius:
            self.eat([target])
            return 0

        if dist_to_target <= self.max_hunting_speed:
            self.angle = self.compute_angle(self.pos, target[0])
            self.pos = target[0].pos
            self.eat([target])
            return target[1]

        direction_x = target[0].pos[0] - self.pos[0]
        direction_y = target[0].pos[1] - self.pos[1]

        normalized_direction = normalize((direction_x, direction_y))

        dx = normalized_direction[0] * self.max_hunting_speed
        dy = normalized_direction[1] * self.max_hunting_speed

        new_x = self.pos[0] + dx
        new_y = self.pos[1] + dy

        self.angle = self.compute_angle(self.pos, (new_x, new_y))
        self.pos = (new_x, new_y)

        return self.max_hunting_speed

    def eat(self, prey):
        ''' Eat potential prey within eating radius
        '''
        for fish, dist in prey:
            if dist <= self.eat_radius:
                self.energy += 1
                self.model.remove_entity(fish)

    def metabolize(self, distance_covered):
        ''' Pay energy cost and may die 
        '''
        self.energy -= self.mass * distance_covered ** 2
        self.energy *= 0.99

    def step(self):
        ''' Tries to find closest prey then either explores or hunts
        '''
        # used to compute metabolism
        distance_covered = 0

        # finds closest prey
        target = self.closest_prey()

        # chooses whether to explore or hunt depending of whether a prey is nearby
        distance_covered = self.explore() if target is None else self.hunt(target)

        # pays cost for moving
        self.metabolize(distance_covered)

        # is forced to stay within boundaries
        if not 0 < self.pos[0]:
            self.pos = (0, self.pos[1])
            self.angle = 0
        if not 0 < self.pos[1]:
            self.pos = (self.pos[0], 0)
            self.angle = pi/2
        if not self.pos[0] < self.model.window[0]:
            self.pos = (self.model.window[0], self.pos[1])
            self.angle = pi
        if not self.pos[1] < self.model.window[1]:
            self.pos = (self.pos[0], self.model.window[1])
            self.angle = 3*pi/2


if __name__ == '__main__':
    SharkAutomaton()
