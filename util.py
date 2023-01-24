import math
from typing import Optional, Tuple

def euclidian_distance(pos_a, pos_b):
    out = 0
    for i in range(len(pos_a)):
        out += (pos_a[i] - pos_b[i]) ** 2
    return math.sqrt(out)

def compute_norm(pos: Tuple[float]) -> float:
    out = sum([p ** 2 for p in pos])
    out = math.sqrt(out)
    return out

def normalize(pos: Tuple[float]) -> Optional[Tuple[float]]:
    norm = compute_norm(pos)
    return None if norm == 0 else tuple([x / norm for x in pos])
