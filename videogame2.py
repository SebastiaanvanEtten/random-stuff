import pygame, random, time, pygame_textinput
pygame.init()

display_height = 1080
display_width = int(display_height * 1.77777777778)
clock = pygame.time.Clock()
fullscreen = pygame.FULLSCREEN
largeText = pygame.font.SysFont(None, 40)
uberText = pygame.font.SysFont(None, 200)
screen = pygame.display.set_mode((display_width,display_height), fullscreen)

#player frames
frame1 = pygame.image.load('image/frame1.png')
frame2 = pygame.image.load('image/frame2.png')
frame3 = pygame.image.load('image/frame3.png')
frame4 = pygame.image.load('image/frame4.png')
frame5 = pygame.image.load('image/frame5.png')
frame11 = pygame.image.load('image/attack1.png')
frame12 = pygame.image.load('image/attack2.png')
frame13 = pygame.image.load('image/attack3.png')
frame14 = pygame.image.load('image/attack4.png')
frame15 = pygame.image.load('image/attack5.png')
frame16 = pygame.image.load('image/attack6.png')

#enemy frames
frame01 = pygame.image.load('image/frame1e.png')
frame02 = pygame.image.load('image/frame2e.png')
frame03 = pygame.image.load('image/frame3e.png')
frame04 = pygame.image.load('image/frame4e.png')
frame05 = pygame.image.load('image/frame5e.png')
frame111 = pygame.image.load('image/frame11.png')
frame112 = pygame.image.load('image/frame12.png')
frame113 = pygame.image.load('image/frame13.png')
frame114 = pygame.image.load('image/frame14.png')
frame115 = pygame.image.load('image/frame15.png')

#map frames
light = pygame.image.load('image/light.png')
vent = pygame.image.load('image/vent.png')
cloudimg = pygame.image.load('image/cloud.png')
lampimg = pygame.image.load('image/lamp.png')
moonimg = pygame.image.load('image/moon.png') # 450x450
grass = pygame.image.load('image/grass.png')
wall1 = pygame.image.load('image/wall1.png')
wall2 = pygame.image.load('image/wall2.png')
store = pygame.image.load('image/store.png')
health = pygame.image.load('image/health.png')
speed = pygame.image.load('image/speed.png')
strength = pygame.image.load('image/strength.png')

#others
fly = pygame.image.load('image/fly.png')
white = (255,255,255)
black = (0,0,0)
gametick = 0
lightblue = (100,100,220)
lightgreen = (100,220,100)
gray = (60,60,60)
darkgray = (30,30,30)
lightyellow = (244,231,115)
bgcolor = lightblue
groundcolor = gray

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()
def printtext(msg,x,y):
    TextSurf15, TextRect15 = text_objects(msg, largeText)
    TextRect15 = (x, y)
    screen.blit(TextSurf15, TextRect15)
def printbig(msg,x,y):
    TextSurf15, TextRect15 = text_objects(msg, uberText)
    TextRect15 = (x, y)
    screen.blit(TextSurf15, TextRect15)
def printcenter(msg,x,y):
    TextSurf15, TextRect15 = text_objects(msg, largeText)
    TextRect15.center = (x, y)
    screen.blit(TextSurf15, TextRect15)

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.frame = 0
        self.yaw = False
        self.framecounter = 1
        self.speed = 8
        self.charframe = 1
        self.frame = frame1
        self.height = 0
        self.gravity = 65
        self.fallspeed = 1.1
        self.score = 0
        self.health = 100
        self.jump = False
        self.scorelist = []
        self.attackframe = 0
        self.attackstate = False
        self.strength = 25
        self.level = 1
        self.xp = 0
        self.xpbarlength = 0
    def drawBars(self):
        #healthbar
        redHP = 0
        greenHP = 0
        if self.health < 0.1:
            self.health = 0
        if self.health > 50:
            greenHP = 255
            redHP = int((100 - self.health) * 5.1)
        elif self.health <= 50:
            redHP = 255
            greenHP = int(self.health * 5.1)
        elif self.health == 0:
            redHP = 255
            greenHP = 0
        if self.health > 99:
            greenHP = 255
            redHP = 0
        pygame.draw.rect(screen, (92,92,101), (41, 41, 308, 46))
        pygame.draw.rect(screen, (redHP, greenHP, 0), (45, 45, self.health * 3, 38))
        printtext('Health: ' + str(int(self.health)) + "%", 50,50)

        #xpbar
        printtext('level',display_width/2-50,23)
        printtext(str(self.level), display_width // 2 - 360, 80)
        printtext(str(self.level + 1), display_width // 2 + 340, 80)
        pygame.draw.rect(screen, (92, 92, 101), (display_width//2-350, 60, 700, 15))
        pygame.draw.rect(screen, (122, 122, 255), (display_width // 2 - 350, 63, self.xpbarlength*7, 9))
    def xpstuff(self):
        self.xpbarlength = self.xp/(self.level*1.2)
        if self.xpbarlength > 100:
            self.xp = 0
            self.xpbarlength = 0
            self.level += 1

    def draw(self):
        if self.attackstate and self.yaw:
            screen.blit(pygame.transform.flip(self.frame, self.yaw, False), (self.x-80, self.y-8))
        elif self.attackstate:
            screen.blit(pygame.transform.flip(self.frame, self.yaw, False), (self.x-15, self.y-8))
        else:
            screen.blit(pygame.transform.flip(self.frame, self.yaw, False), (self.x, self.y))
    def drawscore(self):
        for score in self.scorelist:
         score.update(self)
    def addscore(self, amount):
        score = txtpop("+" + str(amount))
        self.score += amount
        self.scorelist.append(score)
    def move(self):
        self.attack()
        if int(self.framecounter % 8) == 0:
            self.framecounter += 1
            self.charframe += 1
        if self.attackstate == False:
            if self.charframe == 1:
                self.frame = frame1
            elif self.charframe == 2:
                self.frame = frame2
            elif self.charframe == 3:
                self.frame = frame3
            elif self.charframe == 4:
                self.frame = frame4
            elif self.charframe == 5:
                self.frame = frame5
        if self.charframe > 5:
            self.charframe = 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.yaw = True
            self.framecounter += 1
        elif keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.yaw = False
            self.framecounter += 1
        if self.attackstate == False:
            if keys[pygame.K_SPACE]:
                self.attackstate = True
    def attack(self):
        if self.attackstate:
            self.attackframe += 1
            if self.attackframe == 0:
                self.frame = frame11
            elif self.attackframe == 3:
                self.frame = frame12
            elif self.attackframe == 6:
                self.frame = frame13
            elif self.attackframe == 9:
                self.frame = frame14
            elif self.attackframe == 12:
                self.frame = frame15
            elif self.attackframe == 15:
                for enemy in enemylist:
                    if enemy.x + 430 > self.x + 220 > enemy.x and enemy.active:
                        damage = random.randint(0,self.strength)
                        enemy.health -= damage
                        self.xp += damage
                        self.xpstuff()
                        self.addscore(damage)
                self.frame = frame16
            elif self.attackframe == 30:
                self.attackframe = 0
                self.frame = frame1
                self.attackstate = False
    def jumpup(self):
        if self.jump:
            self.y -= self.height
            self.height = self.gravity - self.fallspeed
            self.gravity = self.gravity / 1.2
            if self.gravity < 3:
                self.fallspeed += 1.9
                if self.y > 800:
                    self.jump = False
                    self.gravity = 65
                    self.fallspeed = 1.1
                    self.y = 800
class boxes():
    def __init__(self,x):
        self.x = x
        self.y = -160
        self.active = True
        self.fall = False
        self.scare = False
        self.end = False
        self.fallspeed = 0.45
    def draw(self):
        if self.active == True:
            if self.end == False:
                pygame.draw.rect(screen, (132, 105, 64), (self.x + 100, self.y + 00, 10, 300))  # touw links
                pygame.draw.rect(screen, (132, 105, 64), (self.x + 350, self.y + 00, 10, 300))  # touw rechts
            pygame.draw.rect(screen, (188, 180, 143), (self.x + 40, self.y + 300, 380, 250))  # container bbody
            pygame.draw.rect(screen, (132, 105, 64), (self.x + 35, self.y + 550, 390, 10))  # counter lip
            pygame.draw.rect(screen, (40, 40, 40), (self.x + 90, self.y + 300, 10, 250))  # vertical touw, 1
            pygame.draw.rect(screen, (40, 40, 40), (self.x + 225, self.y + 300, 10, 250))  # vertical touw, 2
            pygame.draw.rect(screen, (40, 40, 40), (self.x + 360, self.y + 300, 10, 250))  # vertical touw, 3
            pygame.draw.rect(screen, (40, 40, 40), (self.x + 40, self.y + 400, 380, 10))  # top, touw, horizontaal
            pygame.draw.rect(screen, (40, 40, 40), (self.x + 40, self.y + 540, 380, 10))  # bottom, touw, horizontaal

            #physics
            if player1.x + 10 > self.x:
                self.fall = True
            if self.fall == True:
                self.y += self.fallspeed
                self.fallspeed += 0.9
            if player1.x + 20 > self.x > player1.x - 380 and self.fall == True and self.end == False and self.y > 400:
                player1.health -= 15
            if self.y >= display_height - 650:
                self.fall = False
                self.end = True
                self.y = display_height - 650

class shop():
    def __init__(self,x):
        self.x = x
        self.y = 0
        self.active = False
        self.width = 950
        self.height = 600
    def draw(self):
        #draw thing
        screen.blit(store, (self.x,680))

        #region check
        if self.x + 280 > player1.x + 80 > self.x:
            printtext('press [F] to use',player1.x-70,player1.y-90)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.active = True

        #de winkel zelf
        while self.active == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.active = False

            player1.draw()
            player1.drawBars()
            pygame.draw.rect(screen, (120,101,84), (display_width//2-(self.width//2),display_height//2-(self.height//2),self.width,self.height))
            printcenter("press [F] to close the store", display_width // 2, 220)
            printcenter("score: " + str(player1.score), display_width // 2 + (self.width / 4 - 15), 270)
            printcenter("current stats", display_width // 2 + (self.width / 4 - 15), 350)
            printtext("health: " + str(round(player1.health, 1)), display_width // 2 + 20, 400)
            printtext("strength: " + str(player1.strength), display_width // 2 + 20, 450)
            printtext("speed: " + str(round(player1.speed, 1)), display_width // 2 + 20, 500)

            for ytab in range(0,5):
                pygame.draw.rect(screen, (100, 80, 60), (
                (display_width // 2 - (self.width // 2)) + 20,
                (display_height // 2 - (self.height // 2)) + 30 + (ytab * 110), 400, 100))
                txt = "none"
                option = "none"

                if ytab == 0:
                    txt = "[$50] health + 10"
                    option = "opt1"
                if ytab == 1:
                    txt = "[$150] strength + 5"
                    option = "opt2"
                if ytab == 2:
                    txt = "[$100] speed + 0.5"
                    option = "opt3"
                if ytab == 3:
                    txt = "[$0] nothing + 0"
                    option = "opt4"
                if ytab == 4:
                    txt = "[$50] Gamble score"
                    option = "opt5"


                button(txt, (display_width // 2 - (self.width // 2)) + 20,
                (display_height // 2 - (self.height // 2)) + 30 +  (ytab * 110), 400, 100, (90, 70, 50),
                (90, 70, 50), action=option)
            screen.blit(health, ((display_width // 2 - (self.width // 2)) + 20, (display_height // 2 - (self.height // 2)) + 30 + (0)))
            screen.blit(strength, ((display_width // 2 - (self.width // 2)) + 20, (display_height // 2 - (self.height // 2)) + 30 + (110)))
            screen.blit(speed, ((display_width // 2 - (self.width // 2)) + 20, (display_height // 2 - (self.height // 2)) + 30 + (220)))
            clock.tick(60)
            pygame.display.flip()

class rollthing:
    def __init__(self,x):
        self.x = x
        self.ballx = x
        self.bally = 140
        self.fallspeed = 1
        self.rollspeed = 1
    def draw(self):
        pygame.draw.circle(screen, (140,140,170), (int(self.ballx),int(self.bally)), 20)
        screen.blit(vent, (self.x-80,0))
        if self.bally < 180:
            self.bally += 0.4
        elif self.bally < 900:
            self.bally += self.fallspeed
            self.fallspeed = self.fallspeed * 1.1
        else:
            self.ballx -= self.rollspeed
            if self.rollspeed < 12:
                self.rollspeed = self.rollspeed * 1.05
        if self.ballx < 0:
            self.ballx = self.x
            self.bally = 140
            self.fallspeed = 1
            self.rollspeed = 1
        if player1.x + 50 > self.ballx > player1.x - 50 and self.bally > 880 and player1.jump == False:
            player1.health -= 2

class level:
    def __init__(self,room):
        self.room = room
    def render(self):
        global bgcolor, groundcolor
        #----------------------------------------------------------------
        #hiermee kan je van level switchen als je tegen de muur aan loopt
        if player1.x > display_width - 200:
            printtext('Press [F] to continue',player1.x-230,player1.y-90)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_f]:
                self.room += 1
                player1.x = 101
        if self.room != 1:
            if player1.x < 100:
                printtext('Press [F] to go back', player1.x + 30, player1.y - 90)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_f]:
                    self.room -= 1
                    player1.x = display_width - 201
        #-----------------------------------------------------------------
        #indeling per level
        #render lvl: 999 background
        if self.room == 1:
            bgcolor = (35,35,35)
            groundcolor = (23, 23, 23)
            screen.blit(moonimg, ((display_width//2)-225, (display_height//2)+10))
            pygame.draw.rect(screen, (23,23,23), (display_width//2-80,display_height-90,150,30))
            cloud1.draw()
            cloud2.draw()
            cloud3.draw()
            cloud4.draw()
            for enemy in enemylist:
                if enemy == enemy1:
                    enemy.active = True
                else:
                    enemy.active = False
            enemy1.draw()
            enemy1.move()
        elif self.room == 2:
            drawwindow(150)
            drawwindow(display_width - 700)
            pygame.draw.rect(screen, (40, 40, 40), (700, 0, 30, display_height - 150))
            pygame.draw.rect(screen, (40, 40, 40), (1150, 0, 30, display_height - 150))
            rollthing1.draw()
            rollthing2.draw()
            light1.draw()
            light2.draw()
            light3.draw()

            for enemy in enemylist:
                if enemy == enemy2:
                    enemy.active = True
                else:
                    enemy.active = False
            enemy2.draw()
            enemy2.move()
            bgcolor = gray
            groundcolor = darkgray
        elif self.room == 3:
            drawwindow(600)
            pygame.draw.rect(screen, (40, 40, 40), (520, 0, 30, display_height - 150))
            pygame.draw.rect(screen, (40, 40, 40), (1140, 0, 30, display_height - 150))
            box1.draw()
            light4.draw()
            light5.draw()
            for enemy in enemylist:
                if enemy == enemy3 or enemy == enemy4:
                    enemy.active = True
                else:
                    enemy.active = False
            enemy3.draw()
            enemy3.move()
            enemy4.draw()
            enemy4.move()
            bgcolor = gray
            groundcolor = darkgray
        elif self.room == 4:
            for enemy in enemylist:
                # if enemy == enemy3 or enemy == enemy4:
                #     enemy.active = True
                # else:
                enemy.active = False
            drawwindow(150)
            drawwindow(display_width - 700)
            pygame.draw.rect(screen, (40, 40, 40), (700, 0, 30, display_height - 150))
            pygame.draw.rect(screen, (40, 40, 40), (1150, 0, 30, display_height - 150))
            light6.draw()
            light7.draw()
            shop1.draw()
            bgcolor = gray
            groundcolor = darkgray
        elif self.room == 5:
            bgcolor = (39, 39, 50)
            groundcolor = (23, 23, 23)
            for enemy in enemylist:
                # if enemy == enemy9:
                #     enemy.active = True
                # else:
                enemy.active = False
            cloud1.draw()
            cloud2.draw()
            cloud3.draw()
            cloud4.draw()
            fly1.draw()
            fly1.move()
        else:
            printtext('level bestaat niet',display_width//2,display_height-300)
            bgcolor = black

def drawwindow(x):
    pygame.draw.rect(screen, lightyellow, (x,200,500,200))
    pygame.draw.rect(screen, gray,(x,296,500,10))
    pygame.draw.rect(screen, gray,(x + 118,200,10,200))
    pygame.draw.rect(screen, gray, (x + 243, 200, 10, 200))
    pygame.draw.rect(screen, gray, (x + 368, 200, 10, 200))

def button(msg,x,y,w,h,ic,ac,action=None):
    def pay(cash,product):
        if player1.score > cash:
            player1.score -= cash
            if product == "hp": player1.health += 10
            if product == "str": player1.strength += 5
            if product == "speed": player1.speed += 0.5
            if product == "gambler":
                pygame.draw.rect(screen, (120, 101, 84), (display_width // 2 + (shop1.width / 4 - 135), 250, 200, 50))
                printcenter("score: " + str(player1.score), display_width // 2 + (shop1.width / 4 - 15), 270)
                pygame.display.flip()
                gambler()

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action == "opt1":
            if player1.health < 90:
                pay(50,"hp")
                time.sleep(0.2)
        if click[0] == 1 and action == "opt2":
            pay(150,"str")
            time.sleep(0.2)
        if click[0] == 1 and action == "opt3":
            if player1.speed < 15:
                pay(100,"speed")
                time.sleep(0.2)
        if click[0] == 1 and action == "opt5":
            pay(50,"gambler")
        else:
            pygame.draw.rect(screen,ac,(x,y,w,h))
    printtext(msg, (x+ 100), (y+(h/2)-10))

def gambler():
    loop = True
    tick = 0
    delta = 2
    cash = 0
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        pygame.draw.rect(screen, (110,110,110), (display_width//2-130,display_height//2-100,365,200))
        tick += 1
        if tick > delta:
            tick = 0
            delta += 2
            if loop:
                cash = random.randint(-150,250)
        if cash > 0:
            printbig("+"+str(cash),display_width//2-100,display_height//2-75)
        else:
            printbig(str(cash), display_width // 2 - 100, display_height // 2 - 75)
        if delta == 30:
            loop = False
        clock.tick(60)
        pygame.display.flip()
    time.sleep(2)
    player1.score += cash


class cloud:
    def __init__(self,x,y,speed):
        self.x = x
        self.y = y
        self.speed = speed
    def draw(self):
        screen.blit(cloudimg, (self.x, self.y))
        self.x += self.speed
        if self.x > display_width + 100:
            self.x = -100

class flickerlight:
    def __init__(self,x,interval):
        self.x = x
        self.count = 0
        self.interval = interval
    def draw(self):
        if gametick == 1:
            self.count += 1
            if self.count > 5:
                self.count = 0
        if self.count == self.interval:
            if (gametick > 20 and gametick < 23) or (gametick > 40 and gametick < 79) or (gametick > 81 and gametick < 86) or (gametick > 88 and gametick < 90):
                screen.blit(pygame.transform.scale(light, (400, 600)), (self.x - 50, 370))
        screen.blit(lampimg, (self.x, -110))

class Enemy:
    def __init__(self,x,y,speed):
        self.x = x
        self.y = y
        self.frame = 0
        self.yaw = False
        self.framecounter = 1
        self.charframe = 1
        self.frame = frame1
        self.attack = False
        self.speed = speed
        self.health = 100
        self.dead = False
        self.active = False
    def draw(self):
        if self.health <= 0:
            self.x = -999
            self.dead = True
        self.framecounter += 1
        if self.framecounter > 60:
            self.framecounter = 0
        if int(self.framecounter % 8) == 0:
            self.framecounter += 1
            self.charframe += 1
        if self.attack == True:
            if self.charframe == 1:
                self.frame = frame111
            elif self.charframe == 2:
                self.frame = frame112
            elif self.charframe == 3:
                self.frame = frame113
            elif self.charframe == 4:
                self.frame = frame114
            elif self.charframe == 5:
                self.frame = frame115
            elif self.charframe > 5:
                self.charframe = 1
        else:
            if self.charframe == 1:
                self.frame = frame01
            elif self.charframe == 2:
                self.frame = frame02
            elif self.charframe == 3:
                self.frame = frame03
            elif self.charframe == 4:
                self.frame = frame04
            elif self.charframe == 5:
                self.frame = frame05
            elif self.charframe > 5:
                self.charframe = 1
        #healthbar
        pygame.draw.rect(screen, (255,0,0), (self.x,self.y - 50,100,10))
        pygame.draw.rect(screen, (0,255,0), (self.x, self.y - 50, self.health, 10))
        screen.blit(pygame.transform.flip(self.frame, self.yaw, False), (self.x, self.y))
    def move(self):
        if player1.x - 70 > self.x or player1.x + 70 < self.x:
            self.attack = False
            if player1.x < self.x:
                self.x -= self.speed
                self.yaw = True
            if player1.x > self.x:
                self.x += self.speed
                self.yaw = False
        else:
            global gametick
            if player1.jump == False:
                player1.health -= 0.2
            if gametick % 2 == 0:
                self.attack = True
        if game.room == 3:
                if enemy4.x - 70 > enemy3.x or enemy4.x + 70 < enemy3.x:
                    pass
                else:
                    enemy3.x -= 1
                if enemy3.x - 70 > enemy4.x or enemy3.x + 70 < enemy4.x:
                    pass
                else:
                    enemy4.x += 1
        #collision check tussen bots voor meer dan 2 tegelijk

        # voeg dan wel if i == enemy2 & if i == enemy1 toe
            # for i in enemylist:
            #     if i == enemy3:
            #         for enemy in enemylist:
            #             if i == enemy:
            #                 pass
            #             else:
            #                 if enemy.x - 70 > enemy3.x or enemy.x + 70 < enemy3.x:
            #                     pass
            #                 else:
            #                     enemy.x += 1
            #     elif i == enemy4:
            #         for enemy in enemylist:
            #             if i == enemy:
            #                 pass
            #             else:
            #                 if enemy.x - 70 > enemy4.x or enemy.x + 70 < enemy4.x:
            #                     pass
            #                 else:
            #                     enemy.x -= 1

class flyingfuck:
    def __init__(self,x):
        self.x = x
        self.y = 245
        self.yaw = False
        self.attack = False
        self.speed = 2
        self.yspeed = 2
        self.gravity = 0
        self.health = 300
        self.dead = False
        self.active = True
        self.Mup = True
        self.Mdown = False
        self.color = (0,255,0)
        self.tick = 0
        self.loop = 0
        self.dropdown = False
    def draw(self):
        screen.blit(fly, (self.x,self.y-110))
        self.healthbar()
    def healthbar(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.x - 20, self.y - 150, 300, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.x - 20, self.y - 150, self.health, 10))
    def move(self):
        if player1.x > self.x:
            self.x += self.speed
        elif player1.x < self.x:
            self.x -= self.speed
        if player1.x + 20 > self.x + 20 > player1.x:
            self.attack = True
        if self.Mup:
            self.moveup()
        if self.Mdown:
            self.movedown()
        if self.attack:
            self.attackinit()
    def attackinit(self):
        self.color = (255,0,0)
        self.Mup = False
        self.Mdown = False
        self.tick += 1
        if not self.dropdown:
            if self.tick > 60:
                self.tick = 0
                self.loop += 1
            if self.tick < 30:
                self.y += 2
            elif self.tick > 30:
                self.y -= 2
        if self.loop > 0:
            self.dropdown = True
            self.speed = 4
            self.y += 20
            if self.y > 900:
                self.y = 900
                self.loop += 1
                if self.loop > 50:
                    self.dropdown = False
                    self.loop = 0
                    self.tick = 0
                    self.attack = False
                    self.Mup = True
                    self.speed = 2



    def moveup(self):
        if self.y < 250:
            self.Mdown = True
            self.Mup = False
            self.yspeed = 2
        self.y -= self.yspeed
        self.yspeed = self.yspeed * 1.035
        if self.y < 425:
            self.yspeed = self.yspeed / 1.07
    def movedown(self):
        if self.y > 600:
            self.Mup = True
            self.Mdown = False
            self.yspeed = 2
        self.y += self.yspeed
        self.yspeed = self.yspeed * 1.035
        if self.y > 425:
            self.yspeed = self.yspeed / 1.07



class txtpop:
    def __init__(self,text):
        self.text = text
        self.x = player1.x
        self.y = player1.y
        self.state = True

    def update(self, player):
        speed = 10
        if self.state == False:
            self.x = player1.x
            self.y = player1.y
        else:
            printtext(self.text, self.x, self.y)
            if self.y > 300:
                self.y -= (speed /2)
            elif self.y <= 300:
                self.x = player1.x
                self.y = player1.y
                player.scorelist.remove(self)
                self.state = False


class cheatinput:
    def __init__(self):
        self.active = False
        self.cheat = ""
        self.god = False
        self.debug = False
    def draw(self):
        textinput = pygame_textinput.TextInput()
        while self.active == True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
            pygame.draw.rect(screen, (80,80,80),(0,0,display_width,45))
            # Feed it with events every frame
            textinput.update(events)
            # Blit its surface onto the screen
            screen.blit(textinput.get_surface(), (10, 10))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.cheat = textinput.get_text()
                self.active = False
                if self.cheat.lower() == "god":
                    if self.god == True:
                        self.god = False
                    else:
                        self.god = True
                if self.cheat.lower() == "1":
                    game.room = 1
                if self.cheat.lower() == "2":
                    game.room = 2
                if self.cheat.lower() == "3":
                    game.room = 3
                if self.cheat.lower() == "4":
                    game.room = 4
                if self.cheat.lower() == "5":
                    game.room = 5
                if self.cheat.lower() == "debug":
                    if self.debug == True:
                        self.debug = False
                    else:
                        self.debug = True
                if self.cheat.lower() == "addscore":
                    player1.score += 200
            pygame.display.flip()

Cheatinput = cheatinput()
rollthing1 = rollthing(1200)
rollthing2 = rollthing(1700)
box1 = boxes(1020)
light1 = flickerlight(300,1)
light2 = flickerlight(900,4)
light3 = flickerlight(1500,2)
light4 = flickerlight(420,3)
light5 = flickerlight(1200,2)
light6 = flickerlight(300,1)
light7 = flickerlight(900,3)
enemy1 = Enemy(1300,800,5)
enemy2 = Enemy(1500,800,5)
enemy3 = Enemy(1100,800,5)
enemy4 = Enemy(1500,800,5)
cloud1 = cloud(display_width,100,1)
cloud2 = cloud(display_width/2,140,0.6)
cloud3 = cloud(display_width/3,200,1.2)
cloud4 = cloud(display_width/0.5,120,1.5)
player1 = Player(300,800)
game = level(1)
shop1 = shop(900)
fly1 = flyingfuck(1100)
enemylist = [enemy1,enemy2,enemy3,enemy4]


def AlwaysActive():
    #render lvl: 2
    player1.jumpup()
    screen.fill(bgcolor)

    #weer zo'n heerlijk stukje code wat ergens anders had gemoeten maar de draw volgorder is messed up
    if game.room == 4:
        pygame.draw.polygon(screen, (39, 39, 50),
                            ([1980, 614], [1872, 628], [1766, 646], [1675, 746], [1644, 834], [1628, 930], [1980, 930]))
        screen.blit(wall2, (1570, 652))
        screen.blit(wall1, (1680, 595))
    #cheats
    if Cheatinput.god == True:
        if player1.health < 100:
            player1.health = 100
    #!cheats
    if game.room == 1:
        pygame.draw.rect(screen, (groundcolor), (0, display_height - 105, display_width, 150))
    else:
        pygame.draw.rect(screen, (groundcolor), (0, display_height - 150, display_width, 150))
    if game.room == 1:
        pygame.draw.polygon(screen, (10, 10, 10), ((display_width - 220, 620), (display_width, 620), (display_width, 370),(display_width - 220, 585)))
        pygame.draw.polygon(screen, (7,7,7), ((display_width - 200, display_height - 150), (display_width, display_height - 120), (display_width, 400),(display_width - 200, 600)))
        pygame.draw.polygon(screen, (30,30,30), ((display_width - 100, display_height - 136), (display_width, display_height - 120), (display_width, 690),(display_width - 100, 700)))
    player1.move()

def playersrender():
    player1.draw()
    if game.room == 1:
        screen.blit(pygame.transform.scale(grass, (520,146)),(0,display_height-229))
        screen.blit(pygame.transform.scale(grass, (520, 146)), (520, display_height - 229))
        screen.blit(pygame.transform.scale(grass, (520, 146)), (1040, display_height - 229))
        screen.blit(pygame.transform.scale(grass, (520, 146)), (1560, display_height - 229))

def deathscreen():
    ds = True
    while ds:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                quit()
        s = pygame.Surface((display_width, display_height))
        s.fill((225, 225, 225))
        s.set_alpha(4)
        screen.blit(s, (0, 0))
        printbig('GAME OVER',display_width//2-420,display_height//2-400)
        pygame.display.flip()

def regioncheck():
    if player1.x > display_width - 80:
        player1.x = display_width - 80
    elif player1.x < 0:
        player1.x = 0

def game_loop():
    global gametick
    gameloop = True
    while gameloop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player1.jump = True
                if event.key == pygame.K_SPACE:
                    player1.charframe = 0
                if event.key == pygame.K_p:
                    enemy1.x = 1300
                    enemy1.y = 800
                    enemy1.health = 100
                    enemy1.dead = False
                    enemy1.active = True

                if event.key == pygame.K_TAB:
                    Cheatinput.active = True

        keys = pygame.key.get_pressed()
        #render lvl:2
        AlwaysActive()
        regioncheck()
        game.render()
        #render lvl:1
        playersrender()
        printcenter('score: ' + str(player1.score), display_width//2-15, 95)
    #<gametick>
        gametick += 1
        if gametick > 120:
            gametick = 1
    #</gametick>
        if keys[pygame.K_ESCAPE]:
            quit()
        # render lvl:0
        Cheatinput.draw()
        player1.drawscore()
        player1.drawBars()
        if player1.health < 0.1:
            deathscreen()
        if Cheatinput.debug == True:
            printtext('test build 1', 20, 20)

            printtext('gametick: ' + str(gametick),20,100)
            printtext('fallspeed: ' + str(round((player1.fallspeed),1)),20,150)
            printtext('gravity: ' + str(round((player1.gravity),1)), 20, 200)
            printtext('level: ' + str(game.room), 20, 250)
            printtext('Health: ' + str(round(player1.health,2)), 20, 350)
            printtext('Enemy frame: ' + str(enemy1.charframe), 20, 400)
            printtext('player level: ' + str(player1.level), 20, 450)


            printtext('position: ' + str(player1.x) + ", " + str(round(player1.y, 1)), 700, 150)
            printtext('L1/count: ' + str(light1.count), 700, 200)
            printtext('enemy1.health: ' + str(enemy1.health), 700, 250)
        clock.tick(60)
        pygame.display.flip()


game_loop()
#so naar milan voor de punten code, gek gedaan man