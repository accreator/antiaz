from hashlib import sha256

class base(object):
    def __init__(self, N=9):
        self.N = N
        self.board = [0 for i in range(N**2)]
        self.count = 0

    def make(self, x, y, color):
        self.board[x*self.N+y] = color
        self.count += 1

    def unmake(self, x, y):
        self.board[x*self.N+y] = 0
        self.count -= 1

    def checkwin(self):
        if self.count < self.N**2:
            return 0
        if int(sha256(bytes(self.board)).hexdigest(), 16) % 2 == 0:
            return -1
        return 1