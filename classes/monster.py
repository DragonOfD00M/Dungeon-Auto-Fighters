import pygame
import json
f = open("jsons/monsters.json")
jmonster = json.load(f)
class Monster:
    #None type functions
    def __init__(self, surface, pixX, pixY, id, name) -> None:
        #For Pygame
        self.x = pixX
        self.y = pixY
        self.w = 50
        self.h = 100
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.surface = surface
        self.id = id
        #Stats
        self.name = name
        i=0
        while i < len(jmonster["LEVEL 1"]):
            if self.name == jmonster["LEVEL 1"][i]["name"]:
                self.hp = jmonster["LEVEL 1"][i]["hp"]
                self.dmg = jmonster["LEVEL 1"][i]["dmg"]
                self.colour = jmonster["LEVEL 1"][i]["colour"]
            i+=1
        self.lv = 1
        self.exp = 0
        self.frozen=False

    def draw(self) -> None:
        if self.frozen:
            pygame.draw.rect(self.surface, self.colour, self.rect)
            pygame.draw.rect(self.surface, (54, 139, 193), self.rect, 2)
            pass
        else:
            pygame.draw.rect(self.surface, self.colour, self.rect)
        font = pygame.font.Font(None, 20)
        stats = font.render(str(self.dmg) + "   " + str(self.lv) + "   " + str(self.hp), True, (255,255,255))
        statsRect = stats.get_rect()
        statsRect.center = (self.w/2+self.x, self.y+self.h-statsRect[3]/2)
        self.surface.blit(stats, statsRect)
        

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