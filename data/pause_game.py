import pygame
import sys
import data.objects


def pause_game(game, screen):
    screen_rect = screen.get_rect()

    text = data.objects.create_text('Paused', 3, 50, (255, 255, 255))
    text_rect = text.get_rect(center=screen_rect.center)

    bg = pygame.Surface(screen_rect[2:4])
    bg.set_alpha(128)
    bg.fill((25, 25, 25))

    screen.blit(bg, (0, 0))

    while game.paused:

        screen.blit(text, text_rect)

        pygame.display.flip()

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_p:
                    game.paused = False
                elif ev.key == pygame.K_m:
                    game.in_menu = True
                    game.paused = False
                    data.menu(game, screen, game.player_stats)
                elif ev.key == pygame.K_r:
                    game.paused = False
                    game.load_game()
