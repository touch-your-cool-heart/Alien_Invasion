import pygame
import setting
from game_function import (
    check_event,
    update_screen,
    update_bullets,
    update_aliens,
    batch_create_aliens,
)
from ship import Ship


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))
    pygame.display.set_caption("Alien Invasion")

    ship = Ship(screen)
    bullets = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    batch_create_aliens(screen, aliens, ship)

    while True:
        check_event(screen, ship, bullets)
        ship.update()
        update_bullets(screen, bullets, aliens, ship)
        update_aliens(screen, aliens, ship)
        update_screen(screen, ship, bullets, aliens)


run_game()
