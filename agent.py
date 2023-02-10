class Agent(object):
    """
            Please do not implement any complex behavior here.
            This class is for composition purpose only, not inheritance.
    """

    def __init__(self, pos):
        super(Agent, self).__init__()
        self.pos = pos

    def step(self):
        raise NotImplementedError
