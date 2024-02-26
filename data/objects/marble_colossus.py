import pygame
import os
from random import randint
from data.objects import bullets
from data.objects.pop_rock import PopRock


class MBC(pygame.sprite.Sprite):

    def __init__(self, spritesheet, colossal_laser_images, colossal_spear_images, pop_rock_bullet_images):
        super().__init__()

        self.spritesheet = pygame.image.load(os.path.join('data/graphics', spritesheet)).convert_alpha()
        self.image = pygame.Surface((128, 128), pygame.SRCALPHA)
        self.image.blit(self.spritesheet, (0, 0), (0, 0, 128, 128))
        self.rect = self.image.get_rect()

        self.animation_count = 0
        self.bullet_timer = [2, 2]
        self.laser_timer = 0
        self.laser_angle = 0
        self.bullet_group = pygame.sprite.Group()
        self.bullet_functions = [self.colossal_spear, self.colossal_rock]

        self.colossal_laser_images = colossal_laser_images
        self.laser_direction = 1
        self.time_since_direction_change = 0
        self.time_to_direction_change = randint(5, 20)

        self.colossal_spear_images = colossal_spear_images
        self.spear_direction = None
        self.current_angle = None

        self.pop_rock_bullets = pop_rock_bullet_images
        self.pop_rock_timer = 4
        self.pop_rock_group = pygame.sprite.Group()

    def update(self, game_map):

        map_center = game_map.rect.center
        self.rect.center = map_center

        self.bullet_timer = [x - 1 / 60 for x in self.bullet_timer]
        self.laser_timer -= 1/60
        self.time_since_direction_change += 1/60
        self.change_laser_direction()
        self.shoot_laser()
        self.shoot_pop_rock()

        if game_map.rotation_state == 1:
            self.laser_angle -= 2
        elif game_map.rotation_state == -1:
            self.laser_angle += 2
        elif game_map.rotation_state == 2:
            self.laser_angle += game_map.rotation_reset
        self.current_angle = 0

        self.spear_direction = game_map.offset.normalize().rotate(180)
        self.image = self.animation()

        self.bullet_group.update(game_map)
        self.pop_rock_group.update(game_map)

    def animation(self):
        frame_width = 128
        frame_height = frame_width
        img = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)

        if any(i <= 0 for i in self.bullet_timer):
            if self.animation_count + 1 >= 30:
                self.animation_count = 0
                self.shoot_bullets()
            self.animation_count += 1
            frame_no = self.animation_count // 10
            frame = pygame.Rect((frame_width * (frame_no % 3), 0, frame_width, frame_height))
            img.blit(self.spritesheet, (0, 0), frame)

        else:
            img.blit(self.spritesheet, (0, 0), (0, 0, 128, 128))
        return img

    def shoot_bullets(self):

        for i in range(2):
            if self.bullet_timer[i] <= 0:
                self.bullet_functions[i]()
        self.bullet_timer = [y if x <= 0 else x for x, y in zip(self.bullet_timer, [5, 6])]

    def shoot_laser(self):
        if self.laser_timer <= 0:
            for i in range(6):
                bullet = bullets.ColossalLaser(self.rect.center, (60 * i + self.laser_angle) % 360,
                                               self.colossal_laser_images)
                self.bullet_group.add(bullet)
            self.laser_timer = 0.2
            self.laser_angle += self.laser_direction * 2
            self.laser_angle %= 360

    def colossal_spear(self):
        for i in range(3):
            spread = [-30, 0, 30]
            bullet = bullets.ColossalSpear(self.rect.center, (self.current_angle + spread[i]) % 360,
                                           self.colossal_spear_images, self.spear_direction)
            self.bullet_group.add(bullet)

    def colossal_rock(self):
        for i in range(36):
            bullet = bullets.ColossalRock(self.rect.center, 10 * i)
            self.bullet_group.add(bullet)

    def change_laser_direction(self):
        if self.time_since_direction_change >= self.time_to_direction_change:
            self.laser_direction *= -1
            self.time_to_direction_change = randint(5, 20)
            self.time_since_direction_change = 0

    def shoot_pop_rock(self):
        if self.pop_rock_timer <= 0:
            pop_rock = PopRock('Pop_Rock.png', self.pop_rock_bullets, self.bullet_group)
            self.pop_rock_group.add(pop_rock)
            self.pop_rock_timer = 2
        else:
            self.pop_rock_timer -= 1/60

