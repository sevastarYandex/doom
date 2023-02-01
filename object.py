import os
import sys
import pygame
import support
import datetime
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
h = pygame.mixer.Sound('data/music/aaaaaa.wav')
h.set_volume(1)
allgroup = pygame.sprite.Group()
wallgroup = pygame.sprite.Group()
herogroup = pygame.sprite.Group()
enemygroup = pygame.sprite.Group()
entitygroup = pygame.sprite.Group()
bulletgroup = pygame.sprite.Group()
weapongroup = pygame.sprite.Group()
medicinegroup = pygame.sprite.Group()
armorgroup = pygame.sprite.Group()
backgroup = pygame.sprite.Group()
emptyimg = 'back/empty.png'
tileimg = {'1': 'tile/ground.png',
           '2': 'tile/wall.png',
           '3': 'tile/home.png',
           '4': 'tile/water.png'}
bulletimg = {'z': emptyimg,
             't': emptyimg,
             'y': 'bullet/usual.png',
             'x': 'bullet/usual.png',
             'w': 'bullet/usual.png',
             'v': 'bullet/vomit.png'}
bulletspec = {'z': (30, 160, 1),
              't': (30, 200, 1),
              'y': (50, 700, 25),
              'x': (40, 700, 6),
              'w': (80, 400, 6),
              'v': (20, 1000, 30)}
medicineimg = {'+': 'medicine/20.png',
               '*': 'medicine/80.png'}
medicinespec = {'+': (20,),
                '*': (80,)}
armorimg = {'}': 'armor/1.25.png',
            '{': 'armor/2.5.png'}
armorspec = {'}': (1.25,),
             '{': (2.5,)}
weaponimg = {'z': 'weapon/duke.png',
             't': 'weapon/duke.png',
             'y': 'weapon/pistol.png',
             'x': 'weapon/automat.png',
             'w': 'weapon/shotgun.png',
             'v': emptyimg}
weaponspec = {'z': (support.DUKE, 20, support.NOLIMITWEAPON, 1, 1, 6, 700, 0),
              't': (support.DUKE, 25, support.NOLIMITWEAPON, 1, 1, 6, 750, 0),
              'y': (support.PISTOL, 1, 10, 10, 10, 2, 600, 1000),
              'x': (support.AUTOMAT, 1, 3, 30, 30, 4, 200, 2000),
              'w': (support.SHOTGUN, 12, 7, 1, 7, 6, 800, 600),
              'v': (support.AUTOMAT, 1, 2, 12, 12, 1, 500, 2500)}
playerimg = {support.DUKE: 'player/duke.png',
             support.PISTOL: 'player/pistol.png',
             support.AUTOMAT: 'player/automat.png',
             support.SHOTGUN: 'player/shotgun.png'}
enemyimg = {'a': {support.DUKE: 'enemy/szombie.png',
             support.PISTOL: emptyimg,
             support.AUTOMAT: emptyimg,
             support.SHOTGUN: emptyimg},
            'c': {support.DUKE: 'enemy/lzombie.png',
             support.PISTOL: emptyimg,
             support.AUTOMAT: emptyimg,
             support.SHOTGUN: emptyimg},
            'b': {support.DUKE: emptyimg,
            support.PISTOL: emptyimg,
            support.AUTOMAT: 'enemy/mutant.png',
            support.SHOTGUN: emptyimg}}
entityspec = {'@': (100, ('z',)),
              'a': (50, ('z',)),
              'c': (100, ('t',)),
              'b': (250, ('v',))}
enemyspeed = {'a': (support.SZDX, support.SZDY),
              'c': (support.LZDX, support.LZDY),
              'b': (support.MDX, support.MDY)}
backimg = 'back/dungeon.png'
level = support.loadLevel(1)
fonimg = 'back/fon.png'
ruleimg = 'back/rules.png'
gamemenuimg = 'back/gamemenu.png'
statimg = 'back/stat.png'
groups = [
        allgroup, wallgroup, herogroup,
    enemygroup, entitygroup, bulletgroup,
    weapongroup, medicinegroup, armorgroup
]
total = len(tuple(filter(lambda x: x in enemyspeed,
                   ''.join(map(lambda x: ''.join(x), level)))))


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

    def __repr__(self):
        return f"{self.__class__.__name__}"


class Field(FloatSprite):
    def __init__(self, x=0, y=0):
        super().__init__(allgroup)
        self.image = support.loadImage(emptyimg)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.setxy()

    @staticmethod
    def create(info):
        x, y = map(float, info.split(', '))
        return Field(x, y)

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

    def __repr__(self):
        return super().__repr__() + f"({self.x}, {self.y})"


class Bullet(FloatSprite):
    def __init__(self, x, y, sin, cos, friend, type, dist=0):
        super().__init__(allgroup, bulletgroup)
        self.dist = dist
        self.sin = sin
        self.cos = cos
        self.type = type
        self.shift, self.maxrange, self.damage = bulletspec[type]
        self.image = support.loadImage(bulletimg[type])
        self.setmask()
        self.rect = self.image.get_rect().move(x, y)
        self.rect = self.rect.move(-self.rect.w // 2, -self.rect.h // 2)
        self.friendtype = friend
        self.setxy()

    @staticmethod
    def create(info):
        info = info.split(', ')
        x, y = map(float, info[:2])
        sin, cos = map(float, info[2:4])
        if info[4] == 'Player':
            friend = Player
        else:
            friend = Enemy
        type = info[5]
        dist = float(info[6])
        return Bullet(x, y, sin, cos, friend, type, dist)

    def update(self):
        self.x += self.shift * self.cos
        self.y += self.shift * self.sin
        self.syncxy()
        x = self.rect.x // support.TILEWIDTH
        x1 = (self.rect.x + self.rect.w - 1) // support.TILEWIDTH
        y = self.rect.y // support.TILEHEIGHT
        y1 = (self.rect.y + self.rect.h - 1) // support.TILEHEIGHT
        self.dist += self.shift
        if self.dist >= self.maxrange:
            self.kill()
            return
        for sprite in wallgroup:
            if pygame.sprite.collide_rect(sprite, self):
                if self.hurt(sprite):
                    self.kill()
                    return
        if support.WALLTYPES in (level[y][x], level[y][x1], level[y1][x], level[y1][x1]):
            self.kill()
            return

    def hurt(self, target):
        if not isinstance(target, Entity):
            return False
        if isinstance(target, self.friendtype):
            return False
        target.suffer(self.damage)
        return True

    def __repr__(self):
        return super().__repr__() + f"({self.x}, {self.y}, {self.sin}, {self.cos}, " \
               f"{self.friendtype.__name__}, {self.type}, {self.dist})"


class Weapon(FloatSprite):
    def __init__(self, x, y, type, ammo=None, nowstore=None, bns=None):
        super().__init__(allgroup, weapongroup)
        self.type = type
        self.kind = weaponspec[self.type][0]
        self.friendtype = None
        self.host = None
        self.bps = weaponspec[self.type][1]
        self.ammo = weaponspec[self.type][2]
        if ammo is not None:
            self.ammo = ammo
        self.store = weaponspec[self.type][3]
        self.maxstore = weaponspec[self.type][4]
        self.nowstore = self.maxstore
        if nowstore is not None:
            self.nowstore = nowstore
        self.scatter = weaponspec[self.type][5]
        self.shoottime = weaponspec[self.type][6]
        self.reloadtime = weaponspec[self.type][7]
        self.beforenextshoot = 0
        if bns is not None:
            self.beforenextshoot = bns
        self.clock = pygame.time.Clock()
        self.image = support.loadImage(weaponimg[self.type])
        self.setmask()
        self.rect = self.image.get_rect().move(x, y)
        self.setxy()

    @staticmethod
    def create(info):
        info = info.split(', ')
        x, y = map(float, info[:2])
        type = info[2]
        ammo = int(info[3])
        nowstore = int(info[4])
        bns = float(info[5])
        return Weapon(x, y, type, ammo, nowstore, bns)

    def __repr__(self):
        return super().__repr__() + \
               f"({self.x}, {self.y}, {self.type}, {self.ammo}, " \
               f"{self.nowstore}, {self.beforenextshoot})"

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
            Bullet(cx, cy, sin, cos, self.friendtype, self.type)
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
    def __init__(self, x, y, w, h, type, imglist, curslot, health=None, armor=None, weapons=None):
        super().__init__(allgroup, wallgroup, entitygroup)
        self.imglist = imglist
        self.armor = 1
        if armor is not None:
            self.armor = armor
        self.w = w
        self.h = h
        self.health = entityspec[type][0]
        self.maxhealth = self.health
        if health is not None:
            self.health = health
        self.currentwp = support.MAINSLOT
        self.weapons = {support.DUKE: None,
                        support.PISTOL: None,
                        support.AUTOMAT: None,
                        support.SHOTGUN: None}
        if weapons is not None:
            for weapon in weapons:
                self.setweapon(weapon)
        else:
            for t in entityspec[type][1]:
                self.setweapon(Weapon(0, 0, t))
        if curslot is not None:
            self.change(curslot)
        self.frames = []
        self.curframe = -1
        self.cut(self.imglist[self.currentwp])
        self.animate()
        self.rect = self.image.get_rect().move(x, y)
        self.setxy()
        self.dx = 0
        self.dy = 0
        self.rx = 0
        self.ry = 0

    def __repr__(self):
        return f"{self.health}, {self.armor}, [" + \
               ", ".join(map(Weapon.__repr__,
                            filter(lambda x: x is not None, self.weapons.values()))) + "]"

    def getweapon(self):
        return self.weapons[self.currentwp]

    def suffer(self, hp):
        if hp > 0:
            hp /= self.armor
        self.health -= hp
        if self.health <= 0:
            self.kill()
            for key in self.weapons:
                weapon = self.weapons[key]
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
        self.syncxy()
        x = self.rect.x // support.TILEWIDTH
        x1 = (self.rect.x + support.TILEWIDTH - 1) // support.TILEWIDTH
        y = self.rect.y // support.TILEHEIGHT
        y1 = (self.rect.y + support.TILEHEIGHT - 1) // support.TILEHEIGHT
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
        weapon.shoot(pos)
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
            if pygame.sprite.collide_mask(self, sprite) and sprite.host is None:
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
    def __init__(self, x, y, health=None, armor=None, weapons=None):
        super().__init__(x, y, support.TILEWIDTH, support.TILEHEIGHT,
                         support.PLAYERTYPE, playerimg,
                         support.DUKE, health, armor, weapons)
        self.add(herogroup)
        self.dx = support.PDX
        self.dy = support.PDY

    @staticmethod
    def create(info):
        totalinfo = info.split(', ')
        x, y = map(float, totalinfo[:2])
        health, armor = float(totalinfo[2]), float(totalinfo[3])
        weapinfo = info[info.find('[') + 1: info.rfind(']')].split('), ')
        weapons = []
        for weap in weapinfo:
            weap = weap[weap.find('(') + 1:]
            weap = weap.rstrip(')')
            weapons.append(Weapon.create(weap))
        return Player(x, y, health, armor, weapons)

    def __repr__(self):
        return f"Player({self.x}, {self.y}, " + super().__repr__() + ")"

    def drawinfo(self, screen):
        font = pygame.font.Font(None, 50)
        img = support.loadImage(statimg)
        lines = (f'Здоровье: {int(self.health)}',
                 f'Броня: {self.armor}',
                 f'Убито врагов: {total - len(enemygroup)}')
        start = 25
        for line in lines:
            text = font.render(line, True, 'white')
            img.blit(text, (30, start))
            start += 100
        screen.blit(img, (0, screen.get_size()[1] - img.get_size()[1]))


class Enemy(Entity):
    def __init__(self, x, y, type, health=None, armor=None, weapons=None):
        super().__init__(x, y, support.TILEWIDTH, support.TILEHEIGHT,
            type, enemyimg[type], None, health, armor, weapons)
        self.type = type
        self.add(enemygroup)
        self.dx, self.dy = enemyspeed[type]
        self.rx = support.MXRX * support.TILEWIDTH
        self.ry = support.MXRY * support.TILEHEIGHT

    @staticmethod
    def create(info):
        totalinfo = info.split(', ')
        x, y = map(float, totalinfo[:2])
        type = totalinfo[2]
        health, armor = int(totalinfo[3]), float(totalinfo[4])
        weapinfo = info[info.find('[') + 1: info.rfind(']')].split('), ')
        weapons = []
        for weap in weapinfo:
            weap = weap[weap.find('(') + 1:]
            weap = weap.rstrip(')')
            weapons.append(Weapon.create(weap))
        return Enemy(x, y, type, health, armor, weapons)

    def __repr__(self):
        return f"Enemy({self.x}, {self.y}, {self.type}, " + super().__repr__() + ")"

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
        self.type = type
        self.friendtype = Player
        self.hp = medicinespec[type][0]
        self.image = support.loadImage(medicineimg[type])
        self.setmask()
        self.rect = self.image.get_rect().move(x, y)
        self.setxy()

    @staticmethod
    def create(info):
        info = info.split(', ')
        x, y = map(float, info[:2])
        type = info[2]
        return Medicine(x, y, type)

    def update(self):
        for sprite in wallgroup:
            if pygame.sprite.collide_mask(sprite, self) and isinstance(sprite, self.friendtype):
                success = self.heal(sprite)
                if success:
                    return

    def heal(self, patient):
        if patient.health == patient.maxhealth:
            return False
        patient.suffer(-self.hp)
        self.kill()
        return True

    def __repr__(self):
        return super().__repr__() + \
               f"({self.x}, {self.y}, {self.type})"


class Armor(FloatSprite):
    def __init__(self, x, y, type):
        super().__init__(allgroup, armorgroup)
        self.type = type
        self.friendtype = Player
        self.coeff = armorspec[type][0]
        self.image = support.loadImage(armorimg[type])
        self.setmask()
        self.rect = self.image.get_rect().move(x, y)
        self.setxy()

    @staticmethod
    def create(info):
        info = info.split(', ')
        x, y = map(float, info[:2])
        type = info[2]
        return Armor(x, y, type)

    def update(self):
        for sprite in wallgroup:
            if pygame.sprite.collide_mask(sprite, self) and isinstance(sprite, self.friendtype):
                success = self.protect(sprite)
                if success:
                    return

    def protect(self, patient):
        if patient.armor >= self.coeff:
            return False
        patient.armor = self.coeff
        self.kill()
        return True

    def __repr__(self):
        return super().__repr__() +\
               f"({self.x}, {self.y}, {self.type})"


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
    def __init__(self, dx=0, dy=0):
        self.dx = dx
        self.dy = dy

    def apply(self, obj):
        obj.x += self.dx
        obj.y += self.dy
        obj.syncxy()

    def disapply(self, obj):
        obj.x -= self.dx
        obj.y -= self.dy
        obj.syncxy()

    def update(self, target):
        self.dx = -(target.x + target.w // 2 - support.WINDOWWIDTH // 2)
        self.dy = -(target.y + target.h // 2 - support.WINDOWHEIGHT // 2)

    def __repr__(self):
        return f"Camera({self.dx}, {self.dy})"


class Shower:
    def __init__(self, levelnum=1):
        self.show = True
        self.upd = 0
        self.setTiles()
        self.player, self.field = None, None
        self.camera = None
        self.sost = support.MENU
        self.dead = True
        Back()

    def newgame(self):
        self.player, self.field = generatelevel()
        self.dead = False
        self.camera = Camera()
        self.sost = support.GAME

    def setTiles(self):
        for type in tileimg:
            tileimg[type] = support.loadImage(tileimg[type])

    def update(self):
        if self.sost != support.GAME:
            return
        self.detect()
        self.animate()
        allgroup.update()
        if self.player.health <= 0:
            h.play()
            self.dead = True
            self.sost = support.GAMEMENU
            for sprite in allgroup:
                sprite.kill()
            self.player = None
            self.field = None
            self.camera = None

    def savegame(self):
        time = datetime.datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S"
        )
        savelevel(time)

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
        pos = (pos[0] - self.camera.dx, pos[1] - self.camera.dy)
        herogroup.update(support.SHOOTKEY, pos)

    def reload(self):
        herogroup.update(support.RELOADKEY)

    def take(self):
        herogroup.update(support.TAKEKEY)

    def change(self, key):
        herogroup.update(support.CHANGEKEY, key)

    def tryload(self, pos):
        saves = sorted(map(lambda x: x.rstrip('.txt').lstrip('data/save/'),
                           os.listdir('data/save')), reverse=True)
        minposy = [50 + 100 * i for i in
                   range(len(os.listdir('data/save')))]
        if not (100 <= pos[0] <= 450):
            return
        self.player = None
        self.camera = None
        self.field = None
        for sprite in allgroup:
            sprite.kill()
        for i in range(len(minposy)):
            if minposy[i] <= pos[1] <= minposy[i] + 50:
                self.sost = support.GAME
                self.camera = Camera()
                self.player, self.field = loadsave(saves[i])
                self.dead = False
                return

    def back(self):
        self.sost = support.MENU
        self.dead = True
        for sprite in allgroup:
            sprite.kill()
        self.player = None
        self.field = None
        self.camera = None

    def draw(self, screen):
        backgroup.draw(screen)
        if self.sost == support.GAMEMENU:
            screen.fill('black')
            img = support.loadImage(gamemenuimg)
            img = pygame.transform.scale(img, (support.WINDOWWIDTH,
                                               support.WINDOWHEIGHT))
            screen.blit(img, (0, 0))
            return
        if self.sost == support.RULE:
            screen.fill('black')
            img = support.loadImage(ruleimg)
            img = pygame.transform.scale(img, (support.WINDOWWIDTH,
                                               support.WINDOWHEIGHT))
            screen.blit(img, (0, 0))
            return
        if self.sost == support.SAVE or self.sost == support.GAMELOAD:
            screen.fill('black')
            font = pygame.font.Font(None, 50)
            savestr = sorted([x.rstrip('.txt').lstrip('data/save/')
                       for x in os.listdir('data/save')], reverse=True)
            xc = 100
            yc = 50
            for string in savestr:
                text = font.render(string, True, (255, 0, 0))
                screen.blit(text, (xc, yc))
                yc += 100
            return
        if self.sost == support.GAME:
            self.camera.update(self.player)
            for sprite in allgroup:
                self.camera.apply(sprite)
            self.field.draw(screen)
            allgroup.draw(screen)
            for sprite in allgroup:
                self.camera.disapply(sprite)
            self.player.drawinfo(screen)
            return
        if self.sost == support.MENU:
            img = support.loadImage(fonimg)
            img = pygame.transform.scale(img, (support.WINDOWWIDTH,
                                               support.WINDOWHEIGHT))
            screen.blit(img, (0, 0))
            return


def generatelevel():
    player = None
    field = Field()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in medicineimg:
                Medicine(x * support.TILEWIDTH,
                         y * support.TILEHEIGHT,
                         level[y][x])
            if level[y][x] in armorimg:
                Armor(x * support.TILEWIDTH,
                      y * support.TILEHEIGHT,
                      level[y][x])
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in weaponimg:
                Weapon(x * support.TILEWIDTH,
                       y * support.TILEHEIGHT,
                       level[y][x])
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in enemyimg:
                Enemy(x * support.TILEWIDTH,
                      y * support.TILEHEIGHT,
                      level[y][x])
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == support.PLAYERTYPE:
                player = Player(x * support.TILEWIDTH,
                                y * support.TILEHEIGHT)
    return player, field


def createman(data):
    classname = data[:data.find('(')]
    info = data[data.find('(') + 1: data.rfind(')')]
    if classname == 'Field':
        return 'FIELD', Field.create(info)
    if classname == 'Bullet':
        Bullet.create(info)
    if classname == 'Weapon':
        Weapon.create(info)
    if classname == 'Player':
        return 'PLAYER', Player.create(info)
    if classname == 'Enemy':
        Enemy.create(info)
    if classname == 'Medicine':
        Medicine.create(info)
    if classname == 'Armor':
        Armor.create(info)
    return '', ''


def loadsave(name):
    with open('data/save/' + name + '.txt', 'r') as save:
        data = save.read()
    data = data.rstrip('\n').split('\n')
    player = None
    field = None
    for line in data:
        res = createman(line)
        if res[0] == 'PLAYER':
            player = res[1]
        if res[0] == 'FIELD':
            field = res[1]
    return player, field


def savelevel(date):
    with open('data/save/' + str(date) + '.txt', 'w') as save:
        for sprite in allgroup:
            if isinstance(sprite, Weapon):
                if sprite.host is not None:
                    continue
            save.write(sprite.__repr__() + '\n')
