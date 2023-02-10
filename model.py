from util import euclidian_distance
from copy import copy

from typing import List, Tuple


class Model(object):
    def __init__(self, width, height):
        '''A model is a continuous space in which fish and shark live.

            Its attributes are:
                * entities, the set of fish (prey)
                * sharks, the set of sharks (predators)
                * window, which is the zone in which the shark lives and in which the fish feels comfortable
                * foods, the food sources
                * regrowing_foods, the food sources that are currently growing
        '''

        super(Model, self).__init__()
        self.entities = set()
        self.sharks = set()
        self.window = (width, height)
        self.foods = set()
        self.regrowing_foods = set()

    def add_entity(self, entity) -> None:
        '''Adds a fish to the model

            An arbitrary threshhold of 100 fish is implemented to limit computational costs
        '''

        if len(self.entities) >= 100:
            return

        assert "pos" in entity.__dict__ and isinstance(entity.pos, tuple)
        self.entities.add(entity)

    def add_shark(self, shark) -> None:
        assert "pos" in shark.__dict__ and isinstance(shark.pos, tuple)
        self.sharks.add(shark)

    def remove_entity(self, entity) -> None:
        self.entities.remove(entity)

    def remove_shark(self, shark) -> None:
        self.sharks.remove(shark)

    def get_neighboring(self, entity: 'Entity', radius: float, is_entity_included: bool, source: List) -> List:
        '''Returns the list of instances of source that are within radius of given entity
        '''

        neighbors = set()
        for potential_neighbor in source:
            if not is_entity_included and potential_neighbor == entity:
                continue
            dist = euclidian_distance(entity.pos, potential_neighbor.pos)
            if radius >= dist:
                neighbors.add((potential_neighbor, dist))
        return neighbors

    def get_neighboring_food(self, entity, radius) -> List['Food']:
        food_set = self.get_neighboring(entity, radius, False, self.foods)
        return [x[0] for x in food_set]

    def get_neighbors(self, entity, radius, is_entity_included) -> List['Fish']:
        '''Returns the list of instances of fish that are within radius of given entity
        '''
        neighbors_w_dist = self.get_neighbors_w_distance(
            entity, radius, is_entity_included)
        neighbors = [x[0] for x in neighbors_w_dist]
        return neighbors

    def get_neighbors_w_distance(self, entity, radius, is_entity_included) -> List[Tuple['Fish', float]]:
        '''Returns the list of instances of fish that are within radius of given entity along with the distances between each and the entity
        '''
        return self.get_neighboring(entity, radius, is_entity_included, self.entities)

    def add_food(self, food) -> None:
        assert "pos" in food.__dict__ and isinstance(food.pos, tuple)
        self.foods.add(food)

    def start_regrowing(self, food) -> None:
        assert "pos" in food.__dict__ and isinstance(food.pos, tuple)
        self.regrowing_foods.add(food)

    def step(self) -> None:
        ''' Runs the steps of every entity and every food source
        '''

        out_food = []
        out_fish = []
        out_shark = []

        regrowing_foods_copy = copy(self.regrowing_foods)
        entities_copy = copy(self.entities)
        sharks_copy = copy(self.sharks)

        for food in self.foods:
            out_food.append(
                {
                    "id": id(food),
                    "pos": food.pos,
                    "available_fraction": food.available_fraction
                }
            )

        for food in regrowing_foods_copy:
            food.step()

        for entity in entities_copy:
            out_fish.append(
                {
                    "id": id(entity),
                    "pos": entity.pos,
                    "nb_neighbors": len(entity.neighbors),
                    "genes": entity.genes
                }
            )
            entity.step()

        for shark in sharks_copy:
            out_shark.append(
                {
                    "id": id(shark),
                    "pos": shark.pos,
                    "step-size": shark.speed,
                    "angle": shark.angle
                }
            )
            shark.step()

        return (out_food, out_fish, out_shark)

    def run_model(self, step_count=100) -> None:
        '''Runs the model for the given number of iterations 
        '''
        for _ in range(step_count):
            self.step()
