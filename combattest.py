import pygame
import sys
import json

team1="COBOLD%3%5#None#None#None#None"
team2="GOBLIN%1%1#GOBLIN%1%1#GOBLIN%1%1#None#None"

f = open("jsons/items.json")
jitem = json.load(f)
f = open("jsons/monsters.json")
jmonster = json.load(f)

pygame.init()
size = screenWidth, screenHeight = 1000, 500
gameWindow = pygame.display.set_mode(size)
gamestate = None
Clock = pygame.time.Clock()



def decodeTeam(string):
    list = string.split("#")
    return list

def redrawWindow(surface):
    surface.fill((0,0,0))
    
    for index, unit in enumerate(lteam1):
        if unit != "None":
            unit=unit.split("%")
            i=0
            while i < len(jmonster["LEVEL 1"]):
                if unit[0] == jmonster["LEVEL 1"][i]["name"]:
                    colour=jmonster["LEVEL 1"][i]["colour"]
                i+=1
            pygame.draw.rect(surface,colour,(350-75*index, 150,50,100))
        else:
            pass
    for index, unit in enumerate(lteam2):
        if unit != "None":
            unit=unit.split("%")
            i=0
            while i < len(jmonster["LEVEL 1"]):
                if unit[0] == jmonster["LEVEL 1"][i]["name"]:
                    colour=jmonster["LEVEL 1"][i]["colour"]
                i+=1
            pygame.draw.rect(surface,colour,(575+75*index, 150,50,100))
        else:
            pass
    pygame.display.flip()

def main(surface):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        redrawWindow(surface)
lteam1=decodeTeam(team1)
lteam2=decodeTeam(team2)
main(gameWindow)


    
