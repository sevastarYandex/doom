import sys
import pygame
import support
allgroup = pygame.sprite.Group()
wallgroup = pygame.sprite.Group()
entitygroup = pygame.sprite.Group()
herogroup = pygame.sprite.Group()
walltypes = ['2']
tileimg = {'1': 'lava.png', '2': 'wall.png'}
playerimg = 'player.png'
enemyimg = {'a': 'enemy.png'}
backimg = 'back.png'


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__(allgroup)
        if type in walltypes:
            self.add(wallgroup)
        self.image = support.loadImage(tileimg[type])
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__(allgroup, wallgroup, entitygroup)
        self.image = support.loadImage(img)
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )
        self.x = self.rect.x
        self.y = self.rect.y
        self.dx = 0
        self.dy = 0
        self.rx = 0
        self.ry = 0
        self.weapon = None

    def move(self, dx, dy, check=True):
        self.x += self.dx * dx
        self.y += self.dy * dy
        self.rect.x = self.x
        self.rect.y = self.y
        if not check:
            return
        if len(pygame.sprite.spritecollide(self, wallgroup, False)) > 1:
            self.move(-dx, -dy, False)

    def detect(self, target):
        difx = abs(self.x - target.x)
        dify = abs(self.y - target.y)
        if difx > self.rx or dify > self.ry:
            return
        dx = (target.x > self.x) - (self.x > target.x)
        dy = (target.y > self.y) - (self.y > target.y)
        self.move(dx, 0)
        self.move(0, dy)

    def shoot(self, angle):
        pass

    def update(self, key, *args):
        if key == support.MOVEKEY:
            self.move(*args)
        if key == support.DETECTKEY:
            self.detect(*args)
        if key == support.SHOOTKEY:
            self.shoot(*args)


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, playerimg)
        self.add(herogroup)
        self.dx = support.PDX
        self.dy = support.PDY

    def detect(self, *args):
        return


class Enemy(Entity):
    def __init__(self, x, y, type):
        super().__init__(x, y, enemyimg[type])
        self.dx = support.EDX
        self.dy = support.EDY
        self.rx = support.MXRX * support.TILEWIDTH
        self.ry = support.MXRY * support.TILEHEIGHT


class Back(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(allgroup)
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
        if isinstance(obj, Entity):
            obj.x = obj.rect.x
            obj.y = obj.rect.y

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

    def isgoing(self):
        return self.show

    def setLevel(self, levelnum=1):
        self.levelnum = levelnum
        level = support.loadLevel(self.levelnum)
        self.player = generatelevel(level)

    def move(self, dx, dy):
        herogroup.update(support.MOVEKEY, dx, dy)

    def detect(self):
        entitygroup.update(support.DETECTKEY, self.player)

    def draw(self, screen):
        self.camera.update(self.player)
        for sprite in allgroup:
            if type(sprite) == Back:
                continue
            self.camera.apply(sprite)
        allgroup.draw(screen)


def generatelevel(level):
    player = None
    px, py = None, None
    Back()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x].isdigit():
                Tile(x, y, level[y][x])
            else:
                Tile(x, y, support.MAINTYPE)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x].isalpha():
                Enemy(x, y, level[y][x])
            elif level[y][x] == '@':
                px = x
                py = y
    return Player(px, py)
