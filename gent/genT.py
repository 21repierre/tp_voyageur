import numpy as np


class genT:

    def __init__(self, N: float):
        self.N = N
        self.mult = N * 10

    def next(self, n: float) -> float:
        return self.N


class bigCos(genT):

    def __init__(self, N):
        super().__init__(N)

    def next(self, n):
        return (self.mult * np.sin(n / 1000) + self.mult + 10 ** - 12) / (n + 1)


class cosAbs(genT):

    def __init__(self, N):
        super().__init__(N)

    def next(self, n):
        return (self.mult * abs(np.cos(n)) + 10 ** -5) / (n + 1)


class linearT(genT):
    def __init__(self, N):
        super().__init__(N)

    def next(self, n):
        return self.mult / (n + 1)


class cloche(genT):
    def __init__(self, N):
        super().__init__(N)
        self.sigma = 2
        self.denom = self.sigma * np.sqrt(2 * np.pi)
        self.mu = self.N // 2

    def next(self, n):
        return self.mult * np.exp(- (n - self.mu) ** 2 / (2 * self.sigma ** 2)) / self.denom