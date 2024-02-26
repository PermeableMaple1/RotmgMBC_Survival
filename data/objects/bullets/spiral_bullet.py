import pygame


class SpiralBullet(pygame.sprite.Sprite):

    def __init__(self, start_pos, angle,  angle0, images, type_, no, tower=True):
        super().__init__()

        self.rotated_images = images
        self.image = self.rotated_images[angle % 360].copy()
        self.angle = angle
        self.rect = self.image.get_rect(center=start_pos)

        self.position_vector = pygame.Vector2((1, 0)).rotate(angle - angle0)
        self.distance = 0
        self.damage = 150
        self.range = 1100
        self.speed = 3.67
        if type_ == 0:
            self.true_dmg = 0
            self.status_effect = None
        else:
            self.true_dmg = 1
            status_effects = ['Quiet', 'Bleeding', 'Curse', 'Pet Stasis', 'Dazed', 'Slowed']
            self.status_effect = status_effects[type_ - 1]

        self.no = no
        self.tower = tower
        self.original_angle = 0
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

        self.angle -= 10
        self.angle %= 360
        self.image = self.rotated_images[self.angle].copy()
        self.original_angle += 6

        if self.tower is True:
            map_position = game_map.tower_positions[self.no] + map_center
        else:
            map_position = game_map.rock_positions[self.no].rotate(self.original_angle) + map_center
        self.rect = self.image.get_rect(center=(map_position + self.position_vector))
        self.hitbox.center = self.rect.center

        if self.distance >= self.range:
            self.kill()
