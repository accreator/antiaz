from hashlib import sha256
import random

class minimax():
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

    def evaluate(self):
        if self.count < self.N**2:
            return 0
        if int(sha256(bytes(self.board)).hexdigest(), 16) % 2 == 0:
            return -1
        return 1

    def search(self, depth, color):
        if depth == 0 or self.count == self.N**2:
            return self.evaluate(), -1, -1
        if depth + self.count < self.N**2:
            empty = [pos for pos in range(self.N**2) if self.board[pos] == 0]
            random.shuffle(empty)
            return 0, empty[0]//self.N, empty[0]%self.N
        bestval = -2
        bestx, besty = -1, -1
        for x in range(self.N):
            for y in range(self.N):
                if self.board[x*self.N + y] == 0:
                    self.make(x, y, color)
                    val,_,_ = self.search(depth-1, 3-color)
                    val = -val
                    self.unmake(x, y)
                    if val == 1:
                        return val, x, y
                    if val > bestval:
                        bestval = val
                        bestx, besty = x, y
        return bestval, bestx, besty

def test():
    game = minimax(4)
    while True:
        for i in range(game.N):
            for j in range(game.N):
                print(game.board[i*game.N+j], end="")
            print()
        l = input("=>").strip().split(",")
        try:
            x, y = int(l[0]), int(l[1])
        except:
            continue
        game.make(x,y,1)
        v, x, y = game.search(3, 2)
        print(v,x,y)
        game.make(x,y,2)

