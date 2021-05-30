#! /usr/bin/python
import pygame as pg

import board
import valid

SQ_X = 100
SQ_Y = 100
SQ_GAP = 1
SQ_COL1 = pg.Color(118,150,86)
SQ_COL2 = pg.Color(238,238,210)

pg.init()
screen = pg.display.set_mode((SQ_X * 8, SQ_Y * 8))

b = board.Chessboard((SQ_X, SQ_Y), (8, 8), (SQ_COL1, SQ_COL2))
b.drawfen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

running_p = True

cbox    = None
cbox_o  = None
piece_selected_p = False

# Circle
csurf = pg.Surface((SQ_X, SQ_Y))
csurf.fill((0, 0, 0))
csurf.set_colorkey((0, 0, 0))
pg.draw.circle(
    csurf,
    pg.Color(111, 199, 135, 200),
    (SQ_X / 2, SQ_Y / 2),
    SQ_X / 6,
)
csurf = csurf.convert_alpha()

while running_p:
    pg.time.wait(50)
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            running_p = False
        elif ev.type == pg.MOUSEBUTTONDOWN:
            cbox_o  = cbox
            cbox    = b.surf2box(pg.mouse.get_pos())

    ###

    if not piece_selected_p:
        if cbox and b.getsqr(cbox):  # clicked on piece
            piece_selected_p = True
    else:
        if cbox_o:
            piece_selected_p = not b.movpiece(cbox_o, cbox, valid.genvalidmoves)
            cbox = cbox_o = None
        else:
            try:  # ...ew.
                for c in b.getvalidmovs(cbox, valid.genvalidmoves):
                    b.putitem(csurf, c)
            except TypeError:
                pass

    ###

    screen.blit(b.getsurf(), (0, 0))

    pg.display.flip()

pg.quit()
