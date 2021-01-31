import numpy as np
from copy import deepcopy
import itertools
from colorama import Fore, Back

class Piece:
    def __init__(self, id, team, name):
        self.id = id
        self.team = team
        self.name = name

    def find_pos(self, board):
        """
        Function to find the indices of the piece chosen to be moved
        """
        i, j = np.where(board == self.id)
        i = int(i)
        j = int(j)

        return (i, j)

    def check_bounds(self, coord):
        """
        Checks if a move is out of the board
        """

        if (coord[0] > 7 or coord[0] < 0) or (coord[1] > 7 or coord[1] < 0) or (coord[0] > 7 and coord[1] < 0):
            return False

        return True

    def collision(self, coords, side):
        for i in coords:
            if backend[i[0]][i[1]].team == side:
                coords.remove(i)
            else:
                continue

        return coords


    def check_legal(self, init_square, final_square, side):
        """
        Function to check if the move made is legal
        """
        legal = False

        legal_moves = self.legal_moves(side)

        if final_square in legal_moves:
            legal = True

        else:
            legal = False

        return legal


class Pawn(Piece):
    cat = 'pawn'

    def legal_moves(self, side):
        coord = self.find_pos(board)
        legal = []
        if self.team == 'black':
            legal = [(coord[0]+1, coord[1])]
            attack_squares = self.attack_squares(side)

            for i in range(len(attack_squares)):
                if self.check_bounds(attack_squares[i]):
                    if backend[attack_squares[i][0]][attack_squares[i][1]].team == 'white':
                        legal.append(attack_squares[i])

        elif self.team == 'white':
            legal = [(coord[0]-1, coord[1])]
            attack_squares = self.attack_squares(side)

            for i in range(len(attack_squares)):
                if self.check_bounds(attack_squares[i]):
                    if backend[attack_squares[i][0]][attack_squares[i][1]].team == 'black':
                        legal.append(attack_squares[i])


        legal = self.collision(legal, self.team)

        return legal

    def attack_squares(self, side):
        coord = self.find_pos(board)
        if self.team == 'black':
            return [(coord[0]+1, coord[1]+1), (coord[0]+1, coord[1]-1)]

        elif self.team == 'white':
            return [(coord[0]-1, coord[1]+1), (coord[0]-1, coord[1]-1)]


class Rook(Piece):
    cat = 'rook'

    def legal_moves(self, side):
        """
        Iterates through row and column rook sits on, adds all available squares
        excluding one rook sits on
        """
        coord = self.find_pos(board)
        legal = []

        for i in range(coord[0], 0, -1):
            if backend[i][coord[1]] == backend[coord[0]][coord[1]]:
                continue

            elif backend[i][coord[1]].team == backend[coord[0]][coord[1]].team:
                break

            elif backend[i][coord[1]] != backend[coord[0]][coord[1]]:
                legal.append((i, coord[1]))

        for i in range(coord[0], len(backend)):
            if backend[i][coord[1]] == backend[coord[0]][coord[1]]:
                continue

            elif backend[i][coord[1]].team == backend[coord[0]][coord[1]].team:
                break

            elif backend[i][coord[1]] != backend[coord[0]][coord[1]]:
                legal.append((i, coord[1]))

        for i in range(coord[1], 0, -1):
            if backend[coord[0]][i] == backend[coord[0]][coord[1]]:
                continue

            elif backend[coord[0]][i].team == backend[coord[0]][coord[1]].team:
                break

            elif backend[coord[0]][i] != backend[coord[0]][coord[1]]:
                legal.append((coord[0],i))

        legal = self.collision(legal, self.team)
        return legal


class Bishop(Piece):
    cat = 'bishop'

    def legal_moves(self, side):

        coord = self.find_pos(board)
        in_bounds = self.check_bounds(coord)
        directions = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        legal = []

        for i in range(len(directions)):
            new_coord = deepcopy(coord)
            in_bounds = True
            while in_bounds == True:

                new_coord = (new_coord[0] + directions[i][0], new_coord[1] + directions[i][1])

                in_bounds = self.check_bounds(new_coord)
                if in_bounds == True:
                    if backend[new_coord[0]][new_coord[1]].team == backend[coord[0]][coord[1]].team:
                        break
                    else:
                        legal.append(new_coord)


        legal = self.collision(legal, self.team)
        return legal


class Knight(Piece):
    cat = 'knight'

    def legal_moves(self, side):

        coord = self.find_pos(board)

        mv_1 = (coord[0]-2, coord[1]-1)
        mv_2 = (coord[0]-1, coord[1]-2)
        mv_3 = (coord[0]+1, coord[1]-2)
        mv_4 = (coord[0]+2, coord[1]-1)
        mv_5 = (coord[0]+2, coord[1]+1)
        mv_6 = (coord[0]+1, coord[1]+2)
        mv_7 = (coord[0]-1, coord[1]+2)
        mv_8 = (coord[0]-2, coord[1]+1)

        legal = [mv_1, mv_2, mv_3, mv_4, mv_5, mv_6, mv_7, mv_8]
        indices = []
        legal2 = []
        for i in range(len(legal)):
            if (legal[i][0] > 7 or legal[i][0] < 0) or (legal[i][1] > 7 or legal[i][1] < 0):
                indices.append(i)

        for j in legal:
            if legal.index(j) in indices:
                continue
            else:
                legal2.append(j)

        legal2 = self.collision(legal2, self.team)

        return legal2


class King(Piece):
    cat = 'king'

    def check_squares(self, side):
        coord = self.find_pos(board)
        attack_matrix = [[0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0]]

        attacked = []
        for i in range(len(backend)):
           for j in range(len(backend[i])):
                if backend[i][j].team != side and backend[i][j].team != 'empty' and backend[i][j] != backend[coord[0]][coord[1]]:
                    attacked.append(backend[i][j].legal_moves(side))

        attacked = list(itertools.chain.from_iterable(attacked))
        for i in range(len(attacked)):
            attack_matrix[attacked[i][0]][attacked[i][1]] = 1

        return attacked

    def legal_moves(self, side):

        coord = self.find_pos(board)
        check = self.check_squares(side)
        mv_1 = (coord[0]-1, coord[1])
        mv_2 = (coord[0]-1, coord[1]-1)
        mv_3 = (coord[0], coord[1]-1)
        mv_4 = (coord[0]+1, coord[1]-1)
        mv_5 = (coord[0]+1, coord[1])
        mv_6 = (coord[0]+1, coord[1]+1)
        mv_7 = (coord[0], coord[1]+1)
        mv_8 = (coord[0]-1, coord[1]+1)

        legal = [mv_1, mv_2, mv_3, mv_4, mv_5, mv_6, mv_7, mv_8]
        indices = []
        legal2 = []
        legal3 = []
        for i in range(len(legal)):
            if (legal[i][0] > 7 or legal[i][0] < 0) or (legal[i][1] > 7 or legal[i][1] < 0):
                indices.append(i)

        for j in legal:
            if legal.index(j) in indices:
                continue
            else:
                legal2.append(j)

        for i in legal2:
            if i in check:
                continue
            else:
                legal3.append(i)


        legal3 = self.collision(legal3, self.team)
        return legal3




class Queen(Piece):
    cat = 'queen'

    def legal_moves(self, side):

        coord = self.find_pos(board)
        legal = []
        in_bounds = self.check_bounds(coord)
        directions = [(-1, -1), (1, -1), (1, 1), (-1, 1)]

        for i in range(len(directions)):
            new_coord = deepcopy(coord)
            in_bounds = True
            while in_bounds == True:

                new_coord = (new_coord[0] + directions[i][0], new_coord[1] + directions[i][1])

                in_bounds = self.check_bounds(new_coord)
                if in_bounds == True:
                    if backend[new_coord[0]][new_coord[1]].team == backend[coord[0]][coord[1]].team:
                        break
                    else:
                        legal.append(new_coord)

        for i in range(coord[0], 0, -1):
            if backend[i][coord[1]] == backend[coord[0]][coord[1]]:
                continue

            elif backend[i][coord[1]].team == backend[coord[0]][coord[1]].team:
                break

            elif backend[i][coord[1]] != backend[coord[0]][coord[1]]:
                legal.append((i, coord[1]))

        for i in range(coord[0], len(backend)):
            if backend[i][coord[1]] == backend[coord[0]][coord[1]]:
                continue

            elif backend[i][coord[1]].team == backend[coord[0]][coord[1]].team:
                break

            elif backend[i][coord[1]] != backend[coord[0]][coord[1]]:
                legal.append((i, coord[1]))

        for i in range(coord[1], 0, -1):
            if backend[coord[0]][i] == backend[coord[0]][coord[1]]:
                continue

            elif backend[coord[0]][i].team == backend[coord[0]][coord[1]].team:
                break

            elif backend[coord[0]][i] != backend[coord[0]][coord[1]]:
                legal.append((coord[0],i))

        legal = list(set(legal))
        legal = self.collision(legal, self.team)

        return legal

class Empty(Piece):
    cat = 'empty'

def translate(l, n):
    """
    Function translates chess square e.g. 'A6', to array index e.g. [0][2]
    """

    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    numbers = [7, 6, 5, 4, 3, 2, 1, 0]
    number_index = int(n)-1

    number = numbers[number_index]
    letter = letters.index(l)

    return (number, letter)

def decideColor(x, y):
    white = Fore.RED
    black = Fore.GREEN
    empty = Fore.WHITE
    if backend[x][y].team == 'black':
        ret_str = black

    elif backend[x][y].team == 'empty':
        ret_str = empty
    else:
        ret_str = white
    return ret_str

def nicePrint():
    print('   ', f'a b c d e f g h \n' \
     f'{Fore.WHITE}  8' ,f'{decideColor(0, 0)}{backend[0][0].name}', f'{decideColor(0, 1)}{backend[0][1].name}', f'{decideColor(0, 2)}{backend[0][2].name}', f'{decideColor(0, 3)}{backend[0][3].name}', f'{decideColor(0, 4)}{backend[0][4].name}', f'{decideColor(0, 5)}{backend[0][5].name}', f'{decideColor(0, 6)}{backend[0][6].name}', f'{decideColor(0, 7)}{backend[0][7].name}', f'{Fore.WHITE} 8\n', \
     f'{Fore.WHITE} 7', f'{decideColor(1, 0)}{backend[1][0].name}', f'{decideColor(1, 1)}{backend[1][1].name}', f'{decideColor(1, 2)}{backend[1][2].name}', f'{decideColor(1, 3)}{backend[1][3].name}', f'{decideColor(1, 4)}{backend[1][4].name}', f'{decideColor(1, 5)}{backend[1][5].name}', f'{decideColor(1, 6)}{backend[1][6].name}', f'{decideColor(1, 2)}{backend[1][7].name}', f'{Fore.WHITE} 7\n', \
     f'{Fore.WHITE} 6', f'{decideColor(2, 0)}{backend[2][0].name}', f'{decideColor(2, 1)}{backend[2][1].name}', f'{decideColor(2, 2)}{backend[2][2].name}', f'{decideColor(2, 3)}{backend[2][3].name}', f'{decideColor(2, 4)}{backend[2][4].name}', f'{decideColor(2, 5)}{backend[2][5].name}', f'{decideColor(2, 6)}{backend[2][6].name}', f'{decideColor(2, 7)}{backend[2][7].name}', f'{Fore.WHITE} 6\n', \
     f'{Fore.WHITE} 5', f'{decideColor(3, 0)}{backend[3][0].name}', f'{decideColor(3, 1)}{backend[3][1].name}', f'{decideColor(3, 2)}{backend[3][2].name}', f'{decideColor(3, 3)}{backend[3][3].name}', f'{decideColor(3, 4)}{backend[3][4].name}', f'{decideColor(3, 5)}{backend[3][5].name}', f'{decideColor(3, 6)}{backend[3][6].name}', f'{decideColor(3, 7)}{backend[3][7].name}', f'{Fore.WHITE} 5\n', \
     f'{Fore.WHITE} 4', f'{decideColor(4, 0)}{backend[4][0].name}', f'{decideColor(4, 1)}{backend[4][1].name}', f'{decideColor(4, 2)}{backend[4][2].name}', f'{decideColor(4, 3)}{backend[4][3].name}', f'{decideColor(4, 4)}{backend[4][4].name}', f'{decideColor(4, 5)}{backend[4][5].name}', f'{decideColor(4, 6)}{backend[4][6].name}', f'{decideColor(4, 7)}{backend[4][7].name}', f'{Fore.WHITE} 4\n', \
     f'{Fore.WHITE} 3', f'{decideColor(5, 0)}{backend[5][0].name}', f'{decideColor(5, 1)}{backend[5][1].name}', f'{decideColor(5, 2)}{backend[5][2].name}', f'{decideColor(5, 3)}{backend[5][3].name}', f'{decideColor(5, 4)}{backend[5][4].name}', f'{decideColor(5, 5)}{backend[5][5].name}', f'{decideColor(5, 6)}{backend[5][6].name}', f'{decideColor(5, 7)}{backend[5][7].name}', f'{Fore.WHITE} 3\n', \
     f'{Fore.WHITE} 2', f'{decideColor(6, 0)}{backend[6][0].name}', f'{decideColor(6, 1)}{backend[6][1].name}', f'{decideColor(6, 2)}{backend[6][2].name}', f'{decideColor(6, 3)}{backend[6][3].name}', f'{decideColor(6, 4)}{backend[6][4].name}', f'{decideColor(6, 5)}{backend[6][5].name}', f'{decideColor(6, 6)}{backend[6][6].name}', f'{decideColor(6, 7)}{backend[6][7].name}', f'{Fore.WHITE} 2\n', \
     f'{Fore.WHITE} 1', f'{decideColor(7, 0)}{backend[7][0].name}', f'{decideColor(7, 1)}{backend[7][1].name}', f'{decideColor(7, 2)}{backend[7][2].name}', f'{decideColor(7, 3)}{backend[7][3].name}', f'{decideColor(7, 4)}{backend[7][4].name}', f'{decideColor(7, 5)}{backend[7][5].name}', f'{decideColor(7, 6)}{backend[7][6].name}', f'{decideColor(7, 7)}{backend[7][7].name}', f'{Fore.WHITE} 1\n',
     '  ', 'a b c d e f g h')


def move(side):
    start = input('Enter piece square: ')
    final = input('Enter move square: ')

    l = start[0]
    n = start[1]
    l2 = final[0]
    n2 = final[1]
    init_square = translate(l, n)
    final_square = translate(l2, n2)

    if backend[init_square[0]][init_square[1]].team == side:

        val = backend[init_square[0]][init_square[1]]

        is_legal = val.check_legal(init_square, final_square, side)

        if is_legal == True:
            print('Legal')
            backend[init_square[0]][init_square[1]] = e
            backend[final_square[0]][final_square[1]] = val
            board[init_square[0]][init_square[1]] = e.id
            board[final_square[0]][final_square[1]] = val.id

            nicePrint()

        else:
            print('Illegal, try again.')
            move(side)

    else:
        print('Pick your own piece please.')
        move(side)

def game():
    i = 0
    playing = True
    nicePrint()
    print('CTRL-C to quit.')

    while playing:
        if i % 2 == 0:
            side = 'white'

        else:
            side = 'black'
        pl = move(side)
        i += 1

# black pawns
bP1 = Pawn('bP1', 'black', 'P')
bP2 = Pawn('bP2', 'black', 'P')
bP3 = Pawn('bP3', 'black', 'P')
bP4 = Pawn('bP4', 'black', 'P')
bP5 = Pawn('bP5', 'black', 'P')
bP6 = Pawn('bP6', 'black', 'P')
bP7 = Pawn('bP7', 'black', 'P')
bP8 = Pawn('bP8', 'black', 'P')

# white pawns
wP1 = Pawn('wP1', 'white', 'P')
wP2 = Pawn('wP2', 'white', 'P')
wP3 = Pawn('wP3', 'white', 'P')
wP4 = Pawn('wP4', 'white', 'P')
wP5 = Pawn('wP5', 'white', 'P')
wP6 = Pawn('wP6', 'white', 'P')
wP7 = Pawn('wP7', 'white', 'P')
wP8 = Pawn('wP8', 'white', 'P')

# black rooks
bR1 = Rook('bR1', 'black', 'R')
bR2 = Rook('bR2', 'black', 'R')

# white rooks
wR1 = Rook('wR1', 'white', 'R')
wR2 = Rook('wR2', 'white', 'R')

# black knights
bKn1 = Knight('bKn1', 'black', 'N')
bKn2 = Knight('bKn2', 'black', 'N')

# white knights
wKn1 = Knight('wKn1', 'white', 'N')
wKn2 = Knight('wKn2', 'white', 'N')

# black bishops
bB1 = Bishop('bB1', 'black', 'B')
bB2 = Bishop('bB2', 'black', 'B')

# white bishops
wB1 = Bishop('wB1', 'white', 'B')
wB2 = Bishop('wB2', 'white', 'B')

# black royals
bQ = Queen('bQ', 'black', 'Q')
bK = King('bK', 'black', 'K')

# white royals
wQ = Queen('wQ', 'white', 'Q')
wK = King('wK', 'white', 'K')

# empty
e = Empty('x', 'empty', 'x')

backend = np.array([[bR1, bKn1, bB1, bQ, bK, bB2, bKn2, bR2],
                 [bP1, bP2, bP3, bP4, bP5, bP6, bP7, bP8],
                 [e, e, e, e, e, e, e, e],
                 [e, e, e, e, e, e, e, e],
                 [e, e, e, e, e, e, e, e],
                 [e, e, e, e, e, e, e, e],
                 [wP1, wP2, wP3, wP4, wP5, wP6, wP7, wP8],
                 [wR1, wKn1, wB1, wQ, wK, wB2, wKn2, wR2]
                 ])

board = np.array([[bR1.id, bKn1.id, bB1.id, bQ.id, bK.id, bB2.id, bKn2.id, bR2.id],
                 [bP1.id, bP2.id, bP3.id, bP4.id, bP5.id, bP6.id, bP7.id, bP8.id],
                 [e.id, e.id, e.id, e.id, e.id, e.id, e.id, e.id],
                 [e.id, e.id, e.id, e.id, e.id, e.id, e.id, e.id],
                 [e.id, e.id, e.id, e.id, e.id, e.id, e.id, e.id],
                 [e.id, e.id, e.id, e.id, e.id, e.id, e.id, e.id],
                 [wP1.id, wP2.id, wP3.id, wP4.id, wP5.id, wP6.id, wP7.id, wP8.id],
                 [wR1.id, wKn1.id, wB1.id, wQ.id, wK.id, wB2.id, wKn2.id, wR2.id]
                 ])

play = game()
