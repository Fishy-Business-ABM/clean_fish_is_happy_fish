from util import euclidian_distance
from copy import copy

class Model(object):
    def __init__(self):
        super(Model, self).__init__()
        self.entities = set()
        self.foods = set()
        self.regrowing_foods = set()

    def add_entity(self, entity):
        assert "pos" in entity.__dict__ and isinstance(entity.pos, tuple)
        self.entities.add(entity)

    def remove_entity(self, entity):
        self.entities.remove(entity)

    def get_neighbors(self, entity, source, radius, is_entity_included):
        neighbors = set()
        for potential_neighbor in source:
            if not is_entity_included and potential_neighbor == entity:
                continue

            if radius >= euclidian_distance(entity.pos, potential_neighbor.pos):
                neighbors.add(potential_neighbor)
        return neighbors

    def add_food(self, food):
        assert "pos" in food.__dict__ and isinstance(food.pos, tuple)
        self.foods.add(food)

    def start_regrowing(self, food):
        assert "pos" in food.__dict__ and isinstance(food.pos, tuple)
        self.regrowing_foods.add(food)
    
    def step(self):
        '''
        TODO: change this to an elegant way of iterating over all regrowing foods and
        all entities, such that it is not a problem if foods or entities are removed from
        the set during iteration.
        '''
        regrowing_foods_copy = copy(self.regrowing_foods)
        entities_copy = copy(self.entities)
        for food in regrowing_foods_copy:
            food.step()
        for entity in entities_copy:
            entity.step()