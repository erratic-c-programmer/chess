#! /usr/bin/python
import pygame as pg

import board
import valid

SQ_X = 60
SQ_Y = 60
SQ_GAP = 1
SQ_COL1 = pg.Color(255, 255, 255)
SQ_COL2 = pg.Color(139, 69, 19)

pg.init()
screen = pg.display.set_mode((SQ_X * 8, SQ_Y * 8))

b = board.Chessboard((SQ_X, SQ_Y), (8, 8), (SQ_COL1, SQ_COL2))
b.drawfen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

running_p = True

selected = None
while running_p:
    pg.time.wait(50)
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            running_p = False
        elif ev.type == pg.MOUSEBUTTONDOWN:
            if not selected:
                selected = b.surf2box(pg.mouse.get_pos())
                print(selected)
            else:  # piece has already been chosen
                b.movpiece(selected, b.surf2box(pg.mouse.get_pos()), valid.genvalidmoves)
                selected = None

    screen.blit(b.getsurf(), (0, 0))

    pg.display.flip()

pg.quit()
