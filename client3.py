#IMPORTS
import pygame
import json
import sys
import math
import random
import time

from classes.monster import Monster
from classes.item import Item
from classes.hitbox import Hitbox
from classes.button import Button
from classes.network import Network


#INITIALIZATION
pygame.init()
random.seed(time.time())

f = open("jsons/items.json")
jitem = json.load(f)

f = open("jsons/monsters.json")
jmonster = json.load(f)

size = screenWidth, screenHeight = 1000, 500
gameWindow = pygame.display.set_mode(size)
gamestate = None
Clock = pygame.time.Clock()

team = [None, None, None, None, None]
monsterShop = [None, None, None, None, None]
itemShop = [None, None, None]

teamBox = []
mShopBox = []
iShopBox = []
boxes = [teamBox, mShopBox, iShopBox]

waitingText = "Waiting for server..."

playerLevel = 1
uid = 1
freeze = False
coins = 10

AvailableMonsters = []
AvailableItems = []

team1 = ""
team2 = ""

#FUNCTIONS
def encodeTeam(list):
    string = "£" 
    for index, unit in enumerate(list):
        try:
            stringbuf=""
            stringbuf=str(unit.name)+"%"+str(unit.dmg)+"%"+str(unit.hp)
        except:
            stringbuf="None"
        if index == len(list)-1:
            string=string+stringbuf
        else:
            string=string+stringbuf+"#"
    return string
def decodeTeam(team):
    team = team.split("#")
    for index, entry in enumerate(team):
        if entry == 'None':
            team[index] = None
        else:
            team[index] = team[index].split("%")
            team[index][1] = int(team[index][1])
            team[index][2] = int(team[index][2])
    return team
def updateLists() -> None:
    for x in jmonster["LEVEL "+str(playerLevel)]:
        AvailableMonsters.append(x["name"])
    for x in jitem["LEVEL "+str(playerLevel)]:
        AvailableItems.append(x["name"])
def fillShops(surface) -> None:
    global uid
    i=0
    while i < len(monsterShop):
        try:
            if monsterShop[i].frozen:
                pass
            else:
                monsterShop[i] = Monster(surface, 50+75*i, 350, uid, AvailableMonsters[random.randint(0, len(AvailableMonsters)-1)])
                uid+=1
        except:
            monsterShop[i] = Monster(surface, 50+75*i, 350, uid, AvailableMonsters[random.randint(0, len(AvailableMonsters)-1)])
            uid+=1
        i+=1
    i=0
    while i < len(itemShop):
        try:
            if itemShop[i].frozen:
                pass
            else:
                itemShop[i] = Item(surface, 50+75*7+75*i, 400, uid, AvailableItems[random.randint(0, len(AvailableItems)-1)])
                uid+=1
        except:
            itemShop[i] = Item(surface, 50+75*7+75*i, 400, uid, AvailableItems[random.randint(0, len(AvailableItems)-1)])
            uid+=1
        i+=1
def makeHitboxes(surface):
    i = 0
    while i < len(team):
        teamBox.append(Hitbox(surface, 500-75*i, 150, 50, 100, i))
        i+=1
    i = 0
    while i < len(monsterShop):
        mShopBox.append(Hitbox(surface, 50+75*i, 350, 50, 100, i))
        i+=1
    i = 0
    while i < len(itemShop):
        iShopBox.append(Hitbox(surface, 50+75*7+75*i, 400, 50, 50, i))
        i+=1
def redrawWindow(surface) -> None:
    global freeze, coins, waitingText
    match gamestate:
        case 0:
            radius=40
            counter=1
            t=1
            T=20
            omega = (2*math.pi)/T
            
            font = pygame.font.Font(None,50)
            text = font.render(waitingText,True,(255,255,255))
            textRect=text.get_rect()
            textRect.center = (screenWidth/2, screenHeight/4)

            surface.fill((0,0,0))

            while t <= T:
                surface.fill((0,0,0))
                surface.blit(text, textRect)
                centerX1 = radius * math.cos(omega * t) + screenWidth/2
                centerY1 = radius * math.sin(omega * t) + screenHeight/2
                centerX2 = radius * math.cos(omega * t-0.75) + screenWidth/2
                centerY2 = radius * math.sin(omega * t-0.75) + screenHeight/2
                centerX3 = radius * math.cos(omega * t-1.5) + screenWidth/2
                centerY3 = radius * math.sin(omega * t-1.5) + screenHeight/2
                center1 = (centerX1, centerY1)
                center2 = (centerX2, centerY2)
                center3 = (centerX3, centerY3)
                pygame.draw.circle(surface,(255/4, 255/4, 255/4),center3,15)
                pygame.draw.circle(surface,(255/2, 255/2, 255/2),center2,15)
                pygame.draw.circle(surface,(255,255,255),center1, 15)
                pygame.display.flip()
                if counter==60:
                    t+=1
                    counter=0
                counter+=1

            
            pygame.display.flip()
        case 1:
            surface.fill((0,0,0))
            for box in teamBox:
                box.draw()
            for box in mShopBox:
                box.draw()
            for box in iShopBox:
                box.draw()

            for unit in monsterShop:
                if unit != None:
                    unit.draw()
            for item in itemShop:
                if item != None:
                    item.draw()
            for unit in team:
                if unit != None:
                    unit.draw()
            
            readyButton.draw()
            rerollButton.draw()
            freezeButton.draw()
            font=pygame.font.Font(None,20)
            coindraw = font.render(str(coins), True, (255,255,0))
            coinrect = coindraw.get_rect()
            surface.blit(coindraw,coinrect)

            if freeze == True:
                mousePos=pygame.mouse.get_pos()
                pygame.draw.line(surface,(255,255,255),freezeButton.rect.center,mousePos)
            
            pygame.display.flip()
        case 2:
            surface.fill((0,0,0))
            
            for box in teamBox:
                box.draw()
            for box in mShopBox:
                box.draw()
            for box in iShopBox:
                box.draw()

            for unit in monsterShop:
                if unit != None:
                    unit.draw()
            for item in itemShop:
                if item != None:
                    item.draw()
            for unit in team:
                if unit != None:
                    unit.draw()
            
            readyButton.draw()
            rerollButton.draw()
            freezeButton.draw()
            font=pygame.font.Font(None,20)
            coindraw = font.render(str(coins), True, (255,255,0))
            coinrect = coindraw.get_rect()
            surface.blit(coindraw,coinrect)
            
            pygame.display.flip()
        case 3:
            surface.fill((0,0,0))


            pygame.display.flip()
        case 4:
            i=0
            surface.fill((0,0,0))
            for index, entry in enumerate(team1):
                if entry != None:    
                    if index == 0:
                        font = pygame.font.Font(size=50)
                        for monster in jmonster["LEVEL 1"]:
                            if monster["name"] == team1[index][0]:
                                colour = monster["colour"]
                        rect = pygame.Rect(screenWidth/2-200,screenHeight/2-100,100,200)
                        pygame.draw.rect(surface,colour,rect)
                        text = font.render(str(team1[index][1])+"      "+str(team1[index][2]), True, (255,255,255))
                        textRect = text.get_rect()
                        textRect.center = (screenWidth/2-200+textRect[2]/2,screenHeight/2+100-textRect[3]/2)
                        surface.blit(text,textRect)
                    else:
                        font = pygame.font.Font(size=20)
                        for monster in jmonster["LEVEL 1"]:
                            if monster["name"] == team1[index][0]:
                            
                                colour = monster["colour"]
                        rect = pygame.Rect(screenWidth/2-275-i*75,screenHeight/2,50,100)
                        pygame.draw.rect(surface,colour,rect)
                        text = font.render(str(team1[index][1])+"      "+str(team1[index][2]), True, (255,255,255))
                        textRect = text.get_rect()
                        textRect.center = (screenWidth/2-275-i*75+textRect[2]/2,screenHeight/2+100-textRect[3]/2)
                        surface.blit(text,textRect)
                        i+=1
            i=0
            for index, entry in enumerate(team2):
                if entry != None:
                    if index == 0:
                        font = pygame.font.Font(size=50)
                        for monster in jmonster["LEVEL 1"]:
                            if monster["name"] == team2[index][0]:
                                colour = monster["colour"]
                        rect = pygame.Rect(screenWidth/2+100,screenHeight/2-100,100,200)
                        pygame.draw.rect(surface,colour,rect)
                        text = font.render(str(team2[index][1])+"      "+str(team2[index][2]), True, (255,255,255))
                        textRect = text.get_rect()
                        textRect.center = (screenWidth/2+100+textRect[2]/2,screenHeight/2+100-textRect[3]/2)
                        surface.blit(text,textRect)
                    else:
                        font = pygame.font.Font(size=20)
                        for monster in jmonster["LEVEL 1"]:
                            if monster["name"] == team2[index][0]:
                                colour = monster["colour"]
                        rect = pygame.Rect(screenWidth/2+225+i*75,screenHeight/2,50,100)
                        pygame.draw.rect(surface,colour,rect)
                        text = font.render(str(team2[index][1])+"      "+str(team2[index][2]), True, (255,255,255))
                        textRect = text.get_rect()
                        textRect.center = (screenWidth/2+225+i*75+textRect[2]/2,screenHeight/2+100-textRect[3]/2)
                        surface.blit(text,textRect)
                        i+=1
            pygame.display.flip()
def freezeMode(surface):
    global freeze
    freeze = True
    while freeze:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                sys.exit()
        for index, unit in enumerate(monsterShop):
            try:
                if unit.is_held():
                    if unit.frozen:
                        unit.frozen = False
                    else:
                        unit.frozen = True
                    freeze = False
            except:
                pass
        for index, unit in enumerate(itemShop):
            try:
                if unit.is_held():
                    if unit.frozen:
                        unit.frozen = False
                    else:
                        unit.frozen = True
                    freeze = False
            except:
                pass
        redrawWindow(surface)
def main(surface) -> None:
    global gamestate, coins, waitingText, team1, team2
    fillShops(surface)
    makeHitboxes(surface)
    running = True
    gamestate = 0
    val = 0
    held = False
    connected = False
    i=0
    counter = 0
    t = 0
    while running:
        match gamestate:
            case 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                if not connected:
                    n=Network()
                if n.id=="Connected0" or n.id=="Connected1":
                    if i==0:
                        connected = True
                        waitingText = "Waiting for players..."
                        i+=1
                    if i==1:
                        Sready = n.send("ready")
                        if Sready == "start":
                            gamestate = 1
                            i=0
                    
                redrawWindow(surface)    

            case 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                for index, unit in enumerate(monsterShop):
                    if unit != None:
                        if unit.is_held() and held==False:
                            val = unit.id
                            held = True
                        elif not unit.is_held() and unit.id == val:
                            val = 0
                            held = False
                            for box in teamBox:
                                if box.is_colliding(unit.rect.center):
                                    if coins >= 3:
                                        coins-=3
                                        if team[box.index] == None:
                                            team[box.index] = unit
                                            team[box.index].frozen = False
                                            monsterShop[index] = None
                                        elif team[box.index] != None:
                                            if team[box.index].name == unit.name:
                                                if team[box.index].lv != 3:
                                                    team[box.index].hp += unit.hp
                                                    team[box.index].dmg += unit.dmg
                                                    team[box.index].exp += unit.exp+1
                                                    monsterShop[index] = None
                                                if team[box.index].exp == 2 and team[box.index].lv == 1:
                                                    team[box.index].lv = 2
                                                elif team[box.index].exp == 5 and team[box.index].lv == 2:
                                                    team[box.index].lv = 3
                        elif unit.id != val:
                            unit.x = 50+75*index
                            unit.y = 350
                            unit.rect = pygame.Rect(unit.x, unit.y, unit.w, unit.h)    
                        unit.move(val)
                for index, unit in enumerate(itemShop):
                    if unit != None:
                        if unit.is_held() and held==False:
                            val = unit.id
                            held = True
                        elif not unit.is_held() and unit.id == val:
                            val = 0
                            held = False
                            for box in teamBox:
                                if box.is_colliding(unit.rect.center):
                                    if coins>=3:
                                        coins-=3
                                        if team[box.index] != None:
                                            team[box.index].hp += unit.hpboost
                                            team[box.index].dmg += unit.dmgboost
                                            itemShop[index] = None
                        elif unit.id != val:
                            unit.x = 50+75*7+75*index
                            unit.y = 400
                            unit.rect = pygame.Rect(unit.x, unit.y, unit.w, unit.h)
                        unit.move(val)
                for index, unit in enumerate(team):
                    if unit != None:
                        if unit.is_held() and held==False:
                            val = unit.id
                            held = True
                        elif not unit.is_held() and unit.id == val:
                            val = 0
                            held = False
                            for box in mShopBox:
                                if box.is_colliding(unit.rect.center):
                                    coins+=team[index].exp+1
                                    team[index] = None
                            for box in teamBox:
                                if box.is_colliding(unit.rect.center):
                                    if team[box.index] == None:
                                        team[box.index] = unit
                                        team[index] = None
                                    elif team[box.index] != None and team[box.index].id != unit.id:
                                        if team[box.index].name == unit.name:
                                            if team[box.index].lv != 3:
                                                team[box.index].hp += unit.hp
                                                team[box.index].dmg += unit.dmg
                                                team[box.index].exp += unit.exp+1
                                                team[index] = None
                                            if team[box.index].exp == 2 and team[box.index].lv == 1:
                                                team[box.index].lv = 2
                                            elif team[box.index].exp == 5 and team[box.index].lv == 2:
                                                team[box.index].lv = 3
                                        else:
                                            placeholder = team[box.index]
                                            team[box.index] = unit
                                            team[index] = placeholder
                        elif unit.id != val:
                            unit.x = 500-75*index
                            unit.y = 150
                            unit.rect = pygame.Rect(unit.x, unit.y, unit.w, unit.h)
                        unit.move(val)
                    if readyButton.is_pressed():
                        "send(ready)"
                        gamestate=2
                    if rerollButton.is_pressed():
                        if coins > 0:
                            coins-=1
                            fillShops(surface)
                    if freezeButton.is_pressed():
                        freezeMode(surface)
                redrawWindow(surface)
            
            case 2:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                "write waiting for other players to get ready"
                Sready = n.send("Ready")
                if Sready == "fight":
                    gamestate = 3
                    i=0
                    print("Go to fight")
            case 3:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                if i == 0:
                    team1 = encodeTeam(team)
                    team2 = n.send(team1)
                    team1 = decodeTeam(team1)
                    team2 = decodeTeam(team2)
                    i+=1
                    gamestate = 4
            case 4:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                if counter == 60:
                    t+=1
                    counter = 0
                else:
                    counter+=1
                if t == 10:
                    if team1[0] == None or team2[0] == None:
                        if team1[0] == None:
                            print("Player 2 won")
                            coins = 10
                            gamestate = 1
                        elif team2[0] == None:
                            print("Player 1 won")
                            coins = 10
                            gamestate = 1
                    else:
                        team1[0][1] = team1[0][1]-team2[0][2]
                        team2[0][1] = team2[0][1]-team1[0][2]
                        if team1[0][1] <= 0:
                            team1.pop(0)
                        if team2[0][1] <= 0:
                            team2.pop(0)
                    t=0


                
                
            

#CODE PART
readyButton = Button(gameWindow, screenWidth-150, 400 ,100, 50, "Ready")
rerollButton = Button(gameWindow, 50, 200, 50, 50, "Roll")
freezeButton = Button(gameWindow, screenWidth-210, 400,50,50,"Freeze")
updateLists()
main(gameWindow)


