import pygame

class Hitbox:
    def __init__(self, surface, pixX, pixY, pixW, pixH, index) -> None:
        self.x = pixX
        self.y = pixY
        self.w = pixW
        self.h = pixH
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.surface = surface

        self.index = index
    def draw(self) -> None:
        pygame.draw.ellipse(self.surface,(255,255,255),(self.x-self.w+75/2, self.y+self.h-37.5/2, 75, 37.5))

    def is_colliding(self, point) -> bool:
        if self.rect.collidepoint(point):
            return True
        else:
            return False