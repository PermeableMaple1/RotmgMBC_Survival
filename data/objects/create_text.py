import pygame


def create_text(text, border, size, color):
    pygame.font.init()
    font = pygame.font.Font('data/graphics/Pixeloid.ttf', size)
    text_img = font.render(text, True, color).convert_alpha()
    outline = font.render(text, True, (0, 0, 0)).convert_alpha()

    img = pygame.Surface((text_img.get_width() + border, text_img.get_height() + border), pygame.SRCALPHA)
    x = img.get_rect().centerx
    y = img.get_rect().centery
    text_rect = text_img.get_rect(center=(x, y))

    outline_rect = outline.get_rect(center=(x + border, y))
    img.blit(outline, outline_rect)
    outline_rect = outline.get_rect(center=(x - border, y))
    img.blit(outline, outline_rect)
    outline_rect = outline.get_rect(center=(x, y + border))
    img.blit(outline, outline_rect)
    outline_rect = outline.get_rect(center=(x, y - border))
    img.blit(outline, outline_rect)
    img.blit(text_img, text_rect)

    return img
