import pygame, random
pygame.init()
display_height = 1080
display_width = int(display_height * 1.77777777778)
screen = pygame.display.set_mode((display_width,display_height), pygame.FULLSCREEN)
clock = pygame.time.Clock()
largeText = pygame.font.SysFont(None, 40)
balltaken = False
gametick = 0

class Player:
    def __init__(self,posx,posy,color,speed):
        self.posx = posx
        self.posy = posy
        self.color = color
        self.score = 0
        self.speed = speed
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.posx,self.posy), 20)
        if self.posx > display_width - 20:
            self.posx = display_width - 20
        elif self.posx < 20:
            self.posx = 20
        elif self.posy < - 20:
            self.posy = display_height
        elif self.posy > display_height + 20:
             self.posy = 0
        # if gametick % 20 == 0:
        #     if balltaken == "player1":
        #         #player1.score += 1
        #     elif balltaken == "player2":
        #         #player2.score += 1
    def selfcontroll(self):
        if self.posy > display_height:
            self.posy = display_height
        if self.posy < 0:
            self.posy = 0
        if balltaken == False:
            if ball1.ballx > self.posx:
                self.posx += self.speed
            if ball1.ballx < self.posx:
                self.posx -= self.speed
            if ball1.bally > self.posy:
                self.posy += self.speed
            if ball1.bally < self.posy:
                self.posy -= self.speed
        elif balltaken == "player2":
            self.posx += self.speed
            if self.posy - player1.posy > 300 or player1.posy - self.posy > 300:
                pass
            elif self.posy == player1.posy:
                    self.posy -= self.speed
            else:
                if player1.posy > self.posy:
                    self.posy -= self.speed
                if player1.posy < self.posy:
                    self.posy += self.speed
        elif balltaken == "player1":
            if player1.posx > self.posx:
                self.posx += self.speed
            if player1.posx < self.posx:
                self.posx -= self.speed
            if player1.posy > self.posy:
                self.posy += self.speed
            if player1.posy < self.posy:
                self.posy -= self.speed

class Ball:
    def __init__(self,ballx,bally):
        self.ballx = ballx
        self.bally = bally
    def draw(self):
        global balltaken
        pygame.draw.circle(screen, (0, 0, 255), (self.ballx, self.bally), 15)
        if player1.posx + 100 > self.ballx + 50 > player1.posx and player1.posy + 100 > self.bally + 50 > player1.posy:
            self.ballx = player1.posx
            self.bally = player1.posy
            balltaken = "player1"
        if player2.posx + 100 > self.ballx + 50 > player2.posx and player2.posy + 100 > self.bally + 50 > player2.posy:
            self.ballx = player2.posx
            self.bally = player2.posy
            balltaken = "player2"
    def move(self):
        if balltaken == False:
            if player2.posx > self.ballx > player1.posx:
                self.ballx -= 5
            elif player1.posx > self.ballx > player2.posx:
                self.ballx -= 5
            if player2.posy > self.bally > player1.posy:
                self.bally -= 5
            elif player1.posy > self.bally > player2.posy:
                self.bally -= 5
            if player1.posx > self.ballx:
                self.ballx -= 5
            if player1.posx < self.ballx:
                self.ballx += 5
            if player1.posy > self.bally:
                self.bally -= 5
            if player1.posy < self.bally:
                self.bally += 5
            if player2.posx > self.ballx:
                self.ballx -= 5
            if player2.posx < self.ballx:
                self.ballx += 5
            if player2.posy > self.bally:
                self.bally -= 5
            if player2.posy < self.bally:
                self.bally += 5

            if balltaken == False:
                if self.ballx > display_width- 300:
                    self.ballx = display_width - 300
                if self.ballx < 300:
                    self.ballx = 300
                if self.bally > display_height - 200:
                    self.bally = display_height - 200
                if self.bally < 200:
                    self.bally = 200
            if balltaken != False:
                if self.ballx > display_width:
                    self.ballx = display_width
                if self.ballx < 0:
                    self.ballx = 0
                if self.bally > display_height:
                    self.bally = display_height
                if self.bally < 0:
                    self.bally = 0



player2 = Player(100,display_height//2,(255,0,0),7)
player1 = Player(display_width-100,display_height//2,(0,255,0),8)
ball1 = Ball(display_width//2,display_height//2)

def resetplayerpos():
    player2.posx = 100
    player1.posy = display_height // 2
    player1.posx = display_width - 100
    player2.posy = display_height // 2

def collision():
    global balltaken
    if balltaken != False:
        if player1.posx + 100 > player2.posx + 50 > player1.posx and player1.posy + 100 > player2.posy + 50 > player1.posy:
            ball1.ballx = display_width//2
            ball1.bally = display_height//2
            balltaken = False
    if ball1.ballx < 100:
        player1.score += 100
        ball1.ballx = display_width // 2
        ball1.bally = display_height // 2
        balltaken = False
        resetplayerpos()
    elif ball1.ballx > display_width-100:
        player2.score += 100
        ball1.ballx = display_width // 2
        ball1.bally = display_height // 2
        balltaken = False
        resetplayerpos()

def text_objects(text, font):
    textSurface = font.render(text, True, (255,255,255))
    return textSurface, textSurface.get_rect()
def playeractions():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player1.posy -= 8
    if keys[pygame.K_DOWN]:
        player1.posy += 8
    if keys[pygame.K_LEFT]:
        player1.posx -= 8
    if keys[pygame.K_RIGHT]:
        player1.posx += 8
    if keys[pygame.K_w]:
        player2.posy -= 8
    if keys[pygame.K_s]:
        player2.posy += 8
    if keys[pygame.K_a]:
        player2.posx -= 8
    if keys[pygame.K_d]:
        player2.posx += 8
    if keys[pygame.K_ESCAPE]:
        quit()
def game_loop():
    global gametick
    gameloop = True
    while gameloop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        screen.fill((90, 90, 90))
        gametick += 1
        if gametick > 60:
            gametick = 1
        playeractions()
        pygame.draw.rect(screen, (255, 255, 255), (100, 0, 5, display_height))
        pygame.draw.rect(screen, (255, 255, 255), (display_width-100, 0, 5, display_height))
        TextSurf1, TextRect1 = text_objects("green score: " + str(player1.score), largeText)
        TextRect1 = (150, 50)
        screen.blit(TextSurf1, TextRect1)
        TextSurf2, TextRect2 = text_objects("red score: " + str(player2.score), largeText)
        TextRect2 = (display_width - 350, 50)
        screen.blit(TextSurf2, TextRect2)
        collision()
        player1.draw()
        player2.draw()
        player2.selfcontroll()
        ball1.draw()
        clock.tick(60)
        pygame.display.flip()
game_loop()