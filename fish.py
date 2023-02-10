import random

from food import Food
from model import Model
from agent import Agent

from typing import Tuple, List
from util import normalize, euclidian_distance, compute_norm

class Fish(Agent):
    """Fish agent, which is the prey in our model

        A fish agent is defined by hard coded parameters, specie parameters, and individual parameters.
        At every given step, the fish agent memoizes the distance it has with the fish nearby.
    
        The parameters defining a fish agent are:
            # hard coded values:
                * max_energy
                * separation_strength
                * min_dist, i.e. how close to something it has to be to touch it
                * cohesion_strength
            # specie parameters:
                * perception
                * mass (see below)
                * genes
                * reproduction_rate
                * lifetime
                * age
            # individual parameters (genes):
                * cohesion_weight
                * align_weight
                * separation_weight
                * avoid_shark_weight
                * towards_food_weight

        /!\\ mass is not to be understood as standard mass but as inertia, it is the relationship between speed and energy loss in dE = mv^2

        In addition to these parameters, some other inner variables are computed:
            * max_speed, equal to 100 000 * mass
            * (initial) energy, equal to 1 * max energy
            * velocity, drawn from a uniform distribution over -1/2 max speed and 1/2 max speed
            * eat_radius, equal to 0.1 * perception

        Fish has one more attribute, which is `neighbors` and it simply holds a memoization of its distance to other fish within perception
    """

    def __init__(
        self,
        model: Model,
        pos: Tuple[float],
        perception: float,
        mass: float,
        reproduction_rate: float,
        genes: List[float],
    ):
        super(Fish, self).__init__(pos)

        # model
        self.model = model
        self.model.add_entity(self)

        # hard coded values
        self.max_energy = 1
        self.separation_strength = 0.05
        self.min_dist = 20
        self.cohesion_strength = 0.005

        # specie-related values
            # variable parameters
        self.perception = perception
        self.mass = mass
        self.genes = genes
        self.reproduction_rate = reproduction_rate
        self.lifetime = random.randint(80,100)
        self.age = 0

            # derived parameters
        self.max_speed = 100000 * self.mass
        self.energy = 1 * self.max_energy # initial energy
        self.velocity = tuple([random.uniform(-self.max_speed/2, self.max_speed/2) for _ in range(len(pos))]) # initial velocity
        self.eat_radius = 0.1 * perception
        
        # individual-related values
        self.cohesion_weight = genes[0]
        self.align_weight = genes[1]
        self.separation_weight = genes[2]
        self.avoid_shark_weight = genes[3]
        self.towards_food_weight = genes[4]

        # memoized values
        self.neighbors = set()


    def comfort_zone(self, velocity, comfort_zone_strength) -> List[float]:
        '''Returns velocity affected by how far the fish is to the comfort zone

            Fish can leave the model, in which case they are attracted to come back within its boundaries
        '''

        for i, pos in enumerate(self.pos):
            if pos <= 0:
                velocity[i] += comfort_zone_strength
                continue
            
            if pos >= self.model.window[i]:
                velocity[i] -= comfort_zone_strength

        return velocity


    def align(self) -> List[float]:
        '''Returns the component of how the fish follows the same direction as the boid it is in
        '''

        neighbors = self.neighbors # set of (neighbor, distance)
        alignment_strength = 0.05
        avg_vel = [float(0) for _ in self.pos]
        align_update = [float(0) for _ in self.pos]        

        if len(neighbors) == 0:
            return align_update

        for i in range(len(self.pos)):
            neighbors_velocity = [n[0].velocity[i] for n in neighbors if n[1] != 0]
            if len(neighbors_velocity) == 0:
                avg_vel[i] = 0
            else:
                avg_vel[i] = sum(neighbors_velocity) / len(neighbors_velocity)
            align_update[i] = (avg_vel[i] - self.velocity[i]) * alignment_strength

        return align_update


    def separation(self) -> List[float]:
        '''Returns the component of how the fish wants to distance itself from its neighbours
        '''

        separation_update = [float(0) for _ in self.pos]

        neighbors = self.neighbors

        if len(neighbors) == 0:
            return separation_update

        # new code
        close_neighbors = [n[0] for n in neighbors if n[1] != 0 and n[1] < self.min_dist]

        for cn in close_neighbors:
            for i, pos in enumerate(self.pos):
               separation_update[i] =  (pos - cn.pos[i]) * self.separation_strength

        return separation_update


    def cohesion(self) -> List[float]:
        '''Returns the component of how the fish wants to stay close to its neighbours
        '''

        cohesion_update = [float(0) for _ in self.pos]
        com = [float(0) for _ in self.pos]

        # new code
        neighbors = [n[0] for n in self.neighbors if n[1] != 0]
        if len(neighbors) == 0:
            return cohesion_update
        
        for i,pos in enumerate(self.pos):
            com[i] = sum([n.pos[i] for n in neighbors])
            com[i] /= len(neighbors)
            cohesion_update[i] = (com[i] - pos) * self.cohesion_strength

        return cohesion_update


    def towards_food(self) -> List[float]:
        '''Returns the component of how the fish wants move in order to eat food
        '''

        towards_food_update = [float(0) for _ in self.pos]

        hunger = 1 - self.energy / self.max_energy

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
        '''Returns the component of how the fish wants to escape the shark
        '''

        avoid_shark_update = [float(0) for _ in self.pos]

        visible_sharks = self.model.get_neighboring(self, self.perception, False, self.model.sharks)
        if len(visible_sharks) == 0:
            return avoid_shark_update

        count = len(visible_sharks)
        for shark in visible_sharks:
            if shark[1] == 0:
                count -= 1
                if count == 0:
                    return avoid_shark_update
                continue

            for i in range(len(self.pos)):
                avoid_shark_update[i] += (self.pos[i] - shark[0].pos[i]) / shark[1]

        for i in range(len(self.pos)):
            avoid_shark_update[i] /= count

        return avoid_shark_update


    def limit_velocity(self, velocity) -> List[float]:
        '''Returns velocity adjusted to max speed
        '''

        vel_length = compute_norm(tuple(velocity))

        if (vel_length < self.max_speed):
            return velocity

        fixed_velocity = [comp * self.max_speed for comp in normalize(tuple(velocity))]

        return fixed_velocity        

    def eat(self) -> None:
        '''Performs the action of eating nearby food
        '''
        if self.energy < self.max_energy:
            available_foods = self.model.get_neighboring_food(self, self.eat_radius)
            
            for food in available_foods:
                eat_fraction = min(food.available_fraction, self.max_energy - self.energy)
                self.energy += eat_fraction
                food.available_fraction -= eat_fraction
                self.model.regrowing_foods.add(food)
    

    def metabolize(self) -> None:
        '''Pays the cost of energy needed to stay alive (and possibly dies)
        '''
        self.energy -= self.mass * compute_norm(self.velocity) ** 2

        if self.energy <= 0 or self.age == self.lifetime:
            self.model.remove_entity(self)

             
    def recombine_genes(self, second_parent) -> List[float]:
        '''Returns a list of crossover-ed genes, that is a unique gene-sequence combining genes from both parents
        '''
        recombine_list = [random.randint(0,1) for _ in range(len(self.genes))]

        child_genes = [gene * recombine_list[i] + (1 - recombine_list[i]) * second_parent.genes[i] for i,gene in enumerate(self.genes)]

        return child_genes

    def mutate(self, genes) -> None:
        '''Mutates one random gene
        '''
        random_gene_nr = random.randint(0,len(genes) - 1)
        genes[random_gene_nr] += random.uniform(-0.1,0.1)
        if genes[random_gene_nr] < 0:
            genes[random_gene_nr] = 0
        return genes

    def reproduce(self) -> None:
        '''Performs the reproduction with a random neighbour
        '''
        if len(self.neighbors) == 0:
            return

        neighbors = list(self.neighbors)
        partner = random.randint(0,len(self.neighbors)-1)
        child_genes = self.recombine_genes(neighbors[partner][0])
        child_genes = self.mutate(child_genes)

        Fish(
            self.model,
            self.pos,
            self.perception,
            self.mass,
            self.reproduction_rate,
            child_genes
        )


    def step(self) -> None:
        '''Performs all the action a fish should do within a single time iteration
        '''

        # ages
        self.age += 1
        self.neighbors = self.model.get_neighbors_w_distance(self, self.perception, False)

        # reproduces if possible
        if self.energy > 0.5 * self.max_energy and random.random() < self.reproduction_rate:
            self.reproduce()

        # computes velocity components based on preferences
        alignment = self.align()
        separation = self.separation()
        cohesion = self.cohesion()
        towards_food = self.towards_food()
        avoid_shark = self.avoid_shark()

        # computes velocity vector
        neo_velocity = []
        for i in range(len(self.pos)):
            component = sum([self.velocity[i],
                             self.align_weight        * alignment[i],
                             self.separation_weight   * separation[i],
                             self.cohesion_weight     * cohesion[i],
                             self.towards_food_weight * towards_food[i],
                             self.avoid_shark_weight  * avoid_shark[i]])

            neo_velocity.append(component)

        # adjusts velocity to respect map boundaries
        neo_velocity = self.comfort_zone(neo_velocity, 1)

        # adjusts velocity to respect max speed
        neo_velocity = self.limit_velocity(neo_velocity)

        # updates position
        neo_pos = [ self.pos[i] + neo_velocity[i] for i in range(len(self.pos)) ]

        # updates velocity and position
        self.velocity = tuple(neo_velocity)
        self.pos = tuple(neo_pos)

        # eats if possible
        self.eat()

        # pays energy cost
        self.metabolize()

