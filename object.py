import pygame
import support
allgroup = pygame.sprite.Group()
tilegroup = pygame.sprite.Group()
herogroup = pygame.sprite.Group()
backgroup = pygame.sprite.Group()
tileimg = {'1': 'lava.png'}
playerimg = 'player.png'
backimg = 'back.png'


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__(allgroup)
        self.add(tilegroup)
        self.image = support.loadImage(tileimg[type])
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(allgroup)
        self.add(herogroup)
        self.image = support.loadImage(playerimg)
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )


class Back(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.add(backgroup)
        self.image = pygame.transform.scale(support.loadImage(backimg),
                                            (support.WINDOWWIDTH, support.WINDOWHEIGHT))
        self.rect = self.image.get_rect().move(0, 0)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - support.WINDOWWIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - support.WINDOWHEIGHT // 2)


class Shower:
    def __init__(self, levelnum=1):
        self.setLevel(levelnum)
        self.show = True
        self.camera = Camera()

    def stop(self):
        self.show = False

    def isshow(self):
        return self.show

    def setLevel(self, levelnum=1):
        self.levelnum = levelnum
        level = support.loadLevel(self.levelnum)
        self.player = generatelevel(level)

    def move(self):
        allgroup.update()

    def draw(self, screen):
        backgroup.draw(screen)
        self.camera.update(self.player)
        for sprite in allgroup:
            self.camera.apply(sprite)
        allgroup.draw(screen)


def generatelevel(level):
    player = None
    Back()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                player = Player(x, y)
            elif level[y][x] != ' ':
                Tile(x, y, level[y][x])
    return player
