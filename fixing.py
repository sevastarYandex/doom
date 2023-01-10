from object import *
import pygame
import support



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