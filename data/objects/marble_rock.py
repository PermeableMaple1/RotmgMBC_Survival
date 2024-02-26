import pygame
import os
from itertools import cycle
from data.objects.bullets import SpiralBullet


class MarbleRock(pygame.sprite.Sprite):

    def __init__(self, spritesheet, rock_type, position_vector, no, bullet_images, bullet_group):
        super().__init__()

        self.spritesheet = pygame.image.load(os.path.join('data/graphics', spritesheet)).convert_alpha()
        self.image = pygame.Surface((49, 49), pygame.SRCALPHA)
        self.image.blit(self.spritesheet, (0, 0), (49 * rock_type, 0, 49, 49))
        self.image = pygame.transform.scale(self.image, (44, 44))
        self.rect = self.image.get_rect(center=position_vector)

        self.rock_type = rock_type
        types = list(range(7))
        starting_type = types.index(self.rock_type)
        self.types = cycle(types[starting_type:] + types[:starting_type])
        self.type_timer = 10
        self.rock_no = no
        self.screen_angle = 0

        self.bullet_images = bullet_images
        self.bullet_group = bullet_group
        self.bullet_timer = 2
        self.bullet_angle = 90

    def update(self, game_map):
        if self.type_timer <= 0:
            self.rock_type = next(self.types)
            self.image = pygame.Surface((49, 49), pygame.SRCALPHA)
            self.image.blit(self.spritesheet, (0, 0), (49 * self.rock_type, 0, 49, 49))
            self.image = pygame.transform.scale(self.image, (44, 44))
            self.type_timer = 8
        else:
            self.type_timer -= 1/60

        self.rect.center = game_map.rect.center + game_map.rock_positions[self.rock_no]

        self.screen_angle = game_map.current_angle
        self.shoot_bullets()

    def shoot_bullets(self):
        if self.bullet_timer <= 0:
            for i in range(3):
                bullet = SpiralBullet(self.rect.center, 120*i + self.bullet_angle + 5 * self.rock_no, self.screen_angle,
                                      self.bullet_images[self.rock_type], self.rock_type, self.rock_no, False)
                self.bullet_group.add(bullet)
            self.bullet_timer = 0.15
            self.bullet_angle += 12
        else:
            self.bullet_timer -= 1 / 60
