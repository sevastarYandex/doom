import sys
import pygame
import support
allgroup = pygame.sprite.Group()
wallgroup = pygame.sprite.Group()
herogroup = pygame.sprite.Group()
enemygroup = pygame.sprite.Group()
entitygroup = pygame.sprite.Group()
bulletgroup = pygame.sprite.Group()
weapongroup = pygame.sprite.Group()
emptyimg = 'back/empty.png'
tileimg = {'1': 'tile/ground.png',
           '2': 'tile/wall.png'}
bulletimg = {'z': 'back/empty.png',
             'y': 'bullet/usual.png',
             'x': 'bullet/usual.png',
             'w': 'bullet/usual.png'}
bulletspec = {'z': (40, 300, 30),
              'y': (50, 600, 25),
              'x': (40, 400, 10),
              'w': (100, 300, 10)}
weaponimg = {'z': 'weapon/duke.png',
             'y': 'weapon/pistol.png',
             'x': 'weapon/automat.png',
             'w': 'weapon/shotgun.png'}
weaponspec = {'z': (support.DUKE, 1, support.NOLIMITWEAPON, 1, 1, 1, 700, 0),
              'y': (support.PISTOL, 1, 2, 10, 10, 2, 600, 1000),
              'x': (support.AUTOMAT, 1, 3, 30, 30, 4, 200, 2000),
              'w': (support.SHOTGUN, 12, 7, 1, 7, 6, 800, 600)}
playerimg = {support.DUKE: 'player/duke.png',
             support.PISTOL: 'player/pistol.png',
             support.AUTOMAT: 'player/automat.png',
             support.SHOTGUN: 'player/shotgun.png'}
enemyimg = {'a': {support.DUKE: 'enemy/duke.png',
                  support.PISTOL: 'enemy/pistol.png',
                  support.AUTOMAT: 'enemy/automat.png',
                  support.SHOTGUN: 'enemy/shotgun.png'}}
entityspec = {'@': (100000, ('z',)),
              'a': (50, ('y',))}
backimg = 'back/dungeon.png'


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
        self.setmask()
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
            if pygame.sprite.collide_rect(sprite, self) and type(sprite) != self.friend:
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
        self.type = type
        self.kind = weaponspec[self.type][0]
        self.friendtype = None
        self.host = None
        self.bps = weaponspec[self.type][1]
        self.ammo = weaponspec[self.type][2]
        self.store = weaponspec[self.type][3]
        self.maxstore = weaponspec[self.type][4]
        self.nowstore = self.maxstore
        self.scatter = weaponspec[self.type][5]
        self.shoottime = weaponspec[self.type][6]
        self.reloadtime = weaponspec[self.type][7]
        self.beforenextshoot = 0
        self.clock = pygame.time.Clock()
        self.image = support.loadImage(weaponimg[self.type])
        self.setmask()
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )
        self.setxy()

    def merge(self, other):
        host1, host2 = self.host, other.host
        self.sethost(host2)
        other.sethost(host1)

    def addammo(self, ammo):
        if self.getammo() == support.NOLIMITWEAPON:
            return
        self.ammo += ammo

    def getammo(self):
        return self.ammo

    def sethost(self, host):
        if isinstance(host, Entity):
            self.x = host.x
            self.y = host.y
            self.syncxy()
            self.image = support.loadImage(emptyimg)
        else:
            self.image = support.loadImage(weaponimg[self.type])
        self.setmask()
        self.host = host
        self.friendtype = type(self.host)

    def update(self):
        if self.host is None:
            return
        self.x = self.host.x
        self.y = self.host.y
        self.syncxy()

    def shoot(self, pos):
        if self.ammo == support.NOLIMITWEAPON:
            self.nowstore = 1
        if not self.nowstore:
            return
        # тоже музон нужен
        self.nowstore -= 1
        cx = self.x + self.rect.w // 2
        cy = self.y + self.rect.h // 2
        px, py = pos
        px -= cx
        py -= cy
        for _ in range(self.bps):
            sin, cos = support.calculateDegree(px, py, self.scatter)
            Bullet(cx, cy, sin, cos, self.friendtype, self.type)

    def reload(self):
        if self.ammo == support.NOLIMITWEAPON:
            return
        self.beforenextshoot -= self.clock.tick()
        if self.beforenextshoot > 0:
            return
        # тут музончик
        if not self.ammo:
            return
        if self.nowstore == self.maxstore:
            return
        self.ammo -= 1
        self.nowstore = min(self.maxstore, self.nowstore + self.store)
        self.beforenextshoot = self.reloadtime
        return

    def click(self, pos):
        self.beforenextshoot -= self.clock.tick()
        if self.beforenextshoot <= 0:
            self.shoot(pos)
            self.beforenextshoot = self.shoottime


class Entity(FloatSprite):
    def __init__(self, x, y, w, h, type, imglist, curslot):
        super().__init__(allgroup, wallgroup, entitygroup)
        self.weapons = {support.DUKE: None,
                        support.PISTOL: None,
                        support.AUTOMAT: None,
                        support.SHOTGUN: None}
        self.imglist = imglist
        self.w = w
        self.h = h
        self.health = entityspec[type][0]
        self.maxhealth = self.health
        self.currentwp = support.MAINSLOT
        for t in entityspec[type][1]:
            weapon = Weapon(0, 0, t)
            self.setweapon(weapon)
        if curslot is not None:
            self.change(curslot)
        self.frames = []
        self.curframe = -1
        self.cut(self.imglist[self.currentwp])
        self.animate()
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
        return self.weapons[self.currentwp]

    def suffer(self, hp):
        self.health -= hp
        if self.health <= 0:
            self.kill()

    def setweapon(self, weapon):
        myweapon = self.weapons[weapon.kind]
        if myweapon is not None:
            weapon.merge(myweapon)
            if weapon.type == myweapon.type:
                weapon.addammo(myweapon.getammo())
                myweapon.addammo(-myweapon.getammo())
        else:
            weapon.sethost(self)
        self.currentwp = weapon.kind
        self.weapons[self.currentwp] = weapon
        img = self.imglist[self.currentwp]
        self.cut(img)

    def cut(self, img):
        sheet = support.loadImage(img)
        cols = sheet.get_width() // self.w
        rows = sheet.get_height() // self.h
        self.frames = [sheet.subsurface(
            pygame.Rect((self.w * (ind % cols), self.h * (ind // cols)), (self.w, self.h)))
        for ind in range(cols * rows)]
        self.masks = [pygame.mask.from_surface(frame) for frame in self.frames]

    def animate(self):
        self.curframe = (self.curframe + 1) % len(self.frames)
        self.image = self.frames[self.curframe]
        self.mask = self.masks[self.curframe]

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
        self.shoot((target.x + target.w // 2, target.y + target.h // 2))
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
        if not weapon.getammo() and not weapon.nowstore:
            self.change(support.MAINSLOT)

    def reload(self):
        weapon = self.getweapon()
        if weapon is None:
            return
        weapon.reload()
        if not weapon.getammo() and not weapon.nowstore:
            self.change(support.MAINSLOT)

    def take(self):
        for sprite in weapongroup:
            if pygame.sprite.collide_mask(self, sprite):
                self.setweapon(sprite)
                return

    def change(self, key):
        if self.weapons[key] is None:
            return
        weapon = self.weapons[key]
        if not weapon.getammo() and not weapon.nowstore:
            return
        self.currentwp = key
        img = self.imglist[self.currentwp]
        self.cut(img)

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
    def __init__(self, x, y):
        super().__init__(x, y, support.TILEWIDTH, support.TILEHEIGHT,
                         support.PLAYERTYPE, playerimg,
                         support.DUKE)
        self.add(herogroup)
        self.dx = support.PDX
        self.dy = support.PDY


class Enemy(Entity):
    def __init__(self, x, y, type):
        super().__init__(x, y, support.TILEWIDTH, support.TILEHEIGHT,
                         type, enemyimg[type], support.DUKE)
        self.add(enemygroup)
        self.dx = support.EDX
        self.dy = support.EDY
        self.rx = support.MXRX * support.TILEWIDTH
        self.ry = support.MXRY * support.TILEHEIGHT

    def move(self, dx, dy, check=True, good=None):
        super().move(dx, dy, check, Enemy)

    def reload(self):
        weapon = self.getweapon()
        if weapon is not None:
            self.weapons[self.currentwp].addammo(weapon.store * 2)
        super().reload()

    def shoot(self, pos):
        super().shoot(pos)
        if not self.getweapon().nowstore:
            self.reload()


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
        enemygroup.update(support.DETECTKEY, self.player)

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
            if level[y][x] in weaponimg:
                Weapon(x, y, level[y][x])
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in enemyimg:
                Enemy(x, y, level[y][x])
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == support.PLAYERTYPE:
                player = Player(x, y)
    return player
