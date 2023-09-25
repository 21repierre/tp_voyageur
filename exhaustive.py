import math
from itertools import permutations
from tqdm.auto import tqdm


def main(villes):
    permuts_villes = permutations(villes)

    best_permut = None
    best_distance = math.inf

    for permut in tqdm(permuts_villes):
        distance_chemin = permut[-1].distance(permut[0])
        for i in range(len(permut) - 1):
            distance_chemin += permut[i].distance(permut[i + 1])

        if distance_chemin <= best_distance:
            best_permut = permut
            best_distance = distance_chemin

    return best_permut, best_distance
