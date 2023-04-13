import pygame

class Button:
    def __init__(self, surface, pixX, pixY, pixW, pixH, text) -> None:
        self.x = pixX
        self.y = pixY
        self.w = pixW
        self.h = pixH
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.surface = surface
        self.text = text
        self.pressed = False

    def draw(self) -> None:
        pygame.draw.rect(self.surface, (255,255,255), self.rect)
        
        font = pygame.font.Font(None, round(self.w/(len(self.text)/2)))
        displayText=font.render(self.text, True, (0,0,0))
        dTextRect = displayText.get_rect()
        dTextRect.center = (self.w/2+self.x, self.h/2+self.y)
        self.surface.blit(displayText,dTextRect)

    def is_pressed(self) -> bool:
        mousePos = pygame.mouse.get_pos()
        mousePress = pygame.mouse.get_pressed()
        if self.rect.collidepoint(mousePos) and mousePress[0]:
            self.pressed = True
        else:
            if self.pressed:
                self.pressed = False
                return True
            else: 
                return False