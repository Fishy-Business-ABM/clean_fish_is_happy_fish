from model import Model
from fish import Fish
from util import compute_norm, normalize
import random
import math

def naive_test_add_fish():
    sea = Model()
    fish = Fish(sea, (0, 0), 0, (0, 0), 0)
    assert len(sea.entities) == 1
    print("PASSED NAIVE TEST")

def naive_fuzzy_test_add_fish():
    sea = Model()
    n_fish = random.randint(1, 1000)
    for _ in range(n_fish):
        Fish(sea, (0, 0), 0, (0, 0), 0)
    assert len(sea.entities) == n_fish
    print("PASSED NAIVE FUZZY TEST")

def naive_test_get_neighbor():
    sea = Model()
    n_fish = random.randint(1, 1000)
    base_fish = Fish(sea, (0, 0), 0, (0, 0), 0)
    for _ in range(n_fish):
        Fish(sea, (0, 0), 0, (0, 0), 0)
    
    assert len(sea.get_neighbors(base_fish, 0, True)) == n_fish + 1 
    assert len(sea.get_neighbors(base_fish, 0, False)) == n_fish
    
    Fish(sea, (0, 1), 0, (0, 0), 0)
    Fish(sea, (1, 0), 0, (0, 0), 0)
    assert len(sea.get_neighbors(base_fish, 0, True)) == n_fish + 1
    assert len(sea.get_neighbors(base_fish, 0, False)) == n_fish
    assert len(sea.get_neighbors(base_fish, 1, True)) == n_fish + 1 + 2
    assert len(sea.get_neighbors(base_fish, 1, False)) == n_fish + 2

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
    Fish(sea, (0, 0), 2, (0, 0), 10).step()
    Fish(sea, (0, 0), 2, (0, 0), 10).step()
    Fish(sea, (0, 0), 2, (0, 0), 10).step()
    Fish(sea, (1, 1), 2, (0, 0), 10).step()
    Fish(sea, (1, 1), 2, (0, 0), 10).step()
    Fish(sea, (1, 1), 2, (0, 0), 10).step()
    print("PASSED NAIVE SANITY CHECK TEST STEP")

if __name__ == '__main__':
    naive_test_add_fish()
    naive_fuzzy_test_add_fish()
    naive_test_get_neighbor()
    naive_test_norm()
    naive_fuzzy_test_normalize()
    naive_sanity_check_test_step()
    # TODO: TEST STEP FOR REAL
