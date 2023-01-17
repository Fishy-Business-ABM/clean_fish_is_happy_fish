import model

from typing import Tuple, List
from util import normalize, euclidian_distance

class Fish(object):
    """docstring for Fish"""
    def __init__(
        self,
        model: model.Model,
        pos: Tuple[float],
        perception: float,
        velocity: Tuple[float],
        max_speed: float
    ):
        super(Fish, self).__init__()

        self.pos = pos
        self.perception = perception
        self.model = model
        self.model.add_entity(self)
        self.velocity = velocity
        self.max_speed = max_speed

    def align(self) -> List[float]:
        neighbors = self.model.get_neighbors(self, self.perception, False)
        steering = [0 for _ in self.pos]
        if len(neighbors) == 0:
            return steering

        for i in range(len(self.pos)):
            for fish in neighbors:
                steering[i] += fish.velocity[i]
            steering[i] /= len(neighbors)


        normalized_steering = normalize(steering)
        if normalized_steering is None:
            return [0 for _ in self.pos]

        scaled_up_steering = [component * self.max_speed for component in normalized_steering]          

        return scaled_up_steering

    def separation(self) -> List[float]:
        steering = [0 for _ in self.pos]
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

        return steering
    
    def cohesion(self) -> List[float]:
        steering = [0 for _ in self.pos]
        neighbors = self.model.get_neighbors(self, self.perception, False)

        if len(neighbors) == 0:
            return steering

        for i in range(len(steering)):
            for fish in neighbors:
                steering[i] += fish.pos[i]
            steering[i] /= len(neighbors)

        return steering

    def step(self):
        alignment = self.align()
        separation = self.separation()
        cohesion = self.cohesion()

        neo_velocity = []
        for i in range(len(self.pos)):
            component = self.velocity[i] + alignment[i] + separation[i] + cohesion[i]
            neo_velocity.append(component)

        neo_pos = [ self.pos[i] + neo_velocity[i] for i in range(len(self.pos)) ]

        self.velocity = tuple(neo_velocity)
        self.pos = tuple(neo_pos)


