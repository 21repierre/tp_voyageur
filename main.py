from __future__ import annotations

import math
import os
import random
import time
from itertools import permutations

import numpy as np
from tqdm import tqdm, trange

import mapping

T_RAYON = 6373.0
ALL_VILLES = []
DISTANCES = None


class Ville:

    def __init__(self, nom, lat, lng):
        self.nom = nom
        self.lat = np.deg2rad(lat)
        self.lng = np.deg2rad(lng)
        self.id = len(ALL_VILLES)
        ALL_VILLES.append(self)

    def __str__(self) -> str:
        return f"{self.nom} - {self.lat} - {self.lng}"

    def distance(self, otherVille: Ville):
        a = (np.sin((otherVille.lat - self.lat) / 2) ** 2 +
             np.cos(self.lat) * np.cos(otherVille.lat) * np.sin((otherVille.lng - self.lng) / 2) ** 2)
        b = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        return T_RAYON * b


class Exhaustive:

    def __init__(self, villes):
        self.villes = villes

    def run(self):
        permuts_villes = permutations(self.villes)

        best_permut = None
        best_distance = math.inf

        for permut in tqdm(permuts_villes):
            distance_chemin = distanceChemin(permut)

            if distance_chemin <= best_distance:
                best_permut = permut
                best_distance = distance_chemin

        return best_permut, best_distance


class Metropolis:
    def __init__(self, villes, N):
        self.N = N
        self.villes = villes
        self.T = N // 1000
        self.baseT = self.N * 10

    def genT(self, n):
        # self.T = 1 / (n + 1) ** (1 / 2) # Tinit=1
        # self.T *= 0.9  # Tinit = N//1000
        # self.T = (10 ** 7 * abs(np.cos(n)) + 10 ** -5) / n
        self.T = (self.baseT * np.cos(n) + self.baseT + 10 ** - 9) / n
        return self.T

    def run(self):
        lenV = len(self.villes)
        # X = [x for x in self.villes]
        XS = [[[x for x in self.villes], 0], [[x for x in self.villes], 0]]
        XS[0][1] = distanceChemin(XS[0][0])
        X = 0
        best = XS[0][0]
        best_distance = XS[0][1]

        for n in trange(self.N):
            i = XS[X][0]
            j = XS[(X + 1) % 2][0]
            # j = [x for x in X]
            t1, t2 = random.randrange(lenV), random.randrange(lenV)
            while t1 == t2:
                t2 = random.randrange(lenV)
            j[t1], j[t2] = j[t2], j[t1]
            dj = distanceChemin(j)
            # rho = np.exp((distanceChemin(i) - dj) / self.genT(n))
            rho = np.exp((XS[X][1] - dj) / self.genT(n))
            if rho >= 1:
                i[t1], i[t2] = i[t2], i[t1]
                X = (X + 1) % 2
                XS[X][1] = dj
            elif random.random() < rho:
                i[t1], i[t2] = i[t2], i[t1]
                X = (X + 1) % 2
                XS[X][1] = dj
            else:
                j[t1], j[t2] = j[t2], j[t1]
            if dj <= best_distance:
                best = j
                best_distance = dj
        return best, best_distance


def distanceChemin(chemin):
    distance_chemin = DISTANCES[chemin[0].id, chemin[-1].id]
    for i in range(len(chemin) - 1):
        distance_chemin += DISTANCES[chemin[i].id, chemin[i + 1].id]
    return distance_chemin


def parseVilles(limit=-1):
    global DISTANCES
    f = open('villes.csv')
    lines = f.readlines()[1:]
    if limit != -1:
        lines = lines[:limit]
    for l in lines:
        lspl = l.split(',')
        ville = Ville(lspl[0].strip(), float(lspl[5].strip()), float(lspl[6].strip()))
        print(ville, end=" / ")

    print()
    DISTANCES = np.zeros((len(ALL_VILLES), len(ALL_VILLES)))

    for i in range(len(ALL_VILLES)):
        for j in range(i + 1, len(ALL_VILLES)):
            DISTANCES[i, j] = ALL_VILLES[i].distance(ALL_VILLES[j])
            DISTANCES[j, i] = DISTANCES[i, j]


def main():
    parseVilles()
    run = int(time.time())
    N = 10 ** 7
    os.makedirs(f"runs/{run}", exist_ok=True)
    mapping.create_map(ALL_VILLES, "debug.html")

    best = Metropolis(ALL_VILLES, N).run()
    for ville in best[0]:
        print(ville, end=" / ")
    print(f"Distance: {round(best[1], 2)}km")

    mapping.create_map(list(best[0]), f"runs/{run}/map.html")
    result = open(f"runs/{run}/result.txt", "w")
    result.write(','.join([x.nom for x in best[0]]))
    result.write(f"\n{best[1]}")
    result.write(f"\n{N}")
    result.close()


if __name__ == '__main__':
    main()
