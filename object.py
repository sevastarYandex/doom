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
# до сюда оставляем
playerimg = {support.KNIFE: 'playerknife.png',
             support.PISTOL: 'playerpistol.png',
             support.AUTOMAT: 'playerautomat.png',
             support.SHOTGUN: 'playershotgun.png'}
enemyimg = {support.KNIFE: 'enemy.png'}
bulletimg = {'z': 'knife.png',
             'y': 'bullet.png',
             'x': 'bullet.png',
             'w': 'bullet.png'}
bulletspec = {'z': (40, 300, 30),
              'y': (50, 600, 25),
              'x': (40, 400, 10),
              'w': (100, 300, 10)}
# скорость, расстояние и урон (в хп)
weaponimg = {'z': 'knife.png',
             'y': 'pistol.png',
             'x': 'automat.png',
             'w': 'shotgun.png'}
weaponspec = {'z': (1, 2, 1, 10, 1000, 0),
              'y': (1, 0, 3, 20, 350, 800),
              'x': (1, 3, 3, 30, 50, 1600),
              'w': (12, 6, 3, 84, 600, 3200)}
enemyhealth = {'a': 100, 'b': 50}
enemyweapon = {}
# пуль за выстрел, разброс в градусах, количество магазинов и их ёмкость
# скорострельность и время перезарядки
backimg = 'back.png'
emptyimg = 'empty.png'


class FloatSprite(pygame.sprite.Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        self.x, self.y = 0, 0

    def setxy(self):
        self.x = self.rect.x
        self.y = self.rect.y

    def syncxy(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def setmask(self):
        self.mask = pygame.mask.from_surface(self.image)


class Tile(FloatSprite):
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
        self.setxy()


class Bullet(FloatSprite):
    def __init__(self, x, y, sin, cos, friend, type):
        super().__init__(allgroup, bulletgroup)
        self.dist = 0
        self.sin = sin
        self.cos = cos
        self.shift, self.maxrange, self.damage = bulletspec[type]
        self.image = support.loadImage(bulletimg[type])
        self.setmask()
        self.rect = self.image.get_rect().move(x, y)
        self.rect = self.rect.move(-self.rect.w // 2, -self.rect.h // 2)
        self.friend = friend
        self.setxy()

    def update(self):
        self.x += self.shift * self.cos
        self.y += self.shift * self.sin
        self.syncxy()
        self.dist += self.shift
        if self.dist >= self.maxrange:
            self.damage = 0
        for sprite in wallgroup:
            if pygame.sprite.collide_mask(sprite, self) and type(sprite) != self.friend:
                self.hurt(sprite)
                self.kill()
                return

    def hurt(self, target):
        if not self.damage:
            return
        if not isinstance(target, Entity):
            return
        target.suffer(self.damage)


class Weapon(FloatSprite):
    def __init__(self, x, y, type):
        super().__init__(allgroup, weapongroup)
        self.friend = None
        self.nowstore = 0 # сколько пуль сейчас в магазине
        self.beforenextshoot = 0 # сколько ещё нельзя стрелять (в мс)
        self.bullettype = type # тип пули
        self.bulletpershot, self.scatter, self.ammo, \
        self.store, self.shoottime, self.reloadtime = weaponspec[type]
        self.clock = pygame.time.Clock()
        self.image = support.loadImage(weaponimg[type])
        self.setmask()
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )
        self.host = None
        self.settype(type)
        self.reload()
        self.setxy()
        if self.weapontype == support.KNIFE:
            self.nowstore = self.store
            self.ammo = 0

    def merge(self, other):
        host1, host2 = self.host, other.host
        self.sethost(host2)
        other.sethost(host1)

    def setammo(self, ammo):
        if self.weapontype == support.KNIFE:
            self.nowstore += ammo
            return
        self.ammo += ammo

    def getammo(self):
        if self.weapontype == support.KNIFE:
            return self.nowstore
        return self.ammo

    def settype(self, type):
        if type in support.KNIFETYPES:
            self.weapontype = support.KNIFE
            return
        if type in support.PISTOLTYPES:
            self.weapontype = support.PISTOL
            return
        if type in support.AUTOMATTYPES:
            self.weapontype = support.AUTOMAT
            return
        if type in support.SHOTGUNTYPES:
            self.weapontype = support.SHOTGUN

    def sethost(self, host):
        if isinstance(host, Entity):
            self.rect = self.rect.move(
                host.x - self.x,
                host.y - self.y
            )
            self.syncxy()
            self.image = support.loadImage(emptyimg)
        else:
            self.image = support.loadImage(weaponimg[self.bullettype])
        self.setmask()
        self.host = host
        self.friend = type(self.host)

    def update(self):
        if self.host is None:
            return
        self.x = self.host.x
        self.y = self.host.y
        self.syncxy()

    def shoot(self, pos):
        amount = min(self.nowstore, self.bulletpershot)
        if amount <= 0:
            return
        # тоже музон нужен
        self.nowstore -= amount
        cx = self.x + self.rect.w // 2
        cy = self.y + self.rect.h // 2
        px, py = pos
        px -= cx
        py -= cy
        for _ in range(amount):
            sin, cos = support.calculateDegree(px, py, self.scatter)
            Bullet(cx, cy, sin, cos, self.friend, self.bullettype)

    def reload(self):
        if self.weapontype == support.KNIFE:
            return
        self.beforenextshoot -= self.clock.tick()
        if self.beforenextshoot > 0:
            return
        # тут музончик
        if not self.ammo:
            self.nowstore = 0
            return
        self.ammo -= 1
        self.nowstore = self.store
        self.beforenextshoot = self.reloadtime
        return

    def click(self, pos):
        self.beforenextshoot -= self.clock.tick()
        if self.beforenextshoot <= 0:
            self.shoot(pos)
            self.beforenextshoot = self.shoottime


class Entity(FloatSprite):
    def __init__(self, x, y, w, h, health, imglist, type):
        super().__init__(allgroup, wallgroup, entitygroup)
        self.weapons = {support.KNIFE: None,
                        support.PISTOL: None,
                        support.AUTOMAT: None,
                        support.SHOTGUN: None}
        self.health = health
        self.weapon = type
        self.w = w
        self.h = h
        self.frames = []
        self.frame = 0
        self.imglist = imglist
        self.cut(self.imglist[self.weapon])
        self.image = self.frames[self.frame]
        self.setmask()
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )
        self.setxy()
        self.dx = 0
        self.dy = 0
        self.rx = 0
        self.ry = 0

    def getweapon(self):
        return self.weapons[self.weapon]

    def suffer(self, hp):
        self.health -= hp
        if self.health <= 0:
            self.kill()

    def setweapon(self, weapon):
        myweapon = self.weapons[weapon.weapontype]
        if myweapon is not None:
            weapon.merge(myweapon)
            if weapon.bullettype == myweapon.bullettype:
                weapon.setammo(myweapon.getammo())
                myweapon.setammo(-myweapon.getammo())
        else:
            weapon.sethost(self)
        self.weapon = weapon.weapontype
        self.weapons[self.weapon] = weapon
        img = self.imglist[self.weapon]
        self.cut(img)

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
        self.setmask()

    def move(self, dx, dy, check=True, good=None):
        self.x += self.dx * dx
        self.y += self.dy * dy
        self.syncxy()
        if not check:
            return
        for sprite in wallgroup:
            if pygame.sprite.collide_mask(self, sprite):
                if type(sprite) != good and sprite != self:
                    self.move(-dx, -dy, False)
                    return
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
        return

    def shoot(self, pos):
        weapon = self.getweapon()
        if weapon is None:
            return
        weapon.click(pos)

    def reload(self):
        weapon = self.getweapon()
        if weapon is None:
            return
        weapon.reload()

    def take(self):
        for sprite in weapongroup:
            if pygame.sprite.collide_mask(self, sprite):
                self.setweapon(sprite)
                return

    def change(self, key):
        if self.weapons[key] is not None:
            if self.weapons[key].getammo():
                self.weapon = key
                self.cut(self.imglist[self.weapon])

    def update(self, *args):
        if not args:
            return
        key = args[0]
        args = args[1:]
        if key == support.ANIMATEKEY:
            self.animate(*args)
        if key == support.MOVEKEY:
            self.move(*args)
        if key == support.DETECTKEY:
            self.detect(*args)
        if key == support.SHOOTKEY:
            self.shoot(*args)
        if key == support.RELOADKEY:
            self.reload(*args)
        if key == support.TAKEKEY:
            self.take(*args)
        if key == support.CHANGEKEY:
            self.change(*args)


class Player(Entity):
    def __init__(self, x, y, health, type):
        super().__init__(x, y,
                         support.TILEWIDTH, support.TILEHEIGHT, health,
                         playerimg, type)
        self.add(herogroup)
        self.dx = support.PDX
        self.dy = support.PDY

    def detect(self, *args):
        return


class Enemy(Entity):
    def __init__(self, x, y, health, type):
        super().__init__(x, y,
                         support.TILEWIDTH, support.TILEHEIGHT, health,
                         enemyimg, type)
        self.dx = support.EDX
        self.dy = support.EDY
        self.rx = support.MXRX * support.TILEWIDTH
        self.ry = support.MXRY * support.TILEHEIGHT

    def move(self, dx, dy, check=True, good=None):
        super().move(dx, dy, check, Enemy)


class Back(FloatSprite):
    def __init__(self):
        super().__init__(allgroup)
        self.image = pygame.transform.scale(support.loadImage(backimg),
                                            (support.WINDOWWIDTH, support.WINDOWHEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.setxy()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.x += self.dx
        obj.y += self.dy
        obj.syncxy()

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - support.WINDOWWIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - support.WINDOWHEIGHT // 2)


class Shower:
    def __init__(self, levelnum=1):
        self.setLevel(levelnum)
        self.show = True
        self.upd = 0
        self.camera = Camera()

    def update(self):
        self.detect()
        self.animate()
        allgroup.update()

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

    def shoot(self, pos):
        herogroup.update(support.SHOOTKEY, pos)

    def reload(self):
        herogroup.update(support.RELOADKEY)

    def take(self):
        herogroup.update(support.TAKEKEY)

    def change(self, key):
        herogroup.update(support.CHANGEKEY, key)

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
            if level[y][x] in enemyweapon:
                Enemy(x, y, level[y][x])
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in weaponimg:
                Weapon(x, y, level[y][x])
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == support.PLAYERTYPE:
                player = Player(x, y)
    return player
