import pygame
from .create_text import create_text


class DmgText(pygame.sprite.Sprite):

    def __init__(self, text, true_dmg, display):
        super().__init__()

        pygame.font.init()
        dmgtext = '-' + str(round(text))

        if true_dmg:
            color = (248, 0, 22)
        else:
            color = (121, 14, 232)

        self.image = create_text(dmgtext, 2, 25, color)

        self.rect = self.image.get_rect(center=display.get_rect().center)
        self.rect.centery -= 18
        self.y0 = self.rect.centery

        self.lifetime = 0

    def update(self):
        y = self.y0 - self.rect.centery
        yn = 54
        if y < yn:
            self.rect.centery -= 2
        if self.lifetime >= 1:
            self.kill()
        self.lifetime += 1/60
