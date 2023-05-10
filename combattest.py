import pygame
import sys
import json

team1="COBOLD%3%5#None#None#None#None"
team2="GOBLIN%1%1#GOBLIN%1%1#GOBLIN%1%1#None#None"

f = open("jsons/monsters.json")
jmonster = json.load(f)

pygame.init()
size = screenWidth, screenHeight = 1000, 500
gameWindow = pygame.display.set_mode(size)
gamestate = None
Clock = pygame.time.Clock()
currentTeam = 1

counter = 0
t = 0
i1 = 0
i2 = 0

def decodeTeam(team):
    result = team.split("#")
    for index, unit in enumerate(result):
        if unit == 'None':
            result[index] = None
        else:
            result[index] = unit.split("%")

    return result

font = pygame.font.Font(None, 50)

def battle(Team1, Team2, surface):
    global counter, t, i1, i2
    if Team1[i1] != None:
        unit1 = Team1[i1]
    else:
        print("Player 2 Wins")
        return [], []
    if Team2[i2] != None:
        unit2 = Team2[i2]
    else:
        print("Player 1 Wins")
        return [], []
    surface.fill((0,0,0))

    for num in [1,2]:
        if num == 1:
            i=0
            while i < len(jmonster["LEVEL 1"]):
                if unit1[0]==jmonster["LEVEL 1"][i]["name"]:
                    colour = jmonster["LEVEL 1"][i]["colour"]
                i+=1
            rect = pygame.Rect(300+t,150,100,200)
            pygame.draw.rect(surface, colour, rect)
            stats1 = font.render(str(unit1[1]) + "      " + str(unit1[2]), True, (255,255,255))
            stats1Rect = stats1.get_rect()
            stats1Rect.center = (350+t, 350-stats1Rect[3]/2)
        elif num == 2:
            i=0
            while i < len(jmonster["LEVEL 1"]):
                if unit2[0]==jmonster["LEVEL 1"][i]["name"]:
                    colour = jmonster["LEVEL 1"][i]["colour"]
                i+=1
            rect = pygame.Rect(600-t,150,100,200)
            pygame.draw.rect(surface, colour, rect)
            stats2 = font.render(str(unit2[1]) + "      " + str(unit2[2]), True, (255,255,255))
            stats2Rect = stats2.get_rect()
            stats2Rect.center = (650-t, 350-stats2Rect[3]/2)
    surface.blit(stats1,stats1Rect)
    surface.blit(stats2,stats2Rect)
    pygame.display.flip()
    if int(unit1[1]) >= 0 and int(unit2[1]) >= 0:
        if counter==10 and t<=100:
            t+=1
            counter=0
        elif t>=100:
                Team1[i1][1] = int(Team1[i1][1])-int(Team2[i2][2])
                Team2[i2][1] = int(Team2[i2][1])-int(Team1[i1][2])
                t=0
        else:
            counter+=1
    if int(Team1[i1][1])<=0:
        i1+=1
    if int(Team2[i2][1])<=0:
        i2+=1
    return Team1, Team2

def main(surface):
    global Team1, Team2
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if Team1 != []:
            Team1, Team2 = battle(Team1, Team2, surface)


Team1 = decodeTeam(team1)
Team2 = decodeTeam(team2)
main(gameWindow)
    
