import math
import random

import numpy as np
import tqdm

T = 1


def main(villes, distances, N=100):
    best = None
    best_distance = math.inf
    lenV = len(villes)
    X = [x for x in villes]

    for n in tqdm.trange(N):
        i = X
        j = [x for x in X]
        t1, t2 = random.randrange(lenV), random.randrange(lenV)
        while t1 == t2:
            t2 = random.randrange(lenV)
        j[t1], j[t2] = j[t2], j[t1]
        dj = distance(j, distances)
        rho = np.exp((distance(i, distances) - dj) / T)
        if rho >= 1:
            X = j
        elif random.random() < rho:
            X = j
        if dj <= best_distance:
            best = j
            best_distance = dj
    return best, best_distance


def distance(chemin, distances):
    distance_chemin = distances[chemin[0].id, chemin[-1].id]
    for i in range(len(chemin) - 1):
        distance_chemin += distances[chemin[i].id, chemin[i + 1].id]
    return distance_chemin
