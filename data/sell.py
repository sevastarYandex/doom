import pygame as pg
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    return image


class Pixel(pg.sprite.Sprite):

    def __init__(self, i, j, num):
        super().__init__(all_sprites)
        x = "p" + num + ".png"
        self.image = load_image(x)
        self.rect = self.image.get_rect()
        self.rect.x = i * 10
        self.rect.y = j * 10


f = open('testxx.txt', 'r', encoding='utf-8')
sc = pg.display.set_mode((0, 0), pg.FULLSCREEN)
lines = f.readlines()
all_sprites = pg.sprite.Group()
for i in range(len(lines)):
    for j in range(len(lines[i])):
        num = lines[i][j]
        if num != '\n':
            Pixel(j, i, num)
while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
    sc.fill((0, 0, 0))
    all_sprites.draw(sc)
    pg.time.delay(100)
    pg.display.flip()