import pygame
import support
allgroup = pygame.sprite.Group()
tilegroup = pygame.sprite.Group()
herogroup = pygame.sprite.Group()
tileimg = {} # тут картинки и их номера блоков


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__(allgroup)
        self.add(tilegroup)
        self.image = img
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        pass

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
