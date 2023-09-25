from __future__ import annotations
import numpy as np

import exhaustive
import mapping
import metropolis1

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
    mapping.create_map(ALL_VILLES, "debug.html")
    #best = exhaustive.main(ALL_VILLES, DISTANCES)
    best = metropolis1.main(ALL_VILLES, DISTANCES, 10**7)
    for ville in best[0]:
        print(ville, end=" / ")
    print(f"Distance: {round(best[1], 2)}km")
    mapping.create_map(list(best[0]), "best.html")


if __name__ == '__main__':
    main()
