import sys
import pygame
import support
allgroup = pygame.sprite.Group()
wallgroup = pygame.sprite.Group()
entitygroup = pygame.sprite.Group()
herogroup = pygame.sprite.Group()
bulletgroup = pygame.sprite.Group()
weapongroup = pygame.sprite.Group()
tileimg = {'1': 'lava.png', '2': 'wall.png'}
playerimg = {'@': 'player.png'}
enemyimg = {'a': 'enemy.png'}
bulletimg = {'1': 'enemy.png', '2': 'enemy.png',
             '3': 'enemy.png', '4': 'enemy.png'}
weaponimg = {'1': 'enemy.png', '2': 'enemy.png',
             '3': 'enemy.png', '4': 'enemy.png'}
backimg = 'back.png'
emptyimg = 'empty.png'


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__(allgroup)
        if type in support.WALLTYPES:
            self.add(wallgroup)
        self.image = support.loadImage(tileimg[type])
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, sin, cos, type):
        super().__init__(allgroup, bulletgroup)
        self.dist = 0
        self.x = x
        self.y = y
        self.shift = 0
        self.sin = sin
        self.cos = cos
        self.maxrange = 0
        self.damage = 0
        self.image = support.loadImage(bulletimg[type])
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update(self):
        self.x += self.shift * self.cos
        self.y += self.shift * self.sin
        self.rect.x = self.x
        self.rect.y = self.y
        self.dist += self.shift
        for sprite in wallgroup:
            if pygame.sprite.collide_mask(sprite, self):
                self.hurt()
                return
        if self.dist >= self.maxrange:
            self.kill()

    def hurt(self, target):
        # дописать
        self.kill()


class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__(allgroup, weapongroup)
        self.bulletdmg = 0 # насколько дамажит пуля
        self.bulletmxr = 0 # насколько далеко летит пуля
        self.bullettype = 0 # тип пули
        self.bulletshift = 0 # сколько пролетает пуля за единицу времени
        self.bulletpershot = 0 # пуль за выстрел
        self.scatter = 0 # разброс
        self.ammo = 0 # сколько магазинов
        self.store = 0 # максимальное кол-во пуль в магазине
        self.nowstore = 0 # сколько пуль сейчас в магазине
        self.shoottime = 0 # минимальная разница по времени между выстрелами (в мс)
        self.reloadtime = 0 # время перезарядки (в мс)
        self.clock = pygame.time.Clock()
        self.beforenextshoot = 0 # сколько ещё нельзя стрелять (в мс)
        self.image = support.loadImage(weaponimg[type])
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )
        self.host = None

    def sethost(self, host):
        self.image = support.loadImage(emptyimg)
        self.rect.move(host.x, host.y)
        self.host = host

    def update(self):
        if self.host is None:
            return
        self.rect.move(self.host.x, self.host.y)

    def shoot(self, pos):
        amount = min(self.nowstore, self.bulletpershot)
        if not amount:
            return False
        # тоже музон нужен
        cx = self.rect.x + self.rect.w // 2
        cy = self.rect.y + self.rect.h // 2
        px, py = pos
        for _ in range(amount):
            sin, cos = support.calculateDegree(cx, cy, px, py, self.scatter)
            Bullet(cx, cy, sin, cos, self.bullettype)
        return True

    def reload(self):
        self.beforenextshoot -= self.clock.tick()
        if self.beforenextshoot > 0:
            return False
        # тут музончик
        if not self.ammo:
            self.nowstore = 0
            return True
        self.ammo -= 1
        self.nowstore = self.store
        self.beforenextshoot = self.reloadtime
        return True

    def click(self, pos):
        self.beforenextshoot -= self.clock.tick()
        if self.beforenextshoot <= 0:
            self.shoot(pos)
            self.beforenextshoot = self.shoottime
            return True
        return False


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, img):
        super().__init__(allgroup, wallgroup, entitygroup)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.frames = []
        self.frame = 0
        self.cut(img)
        self.image = self.frames[self.frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * self.x,
            support.TILEHEIGHT * self.y
        )
        self.dx = 0
        self.dy = 0
        self.rx = 0
        self.ry = 0
        self.weapon = None

    def cut(self, img):
        sheet = support.loadImage(img)
        cols = sheet.get_width() // self.w
        rows = sheet.get_height() // self.h
        self.frames = [sheet.subsurface(
            pygame.Rect((self.w * (ind % cols), self.h * (ind // cols)), (self.w, self.h)))
        for ind in range(cols * rows)]

    def animate(self):
        self.frame = (self.frame + 1) % len(self.frames)
        self.image = self.frames[self.frame]
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, dx, dy, check=True, good=None):
        self.x += self.dx * dx
        self.y += self.dy * dy
        self.rect.x = self.x
        self.rect.y = self.y
        if not check:
            return
        for sprite in wallgroup:
            if pygame.sprite.collide_mask(self, sprite):
                if type(sprite) != good and sprite != self:
                    self.move(-dx, -dy, False)
                    return

    def detect(self, target):
        difx = abs(self.x - target.x) - support.TILEWIDTH
        dify = abs(self.y - target.y) - support.TILEHEIGHT
        if difx > self.rx or dify > self.ry:
            return
        if difx < 0 and dify < 0:
            return
        dx = (target.x > self.x) - (self.x > target.x)
        dy = (target.y > self.y) - (self.y > target.y)
        self.move(dx, 0)
        self.move(0, dy)

    def shoot(self, angle):
        pass

    def update(self, key, *args):
        if key == support.ANIMATEKEY:
            self.animate(*args)
        if key == support.MOVEKEY:
            self.move(*args)
        if key == support.DETECTKEY:
            self.detect(*args)
        if key == support.SHOOTKEY:
            self.shoot(*args)


class Player(Entity):
    def __init__(self, x, y, type):
        super().__init__(x, y,
                         support.TILEWIDTH, support.TILEHEIGHT,
                         playerimg[type])
        self.add(herogroup)
        self.dx = support.PDX
        self.dy = support.PDY

    def detect(self, *args):
        return


class Enemy(Entity):
    def __init__(self, x, y, type):
        super().__init__(x, y,
                         support.TILEWIDTH, support.TILEHEIGHT,
                         enemyimg[type])
        self.dx = support.EDX
        self.dy = support.EDY
        self.rx = support.MXRX * support.TILEWIDTH
        self.ry = support.MXRY * support.TILEHEIGHT

    def move(self, dx, dy, check=True, good=None):
        super().move(dx, dy, check, Enemy)


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
        self.upd = 0
        self.camera = Camera()

    def stop(self):
        self.show = False

    def isgoing(self):
        return self.show

    def setLevel(self, levelnum=1):
        self.levelnum = levelnum
        level = support.loadLevel(self.levelnum)
        self.player = generatelevel(level)

    def animate(self):
        if not self.upd:
            entitygroup.update(support.ANIMATEKEY)
        self.upd += 1
        self.upd %= support.ANIMATEREGULAR

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
    Back()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in tileimg:
                Tile(x, y, level[y][x])
            elif level[y][x] != ' ':
                Tile(x, y, support.MAINTYPE)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in enemyimg:
                Enemy(x, y, level[y][x])
            elif level[y][x] in playerimg:
                player = Player(x, y, level[y][x])
    return player
