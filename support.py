import pygame
import os
import sys
TILEWIDTH = 80
TILEHEIGHT = 80
WINDOWWIDTH = None
WINDOWHEIGHT = None
MOVEKEY = 0
DELTAX = 10
DELTAY = 10


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
    return list(map(lambda x: x.ljust(maxwidth, ' '), levelmap))
