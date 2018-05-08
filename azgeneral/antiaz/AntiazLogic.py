from hashlib import sha256

class Board():
    def __init__(self, n):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def countDiff(self, color):
        #FIXME: only works for n%2 == 1
        #the code sucks!
        s = 0
        for i in range(self.n):
            for j in range(self.n):
                if self[i][j] == 0:
                    return 0
                s += self[i][j]

        if s == 0:
            s = 1

        board = []
        for i in range(self.n):
            for j in range(self.n):
                if s == self[i][j]:
                    board += [1]
                else:
                    board += [2]

        if int(sha256(bytes(board)).hexdigest(), 16) % 2 == 0:
            result = -1
        else:
            result = 1

        if color == s:
            return -result
        return result

    def get_legal_moves(self, color):
        moves = set()  # stores the legal moves.
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==0:
                    newmove= (x,y)
                    moves.add(newmove)
        return list(moves)

    def has_legal_moves(self, color):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==0:
                    return True
        return False

    def execute_move(self, move, color):
        (x,y) = move
        assert self[x][y] == 0

        self[x][y] = color

