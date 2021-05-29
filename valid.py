from piece import *

# NOTE: top left is (0, 0)!

def genvalidmoves(coord: tuple[int, int], board: list[list[str]]) -> list[tuple[int, int]]:
    """
    Generate every possible move for a piece, not incuding blocking, castling, EP or check
    No bound-checking!
    """
    if not fen2piece(board[coord[1]][coord[0]]):
        return []

    piecetype, piececol = fen2piece(board[coord[1]][coord[0]])

    ret = []

    # PAWN
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

        ret.append((coord[0], coord[1] + dir))

        # Capturing
        # yes, this is filthy, but... it works.
        try:
            chk = board[coord[1] + dir][coord[0] + 1]
            print(fen2piece(chk))
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

        print(ret)

    # ROOK
    elif piecetype == PIECES.R:
        for i in range(8):
            ret += [(i, coord[1])]
            ret += [(coord[0], i)]

    # BISHOP
    elif piecetype == PIECES.B:
        # Ugh loops
        i = coord[0]
        j = coord[1]
        while i <= 7 and j <= 7:
            i += 1
            j += 1
            ret.append((i, j))

        i = coord[0]
        j = coord[1]
        while i >= 0 and j >= 0:
            i -= 1
            j -= 1
            ret.append((i, j))

        i = coord[0]
        j = coord[1]
        while i <= 7 and j >= 0:
            i += 1
            j -= 1
            ret.append((i, j))

        i = coord[0]
        j = coord[1]
        while i <= 7 and j <= 7:
            i -= 1
            j += 1
            ret.append((i, j))

    # KNIGHT
    elif piecetype == PIECES.N:
        # Hardcoded, whatever.
        r = lambda x: tuple(reversed(x))
        a = lambda x, y: (x[0] + y[0], x[1] + y[1])
        b = lambda x, y, z: x(a(y, z)) or x(a(y, r(z)))
        b(ret.append, (coord[0], coord[1]), (1, 2))
        b(ret.append, (coord[0], coord[1]), (1, -2))
        b(ret.append, (coord[0], coord[1]), (-1, 2))
        b(ret.append, (coord[0], coord[1]), (-1, -2))
        print(ret)

    # KING
    elif piecetype == PIECES.K:
        for m0 in (coord[0] + 1, coord[1] - 1):
            for m1 in (coord[0] + 1, coord[0] - 1):
                if (m0 <= 7 or m1 <= 7 or m0 >= 0 or m1 >= 0):
                    ret.append((m0, m1))
                    ret.append((m1, m0))

    # QUEEN
    elif piecetype == PIECES.Q:
        for i in range(8):
            ret += [(i, coord[1])]
            ret += [(coord[0], i)]

        # Ugh more loops
        i = coord[0]
        j = coord[1]
        while i <= 7 and j <= 7:
            i += 1
            j += 1
            ret.append((i, j))

        i = coord[0]
        j = coord[1]
        while i >= 0 and j >= 0:
            i -= 1
            j -= 1
            ret.append((i, j))

        i = coord[0]
        j = coord[1]
        while i <= 7 and j >= 0:
            i += 1
            j -= 1
            ret.append((i, j))

        i = coord[0]
        j = coord[1]
        while i <= 7 and j <= 7:
            i -= 1
            j += 1
            ret.append((i, j))


    # OK
    return ret
