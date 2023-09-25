import math
from itertools import permutations
from tqdm.auto import tqdm


def main(villes, distances):
    permuts_villes = permutations(villes)

    best_permut = None
    best_distance = math.inf

    for permut in tqdm(permuts_villes):
        distance_chemin = distances[permut[0].id, permut[-1].id]
        for i in range(len(permut) - 1):
            distance_chemin += distances[permut[i].id, permut[i + 1].id]

        if distance_chemin <= best_distance:
            best_permut = permut
            best_distance = distance_chemin

    return best_permut, best_distance
