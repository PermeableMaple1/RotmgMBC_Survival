import pygame


class PopRockBullet(pygame.sprite.Sprite):

    def __init__(self, start_pos, angle, images, map_center):
        super().__init__()

        self.rotated_images = images
        self.angle = -angle % 360
        self.image = self.rotated_images[self.angle].copy()
        self.rect = self.image.get_rect(center=start_pos)
        self.pos0 = pygame.Vector2(start_pos) - map_center

        self.position_vector = pygame.Vector2((1, 0)).rotate(angle)
        self.distance = 0
        self.damage = 70
        self.range = 352
        self.speed = 5.87
        self.true_dmg = 0

        self.hit = False
        self.hitbox = pygame.Rect(0, 0, 12, 12)

    def update(self, game_map):
        map_center = game_map.rect.center
        # self.pos0 = self.pos0 - map_center
        self.distance += self.speed
        self.position_vector = self.position_vector.normalize() * self.distance

        if game_map.rotation_state == 1:
            self.pos0 = self.pos0.rotate(-2)
            self.position_vector = self.position_vector.rotate(-2)
            self.angle += 2
        elif game_map.rotation_state == -1:
            self.pos0 = self.pos0.rotate(2)
            self.position_vector = self.position_vector.rotate(2)
            self.angle -= 2
        elif game_map.rotation_state == 2:
            self.pos0 = self.pos0.rotate(game_map.rotation_reset)
            self.position_vector = self.position_vector.rotate(game_map.rotation_reset)
            self.angle -= game_map.rotation_reset

        self.angle %= 360
        self.image = self.rotated_images[self.angle].copy()
        self.rect = self.image.get_rect(center=(self.position_vector + self.pos0 + map_center))
        self.hitbox.center = self.rect.center

        if self.distance >= self.range:
            self.kill()
