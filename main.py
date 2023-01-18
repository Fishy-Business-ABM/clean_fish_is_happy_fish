from model import Model
from fish import Fish
from food import Food
from util import compute_norm, normalize
import random
import math

def naive_test_add_fish():
    sea = Model()
    fish = Fish(sea, (0, 0), 0, (0, 0), 0, 0, 0, 0)
    assert len(sea.entities) == 1
    print("PASSED NAIVE TEST")

def naive_fuzzy_test_add_fish():
    sea = Model()
    n_fish = random.randint(1, 1000)
    for _ in range(n_fish):
        Fish(sea, (0, 0), 0, (0, 0), 0, 0, 0, 0)
    assert len(sea.entities) == n_fish
    print("PASSED NAIVE FUZZY TEST")

def naive_test_add_food():
    sea = Model()
    food = Food(sea, (0,0), 1)
    assert len(sea.foods) == 1
    print("PASSED NAIVE TEST ADD FOOD")

def naive_test_get_neighbor():
    sea = Model()
    n_fish = random.randint(1, 1000)
    base_fish = Fish(sea, (0, 0), 0, (0, 0), 0, 0, 0, 0)
    for _ in range(n_fish):
        Fish(sea, (0, 0), 0, (0, 0), 0, 0, 0, 0)
    
    assert len(sea.get_neighbors(base_fish, sea.entities, 0, True)) == n_fish + 1 
    assert len(sea.get_neighbors(base_fish, sea.entities, 0, False)) == n_fish
    
    Fish(sea, (0, 1), 0, (0, 0), 0, 0, 0, 0)
    Fish(sea, (1, 0), 0, (0, 0), 0, 0, 0, 0)
    assert len(sea.get_neighbors(base_fish, sea.entities, 0, True)) == n_fish + 1
    assert len(sea.get_neighbors(base_fish, sea.entities, 0, False)) == n_fish
    assert len(sea.get_neighbors(base_fish, sea.entities, 1, True)) == n_fish + 1 + 2
    assert len(sea.get_neighbors(base_fish, sea.entities, 1, False)) == n_fish + 2

    assert len(sea.get_neighbors(base_fish, sea.foods, 1, False)) == 0
    Food(sea, (0,0), 1)
    assert len(sea.get_neighbors(base_fish, sea.foods, 1, False)) == 1

    print("PASSED NAIVE FUZZY TEST GET NEIGHBOR")

def naive_test_norm():
    assert compute_norm([0, 0]) == 0
    assert compute_norm([0, 1]) == 1
    assert compute_norm([1, 0]) == 1

    norm_11 = compute_norm([1, 1]) 
    assert math.sqrt(2) - 0.0001 < norm_11 and norm_11 < math.sqrt(2) + 0.0001

    print("PASSED NAIVE TEST NORM")

def naive_fuzzy_test_normalize():
    n = random.randint(1, 1000)
    vec = tuple([random.random() for _ in range(n)])
    normalized = normalize(vec)
    assert isinstance(normalized, tuple)
    norm = compute_norm(normalized)
    assert 0.9999 < norm and norm < 1.0001 
    print("PASSED NAIVE FUZZY TEST NORMALIZE")

def naive_sanity_check_test_step():
    sea = Model()
    Fish(sea, (0, 0), 2, (0, 0), 10, 0, 0, 0).step()
    Fish(sea, (0, 0), 2, (0, 0), 10, 0, 0, 0).step()
    Fish(sea, (0, 0), 2, (0, 0), 10, 0, 0, 0).step()
    Fish(sea, (1, 1), 2, (0, 0), 10, 0, 0, 0).step()
    Fish(sea, (1, 1), 2, (0, 0), 10, 0, 0, 0).step()
    Fish(sea, (1, 1), 2, (0, 0), 10, 0, 0, 0).step()
    print("PASSED NAIVE SANITY CHECK TEST STEP")

def naive_test_start_regrowing():
    sea = Model()
    food = Food(sea, (0,0), 1)
    sea.start_regrowing(food)
    assert len(sea.regrowing_foods) == 1
    print("PASSED NAIVE TEST START REGROWING")

def naive_fuzzy_test_regrow():
    sea = Model()
    for _ in range(100):
        regrowth_rate = random.random()
        available_fraction = random.random()
        food = Food(sea, (0,0), regrowth_rate)
        sea.regrowing_foods.add(food)
        food.available_fraction = available_fraction
        food.regrow()
        target_fraction = min(available_fraction + regrowth_rate, 1)
        assert target_fraction - 0.001 < food.available_fraction and food.available_fraction < target_fraction + 0.001
        if target_fraction > 1:
            assert food not in sea.regrowing_foods
    print("PASSED NAIVE FUZZY TEST REGROW")

def naive_test_fish_eat():
    sea = Model()
    food = Food(sea, (0,0), 0.5)
    sea.add_food(food)
    fish = Fish(sea, (0, 0), 0, (0, 0), 0, 0, 0, 0)

    fish.eat()
    assert food.available_fraction == 0
    assert len(sea.regrowing_foods) == 1
    assert 0.9999 < fish.energy and fish.energy < 1.0001

    food.regrow()
    fish.eat()
    assert food.available_fraction == 0
    assert len(sea.regrowing_foods) == 1
    assert 1.4999 < fish.energy and fish.energy < 1.5001

    print("PASSED NAIVE TEST FISH EAT")

def naive_test_fish_metabolize():
    sea = Model()
    fish = Fish(sea, (0, 0), 0, (0, 0), 0, 0.8, 1, 0)

    fish.metabolize()
    assert len(sea.entities) == 1
    assert 0.1999 < fish.energy and fish.energy < 0.2001

    fish.metabolize()
    assert len(sea.entities) == 0

    print("PASSED NAIVE TEST FISH METABOLIZE")

def naive_test_model_step():
    sea = Model()

    fish = Fish(sea, (0,0), 1, (1,0), 1, 0.5, 1, 1)
    sea.add_entity(fish)

    food = Food(sea, (0.5, 0), 0.5)
    sea.add_food(food)
    
    for _ in range(10):
        sea.step()

    print("PASSED NAIVE TEST MODEL STEP")
    

if __name__ == '__main__':
    naive_test_add_fish()
    naive_fuzzy_test_add_fish()
    naive_test_get_neighbor()
    naive_test_norm()
    naive_fuzzy_test_normalize()
    naive_sanity_check_test_step()
    naive_test_add_food()
    naive_test_start_regrowing()
    naive_fuzzy_test_regrow()
    naive_test_fish_eat()
    naive_test_fish_metabolize()
    naive_test_model_step()
    # TODO: TEST STEP FOR REAL
