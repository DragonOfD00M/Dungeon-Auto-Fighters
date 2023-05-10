import pygame
import sys
import json

pygame.init()
jmonster = json.load(open("jsons/monsters.json"))

team1="COBOLD%3%5#GOBLIN%10%10#None#None#None"
team2="GOBLIN%1%1#GOBLIN%1%1#GOBLIN%1%1#None#None"

size = width, height = 1000, 500
surface = pygame.display.set_mode(size)


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


team1 = decodeTeam(team1)
team2 = decodeTeam(team2)

def redrawWindow(surface):
    surface.fill((0,0,0))
    i=0
    for index, entry in enumerate(team1):
        if entry != None:    
            if index == 0:
                font = pygame.font.Font(size=50)
                for monster in jmonster["LEVEL 1"]:
                    if monster["name"] == team1[index][0]:
                        colour = monster["colour"]
                rect = pygame.Rect(width/2-200,height/2-100,100,200)
                pygame.draw.rect(surface,colour,rect)
                text = font.render(str(team1[index][1])+"      "+str(team1[index][2]), True, (255,255,255))
                textRect = text.get_rect()
                textRect.center = (width/2-200+textRect[2]/2,height/2+100-textRect[3]/2)
                surface.blit(text,textRect)
            else:
                font = pygame.font.Font(size=20)

                for monster in jmonster["LEVEL 1"]:
                    if monster["name"] == team1[index][0]:
                        colour = monster["colour"]
                rect = pygame.Rect(width/2-275-i*75,height/2,50,100)
                pygame.draw.rect(surface,colour,rect)
                text = font.render(str(team1[index][1])+"      "+str(team1[index][2]), True, (255,255,255))
                textRect = text.get_rect()
                textRect.center = (width/2-275-i*75+textRect[2]/2,height/2+100-textRect[3]/2)
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
                rect = pygame.Rect(width/2+100,height/2-100,100,200)
                pygame.draw.rect(surface,colour,rect)
                text = font.render(str(team2[index][1])+"      "+str(team2[index][2]), True, (255,255,255))
                textRect = text.get_rect()
                textRect.center = (width/2+100+textRect[2]/2,height/2+100-textRect[3]/2)
                surface.blit(text,textRect)
            else:
                font = pygame.font.Font(size=20)
                for monster in jmonster["LEVEL 1"]:
                    if monster["name"] == team2[index][0]:
                        colour = monster["colour"]
                rect = pygame.Rect(width/2+225+i*75,height/2,50,100)
                pygame.draw.rect(surface,colour,rect)
                text = font.render(str(team2[index][1])+"      "+str(team2[index][2]), True, (255,255,255))
                textRect = text.get_rect()
                textRect.center = (width/2+225+i*75+textRect[2]/2,height/2+100-textRect[3]/2)
                surface.blit(text,textRect)
                i+=1
    pygame.display.flip()
counter = 0
t = 0
while True:
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
                break
            elif team2[0] == None:
                print("Player 1 won")
                break
        else:
            team1[0][1] = team1[0][1]-team2[0][2]
            team2[0][1] = team2[0][1]-team1[0][2]
            if team1[0][1] <= 0:
                team1.pop(0)
            if team2[0][1] <= 0:
                team2.pop(0)
        t=0


    redrawWindow(surface)