import pygame
import sys
import os
from pytmx.util_pygame import load_pygame
from data.objects import create_text
from data.objects import Button


def menu(game, screen, player_stats=None):
    screen_rect = screen.get_rect()
    screen_center = screen_rect.center
    clock = pygame.time.Clock()

    if player_stats is None:
        player_stats = [900, 60, 60, 80]

    title = create_text('Marble Colossus Survival', 3, 50, (255, 255, 255))
    title_rect = title.get_rect(center=(screen_rect.centerx, screen_rect.centery - 150))
    subtitle = create_text('Press \'Space\' to begin!', 3, 25, (255, 255, 255))
    subtitle_rect = subtitle.get_rect(center=(screen_rect.centerx, screen_rect.centery - 50))

    tmx_data = load_pygame(os.path.join(r'data\map', 'lost_halls_boss_room.tmx'))
    layer = tmx_data.get_layer_by_name('Tile Layer 1')
    bg = pygame.Surface((1056, 1056))
    for x, y, surf in layer.tiles():
        bg.blit(surf, (x * 32, y * 32))
    bg = pygame.transform.scale(bg, (1452, 1452))
    bg_rect = bg.get_rect(center=(screen_rect.centerx, screen_rect.top + 150))

    hp_stat = create_text(str(player_stats[0]) + ' HP', 2, 25, (50, 206, 212))
    spd_stat = create_text(str(player_stats[1]) + ' SPD', 2, 25, (43, 207, 106))
    def_stat = create_text(str(player_stats[2]) + ' DEF', 2, 25, (85, 85, 85))
    vit_stat = create_text(str(player_stats[3]) + ' VIT', 2, 25, (255, 7, 44))
    towers_setting = create_text('Towers: ' + str(game.towers), 2, 25, (255, 255, 255))
    new_stats = player_stats

    button_group = pygame.sprite.Group()
    decrease_button = ((0, 12.5), (30, 0), (30, 25))
    increase_button = ((0, 0), (0, 25), (30, 12.5))

    hp_stat_rect = hp_stat.get_rect(center=(screen_center[0] - 200, screen_center[1] + 100))
    hp_button1 = Button(30, 25, hp_stat_rect.centerx - 100, hp_stat_rect.centery,
                        decrease_button, player_stats, 0, -1)
    hp_button2 = Button(30, 25, hp_stat_rect.centerx + 100, hp_stat_rect.centery,
                        increase_button, player_stats, 0, 1)
    button_group.add(hp_button1, hp_button2)

    spd_stat_rect = spd_stat.get_rect(center=(screen_center[0] + 200, screen_center[1] + 100))
    spd_button1 = Button(30, 25, spd_stat_rect.centerx - 100, spd_stat_rect.centery,
                         decrease_button, player_stats, 1, -1)
    spd_button2 = Button(30, 25, spd_stat_rect.centerx + 100, spd_stat_rect.centery,
                         increase_button, player_stats, 1, 1)
    button_group.add(spd_button1, spd_button2)

    def_stat_rect = def_stat.get_rect(center=(screen_center[0] - 200, screen_center[1] + 200))
    def_button1 = Button(30, 25, def_stat_rect.centerx - 100, def_stat_rect.centery,
                         decrease_button, player_stats, 2, -1)
    def_button2 = Button(30, 25, def_stat_rect.centerx + 100, def_stat_rect.centery,
                         increase_button, player_stats, 2, 1)
    button_group.add(def_button1, def_button2)

    vit_stat_rect = vit_stat.get_rect(center=(screen_center[0] + 200, screen_center[1] + 200))
    vit_button1 = Button(30, 25, vit_stat_rect.centerx - 100, vit_stat_rect.centery,
                         decrease_button, player_stats, 3, -1)
    vit_button2 = Button(30, 25, vit_stat_rect.centerx + 100, vit_stat_rect.centery,
                         increase_button, player_stats, 3, 1)
    button_group.add(vit_button1, vit_button2)

    towers_setting_rect = towers_setting.get_rect(center=(screen_center[0], screen_center[1] + 300))
    towers_button1 = Button(30, 25, towers_setting_rect.centerx - 150, towers_setting_rect.centery,
                            decrease_button, player_stats, game.towers, -1)
    towers_button2 = Button(30, 25, towers_setting_rect.centerx + 150, towers_setting_rect.centery,
                            increase_button, player_stats, game.towers, 1)
    button_group.add(towers_button1, towers_button2)

    while game.in_menu:
        clock.tick(60)

        screen.fill((0, 0, 0))
        screen.blit(bg, bg_rect)
        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)

        hp_stat = create_text(str(player_stats[0]) + ' HP', 2, 25, (50, 206, 212))
        spd_stat = create_text(str(player_stats[1]) + ' SPD', 2, 25, (43, 207, 106))
        def_stat = create_text(str(player_stats[2]) + ' DEF', 2, 25, (85, 85, 85))
        vit_stat = create_text(str(player_stats[3]) + ' VIT', 2, 25, (255, 7, 44))
        towers_setting = create_text('Towers: ' + str(game.towers), 2, 25, (255, 255, 255))

        screen.blit(hp_stat, hp_stat_rect)
        screen.blit(def_stat, def_stat_rect)
        screen.blit(spd_stat, spd_stat_rect)
        screen.blit(vit_stat, vit_stat_rect)
        screen.blit(towers_setting, towers_setting_rect)

        mouse = pygame.mouse.get_pos()

        button_group.update()
        button_group.draw(screen)

        pygame.display.flip()

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    button_group.empty()
                    game.player_stats = new_stats
                    screen.blit(bg, bg_rect)
                    pygame.display.flip()
                    game.load_game()
                    game.in_menu = False

            for button in button_group:
                if button.rect.collidepoint(mouse):
                    button.cursor = True
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        new_stats = button.update_stats()
                        if isinstance(new_stats, bool):
                            game.towers = new_stats
                            new_stats = player_stats
                        button.held_down = True
                    elif ev.type == pygame.MOUSEBUTTONUP:
                        button.held_down = False
                        button.timer = 0
                else:
                    button.cursor = False
        for button in button_group:
            if button.held_down:
                button.timer += 1 / 60
                if button.timer > 3:
                    for i in range(5):
                        new_stats = button.update_stats()
                    if isinstance(new_stats, bool):
                        game.towers = new_stats
                        new_stats = player_stats
                elif button.timer > 0.5:
                    new_stats = button.update_stats()
                    if isinstance(new_stats, bool):
                        game.towers = new_stats
                        new_stats = player_stats
