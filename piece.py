import os
import pygame as pg
from types import SimpleNamespace
from typing import Union

from pathconf import *

# colors
COL = SimpleNamespace(
    WHITE = 'w',
    BLACK = 'b'
)
# pieces
PIECES = SimpleNamespace(
    K = 'K',
    P = 'P',
    Q = 'Q',
    R = 'R',
    B = 'B',
    N = 'N'
)

def fen2piece(pchr: str) -> Union[tuple[str, str], None]:
    """
    Converts a FEN piece to a (piece, color) pair
    """
    piecetype = pchr.upper()
    piececol = 'w' if pchr.isupper() else 'b'
    return (piecetype, piececol) if piecetype != '' else None


class Piece:
    def __init__(
            self,
            piecetype: str,
            color: str,
            size: tuple[int, int]
    ) -> None:
        self.piecetype  = piecetype
        self.color      = color
        self.size       = size

        prefix = 'w' if color == COL.WHITE else 'b'
        self.imgpath = os.path.join(
            ASSETSDIR,
            PIECESDIR,
            prefix + self.piecetype + ASSETEXT
        )
        self.imgsurf = pg.image.load(self.imgpath)
        self.imgsurf = pg.transform.scale(self.imgsurf, size)
        self.imgsurf.convert_alpha()
        return

    def getsurf(self) -> pg.Surface:
        return self.imgsurf
