import pygame as pg
from typing import Callable

import piece

class Chessboard:
    def __init__(
            self,
            boxsize: tuple[int, int],
            boxes: tuple[int, int],
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

    def box2surf(self, box_coord: tuple[int, int]) -> tuple[int, int]:
        """
        Gets the top left corner of a square, given the square
        """
        return (
            self.boxsize[0] * box_coord[0],
            self.boxsize[1] * box_coord[1]
        )

    def surf2box(self, surf_coord: tuple[int, int]) -> tuple[int, int]:
        """
        Converts real coordinates to box coordinates
        """
        return (
            surf_coord[0] // self.boxsize[0],
            surf_coord[1] // self.boxsize[1]
        )

    def putitem(self, item_surf: pg.Surface, box_coord: tuple[int, int]) -> None:
        """
        Blits a surface to a box
        """
        self.board_surf.blit(item_surf, self.box2surf(box_coord))
        return

    def putpiece(self, piece_char: str, box_coord: tuple[int, int]) -> None:
        self.arr_rep[box_coord[1]][box_coord[0]] = piece_char

    def movpiece(
            self,
            startcoord: tuple[int, int],
            endcoord: tuple[int, int],
            valid_fn: Callable[[tuple[int, int], list[list[str]]], list[tuple[int, int]]]
    ) -> bool:
        validmoves = valid_fn(startcoord, self.arr_rep)
        if endcoord in validmoves:
            self.arr_rep[endcoord[1]][endcoord[0]] = \
                self.arr_rep[startcoord[1]][startcoord[0]]
            self.arr_rep[startcoord[1]][startcoord[0]] = ''
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
