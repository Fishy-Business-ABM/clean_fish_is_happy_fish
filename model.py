from util import euclidian_distance
from copy import copy

class Model(object):
    def __init__(self,width,height):
        super(Model, self).__init__()
        self.entities = set()
        self.sharks = set()
        self.window = (width,height)
        self.foods = set()
        self.regrowing_foods = set()

    def add_entity(self, entity):
        assert "pos" in entity.__dict__ and isinstance(entity.pos, tuple)
        self.entities.add(entity)

    def add_shark(self, shark):
        assert "pos" in shark.__dict__ and isinstance(shark.pos, tuple)
        self.sharks.add(shark)

    def remove_entity(self, entity):
        self.entities.remove(entity)
    
    def remove_shark(self, shark):
        self.sharks.remove(shark)

    def get_neighboring(self, entity, radius, is_entity_included, source):
        neighbors = set()
        for potential_neighbor in source:
            if not is_entity_included and potential_neighbor == entity:
                continue
            dist = euclidian_distance(entity.pos, potential_neighbor.pos)
            if radius >= dist:
                neighbors.add((potential_neighbor, dist))
        return neighbors

    def get_neighboring_food(self, entity, radius):
        food_set = self.get_neighboring(entity, radius, False, self.foods)
        return [x[0] for x in food_set]


    def get_neighbors(self, entity, radius, is_entity_included):
        neighbors_w_dist = self.get_neighbors_w_distance(entity, radius, is_entity_included)
        neighbors = [x[0] for x in neighbors_w_dist]
        return neighbors

    def get_neighbors_w_distance(self, entity, radius, is_entity_included):
        return self.get_neighboring(entity, radius, is_entity_included, self.entities)

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
        the set during iteration. Also, we should randomize the order in which the fish
        step, otherwise earlier fish always eat away the food of later fish.
        '''
        regrowing_foods_copy = copy(self.regrowing_foods)
        entities_copy = copy(self.entities)
        for food in regrowing_foods_copy:
            food.step()
        for entity in entities_copy:
            entity.step()