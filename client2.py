"""
Pygame bruges til det visuelle og til user input
Sys bruges til at lukke programmet hvis pygame lukkes
json bruges til at læse datafilerne for monstre og items
random bruges til shoppen hvor der kommer tilfældige monstre og items
time bruges til et nyt randomseed hver gang.
math bruges til udregninger. Specielt loading cirklen.
"""
import pygame
import sys
import os
import json
import random
import time
import math

#Initiere pygame og setter randomseedet til tiden i sekunder siden epoch
pygame.init()
random.seed(time.time())

#Åbner monster filen og gemmer dataen i jsonmonster
f = open("monsters.json")
jsonmonster = json.load(f)

f = open("items.json")
jsonitem = json.load(f)

#Definere farver for hurgtigere at bruge dem senere.
black = (0,0,0)
white = (255,255,255)
gray1 = (255/2, 255/2, 255/2)
gray2 = (255/4, 255/4, 255/4)
red = (255,0,0)

#Definere de forskellige lister med faste størelser.
team = [None, None, None, None, None]
teambox = [None, None, None, None, None]
shop = [None, None, None, None, None, None, None]

#Unit ID er en specifik id til hver unit.
uid = 0


class Button:
    """
    Button er en klasse der fungere som en knap. Når den bliver trykket, gør den noget.
    """
    def __init__(self, surface, x, y, width, height, text) -> None:
        """
        posx er pixelkoordinaten for topvenstrehjørnet på x-aksen af knappen og bruger inputtet x.
        posy er pixelkoordinaten for topvenstrehjørnet på y-aksen af knappen og bruger inputtet y.
        width er hvor mange pixels længden af knappen er langs x-aksen og bruger inputtet width.
        height er hvor mange pixels længden af knapper er langs y-aksen og bruger inputtet height.
        rect er et pygame Rect det tager posx, posy, width og height og definere derved knappens størelse.

        surface er en pygame surface som knappen skal være bundet til og bruger indputtet surface.
        text er hvad der skal stå på knappen og bruger inputtet text.
        
        Den retunerer ikke nogle værdier.
        """
        self.posx = x
        self.posy = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.posx, self.posy, self.width, self.height)

        self.surface = surface
        self.text = text

    def draw(self) -> None:
        """
        Funktionen draw bruger pygame funktioner til at tegne en hvid firkant på skærmen med de tidligere definerede størelser 
        og skriver en sort tekst ovenpå med den tidligere definerede tekst.

        Den returnerer ikke nogle værdier.
        """
        font = pygame.font.Font(None, 40)
        btnText = font.render(self.text, True, black)
        btnRect = btnText.get_rect()
        btnRect.center = (self.width/2+self.posx, self.height/2+self.posy)
        pygame.draw.rect(self.surface, white, self.rect)
        self.surface.blit(btnText, btnRect)

    def is_click(self) -> bool:
        """
        Funktionen is_click checker om musens koordinater er inde i knappens rect og om musen er trykket ned.
        Hvis begge ting er sande vil den returnerer True
        Ellers vil den returnerer False
        """
        mousePos = pygame.mouse.get_pos()
        mousePress = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mousePos) and mousePress[0]:
            return True
        else:
            return False

class Position:
    """
    Position er en klasse der fungerer som en hitbox.
    Den representerer en fysisk position i en liste.
    """
    def __init__(self, surface, x, y, arrayIndex) -> None:
        """
        posx er pixelkoordinaten for topvenstrehjørnet på x-aksen af knappen og bruger inputtet x.
        posy er pixelkoordinaten for topvenstrehjørnet på y-aksen af knappen og bruger inputtet y.
        width er hvor mange pixels længden af knappen er langs x-aksen og er fast 50.
        height er hvor mange pixels længden af knapper er langs y-aksen og er fast 100.
        rect er et pygame Rect det tager posx, posy, width og height og definere derved knappens størelse.

        surface er en pygame surface som knappen skal være bundet til og bruger indputtet surface.     
        index er et id der svare til en position i et array.

        Den retunerer ikke nogle værdier.   
        """
        self.posx = x
        self.posy = y
        self.width = 50
        self.height = 100  
        self.rect = pygame.Rect(self.posx, self.posy, self.width, self.height)

        self.surface = surface
        self.index = arrayIndex
    
    def draw(self) -> None:
        """
        Funktionen draw tegner en hvid outline som svarer til hitboxens størelse.

        Den returnerer ikke nogle værdier.
        """
        pygame.draw.rect(self.surface, white, self.rect, 1)

    def is_colliding(self, point) -> bool:
        """
        Funktionen is is_colliding checker tager et input 'point' og tjækker om det punkt er inde for objektets rect.

        Hvis punktet er inde i objektets rect returnerer den True
        Ellers returnerer den False
        """
        if self.rect.collidepoint(point):
            return True
        else:
            return False

class Unit:
    """
    Unit er en klasse 
    """
    def __init__(self, surface, level, unitName, x, y, id, shoppos) -> None:
        """
        
        """
        self.width = 50
        self.height = 100
        self.posx = x
        self.posy = y
        self.rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        
        self.name=str(unitName)
        self.level = "LEVEL " + str(level)
        self.surface = surface
        self.id = id
        self.shoppos = shoppos
        self.teampos = None
        self.unitLV = 1
        self.unitXP = 0

        i=0
        while i < len(jsonmonster[self.level]):
            if jsonmonster[self.level][i]["name"]==self.name:
                self.colour = (jsonmonster[self.level][i]['colour'][0], jsonmonster[self.level][i]['colour'][1], jsonmonster[self.level][i]['colour'][2])
                self.HP=jsonmonster[self.level][i]["HP"]
                self.DMG=jsonmonster[self.level][i]["DMG"]
            i+=1
    def draw(self) -> None:
        """
        
        """
        font=pygame.font.Font(None, 20)
        text = str(self.DMG) + "   " + str(self.unitLV) + "   " + str(self.HP)
        stats = font.render(text, True, white)
        statsRect = stats.get_rect()
        statsRect.center = (self.width/2+self.posx, self.height-statsRect.bottom+self.posy)
        pygame.draw.rect(self.surface, self.colour, self.rect)
        self.surface.blit(stats,statsRect)

    def move(self, value) -> None:
        """
        
        """
        if (value == self.id or value == -1) and self.is_moving():
            mousePos = pygame.mouse.get_pos()
            self.posx = mousePos[0]-self.width/2
            self.posy = mousePos[1]-self.height/2
            self.rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        
    def is_hovered(self) -> bool:
        """
        
        """
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            return True
        else:
            return False
        
    def is_clicked(self) -> bool:
        """
        
        """
        mousePress = pygame.mouse.get_pressed()
        if self.is_hovered() and mousePress[0]:
            return True
        else:
            return False
        
    def is_sold(self) -> bool:
        """
        
        """
        mousePress = pygame.mouse.get_pressed()
        keyPress = pygame.key.get_pressed()
        if self.is_hovered() and mousePress[0] and keyPress[pygame.K_LCTRL]:
            return True
        else:
            return False
        
    def is_moving(self) -> bool:
        """
        
        """
        mousePress = pygame.mouse.get_pressed()
        keyPress = pygame.key.get_pressed()
        if self.is_hovered() and mousePress[0] and keyPress[pygame.K_LSHIFT]:
            return True
        else:
            return False

class Item:
    def __init__(self) -> None:
        pass

    def draw(self) -> None:
        pass

    def move(self) -> None:
        pass

    


gamestate = None
size = screenWidth, screenHeight = 1000,500
gameScreen = pygame.display.set_mode(size)
Clock = pygame.time.Clock()

def redrawWindow(surface):
    """
    
    """
    global coins
    match gamestate:
        case 0:
            #Gamestate 0 er venter på spillere skærmen
            #Alle variabler der skal bruges til udregningen af loading cirklen
            radius=40
            counter=1
            t=1
            T=20
            omega = (2*math.pi)/T
            
            ttw = "Waiting for players..."
            font = pygame.font.Font(None,50)
            text = font.render(ttw,True,white)
            textRect=text.get_rect()
            textRect.center = (screenWidth/2, screenHeight/4)

            surface.fill(black)
            #Loopet tegner loading cirklen
            while t <= T:
                surface.fill(black)
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
                pygame.draw.circle(surface,gray2,center3,15)
                pygame.draw.circle(surface,gray1,center2,15)
                pygame.draw.circle(surface,white,center1, 15)
                pygame.display.flip()
                if counter==60:
                    t+=1
                    counter=0
                counter+=1

            
            pygame.display.flip()
        case 1:
            #Gamestate 1 er den personlige holdbygge skærm.
            surface.fill(black)
            text = str(coins)
            font = pygame.font.Font(None, 20)
            coin = font.render(text, True, (255, 255, 0))
            coinRect = coin.get_rect()
            surface.blit(coin, coinRect)
            ReadyButton.draw()
            for box in teambox:
                try:
                    box.draw()
                except:
                    pass
            for unit in shop:
                try:
                    unit.draw()
                except:
                    pass
            for unit in team:
                try:
                    unit.draw()
                except:
                    pass
            pygame.display.flip()
        case 2:
            surface.fill(black)
            pygame.display.flip()
        case _:
            surface.fill(red)
            pygame.display.flip()

def rerollUnits(surface):
    """
    
    """
    global uid
    i=0
    while i<5:
        shop[i] = Unit(surface,1,monsterList[random.randint(0,len(monsterList)-1)],250+75*i,250,uid,i)
        uid+=1
        i+=1

def main(surface):
    """
    
    """
    global gamestate, uid, coins
    running = True
    held = False
    value = -1
    gamestate = 0
    i=0
    while i<5:
        shop[i] = Unit(surface,1,monsterList[random.randint(0,len(monsterList)-1)],250+75*i,250,uid,i)
        uid+=1
        i+=1
    i=0
    while i<5:
        teambox[i] = Position(surface, 550-75*i, 100, i)
        i+=1
    while running:
        Clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYUP and gamestate == 0:
                if event.key == pygame.K_SPACE:
                    rerollUnits(surface)
                    gamestate = 1
            if event.type == pygame.KEYUP and gamestate == 1:
                if event.key == pygame.K_r and coins >= 1:
                    rerollUnits(surface)
                    coins-=1
                elif event.key == pygame.K_c:
                    coins+=10
        if ReadyButton.is_click():
            gamestate = 2
            running = False
        for unit in shop:
            purchased = False
            try:
                if unit.is_clicked():
                    for posnum, posval in enumerate(team):
                        if posval == None and purchased==False and coins >= 3:
                            team[posnum] = shop[unit.shoppos]
                            shop[unit.shoppos] = None
                            unit.teampos = posnum
                            coins-=3
                            purchased = True    
                        elif purchased:
                            pass
            except:
                pass
        i=0
        for index, unit in enumerate(team):
            try:
                if unit.is_sold():
                    team[unit.teampos] = None
                    coins+=unit.unitXP+1  
                    del unit
                if unit.is_moving() and held==False:
                    value = unit.id
                    held=True
                elif not unit.is_moving() and unit.id == value:
                    value = -1
                    held=False
                    for box in teambox:
                        if box.is_colliding(unit.rect.center):
                            if team[box.index] == None:
                                team[unit.teampos] = None
                                team[box.index] = unit
                                unit.teampos = box.index
                            elif team[box.index] != None and team[box.index].id != unit.id:
                                if team[box.index].name == unit.name and team[box.index].unitLV != 3:
                                    team[box.index].unitXP+=unit.unitXP+1
                                    team[box.index].HP+=unit.HP
                                    team[box.index].DMG+=unit.DMG
                                    team[unit.teampos] = None
                                    if team[box.index].unitXP>=2 and team[box.index].unitLV == 1:
                                        team[box.index].unitLV = 2
                                    elif team[box.index].unitXP>=5 and team[box.index].unitLV == 2:
                                        team[box.index].unitLV = 3
                                elif team[box.index].name != unit.name:
                                    buf1 = team[unit.teampos]
                                    buf2 = unit.teampos
                                    team[unit.teampos] = team[box.index]
                                    unit.teampos = team[box.index].teampos
                                    team[box.index].teampos = buf2
                                    team[box.index] = buf1
                if value != unit.id:
                    team[index].posx = 550-75*unit.teampos
                    team[index].posy = 100
                    team[index].rect = pygame.Rect(team[index].posx, team[index].posy, team[index].width, team[index].height)
                elif value == unit.id:
                    unit.move(value)

            except:
                pass
        redrawWindow(surface)


monsterList = []
for x in jsonmonster["LEVEL 1"]:
    monsterList.append(x["name"])
itemList = []
for x in jsonitem["LEVEL 1"]:
    itemList.append(x["name"])


coins = 10

ReadyButton = Button(gameScreen, screenWidth-175, screenHeight/2-75/2, 150, 75, "READY")

main(gameScreen)
teamsend = team
send = ""


for pos, unit in enumerate(team):
    try:
        teamsend[pos] = unit.name + "¤" + str(unit.HP) + "¤" + str(unit.DMG) + "¤" + str(unit.unitLV) + "¤" + str(unit.unitXP)
    except:
        teamsend[pos] = unit
for pos, unit in enumerate(teamsend):
    if pos < len(teamsend)-1:
        send = send + str(teamsend[pos]) + "%"
    elif pos == len(teamsend)-1:
        send = send + str(teamsend[pos])
#Formaten for send er følgende:
#Navn ¤ liv ¤ skade ¤ level ¤ xp % ... % ---||---.
print(send)