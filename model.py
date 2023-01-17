from util import euclidian_distance

class Model(object):
    def __init__(self):
        super(Model, self).__init__()
        self.entities = set()

    def add_entity(self, entity):
        assert "pos" in entity.__dict__ and isinstance(entity.pos, tuple)
        self.entities.add(entity)

    def get_neighbors(self, entity, radius, is_entity_included):
        neighbors = set()
        for potential_neighbor in self.entities:
            if not is_entity_included and potential_neighbor == entity:
                continue

            if radius >= euclidian_distance(entity.pos, potential_neighbor.pos):
                neighbors.add(potential_neighbor)
        return neighbors
