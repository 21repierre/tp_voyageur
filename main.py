from __future__ import annotations

import math
import os
import random
import time
from itertools import permutations

from matplotlib import pyplot as plt
from tqdm import tqdm, trange

import mapping
from gent.genT import *

np.seterr(all='raise')

# Rayon de la Terre
T_RAYON = 6371
# Villes chargees depuis le CSV
ALL_VILLES = []
# Matrice des distances entre villes
DISTANCES = None


class Ville:
    """
    Classe representant une ville
    """

    def __init__(self, nom, lat, lng, nomMaj):
        """
        Initialisation d'une ville avec:
        - Nom
        - Latitude
        - Longitude
        - Nom en majuscule
        """
        self.nom = nom
        self.nomMaj = nomMaj
        self.lat = np.deg2rad(lat)
        self.lng = np.deg2rad(lng)
        self.id = len(ALL_VILLES)
        ALL_VILLES.append(self)

    def __str__(self) -> str:
        """
        Formattage d'une ville pour print
        """
        return f"{self.nom} - {self.lat} - {self.lng}"

    def distance(self, otherVille: Ville) -> float:
        """
        Calcule la distance avec une autre ville
        """
        a = (np.sin((otherVille.lat - self.lat) / 2) ** 2 +
             np.cos(self.lat) * np.cos(otherVille.lat) * np.sin((otherVille.lng - self.lng) / 2) ** 2)
        b = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        return T_RAYON * b

    def __eq__(self, other: Ville) -> bool:
        try:
            return (self.id, self.nom) == (other.id, other.nom)
        except AttributeError:
            return NotImplemented

    def __hash__(self):
        return hash((self.id, self.nom))

    def __repr__(self):
        return self.__str__()


class Exhaustive:
    """
    Classe de la methode exhaustive
    """

    def __init__(self, villes):
        self.villes = villes

    def run(self):
        """
        Methode de lancement
        """
        # Liste toute les permutations du chemin initial.
        permuts_villes = permutations(self.villes)

        # Sauvegarde du meilleur chemin chemin trouve jusque la
        best_permut = None
        best_distance = math.inf

        # Recherche du meilleur chemin parmis les permutations
        for permut in tqdm(permuts_villes):
            distance_chemin = distanceChemin(permut)

            if distance_chemin <= best_distance:
                best_permut = permut
                best_distance = distance_chemin

        return best_permut, best_distance


class Metropolis:
    """
    Classe de l'implementation de l'algorithme Metropolis
    """

    def __init__(self, villes, N):
        self.N = N
        self.villes = villes
        self.Ts: list[genT] = [linearT(N), bigCos(N), cosAbs(N), cloche(N)]
        self.T = -1

        self.debugDist = [0] * self.N

        self.plateauThreshold = N // 5000
        self.plateauEpsilon = 10
        self.nbPermuCassage = 3

    def genT(self, n):
        return self.Ts[self.T].next(n)

    def run(self):
        lenV = len(self.villes)

        # cache pour i et j pour eviter de recopier une liste et de recalculer la distance
        XS = [[[x for x in self.villes], 0], [[x for x in self.villes], 0]]
        XS[0][1] = distanceChemin(XS[0][0])

        # Meilleur chemin trouve
        best = XS[0][0]
        best_distance = XS[0][1]

        cassageReset = 0
        plateauCount = 0

        try:
            for n in trange(self.N):
                self.debugDist[n] = XS[0][1]
                i = XS[0][0]
                j = XS[1][0]

                # Echange de 2 villes dans le chemin en s'assurant de pas echanger une ville avec elle meme
                t1, t2 = random.randrange(lenV), random.randrange(lenV)
                while t1 == t2:
                    t2 = random.randrange(lenV)
                j[t1], j[t2] = j[t2], j[t1]
                dj = distanceChemin(j)

                # Calcul de rho, en cas d'overflow => 0
                inExp = np.float128((XS[0][1] - dj) / self.genT(n - cassageReset))
                try:
                    rho = np.exp(inExp)
                except FloatingPointError:
                    rho = 0

                if rho >= 1:
                    # On choisit j
                    i[t1], i[t2] = i[t2], i[t1]
                    if abs(dj - XS[0][1]) < self.plateauEpsilon:
                        plateauCount += 1
                    else:
                        plateauCount = 0
                    XS[0][1] = dj
                elif random.random() < rho:
                    # On choisit j
                    i[t1], i[t2] = i[t2], i[t1]
                    if abs(dj - XS[0][1]) < self.plateauEpsilon:
                        plateauCount += 1
                    else:
                        plateauCount = 0
                    XS[0][1] = dj
                else:
                    # On garde i (retire l'echange de ville dans j)
                    j[t1], j[t2] = j[t2], j[t1]
                    plateauCount += 1

                # Sauvegarde le chemin si la distance est meilleure
                if dj < best_distance:
                    best = [x for x in j]
                    best_distance = dj

                # Mecanisme de cassage lors de l'atteinte d'un plateau dans les distances (uniquement lors d'un T lineaire)
                if plateauCount >= self.plateauThreshold and self.T >= 0:
                    plateauCount = 0
                    # print("Plateau", n, dj - XS[0][1])
                    cassageReset = 3 * n // 5 if n / self.N < 0.7 else 5 * n // 6
                    # cassageReset = n
                    for _ in range(self.nbPermuCassage):
                        p1, p2 = random.randrange(lenV), random.randrange(lenV)
                        while p1 == p2:
                            p2 = random.randrange(lenV)
                        XS[0][0][p1], XS[0][0][p2] = XS[0][0][p2], XS[0][0][p1]
        except KeyboardInterrupt as e:
            print("Exiting...")

        return best, best_distance


def distanceChemin(chemin):
    """
    Calcul la distance totale d'un chemin
    """
    distance_chemin = DISTANCES[chemin[0].id, chemin[-1].id]
    for i in range(len(chemin) - 1):
        distance_chemin += DISTANCES[chemin[i].id, chemin[i + 1].id]
    return distance_chemin


def parseVilles(limit=-1):
    """
    Charge les villes depuis le CSV et calcul la matrice distances
    :param limit: limiter le nombre de villes chargees
    :return: None
    """
    global DISTANCES
    f = open('villes.csv')
    lines = f.readlines()[1:]
    if limit != -1:
        lines = lines[:limit]
    for l in lines:
        lspl = l.split(',')
        ville = Ville(lspl[0].strip(), float(lspl[5].strip()), float(lspl[6].strip()), lspl[1].strip())
        print(ville, end=" / ")

    print()
    DISTANCES = np.zeros((len(ALL_VILLES), len(ALL_VILLES)))

    for i in range(len(ALL_VILLES)):
        for j in range(i + 1, len(ALL_VILLES)):
            DISTANCES[i, j] = ALL_VILLES[i].distance(ALL_VILLES[j])
            DISTANCES[j, i] = DISTANCES[i, j]


def loadSave(name):
    """
    Charge une run particuliere
    :param name:
    :return:
    """
    f = open(f"runs/{name}/result.txt", 'r')
    che = f.readlines()[0].split(",")
    chemin = []
    for v in che:
        for ville in ALL_VILLES:
            if ville.nom == v.replace('\n', ''):
                chemin.append(ville)
    return chemin


currentBest = "1695719552"
N = 10 ** 7


def main():
    """
    Fonction de lancement du programme
    :return:
    """
    parseVilles()
    run = int(time.time())
    os.makedirs(f"runs/{run}", exist_ok=True)

    # Charge la meilleure run
    lastBest = loadSave(currentBest)
    print(lastBest)
    print(f"Starting from {currentBest} at {distanceChemin(lastBest)}km.")
    # random.shuffle(lastBest)

    # Calcul un meilleur chemin avec Metropolis
    m = Metropolis(lastBest, N)
    best = m.run()
    for ville in best[0]:
        print(ville, end=" / ")
    print(f"\nDistance: {best[1]}km")
    print(f"Meme chemin: {best == lastBest}")

    # Enregistre la run + une map de la run
    mapping.create_map(list(best[0]), f"runs/{run}/map.html")
    result = open(f"runs/{run}/result.txt", "w")
    result.write(','.join([x.nom for x in best[0]]))
    result.write(f"\n{best[1]}")
    result.write(f"\n{N}")
    result.close()

    Xs = [i for i in range(N)]
    Ys = m.debugDist
    plt.plot(Xs, Ys)
    plt.show()


if __name__ == '__main__':
    main()
