import pygame


class ColossalRock(pygame.sprite.Sprite):

    def __init__(self, start_pos, angle):
        super().__init__()

        self.spritesheet = self.spritesheet = pygame.image.load(
            'data/graphics/Bullets/BulletSheet2.png').convert_alpha()
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        self.image.blit(self.spritesheet, (0, 0), (0, 32, 32, 32))
        self.image = pygame.transform.scale(self.image, (22, 22))
        self.rect = self.image.get_rect(center=start_pos)

        self.position_vector = pygame.Vector2((1, 0)).rotate(angle)
        self.distance = 0
        self.damage = 80
        self.range = 1100
        self.speed = 3.7
        self.true_dmg = 0
        self.status_effect = 'Silenced'

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

        self.rect = self.image.get_rect(center=(map_center + self.position_vector))
        self.hitbox.center = self.rect.center

        if self.distance >= self.range:
            self.kill()
