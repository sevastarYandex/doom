import pygame
import support
import random
import math
allgroup = pygame.sprite.Group()
tilegroup = pygame.sprite.Group()
herogroup = pygame.sprite.Group()
backgroup = pygame.sprite.Group()
wallgroup = pygame.sprite.Group()
shotguns = pygame.sprite.Group()
automats = pygame.sprite.Group()
pistols = pygame.sprite.Group()
knifes = pygame.sprite.Group()
bullets = pygame.sprite.Group()
tileimg = {'1': 'lava.png', '2': 'wall.png'}
playerimg = 'playerknife.png'
backimg = 'back.png'
shotgunimg = 'shotgun.png'
automatimg = 'automat.png'
pistolimg = 'pistol.png'
bulletimg = 'bullet.png'
shotgun_list = []
pistol_list = []
automat_list = []


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__(allgroup)
        self.add(tilegroup)
        if type == '2':
            self.add(wallgroup)
        self.image = support.loadImage(tileimg[type])
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )


class Pistol(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, ammo):
        super().__init__(allgroup)
        self.add(pistols)
        self.image = support.loadImage(pistolimg)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )
        self.dx = support.DELTAX
        self.dy = support.DELTAY
        self.x = self.rect.x
        self.y = self.rect.y
        self.dam = damage
        self.ammo = ammo

    def get_info(self):
        return [self.dam, self.ammo]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, range, dam, deg):
        super().__init__(allgroup)
        self.add(bullets)
        self.x = x
        self.y = y
        self.deg = deg
        self.range = range
        self.dam = dam
        self.image = support.loadImage(bulletimg)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            x + 40,
            y + 40)

    def update(self):
        self.rect = self.rect.move(math.cos(self.deg) * 80, math.sin(self.deg) * 80)
        self.exist = True
        for sprite in wallgroup:
            if pygame.sprite.collide_mask(self, sprite):
                self.exist = False
        if not self.exist:
            self.kill()


class Shotgun(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, ammo):
        super().__init__(allgroup)
        self.add(shotguns)
        self.image = support.loadImage(shotgunimg)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )
        self.dx = support.DELTAX
        self.dy = support.DELTAY
        self.x = self.rect.x
        self.y = self.rect.y
        self.dam = damage
        self.ammo = ammo

    def get_info(self):
        return [self.dam, self.ammo]


class Automat(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, ammo):
        super().__init__(allgroup)
        self.add(automats)
        self.image = support.loadImage(automatimg)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )
        self.dx = support.DELTAX
        self.dy = support.DELTAY
        self.x = self.rect.x
        self.y = self.rect.y
        self.dam = damage
        self.ammo = ammo

    def get_info(self):
        return [self.dam, self.ammo]


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(allgroup)
        self.add(herogroup)
        self.sg = False
        self.ag = False
        self.pis = False
        self.automats = []
        self.pistols = []
        self.shotguns = []
        self.now_weapon = "knife"
        self.image = support.loadImage(playerimg)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )
        self.dx = support.DELTAX
        self.dy = support.DELTAY
        self.x = self.rect.x
        self.y = self.rect.y

    def get_reload(self):
        if self.now_weapon == "knife":
            return 180
        elif self.now_weapon == "pistol":
            return 60
        elif self.now_weapon == "automat":
            return 12
        else:
            return 120

    def update(self, key, *args):
        if key == support.MOVEKEY:
            self.move(*args)

    def move(self, dx, dy):
        self.x += dx * self.dx
        self.y += dy * self.dy
        self.rect.x = self.x
        self.rect.y = self.y
        for sprite in wallgroup:
            if pygame.sprite.collide_mask(self, sprite):
                self.move(-dx, -dy)
                return
        for sprite in automat_list:
            if pygame.sprite.collide_mask(self, sprite) and self.ag is False:
                self.ag = True
                self.automats = sprite.get_info()
                sprite.kill()
        for sprite in pistol_list:
            if pygame.sprite.collide_mask(self, sprite) and self.pis is False:
                self.pis = True
                self.pistols = sprite.get_info()
                sprite.kill()
        for sprite in shotgun_list:
            if pygame.sprite.collide_mask(self, sprite) and self.sg is False:
                self.sg = True
                self.shotguns = sprite.get_info()
                sprite.kill()

    def take_weapon(self):
        for sprite in automat_list:
            if pygame.sprite.collide_mask(self, sprite) and self.ag is True:
                self.ag = True
                self.automats = sprite.get_info()
                sprite.kill()
        for sprite in pistol_list:
            if pygame.sprite.collide_mask(self, sprite) and self.pis is True:
                self.pis = True
                self.pistols = sprite.get_info()
                sprite.kill()
        for sprite in shotgun_list:
            if pygame.sprite.collide_mask(self, sprite) and self.sg is True:
                self.sg = True
                self.shotguns = sprite.get_info()
                sprite.kill()

    def change_weapon(self, weapon):
        if weapon == 'shotgun':
            if self.sg is True:
                self.now_weapon = 'shotgun'
        elif weapon == 'pistol':
            if self.pis is True:
                self.now_weapon = 'pistol'
        elif weapon == 'automat':
            if self.ag is True:
                self.now_weapon = 'automat'
        elif weapon == 'knife':
            self.now_weapon = 'knife'
        playerimg = 'player' + self.now_weapon + '.png'
        self.image = support.loadImage(playerimg)

    def shoot(self, pos):
        self.hor = pos[0] - (support.WINDOWWIDTH // 2)
        self.ver = pos[1] - (support.WINDOWHEIGHT // 2)
        self.tg = self.ver / self.hor
        self.deg = (math.atan(self.tg))
        if self.deg < 0:
            self.deg += 2 * math.pi
        if self.hor < 0:
            if self.ver < 0:
                self.deg += math.pi
            else:
                self.deg -= math.pi
        if self.now_weapon == "knife":
            pass
        elif self.now_weapon == "pistol":
            if self.pistols[1] != 0:
                bullet = Bullet(self.x, self.y, 700, self.pistols[0], self.deg)
                self.pistols[1] -= 1
        elif self.now_weapon == "automat":
            if self.automats[1] != 0:
                self.change = random.randint(-5, 5)
                self.change = self.change * math.pi / 180
                self.deg += self.change
                bullet = Bullet(self.x, self.y, 700, self.automats[0], self.deg)
                self.automats[1] -= 1
        elif self.now_weapon == "shotgun":
            if self.shotguns[1] != 0:
                for i in range(12):
                    self.change = random.randint(-30 + (5 * i), -30 + (5 + 5 * i))
                    self.change = self.change * math.pi / 180
                    self.degi = self.deg + self.change
                    bullet = Bullet(self.x, self.y, 700, self.shotguns[0], self.degi)
                self.shotguns[1] -= 1


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
        if isinstance(obj, Player):
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

    def draw(self, screen):
        backgroup.draw(screen)
        self.camera.update(self.player)
        for sprite in allgroup:
            self.camera.apply(sprite)
        allgroup.draw(screen)
        herogroup.draw(screen)


def generatelevel(level):
    Back()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] != ' ':
                Tile(x, y, level[y][x])
    pl = False
    while pl is False:
        y = random.randint(0, len(level) - 1)
        x = random.randint(0, len(level[y]) - 1)
        if level[y][x] == "1":
            player = Player(x, y)
            pl = True
    for i in range(2):
        pl = False
        while pl is False:
            y = random.randint(0, len(level) - 1)
            x = random.randint(0, len(level[y]) - 1)
            if level[y][x] == "1":
                shotgun_list.append(Shotgun(x, y, 100, 2))
                pl = True
    for i in range(2):
        pl = False
        while pl is False:
            y = random.randint(0, len(level) - 1)
            x = random.randint(0, len(level[y]) - 1)
            if level[y][x] == "1":
                pistol_list.append(Pistol(x, y, 100, 10))
                pl = True
    for i in range(2):
        pl = False
        while pl is False:
            y = random.randint(0, len(level) - 1)
            x = random.randint(0, len(level[y]) - 1)
            if level[y][x] == "1":
                automat_list.append(Automat(x, y, 100, 30))
                pl = True
    return player

