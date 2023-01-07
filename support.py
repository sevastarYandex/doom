import pygame
import os
import sys
import math
import random
TILEWIDTH = 80
TILEHEIGHT = 80
WINDOWWIDTH = None
WINDOWHEIGHT = None
FPS = 72
ANIMATEREGULAR = 5
PDX = 8
PDY = 8
EDX = 4
EDY = 4
MXRX = 10
MXRY = 6
MAINTYPE = '1'
WALLTYPES = ['2']
ANIMATEKEY = 0
MOVEKEY = 1
DETECTKEY = 2
SHOOTKEY = 3


def calculateDegree(cx, cy, px, py, sc):
    px -= cx
    py -= cy
    hyp = (px ** 2 + py ** 2) ** 0.5
    sin = py / hyp
    rad = math.asin(sin)
    rad += random.randint(-sc, sc)
    return math.sin(rad), math.cos(rad)


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


def loadLevel(num):
    filename = os.path.join('data/level/', str(num) + '.txt')
    if not os.path.isfile(filename):
        print(f"Файл с картой '{filename}' не найден")
        sys.exit()
    with open(filename, 'r') as mapfile:
        levelmap = [line.strip() for line in mapfile]
    maxwidth = max(map(len, levelmap))
    return levelmap
