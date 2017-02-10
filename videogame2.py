import pygame, random, time
pygame.init()

display_height = 1080
display_width = int(display_height * 1.77777777778)
clock = pygame.time.Clock()
fullscreen = pygame.FULLSCREEN
largeText = pygame.font.SysFont(None, 40)
screen = pygame.display.set_mode((display_width,display_height), fullscreen)
frame1 = pygame.image.load('frame1.png')
frame2 = pygame.image.load('frame2.png')
frame3 = pygame.image.load('frame3.png')
frame4 = pygame.image.load('frame4.png')
frame5 = pygame.image.load('frame5.png')
frame11 = pygame.image.load('frame11.png')
frame12 = pygame.image.load('frame12.png')
frame13 = pygame.image.load('frame13.png')
frame14 = pygame.image.load('frame14.png')
frame15 = pygame.image.load('frame15.png')
frameduck = pygame.image.load('frameduck.png')
cloudimg = pygame.image.load('cloud.png')
lampimg = pygame.image.load('lamp.png')
white = (255,255,255)
black = (0,0,0)
gametick = 0
jump = False
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
    def drawHpBar(self):
        redHP = 0
        greenHP = 0
        if self.health < 0.1:
            self.health = 0.1
        if self.health > 50:
            greenHP = 255
            redHP = int((100 - self.health) * 5.1)
        elif self.health <= 50:
            redHP = 255
            greenHP = int(self.health * 5.1)
        elif self.health == 0:
            redHP = 255
            greenHP = 0
        pygame.draw.rect(screen, (140,100,50), (41, 41, 308, 46))
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
        elif self.charframe == 0:
            self.frame = frameduck
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
        elif keys[pygame.K_DOWN]:
            self.charframe = 0
    def jump(self):
        global jump
        self.y -= self.height
        self.height = self.gravity - self.fallspeed
        self.gravity = self.gravity / 1.2
        if self.gravity < 3:
            self.fallspeed += 1.9
            if self.y > 800:
                jump = False
                self.gravity = 65
                self.fallspeed = 1.1
                self.y = 800

class food:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.active = True
    def draw(self):
        if self.active:
            pygame.draw.rect(screen, (0,255,0), (self.x,self.y,20,20))
            if player1.x > self.x - 100 and player1.x < self.x + 100:
                player1.score += 10
                Add10Score.state = True
                self.active = False


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
            bgcolor = lightblue
            groundcolor = gray
            pygame.draw.circle(screen, (lightyellow),(display_width//2,300), 150)
            food1.draw()
            food2.draw()
            cloud1.draw()
            cloud2.draw()
            cloud3.draw()
            cloud4.draw()
            cloud5.draw()
            cloud6.draw()
            enemy1.draw()
            enemy1.move()
        elif self.room == 2:
            drawwindow(150)
            drawwindow(display_width - 700)
            pygame.draw.rect(screen, (40, 40, 40), (700, 0, 30, display_height - 150))
            pygame.draw.rect(screen, (40, 40, 40), (1150, 0, 30, display_height - 150))
            screen.blit(lampimg, (300, -110))
            screen.blit(lampimg, (900, -110))
            screen.blit(lampimg, (1500, -110))
            bgcolor = gray
            groundcolor = darkgray
            food3.draw()
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
                self.frame = frame11
            elif self.charframe == 2:
                self.frame = frame12
            elif self.charframe == 3:
                self.frame = frame13
            elif self.charframe == 4:
                self.frame = frame14
            elif self.charframe == 5:
                self.frame = frame15
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
            if jump == False:
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

enemy1 = Enemy(1200,800)
enemy2 = Enemy(1500,800)
enemy3 = Enemy(900,800)
cloud1 = cloud(display_width,100,1)
cloud2 = cloud(display_width/2,140,0.6)
cloud3 = cloud(display_width/3,200,1.2)
cloud4 = cloud(display_width/0.5,120,1.5)
cloud5 = cloud(display_width/0.2,220,1.1)
cloud6 = cloud(display_width/6,70,0.8)
food1 = food(500,display_height - 150)
food2 = food(900,display_height - 150)
food3 = food(700,display_height - 150)
player1 = Player(300,800)
Add10Score = txtpop('+10')
game = level(1)

def AlwaysActive():
    if jump == True:
        player1.jump()
    screen.fill(bgcolor)
    pygame.draw.rect(screen, (groundcolor), (0, display_height - 150, display_width, 150))
    if game.room == 1:
        pygame.draw.polygon(screen, (70, 70, 70), ((display_width - 220, 620), (display_width, 620), (display_width, 370),(display_width - 220, 585)))
        pygame.draw.polygon(screen, (45, 45, 45), ((display_width - 200, display_height - 150), (display_width, display_height - 120), (display_width, 400),(display_width - 200, 600)))
        pygame.draw.polygon(screen, (black), ((display_width - 100, display_height - 136), (display_width, display_height - 120), (display_width, 690),(display_width - 100, 700)))
    player1.move()
    player1.drawHpBar()
    Add10Score.update()

def playersrender():
    player1.draw()


def regioncheck():
    if player1.x > display_width - 80:
        player1.x = display_width - 80
    elif player1.x < 0:
        player1.x = 0

def game_loop():
    global gametick, jump
    gameloop = True
    while gameloop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    jump = True
                if event.key == pygame.K_p:
                    player1.score += 10
                    Add10Score.state = True

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
        printtext('test build 1', 20, 20)
        printtext('gametick: ' + str(gametick),20,100)
        printtext('fallspeed: ' + str(round((player1.fallspeed),1)),20,150)
        printtext('gravity: ' + str(round((player1.gravity),1)), 20, 200)
        printtext('level: ' + str(game.room), 20, 250)
        printtext('score: ' + str(player1.score),20,300)
        printtext('Health: ' + str(round(player1.health,2)), 20, 350)
        printtext('Enemy frame: ' + str(enemy1.framecounter), 20, 400)
        clock.tick(60)
        pygame.display.flip()


game_loop()
