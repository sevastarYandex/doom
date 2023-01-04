import pygame
import support
allgroup = pygame.sprite.Group()
tilegroup = pygame.sprite.Group()
herogroup = pygame.sprite.Group()
tileimg = {'1': 'lava.png'} # тут картинки и их номера блоков
playerimg = 'player.png'


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__(allgroup)
        self.add(tilegroup)
        self.image = support.loadImage(tileimg[type])
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(allgroup)
        self.add(herogroup)
        self.image = support.loadImage(playerimg)
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )

    def shoot(self):
        pass

    def fight(self):
        pass

    def update(self):
        pass


class Camera:
    def __init__(self):
        pass


class Particle(pygame.sprite.Sprite):
    def __init__(self):
        pass


class Shower:
    pass


def generatelevel(level):
    player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                player = Hero(x, y)
            elif level[y][x] != ' ':
                Tile(x, y, level[y][x])
    return player
