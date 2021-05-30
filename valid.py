from itertools import permutations
from copy import deepcopy

from piece import *

# NOTE: top left is (0, 0)!

Coord = tuple[int, int]
def genvalidmoves(
        coord: Coord,
        board: list[list[str]],
        ep: tuple[list[Coord], list[Coord]],  # (white, black)
        castle: str
) -> tuple[
        list[Coord],
        tuple[list[Coord], list[Coord]],
        str,
]:
    """
    Generate every possible move for a piece, not incuding castling, EP or check
    """
    ret     = []

    if not fen2piece(board[coord[1]][coord[0]]):
        return ([], ep, castle)

    piecetype, piececol = fen2piece(board[coord[1]][coord[0]])

    # PAWN {
    dir = 0
    if piecetype == PIECES.P:
        if piececol == COL.WHITE:
            dir = -1
            if coord[1] == 6:
                ret.append((coord[0], coord[1] - 2))
        else:
            dir = 1
            if coord[1] == 1:
                ret.append((coord[0], coord[1] + 2))

        if not fen2piece(board[coord[1] + dir][coord[0]]):
            ret.append((coord[0], coord[1] + dir))

        # Capturing {
        # yes, this is filthy, but... it works.
        try:
            chk = board[coord[1] + dir][coord[0] + 1]
            if fen2piece(chk) and fen2piece(chk)[1] != piececol:
                ret.append((coord[0] + 1, coord[1] + dir))
        except IndexError:
            pass

        try:
            chk = board[coord[1] + dir][coord[0] - 1]
            if fen2piece(chk) and fen2piece(chk)[1] != piececol:
                ret.append((coord[0] - 1, coord[1] + dir))
        except IndexError:
            pass
        # }

        # En-passant -- a seperate case, because it's a stupid rule {
        for cep in ep[1]:  # white; check the black EP list
            if abs(cep[0] - coord[0]) == 1 and cep[1] - coord[1] == -1 and piececol == 'w':
                ret.append(cep)
        for cep in ep[0]:  # black; check the white EP list
            if abs(cep[0] - coord[0]) == 1 and cep[1] - coord[1] == 1 and piececol == 'b':
                ret.append(cep)
        # }
    # }

    # ROOK {
    elif piecetype == PIECES.R:
        # Horizontal right
        for i in range(coord[0] + 1, 8):
            if fen2piece(board[coord[1]][i]):
                if fen2piece(board[coord[1]][i])[1] != piececol:
                    ret.append((i, coord[1]))
                break
            ret.append((i, coord[1]))

        # Horizontal left
        for i in range(coord[0] - 1, -1, -1):
            if fen2piece(board[coord[1]][i]):
                if fen2piece(board[coord[1]][i])[1] != piececol:
                    ret.append((i, coord[1]))
                break
            ret.append((i, coord[1]))

        # Vertical up
        for i in range(coord[1] - 1, -1, -1):
            if fen2piece(board[i][coord[0]]):
                if fen2piece(board[i][coord[0]])[1] != piececol:
                    ret.append((coord[0], i))
                break
            ret.append((coord[0], i))

        # Vertical down
        for i in range(coord[1] + 1, 8):
            if fen2piece(board[i][coord[0]]):
                if fen2piece(board[i][coord[0]])[1] != piececol:
                    ret.append((coord[0], i))
                break
            ret.append((coord[0], i))

    # }

    # BISHOP {
    elif piecetype == PIECES.B:
        # Ugh loops
        i = coord[0]
        j = coord[1]
        while i <= 6 and j <= 6:
            i += 1
            j += 1
            if fen2piece(board[j][i]):
                if fen2piece(board[j][i])[1] != piececol:
                    ret.append((i, j))
                break
            ret.append((i, j))

        i = coord[0]
        j = coord[1]
        while i >= 1 and j >= 1:
            i -= 1
            j -= 1
            if fen2piece(board[j][i]):
                if fen2piece(board[j][i])[1] != piececol:
                    ret.append((i, j))
                break
            ret.append((i, j))

        i = coord[0]
        j = coord[1]
        while i <= 6 and j >= 1:
            i += 1
            j -= 1
            if fen2piece(board[j][i]):
                if fen2piece(board[j][i])[1] != piececol:
                    ret.append((i, j))
                break
            ret.append((i, j))

        i = coord[0]
        j = coord[1]
        while i <= 6 and j <= 6:
            i -= 1
            j += 1
            if fen2piece(board[j][i]):
                if fen2piece(board[j][i])[1] != piececol:
                    ret.append((i, j))
                break
            ret.append((i, j))
    # }

    # KNIGHT {
    elif piecetype == PIECES.N:
                     #
                    r=\
                  lambda\
                 x:tuple(\
                reversed(x\
            ));pass;(a)=lambda\
                x,y:(x[0]+\
            y[0],x[1]+y[1]);b=\
                lambda x,y\
               ,z:[x(a(y,z))
              ,x(a(y,r(z)))];
                    d=\
                 lambda f\
              ,x,y,z:[f(x,y,\
           z[ii])for ii in range
         (len(z))];d(b,ret.append,
         (coord[0],coord[1]),((1,\
         2),(1,-2),(-1,2),(-1,-2)\
                   ))+[1]
                    for\
                   (c)in\
                    ret:
                        try:
                            if fen2piece(board[c[1]][c[0]])[1]==\
                            piececol:ret=list(filter(lambda x: x\
                            !=c,ret))+[]+[]+[]+[]+[]+[]+[]+[]+[];
                        except (TypeError,IndexError):list(filter(lambda x:x!=c,ret))
    # }

    # KING {
    elif piecetype == PIECES.K:
        # Literally the same as Knight except for the numbers
                     #
                    r=\
                  lambda\
                 x:tuple(\
                reversed(x\
            ));pass;(a)=lambda\
                x,y:(x[0]+\
            y[0],x[1]+y[1]);b=\
                lambda x,y\
               ,z:[x(a(y,z))
              ,x(a(y,r(z)))];
                    d=\
                 lambda f\
              ,x,y,z:[f(x,y,\
           z[ii])for ii in range
         (len(z))];d(b,ret.append,
         (coord[0],coord[1]),tuple
         (permutations((1,0,-1,1,\
                -1))));pass
                    for\
                   (c)in\
                    ret:
                        try:
                            if fen2piece(board[c[1]][c[0]])[1]==\
                            piececol:ret=list(filter(lambda x: x\
                            !=c,ret))+[]+[]+[]+[]+[]+[]+[]+[]+[];
                        except (TypeError,IndexError):list(filter(lambda x:x!=c,ret))
    # }

    # QUEEN {
    elif piecetype == PIECES.Q:
        # Horizontal right
        for i in range(coord[0] + 1, 8):
            if fen2piece(board[coord[1]][i]):
                if fen2piece(board[coord[1]][i])[1] != piececol:
                    ret.append((i, coord[1]))
                break
            ret.append((i, coord[1]))

        # Horizontal left
        for i in range(coord[0] - 1, -1, -1):
            if fen2piece(board[coord[1]][i]):
                if fen2piece(board[coord[1]][i])[1] != piececol:
                    ret.append((i, coord[1]))
                break
            ret.append((i, coord[1]))

        # Vertical up
        for i in range(coord[1] - 1, -1, -1):
            if fen2piece(board[i][coord[0]]):
                if fen2piece(board[i][coord[0]])[1] != piececol:
                    ret.append((coord[0], i))
                break
            ret.append((coord[0], i))

        # Vertical down
        for i in range(coord[1] + 1, 8):
            if fen2piece(board[i][coord[0]]):
                if fen2piece(board[i][coord[0]])[1] != piececol:
                    ret.append((coord[0], i))
                break
            ret.append((coord[0], i))

        # Ugh more loops
        i = coord[0]
        j = coord[1]
        while i <= 6 and j <= 6:
            i += 1
            j += 1
            if fen2piece(board[j][i]):
                if fen2piece(board[j][i])[1] != piececol:
                    ret.append((i, j))
                break
            ret.append((i, j))

        i = coord[0]
        j = coord[1]
        while i >= 1 and j >= 1:
            i -= 1
            j -= 1
            if fen2piece(board[j][i]):
                if fen2piece(board[j][i])[1] != piececol:
                    ret.append((i, j))
                break
            ret.append((i, j))

        i = coord[0]
        j = coord[1]
        while i <= 6 and j >= 1:
            i += 1
            j -= 1
            if fen2piece(board[j][i]):
                if fen2piece(board[j][i])[1] != piececol:
                    ret.append((i, j))
                break
            ret.append((i, j))

        i = coord[0]
        j = coord[1]
        while i <= 6 and j <= 6:
            i -= 1
            j += 1
            if fen2piece(board[j][i]):
                if fen2piece(board[j][i])[1] != piececol:
                    ret.append((i, j))
                break
            ret.append((i, j))
    # }


    # OK
    return (ret, ep, castle)

# vim:foldmethod=marker:foldmarker={,}:
