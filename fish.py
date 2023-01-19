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
        max_force: float
    ):
        super(Fish, self).__init__()

        self.pos = pos
        self.perception = perception
        self.model = model
        self.model.add_entity(self)
        self.velocity = velocity
        self.max_speed = max_speed
        self.max_force = max_force

    def align(self) -> List[float]:
        neighbors = self.model.get_neighbors(self, self.perception, False)
        steering = [float(0) for _ in self.pos]
        if len(neighbors) == 0:
            return steering

        for i in range(len(self.pos)):
            for fish in neighbors:
                dist = euclidian_distance(self.pos, fish.pos)
                if dist == 0:
                    continue
                steering[i] += fish.velocity[i]
            steering[i] /= len(neighbors) 


        normalized_steering = normalize(steering)
        if normalized_steering is None:
            return [0 for _ in self.pos]

        scaled_up_steering = [component * self.max_speed - self.velocity[i] for i,component in enumerate(normalized_steering)]          

        if compute_norm(tuple(scaled_up_steering))> self.max_force:
            scaled_up_steering = [value * self.max_force for value in normalize(tuple(scaled_up_steering))]

        return scaled_up_steering

    def separation(self) -> List[float]:
        steering = [float(0) for _ in self.pos]
        neighbors = self.model.get_neighbors(self, self.perception, False)

        if len(neighbors) == 0:
            return steering

        for fish in neighbors:
            dist = euclidian_distance(self.pos, fish.pos)
            if dist == 0:
                continue
            dist_squared = dist ** 2

            for i in range(len(steering)):
                steering_dist = steering[i] + self.pos[i] - fish.pos[i]
                normalized_steering_dist = steering_dist / dist_squared
                averaged_normalized_steering_dist = normalized_steering_dist / len(neighbors)
                steering[i] = averaged_normalized_steering_dist

            if compute_norm(tuple(steering)) > self.max_force:
                steering = [value * self.max_force for value in normalize(tuple(steering))]

        return steering
    
    def cohesion(self) -> List[float]:
        steering = [float(0) for _ in self.pos]
        com = [float(0) for _ in self.pos]
        dist_com = [float(0) for _ in self.pos]
        neighbors = self.model.get_neighbors(self, self.perception, False)

        if len(neighbors) == 0:
            return steering

        for i in range(len(steering)):
            for fish in neighbors:
                dist = euclidian_distance(self.pos, fish.pos)
                if dist == 0:
                    continue

                com[i] += fish.pos[i] 
                
            com[i] /= len(neighbors)
            dist_com[i] = com[i] - self.pos[i]

        if compute_norm(tuple(dist_com)) > 0:
            dist_com = [value * self.max_speed for value in normalize(tuple(dist_com))]

        steering = [dist_com[i]-self.velocity[i] for i in range(len(dist_com))]

        if compute_norm(tuple(steering)) > self.max_force:
            steering = [value * self.max_force for value in normalize(tuple(steering))]


        return steering

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
            s = 2.5
            c = 0.05
            component = v * self.velocity[i] + a * alignment[i] + s * separation[i] + c * cohesion[i]
            neo_velocity.append(component)
        
        speed = compute_norm(neo_velocity)
        if speed > self.max_speed:
            neo_velocity = [ comp * self.max_speed for comp in normalize(neo_velocity) ]

        neo_pos = [ self.pos[i] + neo_velocity[i] for i in range(len(self.pos)) ]

        self.velocity = tuple(neo_velocity)
        self.pos = tuple(neo_pos)


