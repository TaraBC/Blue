import pygame
import sys
import os
import time


# MISC ATTRIBUTES

class colours:  # library of colours in rgb
    white = [255, 255, 255]
    black = [0, 0, 0]
    buttonBlue = [124, 176, 255]
    buttonDarkC = [89, 103, 181]
    space = [29, 41, 81]
    transparent = [0,0,0,0]


# END OF MISC ATTRIBUTES

# BASIC DISPLAY ATTRIBUTES

class mainDisplay:

    def __init__(self):
        self.screenDisplay = pygame.display.set_mode(
            [1200, 720])  # create game window SURFACE object (screen display is a SURFACE)
        pygame.display.set_caption("Blue")  # set window name

class button:
    def __init__(self, x, y, width, height, text, font, fontSize, buttonColour, borderColour, fontColour,Display,
                 xratio, yratio):  # initialize button
        # set attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # draw border
        self.buttonBorder = pygame.Rect(x, y, width, height)  # makes the buttonBorder a rect type
        # fill in button
        pygame.draw.rect(Display.screenDisplay, buttonColour, self.buttonBorder, 0)
        pygame.draw.rect(Display.screenDisplay, borderColour, self.buttonBorder, 10)
        # put text in
        self.buttonBorder.centerx = self.buttonBorder.centerx * xratio  # sets center of button to correct for Text
        self.buttonBorder.centery = self.buttonBorder.centery * yratio
        textFont = pygame.font.SysFont(font, fontSize)  # sets text font
        textSurface = textFont.render(text, False, fontColour,
                                      None)  # renders text surface with the text and fontColour
        Display.screenDisplay.blit(textSurface, self.buttonBorder.center)  # draws text onto screen
        pygame.display.flip()


class text:
    def __init__(self, x, y, font, fontSize, fontColour, text, Display):  # initialize general Text
        textFont = pygame.font.SysFont(font, fontSize)  # sets font
        textSurface = textFont.render(text, False, fontColour, None)  # renders text surface with text and fontcolour
        Display.screenDisplay.blit(textSurface, (x, y))  # draws text onto screen
        pygame.display.flip()


class quitButton:
    def __init__(self, x, y, width, height, fontSize, buttonColour, borderColour, fontColour, Display, xratio,
                 yratio):
        # set attributes
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttonBorder = pygame.Rect(x, y, width, height)
        # draw rect and set rect center
        pygame.draw.rect(Display.screenDisplay, buttonColour, self.buttonBorder, 0)
        pygame.draw.rect(Display.screenDisplay, borderColour, self.buttonBorder, 5)
        self.buttonBorder.centerx = self.buttonBorder.centerx * xratio
        self.buttonBorder.centery = self.buttonBorder.centery * yratio
        # put X in
        textFont = pygame.font.SysFont('Candara', fontSize)
        textSurface = textFont.render('X', False, fontColour, None)
        Display.screenDisplay.blit(textSurface, (self.buttonBorder.center))
        pygame.display.flip()


# END OF BASIC DISPLAY ATTRIBUTES

# FIRST SCREEN CODE

def mainMenu(quit_button, start_button, continue_button,Display):  # making buttons clickable
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.buttonBorder.collidepoint(pygame.mouse.get_pos()):  # tests if pointer is within rect
                    pygame.quit()
                    quit()
                elif start_button.buttonBorder.collidepoint(pygame.mouse.get_pos()):
                    mainGame(Display)
                    break
                elif continue_button.buttonBorder.collidepoint(pygame.mouse.get_pos()):
                    if os.path.isfile('\Saves\sav.txt'):
                        loadGame(Display)
                    else:
                        errorMessage = button((1200 / 20) * 4, (720 / 20) * 8, (1200 / 20) * 12, (720 / 20) * 2,
                                              'No Save file available', 'Candara', 36, colours.buttonDarkC,
                                              colours.space, colours.space, Display, 0.75, 0.945)


def firstScreen(Display):  # firstScreen
    title = text((515), ((720 / 20) * 2), 'Candara', 96, colours.buttonDarkC, 'Blue', Display)
    startButton = button(((1200 / 12) * 2), ((720 / 20) * 5), ((1200 / 12) * 8), (720 / 10), "START", 'Candara', 48,
                         colours.buttonBlue, colours.buttonBlue, colours.buttonDarkC, Display, 0.9,
                         0.9)  # draws START button
    continueButton = button(((1200 / 12) * 3), ((720 / 20) * 8), ((1200 / 12) * 6), (720 / 10), "Continue", 'Candara',
                            36, colours.buttonBlue, colours.buttonBlue, colours.buttonDarkC, Display, 0.9, 0.95)
    quitButton = button(((1200 / 12) * 3), ((720 / 20) * 11), ((1200 / 12) * 6), (720 / 10), "Quit", 'Candara', 36,
                        colours.buttonBlue, colours.buttonBlue, colours.buttonDarkC, Display, 0.97, 0.95)
    mainMenu(quitButton, startButton, continueButton, Display)


# END OF FIRST SCREEN

# START OF MAIN GAME

spriteClock = pygame.time.Clock()
enemyGroup = pygame.sprite.Group()
mainGroup = pygame.sprite.Group()
floorGroups = pygame.sprite.Group()


def spriteAnimate(sprite1, spriteGroup1, clock,Display,maskSet):
    sprite1.index += 1
    if sprite1.index >= len(maskSet):
        sprite1.index = 0
    Display.screenDisplay.blit(sprite1.surface, sprite1.currentCoords)
    sprite1.surface.fill(colours.black)
    pygame.display.flip()
    sprite1.image = maskSet[sprite1.index]
    spriteGroup1.draw(Display.screenDisplay)
    pygame.display.flip()
    currentTime = pygame.time.get_ticks()
    clock.tick(10)


class sprite(pygame.sprite.Sprite):
    def __init__(self, colWidth, colHeight,framesNo,Display, spriteGroup='', spawnX=0, spawnY=0):
        super().__init__()
        self.xSpawn = spawnX
        self.ySpawn = spawnY
        self.width,self.height = colWidth, colHeight
        self.currentCoords = (spawnX, spawnY)
        self.rect = pygame.Rect(spawnX, spawnY,int(colWidth), int(colHeight))
        self.surface = pygame.Surface((colWidth,colHeight))
        self.masks = [None]*framesNo
        self.index = 0
        self.image = self.masks[self.index]
        if spriteGroup != '':
            spriteGroup.add(self)  # if there is a sprite group, add it


        
    def coordUpdate(self,newCoords):
        self.currentCoords = newCoords
        self.rect = pygame.Rect(newCoords[0],newCoords[1],int(self.width), int(self.height))

    def surfaceUpdate(self,newWidth,newHeight):
        self.surface = pygame.Surface((newWidth,newHeight))
        self.width = newWidth
        self.height = newHeight

    def moveRight(self,Display):
        self.currentCoords = list(self.currentCoords)
        self.currentCoords[0] += 20
        self.coordUpdate(self.currentCoords)
        spriteAnimate(self,mainGroup,spriteClock,Display,self.runningMasksR)

    def moveLeft(self,Display):
        self.currentCoords = list(self.currentCoords)
        self.currentCoords[0] -= 20
        self.coordUpdate(self.currentCoords)
        spriteAnimate(self,mainGroup,spriteClock,Display,self.runningMasksL)

class ballEnemy(sprite):
    def __init__(self,Display):
        self.mask1 = pygame.image.load(
            os.path.join(os.getcwd()+'\spriteIMG', 'testmask1.png'))  # sets the images to png images
        self.mask2 = pygame.image.load(os.path.join(os.getcwd()+'\spriteIMG', 'testmask2.png'))
        self.mask3 = pygame.image.load(os.path.join(os.getcwd()+'\spriteIMG', 'testmask3.png'))
        super().__init__(640, 640, 4,Display, enemyGroup)
        self.masks[0] = self.mask1.convert_alpha()
        self.masks[1] = self.mask2.convert_alpha()
        self.masks[2] = self.mask3.convert_alpha()
        self.masks[3] = self.mask2.convert_alpha()
        spriteAnimate(self, enemyGroup, spriteClock, Display,self.masks)

class floor(sprite):
    def __init__(self,Display):
        self.mask1 = (pygame.image.load(os.path.join(os.getcwd()+'\spriteIMG', 'Floor-1.png')))
        super().__init__(720,600,1,Display,floorGroups)
        self.masks[0] = self.mask1.convert_alpha()
        self.image = self.masks[0]
        floorGroups.draw(Display.screenDisplay)
        pygame.display.flip()

class mainSprite(sprite):
    def __init__(self,Display):
        self.mask1 = (pygame.image.load(os.path.join(os.getcwd() + '\spriteIMG', 'foxIdle1.png')))
        self.mask2 = (pygame.image.load(os.path.join(os.getcwd() + '\spriteIMG', 'foxIdle2.png')))
        self.mask3 = (pygame.image.load(os.path.join(os.getcwd() + '\spriteIMG', 'foxIdle3.png')))
        self.mask4 = (pygame.image.load(os.path.join(os.getcwd() + '\spriteIMG', 'foxIdle4.png')))
        super().__init__(52,84,4,Display,mainGroup,20,319)
        self.masks[0] = self.mask1.convert_alpha()
        self.masks[1] = self.mask2.convert_alpha()
        self.masks[2] = self.mask3.convert_alpha()
        self.masks[3] = self.mask2.convert_alpha()
        self.running1 = (pygame.image.load(os.path.join(os.getcwd() + '\spriteIMG','foxrunning-1.png')))
        self.running2 = (pygame.image.load(os.path.join(os.getcwd() + '\spriteIMG','foxrunning-2.png')))
        self.running3 = (pygame.image.load(os.path.join(os.getcwd() + '\spriteIMG','foxrunning-3.png')))
        self.running4 = (pygame.image.load(os.path.join(os.getcwd() + '\spriteIMG','foxrunning-4.png')))
        self.runningMasksR= [self.running1.convert_alpha(),self.running2.convert_alpha(),self.running3.convert_alpha(),self.running4.convert_alpha()]
        self.runningL1 = (pygame.image.load(os.path.join(os.getcwd() + '\spriteIMG','foxRunningL-1.png')))
        self.runningL2 = (pygame.image.load(os.path.join(os.getcwd() + '\spriteIMG', 'foxRunningL-2.png')))
        self.runningL3 = (pygame.image.load(os.path.join(os.getcwd() + '\spriteIMG', 'foxRunningL-3.png')))
        self.runningL4 = (pygame.image.load(os.path.join(os.getcwd() + '\spriteIMG', 'foxRunningL-4.png')))
        self.runningMasksL = [self.runningL1.convert_alpha(),self.runningL2.convert_alpha(),self.runningL3.convert_alpha(),self.runningL4.convert_alpha()]
        runningR = False
        while self.alive():
            spriteAnimate(self,mainGroup,spriteClock,Display,self.masks)
            D_down = False
            A_down = False
            SPACE_down = False
            for event2 in pygame.event.get():
                if event2.type == pygame.KEYDOWN :
                    if event2.key == pygame.K_d :
                        D_down = True
                        self.surfaceUpdate(104,63)
                    elif event2.key == pygame.K_a :
                        A_down = True
                        self.surfaceUpdate(104,63)

            while A_down == True:
                self.moveLeft(Display)
                for event2 in pygame.event.get():
                    if event2.type == pygame.KEYUP:
                        if event2.key == pygame.K_a:
                            A_down = False
                            self.surfaceUpdate(52, 84)
            
            while D_down == True:
                self.moveRight(Display)
                for event2 in pygame.event.get():
                    if event2.type == pygame.KEYUP :
                        if event2.key == pygame.K_d :
                            D_down = False
                            self.surfaceUpdate(52,84)
def mainGame(display):
    display.screenDisplay.fill(colours.black)
    floor1 = floor(display)
    mainSprite1 = mainSprite(display)
    pygame.display.flip()



def loadGame(Display):
    Display.screenDisplay.fill(colours.buttonBlue)
    errorMessage = text((515), ((720 / 20) * 2), 'Candara', 38, colours.buttonDarkC, 'main game is under construction',
                        Display)


# END OF MAIN GAME

# START FUNCTION

def main():
    pygame.init()  # initialize pygame
    display = mainDisplay()  # makes the current display object 'mainDisplay', opening a window
    screen1 = True  # set variable screen1 to True
    maingame = False
    while True:
        firstScreen(display)  # starts first screen
        for event in pygame.event.get():  # for every event that happens in queue
            if event.type == pygame.QUIT:  # if event type is uninitialize pygame
                pygame.quit()  # quit pygame
                quit()  # quit python


main()
