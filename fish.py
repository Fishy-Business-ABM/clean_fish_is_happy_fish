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
        mass: float,
        metaolism: float, # TODO: metabolism now superfluous because of introduction of mass!
        energy: float,
        eat_radius: float
    ):
        super(Fish, self).__init__(pos)
        self.perception = perception
        self.model = model
        self.model.add_entity(self)
        self.velocity = velocity
        self.mass = mass
        self.energy = energy
        self.eat_radius = eat_radius
        self.max_energy = 1

        # Mass, i.e. the relationship between speed and energy-loss in E = 0.5mv^2,
        # is related to the max speed of a fish, TODO: decide on precise relationship
        self.max_speed = 100000 * self.mass

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

    def towards_food(self) -> List[float]:
        towards_food_update = [float(0) for _ in self.pos]

        hunger = 1 - self.energy / self.max_energy
        # if self.energy > self.max_energy / 2:
        #     return towards_food_update

        visible_foods = self.model.get_neighboring(self, self.perception, False, self.model.foods)
        if len(visible_foods) == 0:
            return towards_food_update

        count = len(visible_foods)
        for food in visible_foods:
            attraction = 1 - food[1]/self.perception
            nutritional_value = food[0].available_fraction

            for i in range(len(self.pos)):
                if food[1] == 0:
                    count -= 1
                    continue
                
                direction = food[0].pos[i] - self.pos[i]
                towards_food_update[i] += direction * nutritional_value * hunger * attraction
        
        for i in range(len(self.pos)):
            towards_food_update[i] /= count
        
        return towards_food_update

    def avoid_shark(self) -> List[float]:
        avoid_shark_update = [float(0) for _ in self.pos]

        visible_sharks = self.model.get_neighboring(self, self.perception, False, self.model.sharks)
        if len(visible_sharks) == 0:
            return avoid_shark_update

        count = len(visible_sharks)
        for shark in visible_sharks:
            if shark[1] == 0:
                count -= 1
                continue

            for i in range(len(self.pos)):
                avoid_shark_update[i] += (self.pos[i] - shark[0].pos[i]) / shark[1]
        
        for i in range(len(self.pos)):
            avoid_shark_update[i] /= count
        
        return avoid_shark_update

    def limit_velocity(self, velocity) -> List[float]:
        vel_length = compute_norm(tuple(velocity))

        if (vel_length < self.max_speed):
            return velocity

        fixed_velocity = [comp * self.max_speed for comp in normalize(tuple(velocity))]

        return fixed_velocity        

    # Eat neighboring food and gain energy
    def eat(self):
        if self.energy < self.max_energy:
            available_foods = self.model.get_neighboring_food(self, self.eat_radius)
            
            for food in available_foods:
                eat_fraction = min(food.available_fraction, self.max_energy - self.energy)
                self.energy += eat_fraction
                food.available_fraction -= eat_fraction
                self.model.regrowing_foods.add(food)
    
    # Do metabolism and possibly die
    def metabolize(self):
        self.energy -= self.mass * compute_norm(self.velocity) ** 2

        if self.energy < 0:
            self.model.remove_entity(self)

    def step(self):
        self.neighbors = self.model.get_neighbors(self, self.perception, False)

        alignment = self.align()
        separation = self.separation()
        cohesion = self.cohesion()
        towards_food = self.towards_food()
        avoid_shark = self.avoid_shark()

        inertia_weight = 1
        align_weight = 1
        separation_weight = 1
        cohesion_weight = 1
        towards_food_weight = 5
        avoid_shark_weight = 2

        neo_velocity = []
        for i in range(len(self.pos)):
            component = sum([inertia_weight      * self.velocity[i],
                             align_weight        * alignment[i],
                             separation_weight   * separation[i],
                             cohesion_weight     * cohesion[i],
                             towards_food_weight * towards_food[i],
                             avoid_shark_weight  * avoid_shark[i]])

            neo_velocity.append(component)

        neo_velocity = self.boundary(neo_velocity, 1)
        neo_velocity = self.limit_velocity(neo_velocity)

        neo_pos = [ self.pos[i] + neo_velocity[i] for i in range(len(self.pos)) ]

        self.velocity = tuple(neo_velocity)
        self.pos = tuple(neo_pos)

        self.eat()
        self.metabolize()