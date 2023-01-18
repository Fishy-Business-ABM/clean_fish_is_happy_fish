from util import euclidian_distance

class Model(object):
    def __init__(self):
        super(Model, self).__init__()
        self.entities = set()

    def add_entity(self, entity):
        assert "pos" in entity.__dict__ and isinstance(entity.pos, tuple)
        self.entities.add(entity)

    def get_neighbors(self, entity, radius, is_entity_included):
        neighbors_w_dist = self.get_neighbors_w_distance(entity, radius, is_entity_included)
        neighbors = [x[0] for x in neighbors_w_dist]
        return neighbors

    def get_neighbors_w_distance(self, entity, radius, is_entity_included):
        neighbors = set()
        for potential_neighbor in self.entities:
            if not is_entity_included and potential_neighbor == entity:
                continue
            dist = euclidian_distance(entity.pos, potential_neighbor.pos)
            if radius >= dist:
                neighbors.add((potential_neighbor, dist))
        return neighbors