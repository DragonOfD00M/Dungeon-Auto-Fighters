import pygame
import json
f = open("jsons/items.json")
jitem = json.load(f)
class Item:
    def __init__(self, surface, pixX, pixY, id, name) -> None:
        #For pygame
        self.x = pixX
        self.y = pixY
        self.w = 50
        self.h = 50
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.surface = surface
        self.id = id
        #Stats
        self.name = name
        self.frozen = False
        i = 0
        while i < len(jitem["LEVEL 1"]):
            if self.name == jitem["LEVEL 1"][i]["name"]:
                self.hpboost = jitem["LEVEL 1"][i]["hp"]
                self.dmgboost = jitem["LEVEL 1"][i]["dmg"]
                self.effect = jitem["LEVEL 1"][i]["effect"]
                self.colour = jitem["LEVEL 1"][i]["colour"]
            i+=1

    def draw(self) -> None:
        if self.frozen:
            pygame.draw.rect(self.surface, self.colour, self.rect)
            pygame.draw.rect(self.surface, (54, 139, 193), self.rect, 2)
            pass
        else:
            pygame.draw.rect(self.surface, self.colour, self.rect)

    def move(self, val) -> None:
        mousePos = pygame.mouse.get_pos()
        if self.is_held() and val == self.id:
            self.x = mousePos[0]-self.w/2
            self.y = mousePos[1]-self.h/2
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    #Bool type functions
    def is_held(self) -> bool:
        mousePos = pygame.mouse.get_pos()
        mousePress = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mousePos) and mousePress[0]:
            return True
        else:
            return False