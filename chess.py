import numpy as np


class Piece:
    def __init__(self, name, team):
        self.name = name
        self.team = team

    def find_pos(self, board):
        """
        Function to find the indices of the piece chosen to be moved
        """
        i, j = np.where(board == self.name)
        i = int(i)
        j = int(j)

        return (i, j)

    def check_legal(self, init_square, final_square):
        """
        Function to check if the move made is legal
        """
        legal = False

        legal_moves = self.legal_moves()

        if final_square in legal_moves:
            legal = True

        else:
            legal = False

        return legal


class Pawn(Piece):
    cat = 'pawn'

    def legal_moves(self):
        coord = self.find_pos(board)

        if self.team == 'black':
            return [(coord[0]+1, coord[1])]

        elif self.team == 'white':
            return [(coord[0]-1, coord[1])]


class Rook(Piece):
    cat = 'rook'

    def legal_moves(self):
        coord = self.find_pos(board)
        legal = []

        available_vert = []
        available_horiz = []

        for i in range(len(board)):
            if board[i][coord[1]] == board[coord[0]][coord[1]]:
                continue

            elif board[i][coord[1]] != board[coord[0]][coord[1]]:
                available_vert.append((i, coord[1]))

        for i in range(len(board)):
            if board[coord[0]][i] == board[coord[0]][coord[1]]:
                continue

            elif board[coord[0]][i] != board[coord[0]][coord[1]]:

                available_horiz.append((coord[0],i))

        return available_vert + available_horiz


class Bishop(Piece):
    cat = 'bishop'


class Knight(Piece):
    cat = 'knight'

    def legal_moves(self):

        coord = self.find_pos(board)

        mv_1 = (coord[0]-2, coord[1]-1)
        mv_2 = (coord[0]-1, coord[1]-2)
        mv_3 = (coord[0]+1, coord[1]-2)
        mv_4 = (coord[0]+2, coord[1]-1)
        mv_5 = (coord[0]+2, coord[1]+1)
        mv_6 = (coord[0]+1, coord[1]+2)
        mv_7 = (coord[0]-1, coord[1]+2)
        mv_8 = (coord[0]-2, coord[1]+1)

        return [mv_1, mv_2, mv_3, mv_4, mv_5, mv_6, mv_7, mv_8]



class King(Piece):
    cat = 'king'

    def legal_moves(self):

        coord = self.find_pos(board)

        mv_1 = (coord[0]-1, coord[1])
        mv_2 = (coord[0]-1, coord[1]-1)
        mv_3 = (coord[0], coord[1]-1)
        mv_4 = (coord[0]+1, coord[1]-1)
        mv_5 = (coord[0]+1, coord[1])
        mv_6 = (coord[0]+1, coord[1]+1)
        mv_7 = (coord[0], coord[1]+1)
        mv_8 = (coord[0]-1, coord[1]+1)

        return [mv_1, mv_2, mv_3, mv_4, mv_5, mv_6, mv_7, mv_8]

class Queen(Piece):
    cat = 'queen'


def move():
    print(board)
    l, n = input('Enter piece square: ').split()
    l2, n2 = input('Enter move square: ').split()
    l = int(l)
    n = int(n)
    l2 = int(l2)
    n2 = int(n2)

    init_square = (l, n)
    final_square = (l2, n2)

    val = backend[l][n]

    is_legal = val.check_legal(init_square, final_square)

    if is_legal == True:
        print('LEGAL')
        board[l][n] = 0
        board[l2][n2] = val.name

        print(board)

    else:
        print('Illegal')


# black pawns
bP1 = Pawn('bP1', 'black')
bP2 = Pawn('bP2', 'black')
bP3 = Pawn('bP3', 'black')
bP4 = Pawn('bP4', 'black')
bP5 = Pawn('bP5', 'black')
bP6 = Pawn('bP6', 'black')
bP7 = Pawn('bP7', 'black')
bP8 = Pawn('bP8', 'black')

# white pawns
wP1 = Pawn('wP1', 'white')
wP2 = Pawn('wP2', 'white')
wP3 = Pawn('wP3', 'white')
wP4 = Pawn('wP4', 'white')
wP5 = Pawn('wP5', 'white')
wP6 = Pawn('wP6', 'white')
wP7 = Pawn('wP7', 'white')
wP8 = Pawn('wP8', 'white')

# black rooks
bR1 = Rook('bR1', 'black')
bR2 = Rook('bR2', 'black')

# white rooks
wR1 = Rook('wR1', 'white')
wR2 = Rook('wR2', 'white')

# black knights
bKn1 = Knight('bKn1', 'black')
bKn2 = Knight('bKn2', 'black')

# white knights
wKn1 = Knight('wKn1', 'white')
wKn2 = Knight('wKn2', 'white')

# black bishops
bB1 = Bishop('bB1', 'black')
bB2 = Bishop('bB2', 'black')

# white bishops
wB1 = Bishop('wB1', 'white')
wB2 = Bishop('wB2', 'white')

# black royals
bQ = Queen('bQ', 'black')
bK = King('bK', 'black')

# white royals
wQ = Queen('wQ', 'white')
wK = King('wK', 'white')


backend = np.array([[bR1, bKn1, bB1, bQ, bK, bB2, bKn2, bR2],
                 [bP1, bP2, bP3, bP4, bP5, bP6, bP7, bP8],
                 ['0', '0', '0', '0', '0', '0', '0', '0'],
                 ['0', '0', '0', '0', '0', '0', '0', '0'],
                 ['0', '0', '0', '0', '0', '0', '0', '0'],
                 ['0', '0', '0', '0', '0', '0', '0', '0'],
                 [wP1, wP2, wP3, wP4, wP5, wP6, wP7, wP8],
                 [wR1, wKn1, wB1, wQ, wK, wB2, wKn2, wR2]
                 ])

board = np.array([[bR1.name, bKn1.name, bB1.name, bQ.name, bK.name, bB2.name, bKn2.name, bR2.name],
                 [bP1.name, bP2.name, bP3.name, bP4.name, bP5.name, bP6.name, bP7.name, bP8.name],
                 ['0', '0', '0', '0', '0', '0', '0', '0'],
                 ['0', '0', '0', '0', '0', '0', '0', '0'],
                 ['0', '0', '0', '0', '0', '0', '0', '0'],
                 ['0', '0', '0', '0', '0', '0', '0', '0'],
                 [wP1.name, wP2.name, wP3.name, wP4.name, wP5.name, wP6.name, wP7.name, wP8.name],
                 [wR1.name, wKn1.name, wB1.name, wQ.name, wK.name, wB2.name, wKn2.name, wR2.name]
                 ])

play = move()
