import enum
from numpy import euler_gamma # what does this do ?
from p5 import stroke,circle # what does this do ?
from food import Food
from model import Model
from agent import Agent

from typing import Tuple, List
from util import normalize, euclidian_distance, compute_norm

class Fish(Agent):
    """docstring for Fish"""
    def __init__(
        self,
        model: Model,
        pos: Tuple[float],
        perception: float,
        velocity: Tuple[float],
        max_speed: float,
        metabolism: float,
        energy: float,
        eat_radius: float
    ):
        super(Fish, self).__init__(pos)
        self.perception = perception
        self.model = model
        self.model.add_entity(self)
        self.velocity = velocity
        self.max_speed = max_speed
        self.metabolism = metabolism
        self.energy = energy
        self.eat_radius = eat_radius

    def boundary(self, velocity, boundary_strength) -> List[float]:
        max_dist = 0.1 * self.model.window[0]

        for i,pos in enumerate(self.pos):
            if pos < max_dist:
                velocity[i] += boundary_strength
            if pos > self.model.window[i] - max_dist:
                velocity[i] -= boundary_strength

        return velocity

    def align(self) -> List[float]:
        neighbors = self.neighbors
        alignment_strength = 0.05
        avg_vel = [float(0) for _ in self.pos]
        align_update = [float(0) for _ in self.pos]        
        steering = [0 for _ in self.pos]

        if len(neighbors) == 0:
            return align_update

        for i in range(len(self.pos)):
            for fish in neighbors:
                dist = euclidian_distance(self.pos, fish.pos)
                if dist == 0:
                    continue
                avg_vel[i] += fish.velocity[i]
            avg_vel[i] /= len(neighbors) 
            align_update[i] = (avg_vel[i] - self.velocity[i]) * alignment_strength

        return align_update



    def separation(self) -> List[float]:
        separation_update = [float(0) for _ in self.pos]
        separation_strength = 0.05

        min_dist = 20

        neighbors = self.neighbors
        steering = [0 for _ in self.pos]

        if len(neighbors) == 0:
            return separation_update

        for fish in neighbors:
            dist = euclidian_distance(self.pos, fish.pos)
            if dist == 0 or dist > min_dist:
                continue

            for i, pos in enumerate(self.pos):
               separation_update[i] =  (pos - fish.pos[i]) * separation_strength

        return separation_update
    
    def cohesion(self) -> List[float]:
        cohesion_update = [float(0) for _ in self.pos]
        cohesion_strength = 0.005

        com = [float(0) for _ in self.pos]

        neighbors = self.neighbors
        steering = [0 for _ in self.pos]

        if len(neighbors) == 0:
            return cohesion_update

        for i,pos in enumerate(self.pos):
            for fish in neighbors:
                dist = euclidian_distance(self.pos, fish.pos)
                if dist == 0:
                    continue

                com[i] += fish.pos[i]
                
            com[i] /= len(neighbors)
            cohesion_update[i] = (com[i] - pos) * cohesion_strength

        return cohesion_update

    def limit_velocity(self, velocity) -> List[float]:
        vel_length = compute_norm(tuple(velocity))

        if (vel_length < self.max_speed):
            return velocity

        fixed_velocity = [comp * self.max_speed for comp in normalize(tuple(velocity))]

        return fixed_velocity        

    # Eat neighboring food and gain energy
    def eat(self):
        available_foods = self.model.get_neighboring_food(self, self.eat_radius)
        
        for food in available_foods:
            self.energy += food.available_fraction
            food.available_fraction = 0
            self.model.regrowing_foods.add(food)
    
    # Do metabolism and possibly die
    def metabolize(self):
        self.energy -= self.metabolism

        if self.energy < 0:
            self.model.remove_entity(self)

    def step(self):
        self.neighbors = self.model.get_neighbors(self, self.perception, False)

        alignment = self.align()
        separation = self.separation()
        cohesion = self.cohesion()

        inertia_weight = 1
        align_weight = 1
        separation_weight = 1
        cohesion_weight = 1

        neo_velocity = []
        for i in range(len(self.pos)):
            component = sum([inertia_weight    * self.velocity[i],
                             align_weight      * alignment[i],
                             separation_weight * separation[i],
                             cohesion_weight   * cohesion[i]])

            neo_velocity.append(component)

        neo_velocity = self.boundary(neo_velocity, 1)
        neo_velocity = self.limit_velocity(neo_velocity)

        neo_pos = [ self.pos[i] + neo_velocity[i] for i in range(len(self.pos)) ]

        self.velocity = tuple(neo_velocity)
        self.pos = tuple(neo_pos)

        self.eat()
        self.metabolize()