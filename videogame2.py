import pygame, random, time, pygame_textinput
pygame.init()

display_height = 1080
display_width = int(display_height * 1.77777777778)
clock = pygame.time.Clock()
fullscreen = pygame.FULLSCREEN
largeText = pygame.font.SysFont(None, 40)
uberText = pygame.font.SysFont(None, 200)
screen = pygame.display.set_mode((display_width,display_height), fullscreen)
frame1 = pygame.image.load('frame1.png')
frame2 = pygame.image.load('frame2.png')
frame3 = pygame.image.load('frame3.png')
frame4 = pygame.image.load('frame4.png')
frame5 = pygame.image.load('frame5.png')
frame111 = pygame.image.load('frame11.png')
frame112 = pygame.image.load('frame12.png')
frame113 = pygame.image.load('frame13.png')
frame114 = pygame.image.load('frame14.png')
frame115 = pygame.image.load('frame15.png')
light = pygame.image.load('light.png')
vent = pygame.image.load('vent.png')
frameduck = pygame.image.load('frameduck.png')
cloudimg = pygame.image.load('cloud.png')
lampimg = pygame.image.load('lamp.png')
moonimg = pygame.image.load('moon.png') # 450x450
grass = pygame.image.load('grass.png')
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

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.frame = 0
        self.yaw = False
        self.framecounter = 1
        self.charframe = 1
        self.frame = frame1
        self.height = 0
        self.gravity = 65
        self.fallspeed = 1.1
        self.score = 0
        self.health = 100
        self.jump = False
    def drawHpBar(self):
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
        printtext('Hitpoints: ' + str(int(self.health)) + "%", 50,50)
    def draw(self):
        if int(self.framecounter % 8) == 0:
            self.framecounter += 1
            self.charframe += 1
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
        elif self.charframe > 5:
            self.charframe = 1
        screen.blit(pygame.transform.flip(self.frame, self.yaw, False), (self.x, self.y))
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= 10
            self.yaw = True
            self.framecounter += 1
        elif keys[pygame.K_RIGHT]:
            self.x += 10
            self.yaw = False
            self.framecounter += 1
    def jumpup(self):
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
            if player1.x + 50 > self.x:
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


class food:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.active = True
    def draw(self):
        if self.active:
            pygame.draw.rect(screen, (0,255,0), (self.x,self.y,20,20))
            if player1.x > self.x - 100 and player1.x < self.x + 100 and player1.health < 80 and player1.y > self.y -200:
                player1.health += 20
                self.active = False

class rollthing:
    def __init__(self,x):
        self.x = x
        self.ballx = x
        self.bally = 140
        self.fallspeed = 1
        self.rollspeed = 1
    def draw(self):
        pygame.draw.circle(screen, (40,40,70), (int(self.ballx),int(self.bally)), 20)
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
        if self.room == 1:
            bgcolor = (35,35,35)
            groundcolor = (23, 23, 23)
            screen.blit(moonimg, ((display_width//2)-225, (display_height//2)+10))
            pygame.draw.rect(screen, (23,23,23), (display_width//2-80,display_height-90,150,30))
            cloud1.draw()
            cloud2.draw()
            cloud3.draw()
            cloud4.draw()
            enemy1.draw()
            enemy1.move()
        elif self.room == 2:
            drawwindow(150)
            drawwindow(display_width - 700)
            pygame.draw.rect(screen, (40, 40, 40), (700, 0, 30, display_height - 150))
            pygame.draw.rect(screen, (40, 40, 40), (1150, 0, 30, display_height - 150))
            rollthing1.draw()
            rollthing2.draw()

            #flickering light
            #screen.blit(pygame.transform.scale(light,(400,600)), (850,370))
            #screen.blit(pygame.transform.scale(light,(400,600)), (1450,370))
            light1.draw()
            light2.draw()
            light3.draw()
            bgcolor = gray
            groundcolor = darkgray
            food3.draw()
        elif self.room == 3:
            drawwindow(600)
            pygame.draw.rect(screen, (40, 40, 40), (520, 0, 30, display_height - 150))
            pygame.draw.rect(screen, (40, 40, 40), (1140, 0, 30, display_height - 150))
            box1.draw()
            light4.draw()
            light5.draw()
            bgcolor = gray
            groundcolor = darkgray
        else:
            printtext('level bestaat niet',display_width//2,display_height-300)
            bgcolor = black

def drawwindow(x):
    pygame.draw.rect(screen, lightyellow, (x,200,500,200))
    pygame.draw.rect(screen, gray,(x,296,500,10))
    pygame.draw.rect(screen, gray,(x + 118,200,10,200))
    pygame.draw.rect(screen, gray, (x + 243, 200, 10, 200))
    pygame.draw.rect(screen, gray, (x + 368, 200, 10, 200))

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
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.frame = 0
        self.yaw = False
        self.framecounter = 1
        self.charframe = 1
        self.frame = frame1
        self.attack = False
    def draw(self):
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
                self.frame = frame1
            elif self.charframe == 2:
                self.frame = frame2
            elif self.charframe == 3:
                self.frame = frame3
            elif self.charframe == 4:
                self.frame = frame4
            elif self.charframe == 5:
                self.frame = frame5
            elif self.charframe > 5:
                self.charframe = 1
        screen.blit(pygame.transform.flip(self.frame, self.yaw, False), (self.x, self.y))
    def move(self):
        if player1.x - 70 > self.x or player1.x + 70 < self.x:
            self.attack = False
            if player1.x < self.x:
                self.x -= 5
                self.yaw = True
            if player1.x > self.x:
                self.x += 5
                self.yaw = False
        else:
            global gametick
            if player1.jump == False:
                player1.health -= 0.2
            if gametick % 2 == 0:
                gametick += 1
                self.attack = True
class txtpop:
    def __init__(self,text):
        self.text = text
        self.x = player1.x
        self.y = player1.y
        self.state = False
    def update(self):
        speed = 10
        if self.state == False:
            self.x = player1.x
            self.y = player1.y
        else:
            printtext(self.text, self.x, self.y)
            if self.y > 300:
                self.y -= (speed /2)
            elif self.y <= 300:
                self.state = False
                self.x = player1.x
                self.y = player1.y

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
                self.cheat = (textinput.get_text())
                self.active = False
                if self.cheat == "god":
                    if self.god == True:
                        self.god = False
                    else:
                        self.god = True
                if self.cheat == "1":
                    game.room = 1
                if self.cheat == "2":
                    game.room = 2
                if self.cheat == "3":
                    game.room = 3
                if self.cheat == "4":
                    game.room = 4
                if self.cheat == "debug":
                    if self.debug == True:
                        self.debug = False
                    else:
                        self.debug = True
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
enemy1 = Enemy(1200,800)
enemy2 = Enemy(1500,800)
enemy3 = Enemy(900,800)
cloud1 = cloud(display_width,100,1)
cloud2 = cloud(display_width/2,140,0.6)
cloud3 = cloud(display_width/3,200,1.2)
cloud4 = cloud(display_width/0.5,120,1.5)
food1 = food(500,display_height - 150)
food2 = food(900,display_height - 150)
food3 = food(700,display_height - 150)
player1 = Player(300,800)
Add10Score = txtpop('+10')
game = level(1)



def AlwaysActive():
    if player1.jump:
        player1.jumpup()
    screen.fill(bgcolor)
    #cheats
    if Cheatinput.god == True:
        if player1.health < 100:
            player1.health += 1
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
    player1.drawHpBar()
    Add10Score.update()

def playersrender():
    player1.draw()
    if game.room == 1:
        screen.blit(pygame.transform.scale(grass, (520,140)),(0,display_height-229))
        screen.blit(pygame.transform.scale(grass, (520, 140)), (520, display_height - 229))
        screen.blit(pygame.transform.scale(grass, (520, 140)), (1040, display_height - 229))
        screen.blit(pygame.transform.scale(grass, (520, 140)), (1560, display_height - 229))

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
                    player1.score += 10
                    Add10Score.state = True
                if event.key == pygame.K_TAB:
                    Cheatinput.active = True

        keys = pygame.key.get_pressed()

        AlwaysActive()
        regioncheck()
        game.render()
        playersrender()
    #<gametick>
        gametick += 1
        if gametick > 120:
            gametick = 1
    #</gametick>
        if keys[pygame.K_ESCAPE]:
            quit()
        Cheatinput.draw()
        if player1.health < 0.1:
            deathscreen()
        if Cheatinput.debug == True:
            printtext('test build 1', 20, 20)
            printtext('position: ' + str(player1.x) + ", " + str(round(player1.y, 1)), 700, 100)
            printtext('L1/count: ' + str(light1.count), 700, 150)
            printtext('L2/count: ' + str(light2.count), 700, 200)
            printtext('L3/count: ' + str(light3.count), 700, 250)
            printtext('gametick: ' + str(gametick),20,100)
            printtext('fallspeed: ' + str(round((player1.fallspeed),1)),20,150)
            printtext('gravity: ' + str(round((player1.gravity),1)), 20, 200)
            printtext('level: ' + str(game.room), 20, 250)
            printtext('score: ' + str(player1.score),20,300)
            printtext('Health: ' + str(round(player1.health,2)), 20, 350)
            printtext('Enemy frame: ' + str(enemy1.charframe), 20, 400)
        clock.tick(60)
        pygame.display.flip()


game_loop()
