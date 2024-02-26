import pygame


class ColossalLaser(pygame.sprite.Sprite):

    def __init__(self, start_pos, angle, images):
        super().__init__()

        self.rotated_images = images
        self.image = self.rotated_images[angle].copy()
        self.angle = angle
        self.rect = self.image.get_rect(center=start_pos)

        self.position_vector = pygame.Vector2((1, 0)).rotate(angle)
        self.distance = 0
        self.damage = 300
        self.range = 818
        self.speed = 2.2
        self.true_dmg = 1
        self.status_effect = None

        self.hit = False
        self.hitbox = pygame.Rect(0, 0, 12, 12)

    def update(self, game_map):
        map_center = game_map.rect.center
        self.distance += self.speed
        self.position_vector = self.position_vector.normalize() * self.distance

        if game_map.rotation_state == 1:
            self.position_vector = self.position_vector.rotate(-2)
        elif game_map.rotation_state == -1:
            self.position_vector = self.position_vector.rotate(2)
        elif game_map.rotation_state == 2:
            self.position_vector = self.position_vector.rotate(game_map.rotation_reset)

        self.angle += 2
        self.angle %= 360
        self.image = self.rotated_images[self.angle].copy()
        self.rect = self.image.get_rect(center=(map_center+self.position_vector))
        self.hitbox.center = self.rect.center

        if self.distance >= self.range:
            self.kill()
