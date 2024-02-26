import pygame


class Map(pygame.sprite.Sprite):

    def __init__(self, rotated_images, wall_masks, screen):
        super().__init__()

        screen_rect = screen.get_rect()
        self.rotated_images = rotated_images
        self.wall_masks = wall_masks
        self.image = self.rotated_images[0].copy()
        self.wall_mask = self.wall_masks[0].copy()

        pos0 = pygame.math.Vector2(screen_rect.centerx, screen_rect.top + 150)
        self.offset = pos0 - screen_rect.center
        self.rect = self.image.get_rect(center=pos0)
        self.wall_mask_rect = self.wall_mask.get_rect(center=self.rect.center)
        self.current_angle = 0
        self.rotation_reset = 0
        self.rotation_state = 0

        self.tower_positions = [pygame.Vector2(-352, -352),
                                pygame.Vector2(352, -352),
                                pygame.Vector2(-352, 352),
                                pygame.Vector2(352, 352)]

        self.rock_positions = [pygame.Vector2(66, 0), pygame.Vector2(66, 0).rotate(-10)]

    def update(self, screen, scroll, screen_angle, rotation):
        screen_center = pygame.math.Vector2(screen.get_rect().center)
        rect_center = pygame.math.Vector2(self.rect.center) - scroll

        self.image = self.rotated_images[screen_angle].copy()
        self.wall_mask = self.wall_masks[screen_angle].copy()

        self.offset = rect_center - screen_center

        if rotation == 1:
            position_vector = self.offset.rotate(-2)
            self.tower_positions = [x.rotate(-2) for x in self.tower_positions]
            self.rock_positions = [x.rotate(-2) for x in self.rock_positions]
        elif rotation == -1:
            position_vector = self.offset.rotate(2)
            self.tower_positions = [x.rotate(2) for x in self.tower_positions]
            self.rock_positions = [x.rotate(2) for x in self.rock_positions]
        elif rotation == 2:
            self.rotation_reset = self.current_angle
            position_vector = self.offset.rotate(self.rotation_reset)
            self.tower_positions = [x.rotate(self.rotation_reset) for x in self.tower_positions]
            self.rock_positions = [x.rotate(self.rotation_reset) for x in self.rock_positions]
        else:
            position_vector = self.offset

        self.rock_positions = [x.rotate(-6) for x in self.rock_positions]

        self.current_angle = screen_angle
        self.rotation_state = rotation
        self.rect = self.image.get_rect(center=(screen_center + position_vector))
        self.wall_mask_rect = self.wall_mask.get_rect(center=self.rect.center)
