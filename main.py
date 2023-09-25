from __future__ import annotations
import numpy as np

import exhaustive

T_RAYON = 6373.0


class Ville:
    def __init__(self, nom, lat, lng):
        self.nom = nom
        self.lat = np.deg2rad(lat)
        self.lng = np.deg2rad(lng)

    def __str__(self) -> str:
        return f"{self.nom} - {self.lat} - {self.lng}"

    def distance(self, otherVille: Ville):
        a = np.sin((otherVille.lat - self.lat) / 2) ** 2 + np.cos(self.lat) * np.cos(otherVille.lat) * np.sin(
            (otherVille.lng - self.lng) / 2) ** 2
        b = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        return T_RAYON * b


ALL_VILLES = []


def parseVilles(limit=-1):
    f = open('villes.csv')
    lines = f.readlines()[1:]
    if limit != -1:
        lines = lines[:limit]
    for l in lines:
        lspl = l.split(',')
        ville = Ville(lspl[0].strip(), float(lspl[5].strip()), float(lspl[6].strip()))
        print(ville, end=" / ")
        ALL_VILLES.append(ville)
    print()
    # print(ALL_VILLES)


def main():
    parseVilles(2)
    print(Ville("", 52.2296756, 21.0122287).distance(Ville("", 52.406374, 16.9251681)))
    print(ALL_VILLES[0].distance(ALL_VILLES[1]))
    best = (exhaustive.main(ALL_VILLES))
    for ville in best[0]:
        print(ville, end=" / ")
    print(f"Distance: {round(best[1], 2)}m")


if __name__ == '__main__':
    main()
