""" Grace Li, Rabbot Invasion Game
May 18, 2018. ICS3U1-02 (Mr. Saleem)

Purpose: the player's farm is being invaded by robotic rabbots, also known
as RABBOTS. Your goal is to build cannons which will shoot carrot bullets
to attack the rabbots."""

playerName = input("Welcome to RABBOT INVASION.\nPlease enter your username. ")
playerName = playerName.upper() #STRING MANIPULATION
print ("Welcome, %s!" %playerName)

import pygame #import necessary values
from random import randint
pygame.init()
done, clock = False, pygame.time.Clock()
window = pygame.display.set_mode((800,600)) #set up basic display and background
pygame.display.set_caption("RABBOT INVASION")

#intialize variables
font, fontSmall = pygame.font.Font(None, 55),pygame.font.Font(None, 40)
bank_text = font.render("500", True, (245,230,0))
score_text = font.render("0", True, (255,255,255))
playerName_text = font.render(playerName, True, (255,255,255))
playerName_small = fontSmall.render(playerName, True, (255,255,255))
mouseX, mouseY, gameMode, gameLevel, rc = 0, 0, "title", "level one", 0
timer, bank, score, cannon_img, placingCannon = 0, 500, 0, False, False

#the times when the rabbots will appear on screen
rabbotsGenTimesList = [60,90,150,200,300,400,550,700,850,1000,1100,1200,1250,\
                       1350,1450,1600,1800,1830,1900,1900,1900,1900,2000,2000,\
                       2000,2000,2020,2020,2060,2060,2120,2120,2120,2200,2200,\
                       2250,2300]
rabbotTypesList = [0,0,0,0,1,1,1,0,2,2,2,0,0,0,1,2,0,2,2,2,2,2,2,2,2,2,2,2,1,1,\
                   0,1,2,1,2,2,2] #custom set times and rabbot types

rabbotsList, bulletsList, cannonsList, = [], [], []
cannonBuyHitboxesList, cannonsPriceCheckList = [], [100,125,175,250,350,500]
occupiedSquaresList, mac, genCount = [], False, 90

#import sounds
clang_sound = pygame.mixer.Sound("clang.ogg")
clink_sound = pygame.mixer.Sound("clink.ogg")
plop_sound = pygame.mixer.Sound("plop.ogg")

#import images
bullet_cardboard = pygame.image.load("bullet_cardboard.png")
bullet_metal = pygame.image.load("bullet_metal.png")
bullet_iron = pygame.image.load("bullet_iron.png")
bullet_gold = pygame.image.load("bullet_gold.png")
bullet_platinum = pygame.image.load("bullet_platinum.png")
bullet_legendary = pygame.image.load("bullet_legendary.png")

cannonImages = [pygame.image.load("cannon_cardboard.png"),pygame.image.load(\
    "cannon_metal.png"),pygame.image.load("cannon_iron.png"),pygame.image.load\
    ("cannon_gold.png"),pygame.image.load("cannon_platinum.png"),\
    pygame.image.load("cannon_legendary.png")]

rabbot_bronze = pygame.image.load("rabbot_bronze.png")
rabbot_silver = pygame.image.load("rabbot_silver.png")
rabbot_gold = pygame.image.load("rabbot_gold.png")

game_background = pygame.image.load("game_background.png")
game_background_wgrid = pygame.image.load("game_background_wgrid.png")
game_titlescreen = pygame.image.load("game_titlescreen.png")
failed_screen = pygame.image.load("failed_screen.png")
success_screen = pygame.image.load("success_screen.png")
paused_screen = pygame.image.load("paused_screen.png")
infinity_screen = pygame.image.load("infinity_screen.png")

dialogueImages = [pygame.image.load("dialogue_1.png"),pygame.image.load(\
    "dialogue_2.png"),pygame.image.load("dialogue_3.png"),pygame.image.load(\
    "dialogue_4.png"),pygame.image.load("dialogue_5.png"),pygame.image.load(\
    "dialogue_6.png"),pygame.image.load("dialogue_7.png"),pygame.image.load(\
    "dialogue_8.png"),pygame.image.load("dialogue_9.png"),pygame.image.load(\
    "dialogue_10.png"),pygame.image.load("dialogue_11.png"),pygame.image.load(\
    "dialogue_12.png"),pygame.image.load("dialogue_13.png"),pygame.image.load(\
    "dialogue_14.png"),pygame.image.load("dialogue_15.png"),pygame.image.load(\
    "dialogue_16.png"),pygame.image.load("dialogue_17.png"),pygame.image.load(\
    "dialogue_18.png")]

#def functions and classes
class Hitbox: #will create a hitbox for various functions such as clicking on
    #text or a rabbot reaching the game over line
    def __init__(self,x,y,w,h):
        self.x, self.y, self.w, self.h = x, y, w, h
    
    def clickedOn(self,mX,mY,toReturn,dest): #if textbox was clicked on
        returnMode = toReturn
        if mX > self.x and mX < self.x + self.w:
            if mY > self.y and mY < self.y + self.h:
                returnMode = dest
        return returnMode

    def isBought(self,mX,mY,index): #detects if user wants to buy a cannon
        returnStatus = -1
        if mX > self.x and mX < self.x + self.w:
            if mY > self.y and mY < self.y + self.h:
                returnStatus = index
        return returnStatus
                
def isPaused(mode,level): #flips between paused and unpause when space pressed
    if mode != "paused": return "paused"
    else: return level

def showBackground(ifPlacingCannon): #detects which bg image to display
    if ifPlacingCannon: #show grid if placing cannon
        window.blit(game_background_wgrid, (0,0))
    else: window.blit(game_background, (0,0)) #show bg without grid
        
class Rabbot: #Parent class rabbot
    def __init__(self,hp,speed,damage,lane):
        self.hp, self.speed, self.damage,self.attack = hp, speed, damage, False
        self.x, self.y, self.lane, self.alive = 800, lane*75, lane, True
        if mac: self.speed = self.speed*2

    def update(self):
        if not self.attack: self.x -= self.speed #if rabbot is moving, move
        self.alive = self.hp > 0 #set variable which will kill/not kill rabbot

class RabbotBronze(Rabbot): #subclass/childclasses for different types of rabbot
    def __init__(self): #all rabbot subclasses call on parent Rabbot
        Rabbot.__init__(self,100,1,6,lane)
        self.image = rabbot_bronze
    def update(self): Rabbot.update(self)

class RabbotSilver(Rabbot):
    def __init__(self):
        Rabbot.__init__(self,200,2,12,lane)
        self.image = rabbot_silver
    def update(self): Rabbot.update(self)

class RabbotGold(Rabbot):
    def __init__(self):
        Rabbot.__init__(self,300,4,35,lane)
        self.image = rabbot_gold
    def update(self): Rabbot.update(self)

class Bullet: #class bullet which will have different stats based on
    #which cannon type calls it
    def __init__(self, speed, damage, x, y, image, lane):
        self.speed, self.damage, self.x, self.y = speed, damage, x+60, y
        self.image, self.width, self.height, self.lane = image, 75, 40, lane
        if mac: self.speed = self.speed*2

    def update (self): self.x += self.speed #move bullet forward
    
class Cannon: #parent class cannon
    def __init__(self,mX,mY,speed,damage,bulletsPerSec,resistance):
        self.x, self.y, self.speed = (mX//75)*75, 125+((mY-125)//75)*75, speed
        self.damage, self.counter = damage, int(60/bulletsPerSec)
        #if mac: self.counter = int(self.counter/2)
        self.resistance, self.column = resistance, (mX-75)//75+1
        self.row, self.timer = (mY-125)//75+1, self.counter
        self.lane, self.alive, self.bulletsList = self.row, True,  []
        
    def shootBullet(self):
        self.alive = self.resistance > 0
        if self.counter == self.timer:
            self.bulletsList.append(Bullet(self.speed,self.damage,self.x,\
                                           self.y,self.bulletImage,self.row))
        self.timer -= 1 #counts to see if need to shoot new bullet
        if self.timer == 0: self.timer = self.counter
        
class CannonCardboard(Cannon): #child/subclass for different types of cannons
    def __init__(self): #all cannon subclasses call on parent class Cannon
        Cannon.__init__(self,mouseX,mouseY,2,22,1,100)
        self.image, self.bulletImage = cannonImages[0], bullet_cardboard
    def shootBullet(self): Cannon.shootBullet(self)
      
class CannonMetal(Cannon):
    def __init__(self):
        Cannon.__init__(self,mouseX,mouseY,3,26,2,150)
        self.image, self.bulletImage = cannonImages[1], bullet_metal
    def shootBullet(self): Cannon.shootBullet(self)
        
class CannonIron(Cannon):
    def __init__(self):
        Cannon.__init__(self,mouseX,mouseY,4,30,3,200)
        self.image, self.bulletImage = cannonImages[2], bullet_iron
    def shootBullet(self): Cannon.shootBullet(self)
        
class CannonGold(Cannon):
    def __init__(self):
        Cannon.__init__(self,mouseX,mouseY,5,32,4,250)
        self.image, self.bulletImage = cannonImages[3], bullet_gold
    def shootBullet(self): Cannon.shootBullet(self)
        
class CannonPlatinum(Cannon):
    def __init__(self):
        Cannon.__init__(self,mouseX,mouseY,7,34,5,300)
        self.image, self.bulletImage = cannonImages[4], bullet_platinum
    def shootBullet(self): Cannon.shootBullet(self)
        
class CannonLegendary(Cannon):
    def __init__(self):
        Cannon.__init__(self,mouseX,mouseY,10,36,13,450)
        self.image, self.bulletImage = cannonImages[5], bullet_legendary
    def shootBullet(self): Cannon.shootBullet(self)

#detect which cannon type to create and call the right class        
def createCannonType(cannonsList, cannonType):
    if cannonType == 0: cannonsList.append(CannonCardboard())
    elif cannonType == 1: cannonsList.append(CannonMetal())
    elif cannonType == 2: cannonsList.append(CannonIron())
    elif cannonType == 3: cannonsList.append(CannonGold())
    elif cannonType == 4: cannonsList.append(CannonPlatinum())
    elif cannonType == 5: cannonsList.append(CannonLegendary())

#detect which rabbot type to create and call the right class
def createRabbotType(rabbotsList, rabbotType):
    if rabbotType == 0: rabbotsList.append(RabbotBronze())
    elif rabbotType == 1: rabbotsList.append(RabbotSilver())
    elif rabbotType == 2: rabbotsList.append(RabbotGold())
        
#prevents two or more cannons from being placed in the same spot
def ifSpaceFree(occupiedList, mX, mY):
    column, row = (mX-75)//75+1, (mY-125)//75+1 #row is down, col is across
    duplicate = 0
    for n in range (len(occupiedList)):
        if row == occupiedList[n][0] and column == occupiedList[n][1]:
            duplicate += 1
    return not duplicate #will return true if space is free for cannon to place

def bankAndScore(bank,score): #will show the bank and score values
    window.blit(bank_text, (90,34))
    window.blit(score_text, (570,34))

def buyCannon(mX, mY): #uses mouse coor to find which cannon user wants to buy
    if mY > 477 and mY < 477+75:
        if mX > 13 and mX < 529:
            for n in range(1,7):
                if mX < 13+n*86: return n

#returns new bank balance, text image, and cannon image if true                
def checkIfEnoughMoney(bank,bank_text,cannon_img):
    if bank >= cannonsPriceCheckList[cannonType]:
        bank -= cannonsPriceCheckList[cannonType]
        bank_text = font.render(str(bank), True, (245,230,0))
        cannon_img = cannonImages[cannonType]
    return bank, bank_text, cannon_img

def collision(bullet, rabbot): #finds collision between two sprite groups
    r = False #return false unless a statement is true
    if bullet.lane == rabbot.lane: #if x values can collide
        if bullet.x + 65 > rabbot.x:
            r = True #return true
    return r

def displayProgress(rabbotsLeft): #draw a white circle showing user progress
    x, y = 754-5*rabbotsLeft, 510
    pygame.draw.circle(window, (255,255,255), (x,y), 12)

def returnVarForLevelOne(): #resets all variables for the first level
    return 0, 0, 0, 0, "level one", 500, 0, False, False, [], [], [], [], \
           len(rabbotsGenTimesList), font.render(("500"), True, (245,230,0)),\
           font.render(("0"), True, (255,255,255))

def returnVarForLevelInfinity(): #resets all variables for infinity level
    return 0, 0, 0, 0, 90, 500, 0, False, False, [], [], [], [],"infinity",90,\
           font.render("500", True, (245,230,0)),"level one", 0, 2,\
           font.render("0", True, (255,255,255))

#make hitboxes
tutorialHitbox, playHitbox = Hitbox(120,420,200,100), Hitbox(500,420,200,100)

for n in range (6): #cannon shop hitboxes for buying
    cannonBuyHitboxesList.append(Hitbox(13+n*86,477,75,75))
    
gameOverHitbox = Hitbox(0,0,75,600)
yesHitbox, noHitbox = Hitbox(345,128,75,34), Hitbox(520,128,65,34)

while not done: ### MAIN GAME LOOP ###
    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONUP: #get mouse pos if clicked
            mouseX, mouseY = pygame.mouse.get_pos()
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE: #if pause/unpause pressed
                if gameMode == "level one" or gameMode == "paused":
                    gameMode = isPaused(gameMode, "level one")
                    
            elif event.key == pygame.K_RIGHT: #if view next slide in tutorial
                if gameMode == "tutorial":
                    slideCounter += 1
                    
        elif event.type == pygame.QUIT: done = True #end while loop if quit
            
    if gameMode == "title": #if user on title screen
        window.blit(game_titlescreen, (0,0))
        
        if mouseX != 0 and mouseY != 0: #check if user wants to go to tutorial
            gameMode =tutorialHitbox.clickedOn(mouseX,mouseY,"title","tutorial")
            slideCounter = 0

            #if not, check if user wants to start game
            if gameMode == "title":
                gameMode=playHitbox.clickedOn(mouseX,mouseY,"title","level one")
                if gameMode == "level one":
                    mouseX, mouseY, rc, timer, gameLevel, bank, score,\
                cannon_img,placingCannon, rabbotsList, bulletsList,cannonsList,\
                occupiedSquaresList, rabbotsLeft, bank_text, score_text\
                =returnVarForLevelOne()
            
    elif gameMode == "tutorial": #if user wants to learn how-to-play
        if slideCounter < 18:
            window.blit(dialogueImages[slideCounter], (0,0))
            window.blit(playerName_text, (115,525))

        else: #if end of slideshow reached
            gameMode = "level one"
            mouseX, mouseY, rc, timer, gameLevel, bank, score, cannon_img,\
            placingCannon, rabbotsList, bulletsList, cannonsList,\
            occupiedSquaresList,rabbotsLeft, bank_text, score_text\
            = returnVarForLevelOne()

    elif gameMode == "level one": #if user wants to start game
        showBackground(placingCannon) #show bg images
        bankAndScore(bank,score) #show bank and score images
        pygame.draw.rect(window,(255,0,0),(0,125,75,300),5)

        if gameLevel == "level one":
            displayProgress(rabbotsLeft)
            for t in rabbotsGenTimesList: #check if generate new rabbot
                if t == timer: #if time reached to generate new rabbot
                    lane = randint(1,4) #put rabbot in a random lane
                    rabbotType = rabbotTypesList[rc]
                    createRabbotType(rabbotsList, rabbotType)#create rabbot and
                    rc += 1 #add to list of rabbots
                    
        else: #for infinity mode
            genCount -= 1
            if genCount == 0: #make two when timer is 0
                for m in range (int(rabbotAmount)):
                    lane = randint(1,4)
                    createRabbotType(rabbotsList, randint(0,maxRabbotType))
                rc, genCount, genTime = rc+1, genTime, genTime-2
                if genTime == 70: maxRabbotType = 1
                elif genTime == 50: maxRabbotType = 2
                if genTime < 5:
                    genTime = 5
                    rabbotAmount += 0.2
                
        counter = 0               
        for n in range (len(rabbotsList)): #for each rabbot sprite
            n -= counter
            rabbotsList[n].update() #update pos and alive/dead status
            if rabbotsList[n].x < 0:
                gameMode = "over"
                scored = fontSmall.render(str(score), True, (255,255,255))
            if rabbotsList[n].alive:
                #show rabbot images to window
                window.blit(rabbotsList[n].image,(rabbotsList[n].x,\
                                                  rabbotsList[n].y))
            else: #if rabbot has been defeated
                score += (rabbotsList[n].speed+2)**2
                score_text = font.render(str(score),True,(255,255,255))
                del rabbotsList[n]
                counter, rabbotsLeft = counter+1, rabbotsLeft-1
                if gameLevel == "level one": bank += 70
                else: bank+= 35
                bank_text = font.render(str(bank), True, (245,230,0))
                clang_sound.play()
                if rabbotsLeft == 0 and gameLevel == "level one":
                    gameMode = "success"

        delCounter = 0
        for can in range (len(cannonsList)): #update cannon positions
            if can < len(cannonsList)-delCounter:
                can -= delCounter
                if not cannonsList[can].alive: #remove if dead cannon
                    del cannonsList[can]
                    del occupiedSquaresList[can]
                    delCounter += 1
                
        for c in range (len(cannonsList)): #for each cannon sprite
            cannonsList[c].shootBullet() #check if need to shoot bullet
            window.blit(cannonsList[c].image, (cannonsList[c].x, \
                                               cannonsList[c].y))
            remove = False #set variable if need to kill first bullet

            for b in range (len(cannonsList[c].bulletsList)): #for each bullet
                cannonsList[c].bulletsList[b].update() #update bullet
                #show bullet image on screen
                window.blit(cannonsList[c].bulletsList[b].image,\
                            (cannonsList[c].bulletsList[b].x,\
                            cannonsList[c].bulletsList[b].y))
                
                if b == 0: #if first bullet from cannon
                    for r in range (len(rabbotsList)):
                        
                        #check if bullet hits a rabbot
                        if collision(cannonsList[c].bulletsList[b], \
                                  rabbotsList[r]):

                            #subtract damage from rabbot health
                            rabbotsList[r].hp -= cannonsList[c].damage
                            remove = True #kill first bullet
                            clink_sound.play() #play sound

                            #if bullet reaches end of screen, kill it
                    if cannonsList[c].bulletsList[b].x > (800-75): remove = True
            if remove: #if told to kill first bullet, remove from list
                del cannonsList[c].bulletsList[0]

            for rab in range (len(rabbotsList)): #check if rabbot has reached
                if collision (cannonsList[c], rabbotsList[rab]):# a cannon
                    cannonsList[c].resistance -= rabbotsList[rab].damage
                    rabbotsList[rab].attack = True
                    if cannonsList[c].resistance < 0: #if cannon is dead
                        rabbotsList[rab].attack = False
                    
        if not cannon_img: #if not buying cannon
            if 477+75 > mouseY > 477: #if user clicks, check positions
                if 529 > mouseX > 13:
                    #find cannon type to buy
                    cannonType = buyCannon(mouseX, mouseY) -1
                    bank, bank_text, cannon_img = \
                          checkIfEnoughMoney(bank,bank_text,cannon_img)
            mouseX, mouseY = 0, 0

        if cannon_img: #if user has just purchased cannon and needs to place it
            showX, showY = pygame.mouse.get_pos() #show cannon img at mouse
            window.blit(cannon_img, (showX-50,showY-25))
            placingCannon = True

            #if user clicks to place, check positions
            if 675 > mouseX > 75 and 425 > mouseY > 125:
                if ifSpaceFree(occupiedSquaresList, mouseX, mouseY):
                    createCannonType(cannonsList, cannonType)
                    occupiedSquaresList.append((cannonsList[-1].row,\
                                                cannonsList[-1].column))
                    plop_sound.play()
                    cannon_img, placingCannon = False, False
                mouseX, mouseY = 0, 0
                                          
    elif gameMode == "paused": #if game is paused
        window.blit(paused_screen, (0,0)) #show paused image
        mouseX, mouseY = 0, 0 #void any mouse clicks

    elif gameMode == "over": #if player dies
        if gameLevel == "level one": #If first level, ask to play again
            window.blit(failed_screen, (0,0))
            gameMode = yesHitbox.clickedOn(mouseX,mouseY,"over","level one")
            if gameMode == "level one":
                mouseX, mouseY, rc, timer, gameLevel, bank, score, cannon_img,\
                placingCannon,rabbotsList,bulletsList,cannonsList,\
                occupiedSquaresList, rabbotsLeft, bank_text, score_text\
                =returnVarForLevelOne()
            else: gameMode = noHitbox.clickedOn(mouseX,mouseY,"over","title")
            
        elif gameLevel == "infinity": #if inifnity level, ask to play again
            window.blit(infinity_screen, (0,0))
            window.blit(scored,(510,72))
            window.blit(playerName_small,(130,45))
            gameMode = yesHitbox.clickedOn(mouseX,mouseY,"over","level one")
            if gameMode == "level one":
                mouseX, mouseY, rc, timer, genTime,bank, score, cannon_img,\
            placingCannon, rabbotsList, bulletsList, cannonsList,\
            occupiedSquaresList, gameLevel, genCount, bank_text,gameMode,\
            maxRabbotType, rabbotAmount,score_text = returnVarForLevelInfinity()
            else: gameMode = noHitbox.clickedOn(mouseX,mouseY,"over","title")

    elif gameMode == "success": #if player passes level 1
        window.blit(success_screen, (0,0))
        gameMode = yesHitbox.clickedOn(mouseX,mouseY,"success","infinity")
        if gameMode == "infinity": #if player wants to play infinity
            mouseX, mouseY, rc, timer, genTime,bank, score, cannon_img,\
            placingCannon, rabbotsList, bulletsList, cannonsList,\
            occupiedSquaresList, gameLevel, genCount, bank_text,gameMode,\
            maxRabbotType, rabbotAmount,score_text = returnVarForLevelInfinity()
        
    pygame.display.flip()
    clock.tick(30)
    if gameMode != "paused": timer += 1 #update timer if not paused
    
pygame.quit()
