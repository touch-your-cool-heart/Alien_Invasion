from asyncio import Event
import sys
import pygame
import setting
from ship import Ship
from bullet import Bullet
from alien import Alien


def check_event(screen: pygame.Surface, ship: Ship, bullets: pygame.sprite.Group):
    """事件监听"""
    for event in pygame.event.get():
        # 退出
        if event.type == pygame.QUIT:
            exit()
        # 键盘按下
        elif event.type == pygame.KEYDOWN:
            handle_keydown(screen, ship, bullets, event)
        # 键盘弹起
        elif event.type == pygame.KEYUP:
            ship.move_action = "stop"


def handle_keydown(
    screen: pygame.Surface,
    ship: Ship,
    bullets: pygame.sprite.Group,
    event: Event,
):
    """键盘按下事件处理"""
    if event.key == pygame.K_RIGHT:
        ship.move_action = "right"
    elif event.key == pygame.K_LEFT:
        ship.move_action = "left"
    elif event.key == pygame.K_SPACE:
        if len(bullets) < setting.bullet_count_limit:
            bullet = Bullet(screen, ship)
            bullets.add(bullet)
    elif event.key == pygame.K_ESCAPE:
        exit()
    else:
        ship.move_action = "stop"


def update_screen(
    screen: pygame.Surface,
    ship: Ship,
    bullets: pygame.sprite.Group,
    aliens: pygame.sprite.Group,
):
    """重绘画面"""
    screen.fill(setting.screen_bg_color)
    ship.draw()
    for bullet in bullets:
        bullet.draw()
    for alien in aliens:
        alien.draw()
    pygame.display.flip()


def update_bullets(
    screen: pygame.Surface,
    bullets: pygame.sprite.Group,
    aliens: pygame.sprite.Group,
    ship: Ship,
):
    """更新所有子弹位置"""
    bullets.update()
    remove_overflow_bullets(bullets)
    # 碰撞检测并销毁
    pygame.sprite.groupcollide(bullets, aliens, True, True)
    # 重新生成外星人群
    if len(aliens) == 0:
        bullets.empty()
        batch_create_aliens(screen, aliens, ship)


def update_aliens(screen: pygame.Surface, aliens: pygame.sprite.Group, ship: Ship):
    """更新外星人群位置"""
    change_aliens_direction(aliens)
    aliens.update()
    if check_game_over(screen, aliens, ship):
        print("Game over!!!")
        exit()


def batch_create_aliens(
    screen: pygame.Surface, aliens: pygame.sprite.Group, ship: Ship
):
    """批量创建外星人"""
    alien = Alien(screen)
    aliens_line_count = get_alien_line_count(alien.rect.width)
    alien_lines = get_alien_lines(alien.rect.height, ship.rect.height)

    for line_index in range(alien_lines):
        for alien_index in range(aliens_line_count):
            create_alien(screen, aliens, alien_index, line_index)


def check_game_over(screen: pygame.Surface, aliens: pygame.sprite.Group, ship: Ship):
    """检测游戏是否失败"""
    # 是否和飞船发生碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        return True
    # 外星人是否触碰到屏幕底部
    for alien in aliens:
        if alien.rect.bottom >= screen.get_rect().bottom:
            return True
    return False


def exit():
    """退出游戏"""
    pygame.quit()
    sys.exit()


# --------------------------------------------------------------------------


def remove_overflow_bullets(bullets: pygame.sprite.Group):
    """移出超出屏幕的子弹"""
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def change_aliens_direction(aliens: pygame.sprite.Group):
    """触碰屏幕边缘后，改变外星人群移动方向"""
    isTouchEdge = False
    for alien in aliens:
        if alien.check_edge():
            isTouchEdge = True
            break
    if isTouchEdge == False:
        return
    for alien in aliens:
        alien.rect.y += setting.alien_speed_y
    setting.alien_move_direction *= -1


def get_alien_line_count(alien_width: int):
    """计算每行最多可容纳外星人数量"""
    available_width = setting.screen_width - 2 * alien_width
    return int(available_width / (2 * alien_width))


def get_alien_lines(alien_height: int, ship_height: int):
    """最多容纳多少行"""
    available_height = setting.screen_height - 3 * alien_height - ship_height
    return int(available_height / (2 * alien_height))


def create_alien(
    screen: pygame.Surface, aliens: pygame.sprite.Group, x_index: int, y_index: int
):
    """创建外星人"""
    alien = Alien(screen)
    alien.x = alien.rect.width + x_index * 2 * alien.rect.width
    alien.rect.x = alien.x
    alien.y = alien.rect.height + y_index * 2 * alien.rect.height
    alien.rect.y = alien.y
    aliens.add(alien)
