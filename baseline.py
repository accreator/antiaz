from hashlib import sha256
from random import shuffle

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

class random(base):
    def play(self, color):
        empty = [pos for pos in range(self.N**2) if self.board[pos] == 0]
        shuffle(empty)
        return 0, empty[0]//self.N, empty[0]%self.N

class minimax(base):
    def search(self, depth, color):
        if depth == 0 or self.count == self.N**2:
            return self.checkwin(), -1, -1
        if depth + self.count < self.N**2:
            empty = [pos for pos in range(self.N**2) if self.board[pos] == 0]
            shuffle(empty)
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

    def play(self, color):
        return self.search(8, color)

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
        v, x, y = game.play(2)
        print(v,x,y)
        game.make(x,y,2)

def benchmark():
    N = 9
    win_random = 0
    win_minimax = 0
    for k in range(1000):
        judge = base(N)
        agent_random = random(N)
        agent_minimax = minimax(N)
        for l in range(N*N):
            color = l % 2 + 1
            if (k + l) % 2 == 0:
                v, x, y = agent_random.play(color)
            else:
                v, x, y = agent_minimax.play(color)
            judge.make(x, y, color)
            agent_random.make(x, y, color)
            agent_minimax.make(x, y, color)

        if judge.checkwin() == 1:
            winner = N*N%2 + 1
        else:
            winner = (N*N-1)%2 + 1
        if winner == k % 2 + 1:
            win_random += 1
        else:
            win_minimax += 1
    print(win_random, win_minimax)

#benchmark()
#1000 games, 9x9 board
#random 97:903 minimax(depth=9)
#random 119:881 minimax(depth=8)





