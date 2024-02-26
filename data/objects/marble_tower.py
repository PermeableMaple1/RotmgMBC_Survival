import pygame
import os
from itertools import cycle, islice
from data.objects.bullets import SpiralBullet
from random import choice


class Tower(pygame.sprite.Sprite):

    def __init__(self, spritesheet, tower_type, position_vector, no, bullet_images, bullet_group):
        super().__init__()

        self.spritesheet = pygame.image.load(os.path.join('data/graphics', spritesheet)).convert_alpha()
        self.image = pygame.Surface((44, 109), pygame.SRCALPHA)
        self.image.blit(self.spritesheet, (0, 0), (44 * tower_type, 0, 44, 109))
        self.rect = self.image.get_rect(center=position_vector)

        self.tower_type = tower_type
        types = list(range(7))
        starting_type = types.index(self.tower_type)
        self.types = cycle(types[starting_type:]+types[:starting_type])
        self.type_timer = 34
        self.tower_no = no
        self.screen_angle = 0

        self.bullet_images = bullet_images
        self.bullet_group = bullet_group
        self.bullet_timer = 2
        self.behavior_timer = [18, 10, 10]
        self.bullet_behaviors = [self.shot_behavior1, self.shot_behavior2, self.shot_behavior3]
        self.behavior_no = islice(cycle([0, 1, 2]), choice([0, 1, 2]), None)
        self.current_behavior = next(self.behavior_no)
        self.shot_behavior3_angle = 90

    def update(self, game_map):
        if self.type_timer <= 0:
            self.tower_type = next(self.types)
            self.image = pygame.Surface((44, 109), pygame.SRCALPHA)
            self.image.blit(self.spritesheet, (0, 0), (44 * self.tower_type, 0, 44, 109))
            self.type_timer = 32
        else:
            self.type_timer -= 1/60

        self.rect.bottom = game_map.tower_positions[self.tower_no][1] + game_map.rect.centery
        self.rect.centerx = game_map.tower_positions[self.tower_no][0] + game_map.rect.centerx

        self.screen_angle = game_map.current_angle
        self.shoot_bullets()

    def shoot_bullets(self):
        if self.bullet_timer <= 0:
            if self.behavior_timer[self.current_behavior] <= 0:
                self.current_behavior = next(self.behavior_no)
                self.behavior_timer = [y if x <= 0 else x for x, y in zip(self.behavior_timer, [16, 8, 8])]
            self.bullet_behaviors[self.current_behavior]()
        else:
            self.bullet_timer -= 1 / 60
            self.behavior_timer[self.current_behavior] -= 1/60

    def shot_behavior1(self):
        for i in range(8):
            bullet = SpiralBullet(self.rect.center, 45*i, self.screen_angle, self.bullet_images[self.tower_type],
                                  self.tower_type, self.tower_no)
            self.bullet_group.add(bullet)
        self.bullet_timer = 2

    def shot_behavior2(self):
        for i in range(10):
            bullet = SpiralBullet(self.rect.center, 36*i, self.screen_angle, self.bullet_images[self.tower_type],
                                  self.tower_type, self.tower_no)
            self.bullet_group.add(bullet)
        self.bullet_timer = 2

    def shot_behavior3(self):
        for i in range(2):
            bullet = SpiralBullet(self.rect.center, 180*i + self.shot_behavior3_angle, self.screen_angle,
                                  self.bullet_images[self.tower_type],
                                  self.tower_type, self.tower_no)
            self.bullet_group.add(bullet)
        self.shot_behavior3_angle -= 18
        self.bullet_timer = 0.5
