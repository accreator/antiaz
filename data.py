import numpy as np
import os.path
from random import shuffle
from base import base

class DATA:
    def __init__(self, N):
        self.N = N

    def gen(self, dataset, size):
        judge = base(self.N)
        judge.count = self.N**2
        for i in range(self.N**2):
            judge.board[i] = i % 2 + 1
        datax = []
        datay = []
        for i in range(size):
            shuffle(judge.board)
            for j in range(self.N**2):
                if judge.board[j] == (self.N**2-1) % 2 + 1:
                    judge.unmake(j // self.N, j % self.N)
                    for k in range(self.N**2):
                        datax += [1 if judge.board[k] == 1 else 0]
                        datax += [1 if judge.board[k] == 2 else 0]
                    judge.make(j // self.N, j % self.N, (self.N**2-1) % 2 + 1)
                    datay += [(-judge.checkwin() + 1)/2]
        datax = np.asarray(datax, dtype=np.int8)
        datax = datax.reshape([-1, self.N, self.N, 2])
        datay = np.asarray(datay, dtype=np.int8)
        np.savez(dataset + "_x.npz", datax)
        np.savez(dataset + "_y.npz", datay)

    def load(self, dataset):
        return np.load(dataset + "_x.npz")["arr_0"], np.load(dataset + "_y.npz")["arr_0"]

    def load_trn(self):
        return self.load("trn")

    def load_vld(self):
        return self.load("vld")

    def load_tst(self):
        return self.load("tst")

'''
data = DATA(9)
data.gen("trn", 8000)
data.gen("vld", 1000)
data.gen("tst", 1000)
'''