import pygame
import os
from random import randint
from data.objects import bullets


class PopRock(pygame.sprite.Sprite):

    def __init__(self, spritesheet, bullet_images, bullet_group):
        super().__init__()

        self.spritesheet = pygame.image.load(os.path.join('data/graphics', spritesheet)).convert_alpha()
        self.image = pygame.Surface((49, 49), pygame.SRCALPHA)
        self.image.blit(self.spritesheet, (0, 0), (0, 0, 49, 49))
        self.image = pygame.transform.scale(self.image, (44, 44))
        self.rect = self.image.get_rect()

        self.position_vector = pygame.Vector2((1, 0)).rotate(randint(0, 359))

        self.bullet_images = bullet_images
        self.bullet_group = bullet_group
        self.distance = 1
        self.player_vector = pygame.Vector2((0, 0))
        self.speed = randint(2, 4) * 44 / 60
        self.lifespan = 8
        self.fuse = 0.75
        self.range = 704

        self.explosion = False
        self.blink = 0
        self.fade = 1

    def update(self, game_map):
        map_center = game_map.rect.center
        self.player_vector = (self.position_vector + game_map.offset)

        conditions = [self.player_vector.magnitude() <= 30, self.explosion, self.distance >= self.range,
                      self.lifespan <= 0]
        if any(conditions):
            self.explode(map_center)

        if self.explosion is False:
            if self.player_vector.magnitude() <= 220:
                self.position_vector = self.position_vector - self.player_vector.normalize()*self.speed
                self.distance = self.position_vector.magnitude()
            else:
                self.distance += self.speed
                self.position_vector = self.position_vector.normalize() * self.distance

        if game_map.rotation_state == 1:
            self.position_vector = self.position_vector.rotate(-2)
        elif game_map.rotation_state == -1:
            self.position_vector = self.position_vector.rotate(2)
        elif game_map.rotation_state == 2:
            self.position_vector = self.position_vector.rotate(game_map.rotation_reset)

        self.rect = self.image.get_rect(center=(map_center+self.position_vector))

        self.lifespan -= 1/60

    def explode(self, map_center):
        self.explosion = True
        self.image = pygame.Surface((49, 49), pygame.SRCALPHA)
        self.image.blit(self.spritesheet, (0, 0), (49, 0, 49, 49))
        self.image = pygame.transform.scale(self.image, (44, 44))

        self.blink += 25 * self.fade
        if self.blink // 200 != 0:
            self.fade *= -1
            self.blink += 25 * self.fade
        self.image.fill((self.blink, 0, 0, 0), None, pygame.BLEND_RGBA_ADD)

        if self.fuse <= 0:
            for i in range(8):
                bullet = bullets.PopRockBullet(self.rect.center, 45 * i, self.bullet_images,
                                               map_center)
                self.bullet_group.add(bullet)
            self.kill()

        self.fuse -= 1/60
