import pygame
import support
allgroup = pygame.sprite.Group()
tilegroup = pygame.sprite.Group()


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
    pass


class Camera:
    pass


class Particle(pygame.sprite.Sprite):
    pass
