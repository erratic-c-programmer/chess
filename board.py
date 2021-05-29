import pygame as pg
from typing import Callable, Union

import piece

Coord = tuple[int, int]


class Chessboard:
    def __init__(
            self,
            boxsize: Coord,
            boxes: Coord,
            colors: tuple[pg.Color, pg.Color],
    ) -> None:
        self.boxsize    = boxsize
        self.boxes      = boxes
        self.colors     = colors
        self.arr_rep    = [['' for _ in range(boxes[0])] for _ in range(boxes[1])]

        self.totalsize = (
            self.boxsize[0] * self.boxes[0],
            self.boxsize[1] * self.boxes[1]
        )

        self.board_surf = pg.Surface(self.totalsize)
        self.board_surf = self.board_surf.convert()
        self.enpassant  = ([], [])
        self.castle     = ""
        self.whitep     = True

    def drawboard(self):
        # Draw
        for i in range(self.boxes[0]):
            for j in range(self.boxes[1]):
                pg.draw.rect(
                    self.board_surf,
                    self.colors[(i + j) % 2],
                    (
                        i * self.boxsize[0],
                        j * self.boxsize[1]
                    )
                    + self.boxsize  # NOTE: tuple append
                )
        return

    def getsurf(self) -> pg.surface.Surface:
        self.drawboard()
        for i, l in enumerate(self.arr_rep):
            for j, p in enumerate(l):
                if p == '':
                    continue
                self.putitem(
                    piece.Piece(
                        p.upper(),
                        'w' if p.isupper() else 'b',
                        (self.boxsize[0], self.boxsize[1])
                    ).getsurf(),
                    (j, i)
                )
        return self.board_surf

    def getarr_rep(self):
        """
        Returns an array representation of the chessboard
        """
        return self.arr_rep

    def box2surf(self, box_coord: Coord) -> Coord:
        """
        Gets the top left corner of a square, given the square
        """
        return (
            self.boxsize[0] * box_coord[0],
            self.boxsize[1] * box_coord[1]
        )

    def surf2box(self, surf_coord: Coord) -> Coord:
        """
        Converts real coordinates to box coordinates
        """
        return (
            surf_coord[0] // self.boxsize[0],
            surf_coord[1] // self.boxsize[1]
        )

    def putitem(self, item_surf: pg.Surface, box_coord: Coord) -> None:
        """
        Blits a surface to a box
        """
        self.board_surf.blit(item_surf, self.box2surf(box_coord))
        return

    def putpiece(self, piece_char: str, box_coord: Coord) -> None:
        self.arr_rep[box_coord[1]][box_coord[0]] = piece_char

    def movpiece(
            self,
            startcoord: Coord,
            endcoord: Coord,
            valid_fn: Callable[
                [Coord, list[list[str]], tuple[list[Coord], list[Coord]], str],
                tuple[
                    list[Coord],
                    tuple[list[Coord], list[Coord]],
                    str
                ]
            ]
    ) -> bool:
        """
        Moves a piece if it's valid; we must handle some of en-passant here
        """
        spiece = piece.fen2piece(self.arr_rep[startcoord[1]][startcoord[0]])
        validmoves, self.enpassant, self.castle = valid_fn(
            startcoord, self.arr_rep, self.enpassant, self.castle
        )

        if endcoord in validmoves:
            # En-passant {
            if spiece and spiece[0] == piece.PIECES.P:
                # clear backlog {
                self.enpassant[not self.whitep].clear()
                # }

                # adding the square {
                if endcoord[1] - startcoord[1] == -2:  # white
                    self.enpassant[0].append((startcoord[0], startcoord[1] - 1))
                elif endcoord[1] - startcoord[1] == 2:  # black
                    self.enpassant[1].append((startcoord[0], startcoord[1] + 1))
                # }

                # capturing {
                ep_sqr = None
                if not piece.fen2piece(self.arr_rep[endcoord[1]][endcoord[0]]):  # not a normal cap
                    if endcoord[1] - startcoord[1] == -1:  # white
                        if endcoord[0] - startcoord[0] == 1 :  # right
                            ep_sqr = (startcoord[0] + 1, startcoord[1])
                        elif endcoord[0] - startcoord[0] == -1 :  # left
                            ep_sqr = (startcoord[0] - 1, startcoord[1])

                    # black
                    elif endcoord[1] - startcoord[1] == 1:
                        if endcoord[0] - startcoord[0] == 1:  # right
                            ep_sqr = (startcoord[0] + 1, startcoord[1])
                        if endcoord[0] - startcoord[0] == -1:  # left
                            ep_sqr = (startcoord[0] - 1, startcoord[1])

                    # ...and remove that piece
                    if ep_sqr:
                        self.arr_rep[ep_sqr[1]][ep_sqr[0]] = ''
                # }
            # }

            self.arr_rep[endcoord[1]][endcoord[0]] = \
                self.arr_rep[startcoord[1]][startcoord[0]]
            self.arr_rep[startcoord[1]][startcoord[0]] = ''

            self.whitep = not self.whitep
            return True

        else:
            return False

    def drawfen(self, fenstr: str) -> None:
        """
        Blits a FEN string onto a board
        """
        board_layout = fenstr.split(' ')[0]
        i = 0
        for c in board_layout.split('/'):
            j = 0
            for d in c:
                if d.isnumeric():
                    j += int(d)
                else:
                    self.putpiece(d, (j, i))
                    j += 1
            i += 1
        return

# vim:foldmethod=marker:foldmarker={,}:
