from random import random, uniform
from model import Model
from genetic_algorithm import GeneticAlgorithm, PrintRecorder
from food import Food
from shark import Shark
from fish import Fish

def shark_fitness(individual):
    weights, score = individual
    assert len(weights) == 42, f"{len(weights)}: {weights}"

    n_fish = 30

    width = 800
    height = 800

    initial_max_speed = 10

    sea = Model(width,height)

    Food(sea, (0.2 * width, 0.2 * height), 0.005)
    Food(sea, (0.2 * width, 0.8 * height), 0.005)
    Food(sea, (0.8 * width, 0.2 * height), 0.005)
    Food(sea, (0.8 * width, 0.8 * height), 0.005)
    Food(sea, (0.4 * width, 0.4 * height), 0.005)
    Food(sea, (0.4 * width, 0.6 * height), 0.005)
    Food(sea, (0.6 * width, 0.4 * height), 0.005)
    Food(sea, (0.4 * width, 0.4 * height), 0.005)


    sharky = Shark(model=sea,
      pos=(0.5 * width, 0.5 * height),
      perception=200,
      nb_seeable_fish=5,
      nb_deep_neurons=3,
      weights=weights,
      eat_radius=20,
      energy=100,
      mass=0.2)

    for _ in range(100):
        for _ in range(n_fish):
            genes = [random(),random(),random(),2*random(), 5] + [0.0001]

            pos = (random() * width, random() * height)
            vel = (initial_max_speed, initial_max_speed)
            perception = 75

            fish = Fish(
                    model=sea,
                    pos=pos,
                    perception=perception,
                    velocity=vel,
                    energy=1,
                    eat_radius=15,
                    genes=genes
                )

    i = 0
    while i < 1000:
        sea.step()
        if sharky.energy <= 0:
            break
        i += 1
    return i


if __name__ == '__main__':
    pr = PrintRecorder()
    pop = [[ 1 - random() * 2 for _ in range(42)] for _ in range(1000)]
    ga = GeneticAlgorithm(
        pop,
        shark_fitness,
        1,
        lambda x: x + 1 - random() * 2,
        0.1
    )
    ga.run(500, pr)
  