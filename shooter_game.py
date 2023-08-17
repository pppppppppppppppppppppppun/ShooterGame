from pygame import *
from random import *
from time import time as timer
window = display.set_mode((700, 500))
display.set_caption("Shooter Game")
background = transform.scale(image.load("galaxy.jpg"), (700,500))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire = mixer.Sound("fire.ogg")
mixer.music.set_volume(0.1)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x=65, size_y=65):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.y, -10, 15, 15)
        bullets.add(bullet)
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()
pointnn = 0
missnn = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missnn
        if self.rect.y >= 500:
            self.rect.y =   0
            self.rect.x = randint(0, 600)
            missnn = missnn + 1
game = True
player = Player("rocket.png", 320, 400, 5)

font.init()
ufo_group = sprite.Group()
for i in range(5):
    ufo = Enemy("ufo.png", randint(0, 600), 0, randint(2, 3))
    ufo_group.add(ufo)
asteroidgroup = sprite.Group()
for i in range(3):
    asteroid = Enemy("asteroid.png", randint(0, 600), 0, randint(2, 3))
    asteroidgroup.add(asteroid)
font = font.SysFont("Arial", 40)
win = font.render(
    "You win!", True, (255, 215, 0))
lose = font.render(
    "You lose", True, (255, 0, 0))
point  = font.render(
    "Points: ", True, (255, 0, 0))
miss = font.render(
    "Missed: ", True, (255, 0, 0))
load = font.render(
    "Reloading: ", True, (255, 0, 0))


pointn = font.render(
    str(pointnn), True, (255, 0, 0))
missn = font.render(
    str(missnn), True, (255, 0, 0))

bullets = sprite.Group()
finish = False
rreload = False
numberb = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if numberb <= 20 and rreload == False:
                    numberb += 1
                    player.fire()
                    fire.play()
                if numberb >= 20 and rreload == False:
                    rreload = True
                    ltime = timer()
    if finish != True:
        window.blit(background, (0, 0))
        window.blit(miss, (10,50) )
        window.blit(point, (10,10) )
        missn = font.render(str(missnn), True, (255, 0, 0))
        window.blit(missn, (138,50) )
        window.blit(pointn, (130,10) )
        player.reset()
        player.update()
        ufo_group.draw(window)
        ufo_group.update()
        bullets.draw(window)
        bullets.update()
        asteroidgroup.draw(window)
        asteroidgroup.update()
        sprites_list = sprite.groupcollide(
            ufo_group, bullets, True, True)
        for collide in sprites_list:
            ufo = Enemy("ufo.png", randint(0, 600), 0, randint(2, 3))
            ufo_group.add(ufo)
            pointnn += 1
            pointn = font.render(
                str(pointnn), True, (255, 0, 0))
        if pointnn >= 12:
            window.blit(win,(270, 250))
            finish = True
        if missnn >= 60:
            window.blit(lose, (270, 250))
            finish = True
        if sprite.spritecollide(player, asteroidgroup, False):
            window.blit(lose, (270, 250))
            finish = True
        if rreload == True:
            newtime = timer()
            if newtime - ltime < 2:
                window.blit(load,(270, 250))
            else:
                rreload = False
                numberb = 0
    display.update()


    
    