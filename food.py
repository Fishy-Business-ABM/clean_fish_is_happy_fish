import model

from typing import Tuple

class Food(object):
    def __init__(self, model: model.Model, pos: Tuple[float], regrowth_rate: float):
        super(Food, self).__init__()

        self.model = model
        self.pos = pos
        self.regrowth_rate = regrowth_rate
        self.available_fraction = 1

        self.model.add_food(self)

    # Regrow at set rate
    def regrow(self):
        self.available_fraction += self.regrowth_rate

        # Stop growing if fully grown
        if self.available_fraction > 1:
            self.available_fraction = 1
            self.model.regrowing_foods.remove(self)
    
    def step(self):
        self.regrow()