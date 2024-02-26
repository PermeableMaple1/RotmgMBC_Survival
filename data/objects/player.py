import pygame
import os


class Player(pygame.sprite.Sprite):

    def __init__(self, spritesheet, player_stats):
        super().__init__()

        self.spritesheet = pygame.image.load(os.path.join('data/graphics', spritesheet)).convert_alpha()
        self.image = pygame.Surface((56, 56), pygame.SRCALPHA)
        self.image.blit(self.spritesheet, (56, 0), (0, 0, 56, 56))
        self.rect = self.image.get_rect()

        self.hp = player_stats[0]
        self.maxhp = self.hp
        self.hp_ratio = 1
        self.player_spd = player_stats[1]
        self.defence = player_stats[2]
        self.vit = player_stats[3]
        self.damage_factor = 1

        self.animation_count = 0
        self.last_direction = 0

        self.blink = 0
        self.fade = 1

        self.dead = False

    def main(self, keys, screen_angle):
        rotation_state = 0
        scroll = pygame.math.Vector2(0, 0)

        if keys[pygame.K_a]:
            scroll[0] = 44 * (-5.6 * (self.player_spd + 53.5) / 75) / 60
        elif keys[pygame.K_d]:
            scroll[0] = 44 * (5.6 * (self.player_spd + 53.5) / 75) / 60
        if keys[pygame.K_w]:
            scroll[1] = 44 * (-5.6 * (self.player_spd + 53.5) / 75) / 60
        elif keys[pygame.K_s]:
            scroll[1] = 44 * (5.6 * (self.player_spd + 53.5) / 75) / 60

        if keys[pygame.K_e]:
            screen_angle += 2
            rotation_state = 1
        elif keys[pygame.K_q]:
            screen_angle -= 2
            rotation_state = -1
        screen_angle %= 360

        if keys[pygame.K_z]:
            screen_angle = 0
            rotation_state = 2

        self.image = self.animation(keys)
        self.hp_ratio = self.hp / self.maxhp
        if self.hp_ratio < 1:
            self.hp += (0.24 * self.vit + 1) / 60

        if self.hp_ratio <= 0.2:
            self.blink += 15 * self.fade
            if self.blink // 200 != 0:
                self.fade *= -1
                self.blink += 15 * self.fade
            self.image.fill((self.blink, 0, 0, 0), None, pygame.BLEND_RGBA_ADD)

        return scroll, screen_angle, rotation_state

    def animation(self, keys):
        frame_width = 56
        frame_height = frame_width
        img = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)

        if keys[pygame.K_a]:
            if self.animation_count + 1 >= 30:
                self.animation_count = 0
            self.animation_count += 1
            frame_no = self.animation_count//15
            frame = pygame.Rect((frame_width * (frame_no % 3), 0, frame_width, frame_height))
            img.blit(self.spritesheet, (0, 0), frame)
            img = pygame.transform.flip(img, True, False)
            self.last_direction = 0

        elif keys[pygame.K_d]:
            if self.animation_count + 1 >= 30:
                self.animation_count = 0
            self.animation_count += 1
            frame_no = self.animation_count//15
            frame = pygame.Rect((frame_width * (frame_no % 3), 0, frame_width, frame_height))
            img.blit(self.spritesheet, (0, 0), frame)
            self.last_direction = 1

        elif keys[pygame.K_s]:
            if self.animation_count + 1 >= 30:
                self.animation_count = 0
            self.animation_count += 1
            frame_no = self.animation_count // 15
            frame = pygame.Rect((frame_width * (frame_no % 3), 56, frame_width, frame_height))
            img.blit(self.spritesheet, (0, 0), frame)
            self.last_direction = 2

        elif keys[pygame.K_w]:
            if self.animation_count + 1 >= 30:
                self.animation_count = 0
            self.animation_count += 1
            frame_no = self.animation_count // 15
            frame = pygame.Rect((frame_width * (frame_no % 3), 112, frame_width, frame_height))
            img.blit(self.spritesheet, (0, 0), frame)
            self.last_direction = 3

        else:
            if self.last_direction == 0:
                frame = pygame.Rect((56, 0, frame_width, frame_height))
                img.blit(self.spritesheet, (0, 0), frame)
                img = pygame.transform.flip(img, True, False)

            elif self.last_direction == 1:
                frame = pygame.Rect((56, 0, frame_width, frame_height))
                img.blit(self.spritesheet, (0, 0), frame)

            elif self.last_direction == 2:
                frame = pygame.Rect((112, 0, frame_width, frame_height))
                img.blit(self.spritesheet, (0, 0), frame)

            elif self.last_direction == 3:
                frame = pygame.Rect((112, 56, frame_width, frame_height))
                img.blit(self.spritesheet, (0, 0), frame)

            self.animation_count = 0

        return img

    def healthbar(self, display):
        outline = pygame.Rect(self.rect.centerx - 22, self.rect.centery + 25, 45, 8)
        healthbar = pygame.Rect(self.rect.centerx - 22, self.rect.centery + 25, 45 * self.hp_ratio, 8)

        if self.hp_ratio <= 0.2:
            color = [200, 0, 0]
        elif self.hp_ratio < 0.5:
            color = [255, 150, 0]
        else:
            color = [50, 200, 0]

        pygame.draw.rect(display, color, healthbar)
        pygame.draw.rect(display, [0, 0, 0], outline, 1)
