import enum
from numpy import euler_gamma
import model
from p5 import stroke,circle

from typing import Tuple, List
from util import normalize, euclidian_distance, compute_norm

class Fish(object):
    """docstring for Fish"""
    def __init__(
        self,
        model: model.Model,
        pos: Tuple[float],
        perception: float,
        velocity: Tuple[float],
        max_speed: float,
    ):
        super(Fish, self).__init__()

        self.pos = pos
        self.perception = perception
        self.model = model
        self.model.add_entity(self)
        self.velocity = velocity
        self.max_speed = max_speed

    def boundary(self, velocity) -> List[float]:
        max_dist = 100
        boundary_strength = 1

        for i,pos in enumerate(self.pos):
            if pos < max_dist:
                velocity[i] += boundary_strength
            if pos > self.model.window[i] - max_dist:
                velocity[i] -= boundary_strength

        return velocity

    def align(self) -> List[float]:
        neighbors = self.model.get_neighbors(self, self.perception, False)

        alignment_strength = 0.05
        avg_vel = [float(0) for _ in self.pos]
        align_update = [float(0) for _ in self.pos]

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

        neighbors = self.model.get_neighbors(self, self.perception, False)

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

        neighbors = self.model.get_neighbors(self, self.perception, False)

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

    def show(self):
        stroke(255)
        circle(self.pos,10)

    def step(self):
        alignment = self.align()
        separation = self.separation()
        cohesion = self.cohesion()

        neo_velocity = []
        for i in range(len(self.pos)):
            v = 1
            a = 1
            s = 1
            c = 1

            component = v * self.velocity[i] + a * alignment[i] + s * separation[i] + c * cohesion[i]

            neo_velocity.append(component)

        neo_velocity = self.limit_velocity(neo_velocity)
        neo_velocity = self.boundary(neo_velocity)

        neo_pos = [ self.pos[i] + neo_velocity[i] for i in range(len(self.pos)) ]

        self.velocity = tuple(neo_velocity)
        self.pos = tuple(neo_pos)


