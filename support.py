import pygame
import os
import sys
import math
import random
MENUNEW1 = (566, 191)
MENUNEW2 = (861, 274)
MENULOAD1 = (874, 290)
MENULOAD2 = (1159, 381)
MENURULE1 = (569, 420)
MENURULE2 = (859, 508)
MENUEXIT1 = (872, 538)
MENUEXIT2 = (1164, 633)
MENU = 1
RULE = 2
SAVE = 3
GAME = 4
GAMEMENU = 5
DUKE = 1
PISTOL = 2
AUTOMAT = 3
SHOTGUN = 4
NOLIMITWEAPON = -1
TILEWIDTH = 80
TILEHEIGHT = 80
WINDOWWIDTH = None
WINDOWHEIGHT = None
FPS = 60
ANIMATEREGULAR = 30
PDX = 8
PDY = 8
EDX = 4
EDY = 4
MXRX = 10
MXRY = 6
MAINTYPE = '1'
WALLTYPES = '2'
PLAYERTYPE = '@'
MAINSLOT = DUKE
ANIMATEKEY = 0
MOVEKEY = 1
DETECTKEY = 2
SHOOTKEY = 3
RELOADKEY = 4
TAKEKEY = 5
CHANGEKEY = 6


def calculateDegree(px, py, sc):
    hyp = (px ** 2 + py ** 2) ** 0.5
    if not hyp:
        return 0, 1
    sin = py / hyp
    rad = math.asin(sin)
    sc /= 180 / math.pi
    rad += (random.random() - 0.5) * 2 * sc
    sin = math.sin(rad)
    cos = math.cos(rad)
    if px < 0:
        cos = -cos
    return sin, cos


def loadImage(name, colorkey=None):
    fullname = os.path.join('data/image/', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def make_playlist():
    melodies = ['BFG_Division.mp3', 'Damnation.mp3', 'Rip_Tear.mp3', 'Skullhacker.mp3', 'The_New_Order.mp3']
    x = len(melodies)
    playl = []
    while len(playl) != x:
        new = random.choice(melodies)
        new1 = os.path.join('data/music/', new)
        playl.append(new1)
        melodies.pop(melodies.index(new))
    return playl


def loadLevel(num):
    filename = os.path.join('data/level/', str(num) + '.txt')
    if not os.path.isfile(filename):
        print(f"Файл с картой '{filename}' не найден")
        sys.exit()
    with open(filename, 'r') as mapfile:
        levelmap = [list(line.strip()) for line in mapfile]
    maxwidth = max(map(len, levelmap))
    return levelmap
