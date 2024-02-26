import pygame
import sys
import data


def run_game(screen, game):
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        screen.fill((0, 0, 0))

        keys = pygame.key.get_pressed()

        game.update(keys)

        game.draw()

        data.post_time(game.total_time / 1000, screen)
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                sys.exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_p:
                    game.paused = True
                    data.pause_game(game, screen)
                elif ev.key == pygame.K_m:
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
        if pygame.display.get_active() is False:
            game.paused = True
            data.pause_game(game, screen)

        if game.player.hp < 0:
            game.player.dead = True
            data.death(game, screen)

        game.total_time += clock.get_time()
        pygame.display.flip()
