import random

import pygame as pg


pg.init()
size = width, height = 550, 630
screen = pg.display.set_mode(size)

running = True
clock = pg.time.Clock()
with open('map') as f:
    map = list(map(lambda x: list(x.strip()), f.readlines()))


class Dot(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(all_dots)
        self.image = pg.Surface((6, 6),
                                    pg.SRCALPHA, 32)
        pg.draw.circle(self.image, pg.Color("red"),
                           (3, 3), 3)
        self.rect = pg.Rect(x, y, 6, 6)


class BigDot(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(all_Big_dots)
        self.image = pg.Surface((16, 16),
                                    pg.SRCALPHA, 32)
        pg.draw.circle(self.image, pg.Color("red"),
                           (8, 8), 8)
        self.rect = pg.Rect(x, y, 16, 16)


class Priv(pg.sprite.Sprite):
    def __init__(self, x, y, napr):
        super().__init__(all_sprites)
        self.add(all_privs)
        self.image = pg.image.load('priv.png')
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = pg.Rect(x, y, 50, 50)
        self.x = x
        self.y = y
        self.napr = napr

    def update(self, *args):
        self.rect = pg.Rect(self.x, self.y, 50, 50)
        if self.napr == 'r':
            self.x += 1
            if len(pg.sprite.spritecollide(self, all_walls, False)):
                self.napr = random.choice(['u', 'd'])
                self.x -= 2
        elif self.napr == 'l':
            self.x -= 1
            if len(pg.sprite.spritecollide(self, all_walls, False)):
                self.napr = random.choice(['u', 'd'])
                self.x += 2
        elif self.napr == 'u':
            self.y -= 1
            if len(pg.sprite.spritecollide(self, all_walls, False)):
                self.napr = random.choice(['l', 'r'])
                self.y += 2
        elif self.napr == 'd':
            self.y += 1
            if len(pg.sprite.spritecollide(self, all_walls, False)):
                self.napr = random.choice(['l', 'r'])
                self.y -= 2


class Wall(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(all_walls)
        self.image = pg.image.load('wall.jfif')
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = pg.Rect(x, y, 50, 50)


class Packman(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pg.image.load('packman.png')
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = pg.Rect(x, y, 50, 50)
        self.x = x
        self.y = y
        self.health = 3
        self.f = True
        self.napr = 0

    def update(self, *args):
        self.rect = pg.Rect(self.x + args[0][0], self.y + args[0][1], 50, 50)
        if len(pg.sprite.spritecollide(self, all_privs, False)) and self.f:
            self.health -= 1
            self.f = False
        if len(pg.sprite.spritecollide(self, all_privs, False)) == 0:
            self.f = True
        if len(pg.sprite.spritecollide(self, all_walls, False)):
            self.rect = pg.Rect(self.x, self.y, 50, 50)
        else:
            self.x += args[0][0]
            self.y += args[0][1]
        self.image = pg.transform.rotate(self.image, 360 - self.napr + args[0][2])
        self.napr = args[0][2]
        if pg.sprite.spritecollide(self, all_dots, True):
            if self.health < 3:
                self.health += 1
        if pg.sprite.spritecollide(self, all_Big_dots, True):
            del_priv = random.choice(list_of_priv)
            all_privs.remove(del_priv)
            all_sprites.remove(del_priv)
            list_of_priv.remove(del_priv)
        if self.health == 0:
            exit()
        for i in range(self.health):
            pg.draw.rect(screen, (255, 255, 255), (450 + i * 30, 0, 20, 20), 10)


all_sprites = pg.sprite.Group()
all_privs = pg.sprite.Group()
all_walls = pg.sprite.Group()
all_dots = pg.sprite.Group()
all_Big_dots = pg.sprite.Group()

list_of_priv = []

for i, st in enumerate(map):
    for g, el in enumerate(st):
        if el == '1':
            Wall(i * 50, g * 50 + 30)
        elif el == '2':
            Dot(i * 50 + 25, g * 50 + 55)
        elif el == '3':
            BigDot(i * 50 + 25, g * 50 + 55)

list_of_priv.append(Priv(75, 105, 'l'))
Packman(200, 230)
d = (0, 0, 0)


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
            d = (0, 2, 270)
        if event.type == pg.KEYDOWN and event.key == pg.K_UP:
            d = (0, -2, 90)
        if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
            d = (-2, 0, 180)
        if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
            d = (2, 0, 0)
    screen.fill((0, 0, 0))
    all_sprites.update(d)
    all_sprites.draw(screen)
    if len(all_dots) == 0:
        running = False
    clock.tick(60)
    pg.display.flip()
pg.quit()