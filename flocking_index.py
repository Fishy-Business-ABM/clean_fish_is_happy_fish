import numpy as np
from numpy._typing import NDArray
import model
width = 1000
height = 1000


def distance(x):
    D = np.empty((0, len(x)))
    for point in x:
        distance = np.array(
            [[np.linalg.norm(np.array(point.pos)-np.array(point2.pos)) for point2 in x]])
        D = np.append(D, distance, axis=0)
    return D


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def flocking_index(model) -> float:
    """Flocking index calculated as in the paper referenced in the report. With gamma set to a low number to smooth out
       the cutoff for when a fish is considered part of a flock slightly."""

    gamma = 0.05

    if len(model.entities) < 2:
        return None

    delta = 0.5
    m = 20
    fish = np.array(list(model.entities))
    N = len(fish)
    pairwise_distance = distance(fish)
    pairwise_heading = np.empty((0, N))
    for point in fish:
        heading_angles = np.array([[angle_between(
            np.array(point.velocity), np.array(point2.velocity)) for point2 in fish]])
        pairwise_heading = np.append(pairwise_heading, heading_angles, axis=0)

    pairwise_distance = 1 - 1/(1+np.exp(-gamma*(pairwise_distance-delta*m)/m))
    pairwise_heading = 1-pairwise_heading/np.pi

    flocking_index = 1/(N*(N-1)/2) * sum((pairwise_heading *
                                          pairwise_distance)[np.triu_indices(N, k=1)])
    return flocking_index
