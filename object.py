import sys
import pygame
import support
pygame.init()
k = pygame.mixer.Sound('data/music/knife.wav')
k.set_volume(0.5)
a = pygame.mixer.Sound('data/music/auto.wav')
a.set_volume(0.5)
p = pygame.mixer.Sound('data/music/pistol.wav')
p.set_volume(0.5)
s = pygame.mixer.Sound('data/music/shotgun.wav')
s.set_volume(0.5)
r = pygame.mixer.Sound('data/music/reload.wav')
r.set_volume(0.5)
allgroup = pygame.sprite.Group()
wallgroup = pygame.sprite.Group()
herogroup = pygame.sprite.Group()
enemygroup = pygame.sprite.Group()
entitygroup = pygame.sprite.Group()
bulletgroup = pygame.sprite.Group()
weapongroup = pygame.sprite.Group()
medicinegroup = pygame.sprite.Group()
armorgroup = pygame.sprite.Group()
emptyimg = 'back/empty.png'
tileimg = {'1': 'tile/ground.png',
           '2': 'tile/wall.png',
           '3': 'tile/home.png',
           '4': 'tile/water.png'}
bulletimg = {'z': 'back/empty.png',
             'y': 'bullet/usual.png',
             'x': 'bullet/usual.png',
             'w': 'bullet/usual.png'}
bulletspec = {'z': (40, 300, 2),
              'y': (50, 700, 25),
              'x': (40, 700, 10),
              'w': (80, 400, 10)}
medicineimg = {'+': 'medicine/20.png',
               '*': 'medicine/80.png'}
medicinespec = {'+': (20,),
                '*': (80,)}
backgroup = pygame.sprite.Group()
armorimg = {'}': 'armor/1.25.png',
            '{': 'armor/2.5.png'}
armorspec = {'}': (1.25,),
             '{': (2.5,)}
weaponimg = {'z': 'weapon/duke.png',
             'y': 'weapon/pistol.png',
             'x': 'weapon/automat.png',
             'w': 'weapon/shotgun.png'}
weaponspec = {'z': (support.DUKE, 15, support.NOLIMITWEAPON, 1, 1, 6, 700, 0),
              'y': (support.PISTOL, 1, 10, 10, 10, 2, 600, 1000),
              'x': (support.AUTOMAT, 1, 3, 30, 30, 4, 200, 2000),
              'w': (support.SHOTGUN, 12, 7, 1, 7, 6, 800, 600)}
playerimg = {support.DUKE: 'player/duke.png',
             support.PISTOL: 'player/pistol.png',
             support.AUTOMAT: 'player/automat.png',
             support.SHOTGUN: 'player/shotgun.png'}
enemyimg = {'a': {support.DUKE: 'enemy/duke.png',
             support.PISTOL: 'enemy/pistol.png',
             support.AUTOMAT: 'enemy/automat.png',
             support.SHOTGUN: 'enemy/shotgun.png'},
            'b': {support.DUKE: 'enemy/duke.png',
            support.PISTOL: 'enemy/pistol.png',
            support.AUTOMAT: 'enemy/automat.png',
            support.SHOTGUN: 'enemy/shotgun.png'},
            'c': {support.DUKE: 'enemy/duke.png',
             support.PISTOL: 'enemy/pistol.png',
             support.AUTOMAT: 'enemy/automat.png',
             support.SHOTGUN: 'enemy/shotgun.png'},
            'd': {support.DUKE: 'enemy/duke.png',
             support.PISTOL: 'enemy/pistol.png',
             support.AUTOMAT: 'enemy/automat.png',
             support.SHOTGUN: 'enemy/shotgun.png'}}
entityspec = {'@': (1000, ('z',)),
              'a': (50, ('y',)),
              'b': (50, ('z',)),
              'c': (50, ('x',)),
              'd': (50, ('w',))}
backimg = 'back/dungeon.png'
level = support.loadLevel(1)


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


class Field(FloatSprite):
    def __init__(self):
        super().__init__(allgroup)
        self.image = support.loadImage(emptyimg)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def draw(self, screen):
        x1 = -self.x // support.TILEWIDTH
        y1 = -self.y // support.TILEHEIGHT
        x2 = (-self.x + support.WINDOWWIDTH) // support.TILEWIDTH
        y2 = (-self.y + support.WINDOWHEIGHT) // support.TILEHEIGHT
        for y in range(max(0, y1), min(y2 + 1, len(level))):
            for x in range(max(0, x1), min(x2 + 1, len(level[y]))):
                obj = level[y][x]
                if obj not in tileimg:
                    obj = support.MAINTYPE
                surf = tileimg[obj]
                screen.blit(surf, pygame.Rect(x * support.TILEWIDTH + self.x,
                                              y * support.TILEHEIGHT + self.y,
                                              surf.get_width(), surf.get_height()))


class Tile(FloatSprite):
    def __init__(self, x, y, type):
        super().__init__(allgroup)
        self.image = support.loadImage(tileimg[type])
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )
        self.setxy()


class Bullet(FloatSprite):
    def __init__(self,posi, x, y, sin, cos, friend, type):
        super().__init__(allgroup, bulletgroup)
        self.dist = 0
        self.sin = sin
        self.cos = cos
        self.shift, self.maxrange, self.damage = bulletspec[type]
        self.image = support.loadImage(bulletimg[type])
        self.setmask()
        self.rect = self.image.get_rect().move(x, y)
        self.rect = self.rect.move(-self.rect.w // 2, -self.rect.h // 2)
        self.friendtype = friend
        self.setxy()
        self.spx, self.spy = posi

    def update(self):
        self.x += self.shift * self.cos
        self.y += self.shift * self.sin
        self.spx += self.shift * self.cos
        self.spy += self.shift * self.sin
        x = int(self.spx // 80)
        x1 = int((self.spx + 4) // 80)
        y = int(self.spy // 80)
        y1 = int((self.spy + 4) // 80)
        self.syncxy()
        self.dist += self.shift
        if self.dist >= self.maxrange:
            self.kill()
        for sprite in wallgroup:
            if pygame.sprite.collide_rect(sprite, self) and type(sprite) != self.friendtype:
                self.hurt(sprite)
                self.kill()
                return
        if level[y][x] == '2' or level[y][x1] == '2' or level[y1][x] == '2' or level[y1][x1] == '2':
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

    def shoot(self, pos, posi):
        self.beforenextshoot -= self.clock.tick()
        if self.ammo == support.NOLIMITWEAPON:
            self.nowstore = 1
        if not self.nowstore:
            return
        if self.beforenextshoot > 0:
            return
        if self.type == "w":
            s.play()
        elif self.type == "y":
            p.play()
        elif self.type == "x":
            a.play()
        else:
            k.play()
        self.nowstore -= 1
        cx = self.x + self.rect.w // 2
        cy = self.y + self.rect.h // 2
        px, py = pos
        px -= cx
        py -= cy
        for _ in range(self.bps):
            sin, cos = support.calculateDegree(px, py, self.scatter)
            Bullet(posi, cx, cy, sin, cos, self.friendtype, self.type)
        self.beforenextshoot = self.shoottime

    def reload(self):
        self.beforenextshoot -= self.clock.tick()
        if self.ammo == support.NOLIMITWEAPON:
            return
        if self.beforenextshoot > 0:
            return
        if not self.ammo:
            return
        if self.nowstore == self.maxstore:
            return
        r.play()
        self.ammo -= 1
        self.nowstore = min(self.maxstore, self.nowstore + self.store)
        self.beforenextshoot = self.reloadtime
        return


class Entity(FloatSprite):
    def __init__(self, x, y, w, h, type, imglist, curslot):
        super().__init__(allgroup, wallgroup, entitygroup)
        self.weapons = {support.DUKE: None,
                        support.PISTOL: None,
                        support.AUTOMAT: None,
                        support.SHOTGUN: None}
        self.imglist = imglist
        self.armor = 1
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
        self.stx = x * 80
        self.sty = y * 80
        self.dx = 0
        self.dy = 0
        self.rx = 0
        self.ry = 0

    def getweapon(self):
        return self.weapons[self.currentwp]

    def suffer(self, hp):
        if hp > 0:
            hp /= self.armor
        self.health -= hp
        if self.health <= 0:
            self.kill()
            return
        self.health = min(self.health, self.maxhealth)

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
        self.stx += self.dx * dx
        self.sty += self.dy * dy
        x = self.stx // 80
        x1 = (self.stx + 79) // 80
        y = self.sty // 80
        y1 = (self.sty + 79) // 80
        self.syncxy()
        if not check:
            return
        for sprite in wallgroup:
            if pygame.sprite.collide_mask(self, sprite):
                if sprite != self:
                    self.move(-dx, -dy, False)
                    return
        if level[y][x] == '2' or level[y1][x] == '2' or level[y][x1] == '2' or level[y1][x1] == '2':
            self.move(-dx, -dy, False)
            return
        return

    def detect(self, target):
        difx = abs(self.x - target.x) - support.TILEWIDTH
        dify = abs(self.y - target.y) - support.TILEHEIGHT
        if difx > self.rx or dify > self.ry:
            return
        self.shoot((target.x + target.w // 2, target.y + target.h // 2))
        self.reload()
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
        posi = [self.stx + 40, self.sty + 40]
        weapon.shoot(pos, posi)
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
        weapon = self.weapons[key]
        if weapon is None:
            return
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
            type, enemyimg[type], None)
        self.add(enemygroup)
        self.dx = support.EDX
        self.dy = support.EDY
        self.rx = support.MXRX * support.TILEWIDTH
        self.ry = support.MXRY * support.TILEHEIGHT

    def move(self, dx, dy, check=True, good=None):
        super().move(dx, dy, check, Enemy)

    def reload(self):
        weapon = self.getweapon()
        weapon.ammo = 2
        if weapon.nowstore:
            return
        super().reload()

    def shoot(self, pos):
        super().shoot(pos)
        self.reload()


class Medicine(FloatSprite):
    def __init__(self, x, y, type):
        super().__init__(allgroup, medicinegroup)
        self.friendtype = Player
        self.hp = medicinespec[type][0]
        self.image = support.loadImage(medicineimg[type])
        self.setmask()
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )
        self.setxy()

    def update(self):
        for sprite in wallgroup:
            if pygame.sprite.collide_mask(sprite, self) and type(sprite) == self.friendtype:
                success = self.heal(sprite)
                if success:
                    return

    def heal(self, patient):
        if patient.health == patient.maxhealth:
            return False
        patient.suffer(-self.hp)
        self.kill()
        return True


class Armor(FloatSprite):
    def __init__(self, x, y, type):
        super().__init__(allgroup, armorgroup)
        self.friendtype = Player
        self.coeff = armorspec[type][0]
        self.image = support.loadImage(armorimg[type])
        self.setmask()
        self.rect = self.image.get_rect().move(
            support.TILEWIDTH * x,
            support.TILEHEIGHT * y
        )
        self.setxy()

    def update(self):
        for sprite in wallgroup:
            if pygame.sprite.collide_mask(sprite, self) and type(sprite) == self.friendtype:
                success = self.protect(sprite)
                if success:
                    return

    def protect(self, patient):
        if patient.armor >= self.coeff:
            return False
        patient.armor = self.coeff
        self.kill()
        return True


class Back(FloatSprite):
    def __init__(self):
        super().__init__(backgroup)
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
        self.dx = -(target.x + target.w // 2 - support.WINDOWWIDTH // 2)
        self.dy = -(target.y + target.h // 2 - support.WINDOWHEIGHT // 2)


class Shower:
    def __init__(self, levelnum=1):
        self.show = True
        self.upd = 0
        self.setTiles()
        self.camera = Camera()
        self.player, self.field = generatelevel()

    def setTiles(self):
        for type in tileimg:
            tileimg[type] = support.loadImage(tileimg[type])

    def update(self):
        self.detect()
        self.animate()
        allgroup.update()

    def stop(self):
        self.show = False

    def isgoing(self):
        return self.show

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
            if type(sprite) == Back or type(sprite) == Field:
                continue
            self.camera.apply(sprite)
        backgroup.draw(screen)
        self.field.x += self.camera.dx
        self.field.y += self.camera.dy
        self.field.draw(screen)
        allgroup.draw(screen)

    def retur_lev(self):
        return self.level


def generatelevel():
    player = None
    Back()
    field = Field()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in medicineimg:
                Medicine(x, y, level[y][x])
            if level[y][x] in armorimg:
                Armor(x, y, level[y][x])
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
    return player, field
