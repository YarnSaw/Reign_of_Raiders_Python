import pygame as py
FPS = 60
WIDTH = 1024
HEIGHT = 768
TITLE = "Reign of Raiders" 
font="Emulogic"

ground=[(0,HEIGHT-40,WIDTH,40)]

pygameKeys = [py.K_a,py.K_b,py.K_c,py.K_d,py.K_e,py.K_f,py.K_g,py.K_h,py.K_i,py.K_j,py.K_k,py.K_l,py.K_m,
              py.K_n,py.K_o,py.K_p,py.K_q,py.K_r,py.K_s,py.K_t,py.K_u,py.K_v,py.K_w,py.K_x,py.K_y,py.K_z,
              py.K_RIGHT,py.K_LEFT,py.K_UP,py.K_DOWN,py.K_SPACE]
pygameLetters = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
                 'n','o','p','q','r','s','t','u','v','w','x','y','z',
                 'Right Arrow','Left Arrow','Up Arrow','Down Arrow','Space']

jumpKey = pygameKeys[25]
shootKey = pygameKeys[23]
reloadKey = pygameKeys[2]
drawGunKey = pygameKeys[5]
moveLeftKey = pygameKeys[27]
moveRightKey = pygameKeys[26]
enterDoorKey = pygameKeys[28]
skillKey = pygameKeys[18]

SPEED = 8
JUMP = 15
GRAVITY = 0.5

grey = (150,150,150)
black = (0,0,0)
blue = (0,0,255)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
darkGrey = (40,40,40)
purple = (255,0,255)
