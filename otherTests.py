


testChristophe = [['BONLOC   ', 43.366667, -1.266667, 1.76], ['ROQUEFORT   ', 43.766667, 0.6, 0.69],
                  ['MONTBEL   ', 42.983333, 1.983333, 2.08], ['QUILLAN   ', 42.866667, 2.183333, 1.72],
                  ['MAZAMET   ', 43.5, 2.4, 1.72], ['POUILLY LE MONIAL ', 45.966667, 4.65, 1.49],
                  ['COUTOUVRE   ', 46.066667, 4.216667, 1.65], ['FROLOIS   ', 47.533333, 4.633333, 1.61],
                  ['MONTIER EN L ISLE', 48.266667, 4.666667, 1.77], ['MACHY   ', 48.133333, 4.05, 1.19],
                  ['VASSELAY   ', 47.166667, 2.4, 0.67], ['CHATILLON SUR CHER ', 47.266667, 1.5, 2.23],
                  ['LA PORCHERIE  ', 45.583333, 1.533333, 1.69], ['SAINT PAUL D ESPIS', 44.133333, 0.983333, 1.27],
                  ['CONNE DE LABARDE ', 44.783333, 0.55, 1.27], ['MEDILLAC   ', 45.233333, 0.033333, 2.57],
                  ['CLOUE   ', 46.433333, 0.166667, 1.0], ['PORT DE PILES ', 47.0, 0.6, 1.77],
                  ['BILLIERS   ', 47.533333, -2.483333, 1.7], ['LOUDEAC   ', 48.166667, -2.75, 2.04],
                  ['SAINT JEAN DE LA', 48.7, -1.366667, 1.34], ['OUFFIERES   ', 49.016667, -0.483333, 0.93],
                  ['SAINT PIERRE DES ORMES', 48.3, 0.416667, 1.69], ['SAINT HILAIRE LE CHATEL', 48.55, 0.533333, 1.49],
                  ['LES MENUS  ', 48.516667, 0.933333, 2.19], ['BONNEVILLE APTOT  ', 49.25, 0.766667, 1.83],
                  ['TOCQUEVILLE LES MURS ', 49.666667, 0.5, 1.53],
                  ['BOUILLANCOURT EN SERY ', 49.966667, 1.633333, 1.76], ['GUESCHART   ', 50.233333, 2.0, 2.18],
                  ['BOURNONVILLE   ', 50.7, 1.85, 1.38], ['LIEVIN   ', 50.416667, 2.766667, 1.24],
                  ['HENDECOURT LES RANSART ', 50.2, 2.733333, 1.57], ['COURTEUIL   ', 49.2, 2.533333, 1.63],
                  ['MACOGNY   ', 49.166667, 3.233333, 1.57], ['CHIERRY   ', 49.033333, 3.433333, 2.12],
                  ['VIEUX RENG  ', 50.333333, 4.05, 2.04], ['MOURON   ', 49.316667, 4.783333, 1.94],
                  ['BEINHEIM   ', 48.866667, 8.083333, 2.75], ['COURMONT   ', 47.616667, 6.633333, 1.91],
                  ['LE VAL DE GOUHENANS', 47.616667, 6.483333, 1.38]]


def loadChristophe(ALL_VILLES):
    ret = []
    for elem in testChristophe:
        for v in ALL_VILLES:
            if v.nomMaj == elem[0].strip():
                ret.append(v)

    print(len(ret))
    assert len(ret) == len(ALL_VILLES)
    return ret


testVic = [0, 21, 10, 4, 8, 19, 12, 30, 17, 39, 26, 5, 14, 1, 9, 29, 36, 23, 7, 24, 33, 31, 6, 18, 27, 25, 34, 35, 22,
           13, 37, 15, 16, 2, 11, 3, 28, 32, 20, 38]


def loadVic(ALL_VILLES):
    ret = []
    for elem in testVic:
        for v in ALL_VILLES:
            if v.id == elem:
                ret.append(v)
    print(len(ret))
    assert len(ret) == len(ALL_VILLES)
    return ret