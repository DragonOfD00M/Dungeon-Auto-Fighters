import pygame
import sys
import os
import json
import random
import time

random.seed(time.time())

f = open('monsters.json')
jsonmonster = json.load(f)

black = (0,0,0)
white = (255,255,255)

size = gameWidth, gameHeight = 1000, 500
gameWindow = pygame.display.set_mode(size)

class Button:
    def __init__(self, surface, x, y, width, height) -> None:
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.colour = (255,255,255)

    def draw(self) -> None:
        pygame.draw.rect(self.surface, self.colour, self.rect)

    def is_hovered(self) -> bool:
        mousePos = pygame.mouse.get_pos()
        if self.x <= mousePos[0] <= self.x + self.width and self.y <= mousePos[1] <= self.y + self.width:
            return True
        else:
            return False

    def is_clicked(self) -> bool:
        mousePress = pygame.mouse.get_pressed()
        if mousePress[0] and self.is_hovered():
            return True
        else:
            return False

class UnitSpot:
    def __init__(self, surface, x, y, spotnumber) -> None:
        self.surface = surface
        self.colour = white
        self.x = x
        self.y = y
        self.width = 100
        self.height = 50
        self.rect = pygame.Rect(self.x+self.width/2, self.y+self.height/2, self.width, self.height)
        self.spotnumber = spotnumber
        
    def draw(self) -> None:
        pygame.draw.ellipse(self.surface, self.colour, self.rect)


    def is_inUse(self, rect) -> bool:
        if self.rect.colliderect(rect):
            return True
        else:
            return False
        
class Unit:
    def __init__(self, surface, x, y, level ,type, hash) -> None:
        self.surface = surface
        self.xStart = x
        self.yStart = y
        self.x = self.xStart
        self.y = self.yStart
        self.width = 50
        self.height = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.colour = (255,255,255)
        self.level = "LEVEL "+str(level)
        self.type = type
        self.hash = hash

        i=0
        while i < len(jsonmonster[self.level]):
            if jsonmonster[self.level][i]['name'] == self.type:
                self.colour = (jsonmonster[self.level][i]['colour'][0], jsonmonster[self.level][i]['colour'][1], jsonmonster[self.level][i]['colour'][2])
            i+=1

    def reset(self):
        self.x = self.xStart
        self.y = self.yStart
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self) -> None:
        pygame.draw.rect(self.surface, self.colour, self.rect)

    def is_hovered(self) -> bool:
        mousePos = pygame.mouse.get_pos()
        if self.x <= mousePos[0] <= self.x + self.width and self.y <= mousePos[1] <= self.y + self.height:
            return True
        else:
            return False

    def is_holding(self) -> bool:
        mousePress = pygame.mouse.get_pressed()
        if mousePress[0] and self.is_hovered():
            return True
        else:
            return False

    def move(self, value) -> None:
        if self.is_holding() and (value == self.hash or value == 0):
            mousePos = pygame.mouse.get_pos()
            self.x = mousePos[0] - self.width/2
            self.y = mousePos[1] - self.height/2
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

def redrawWindow(window):
    window.fill(black)
    reroll.draw()
    for spot in spots:
        spot.draw()
    for unit in units:
        unit.draw()
    pygame.display.flip()
 
def rollUnits(window):
    units.clear()
    i = 0
    while i < 5:
        units.append(Unit(window,60 * i, 300, 1, monsters[random.randint(0,2)], i)) 
        i+=1

def moveUnits():
    global held, value
    for unit in units:
        unit.move(value)
        if unit.is_holding() and held == False:
            value = unit.hash
            held = True
        if unit.hash == value and unit.is_holding() != True:
            value = 0
            held = False
            
            for spot in spots:
                if spot.is_inUse(unit.rect):
                    spotsUsed[int(spot.spotnumber)] = unit.hash
                    unit.x = spot.x + spot.width/2 + unit.width/2
                    unit.y = spot.y - spot.height/2 - unit.height/6
                    unit.rect = pygame.Rect(unit.x, unit.y, unit.width, unit.height)
                elif not spot.is_inUse(unit.rect):
                    unit.reset()
                    

def main(window):
    run = True
    i = 0
    while i < 5:
        spots.append(UnitSpot(window,105*i-50,100, str(i)))
        spotsUsed.append(None)
        i+=1
    i = 0
    while i < 5:
        units.append(Unit(window,60 * i, 300, 1, monsters[random.randint(0,2)], i)) 
        i+=1
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
        moveUnits()
        if reroll.is_clicked():
            rollUnits(window)
        redrawWindow(window)

        
reroll = Button(gameWindow, 500, 250, 100, 100)  
spots = []
spotsUsed = []
units = []
monsters = ['GOBLIN','COBOLD','HUMAN']

os.system('cls')
held = False
value = 0
main(gameWindow)
        
