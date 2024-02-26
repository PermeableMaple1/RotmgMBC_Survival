import pygame
import sys
import data
from data.objects import create_text


def death(game, screen):
    screen_rect = screen.get_rect()

    title = create_text('You died!', 3, 60, (255, 7, 44))
    title_rect = title.get_rect(center=(screen_rect.centerx, screen_rect.centery - 150))

    subtitle = create_text('Press r to try again.', 2, 25, (255, 255, 255))
    subtitle_rect = subtitle.get_rect(center=(screen_rect.centerx, screen_rect.centery + 150))

    game.death_screen()

    while game.player.dead:

        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)

        pygame.display.flip()

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_m:
                    game.in_menu = True
                    game.tower_group.empty()
                    game.marble_rock_group.empty()
                    game.text_group.empty()
                    game.MBC.bullet_group.empty()
                    data.menu(game, screen, game.player_stats)
                elif ev.key == pygame.K_r:
                    game.tower_group.empty()
                    game.marble_rock_group.empty()
                    game.text_group.empty()
                    game.MBC.bullet_group.empty()
                    game.load_game()
