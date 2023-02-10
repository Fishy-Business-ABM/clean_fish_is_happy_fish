import model

from typing import Tuple


class Food(object):
    '''Food is a regrowing food source for fish.

        It regrows at a set rate until it is fully grown.
        It is caracterized by 4 attributes:
            * model, the model in which the food source is
            * pos, the position of the food source
            * regrowth_rate, the rate at which the food source generates food
            * available_fraction, the maximum available food
    '''

    def __init__(self, model: model.Model, pos: Tuple[float], regrowth_rate: float):
        super(Food, self).__init__()

        self.model = model
        self.pos = pos
        self.regrowth_rate = regrowth_rate
        self.available_fraction = 1

        self.model.add_food(self)

    def regrow(self) -> None:
        '''Regrows food at a set rate
        '''

        self.available_fraction += self.regrowth_rate

        # Stop growing if fully grown
        if self.available_fraction > 1:
            self.available_fraction = 1
            self.model.regrowing_foods.remove(self)

    def step(self) -> None:
        self.regrow()
