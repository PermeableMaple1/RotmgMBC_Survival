import pygame
import os
from random import shuffle
import math
import data
from data import objects
from pytmx.util_pygame import load_pygame


class Game:

    def __init__(self, screen, player_stats=None):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.loading_progress = 0

        self.screen_angle = 0
        self.total_time = 0

        self.game_map = None
        self.map_images = {}
        self.wall_masks = {}
        self.player = None
        self.MBC = None

        if player_stats is None:
            self.player_stats = [900, 60, 60, 80]
        self.player_hitbox = pygame.Rect((self.screen_rect.centerx - 15, self.screen_rect.centery - 36), (32, 40))
        surf = pygame.Surface((26, 26), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 255, 255, 255), (13, 13), 13)
        self.player_wall_hitbox = pygame.mask.from_surface(surf)
        self.player_wall_hitbox_rect = self.player_wall_hitbox.get_rect(center=(self.screen_rect.centerx,
                                                                                self.screen_rect.centery))

        self.colossal_laser_images = None
        self.colossal_spear_images = None
        self.bulletsheet1_images = []

        self.loading_bar()
        text = objects.create_text('Loading...', 1, 25, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.centerx = self.screen_rect.centerx
        text_rect.centery = self.screen_rect.centery - 30
        self.screen.blit(text, text_rect)
        pygame.display.flip()

        self.generate_rotated_images()

        self.pop_rock_bullets = self.bulletsheet1_images[7]

        self.tower_group = pygame.sprite.Group()
        self.towers = True
        self.marble_rock_group = pygame.sprite.Group()
        self.text_group = pygame.sprite.Group()

        self.paused = False
        self.in_menu = True

    def generate_rotated_images(self):
        tmx_data = load_pygame(os.path.join(r'data\map', 'lost_halls_boss_room.tmx'))
        layer = tmx_data.get_layer_by_name('Tile Layer 1')

        walls = []
        for tile in layer.__iter__():
            if tile[2] == 1:
                walls.append(tile[:2])

        image = pygame.Surface((1056, 1056))
        wall_image = pygame.Surface((1056, 1056), pygame.SRCALPHA)

        for x, y, surf in layer.tiles():
            image.blit(surf, (x * 32, y * 32))
            if (x, y) in walls:
                wall_image.blit(surf, (x * 32, y * 32))

        image = pygame.transform.scale(image, (1452, 1452))
        wall_image = pygame.transform.scale(wall_image, (1452, 1452))

        self.map_images = self.rotate_images(image)
        wall_images = self.rotate_images(wall_image)

        for angle in wall_images:
            wall_mask = pygame.mask.from_surface(wall_images[angle])
            self.wall_masks[angle] = wall_mask

        mbc_bullet_spritesheet = pygame.image.load(
            'data/graphics/Bullets/BulletSheet2.png').convert_alpha()

        image = pygame.Surface((32, 32), pygame.SRCALPHA)
        image.blit(mbc_bullet_spritesheet, (0, 0), (0, 0, 32, 32))
        self.colossal_laser_images = self.rotate_images(image)

        image = pygame.Surface((32, 32), pygame.SRCALPHA)
        image.blit(mbc_bullet_spritesheet, (0, 0), (32, 0, 32, 32))
        image = pygame.transform.scale(image, (48, 48))
        image = pygame.transform.rotate(image, -45)
        self.colossal_spear_images = self.rotate_images(image)

        bullet_sheet1 = pygame.image.load(
            'data/graphics/Bullets/BulletSheet1.png').convert_alpha()
        for i in range(8):
            image = pygame.Surface((32, 32), pygame.SRCALPHA)
            image.blit(bullet_sheet1, (0, 0), (32 * i, 0, 32, 32))
            image = pygame.transform.scale(image, (38, 38))
            if i == 7:
                image = pygame.transform.rotate(image, -45)
            rotated_images = self.rotate_images(image)
            self.bulletsheet1_images.append(rotated_images)

    def load_game(self):
        self.screen_angle = 0
        self.total_time = 0

        self.game_map = objects.Map(self.map_images, self.wall_masks, self.screen)

        self.player = objects.Player('Player.png', self.player_stats)
        self.player.rect.centerx = self.screen_rect.centerx
        self.player.rect.centery = self.screen_rect.centery - 18

        self.MBC = objects.MBC('MBC.png', self.colossal_laser_images, self.colossal_spear_images,
                               self.pop_rock_bullets)

        if self.towers is True:
            towers = list(range(7))
            shuffle(towers)
            for i in range(4):
                tower_type = towers.pop()
                tower = objects.Tower('Towers.png', tower_type, self.game_map.tower_positions[i], i,
                                      self.bulletsheet1_images, self.MBC.bullet_group)
                self.tower_group.add(tower)

        rocks = list(range(7))
        shuffle(rocks)
        for i in range(2):
            rock_type = rocks.pop()
            rock = objects.MarbleRock('Rocks.png', rock_type, self.game_map.rock_positions[i], i,
                                      self.bulletsheet1_images, self.MBC.bullet_group)
            self.marble_rock_group.add(rock)

    def update(self, keys):

        scroll, self.screen_angle, rotation = self.player.main(keys, self.screen_angle)
        scroll = self.wall_collision(scroll)

        self.game_map.update(self.screen, scroll, self.screen_angle, rotation)
        self.MBC.update(self.game_map)
        self.tower_group.update(self.game_map)
        self.marble_rock_group.update(self.game_map)
        self.bullet_damage()
        self.text_group.update()

    def draw(self):

        self.screen.blit(self.game_map.image, self.game_map.rect)
        self.screen.blit(self.player.image, self.player.rect)
        self.MBC.pop_rock_group.draw(self.screen)
        self.MBC.bullet_group.draw(self.screen)
        self.marble_rock_group.draw(self.screen)
        self.screen.blit(self.MBC.image, self.MBC.rect)
        self.tower_group.draw(self.screen)
        self.text_group.draw(self.screen)

        self.player.healthbar(self.screen)

    def wall_collision(self, scroll):
        offset_x = self.game_map.wall_mask_rect.left - self.player_wall_hitbox_rect.left
        offset_y = self.game_map.wall_mask_rect.top - self.player_wall_hitbox_rect.top
        area = self.player_wall_hitbox.overlap_area(self.game_map.wall_mask, (offset_x, offset_y))
        dx = self.player_wall_hitbox.overlap_area(self.game_map.wall_mask, (offset_x + 1, offset_y)) - \
            self.player_wall_hitbox.overlap_area(self.game_map.wall_mask, (offset_x - 1, offset_y))
        dy = self.player_wall_hitbox.overlap_area(self.game_map.wall_mask, (offset_x, offset_y + 1)) - \
            self.player_wall_hitbox.overlap_area(self.game_map.wall_mask, (offset_x, offset_y - 1))
        normal = pygame.math.Vector2(-dx, -dy)
        wall_parallel_left = pygame.math.Vector2(-dy, dx)
        wall_parallel_right = pygame.math.Vector2(dy, -dx)

        if dx or dy:
            left_con = abs(scroll.angle_to(wall_parallel_left)) < 90 or abs(scroll.angle_to(wall_parallel_left)) > 270
            right_con = abs(scroll.angle_to(wall_parallel_right)) < 90 or abs(scroll.angle_to(wall_parallel_right)) > 270
            if (dx * scroll[0]) < 0:
                if left_con and scroll[0] != 0:
                    scroll.scale_to_length(
                        math.floor(scroll.magnitude() * math.cos(math.radians(scroll.angle_to(wall_parallel_left)))))
                    scroll = scroll.rotate(scroll.angle_to(wall_parallel_left))
                elif right_con and scroll[0] != 0:
                    scroll.scale_to_length(
                        math.floor(scroll.magnitude() * math.cos(math.radians(scroll.angle_to(wall_parallel_right)))))
                    scroll = scroll.rotate(scroll.angle_to(wall_parallel_right))
                else:
                    scroll[0] = 0
            if (dy * scroll[1]) < 0:
                if left_con and scroll[1] != 0:
                    scroll.scale_to_length(
                        math.floor(scroll.magnitude() * math.cos(math.radians(scroll.angle_to(wall_parallel_left)))))
                    scroll = scroll.rotate(scroll.angle_to(wall_parallel_left))
                elif right_con and scroll[1] != 0:
                    scroll.scale_to_length(
                        math.floor(scroll.magnitude() * math.cos(math.radians(scroll.angle_to(wall_parallel_right)))))
                    scroll = scroll.rotate(scroll.angle_to(wall_parallel_right))
                else:
                    scroll[1] = 0
            if area > 20:
                scroll = scroll - normal.normalize()

        return scroll

    def bullet_damage(self):
        for bullet in self.MBC.bullet_group:
            if self.player_hitbox.colliderect(bullet.hitbox) and bullet.hit is False:
                if bullet.true_dmg * self.player.defence >= bullet.damage:
                    damage = 1
                else:
                    damage = (bullet.damage - bullet.true_dmg * self.player.defence) * self.player.damage_factor
                    dmgtext = objects.DmgText(damage, bullet.true_dmg, self.screen)
                    self.text_group.add(dmgtext)
                self.player.hp -= damage
                bullet.hit = True

    def death_screen(self):

        self.screen.blit(self.game_map.image, self.game_map.rect)

        self.player.image = pygame.Surface((56, 56), pygame.SRCALPHA)
        self.player.image.blit(self.player.spritesheet, (0, 0), (112, 112, 56, 56))
        self.screen.blit(self.player.image, self.player.rect)

        self.MBC.pop_rock_group.draw(self.screen)
        self.MBC.bullet_group.draw(self.screen)
        self.marble_rock_group.draw(self.screen)
        self.screen.blit(self.MBC.image, self.MBC.rect)
        self.tower_group.draw(self.screen)
        data.post_time(self.total_time / 1000, self.screen)

        bg = pygame.Surface(self.screen_rect[2:4])
        bg.set_alpha(128)
        bg.fill((25, 25, 25))
        self.screen.blit(bg, (0, 0))

    def rotate_images(self, image):
        rotated_images = {}

        for angle in range(0, 360, 1):
            rotated_image = pygame.transform.rotate(image, angle)
            rotated_images[angle] = rotated_image
        self.loading_progress += 1 / 12
        self.loading_bar()

        return rotated_images

    def loading_bar(self):
        loading_bar = pygame.rect.Rect(self.screen_rect.centerx - 100, self.screen_rect.centery, 200, 25)
        progress_bar = pygame.rect.Rect(self.screen_rect.centerx - 100, self.screen_rect.centery,
                                        int(200 * self.loading_progress), 25)
        pygame.draw.rect(self.screen, (255, 255, 255), loading_bar, 3)
        pygame.draw.rect(self.screen, (255, 255, 255), progress_bar)

        pygame.display.update(progress_bar)
        pygame.event.pump()
