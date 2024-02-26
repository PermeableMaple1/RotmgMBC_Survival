import pygame
import data
# import os
# import sys

# if getattr(sys, 'frozen', False):
#     os.chdir(os.path.dirname(sys.executable))

window_width = 1000
window_height = 1000

if __name__ == '__main__':
    pygame.display.init()

    screen = pygame.display.set_mode((window_width, window_height), flags=pygame.SCALED, vsync=1)
    screen_rect = screen.get_rect()
    screen_center = screen_rect.center

    pygame.display.set_caption('Look upon my mighty bulwark!')
    pygame.display.set_icon(pygame.image.load('data/graphics/spooky.png').convert_alpha())

    game = data.Game(screen)

    data.menu(game, screen)

    data.run_game(screen, game)
