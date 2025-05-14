import pygame
from ship import Ship
import setting


class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface, ship: Ship):
        super().__init__()
        self.screen = screen
        # 子弹位置信息
        self.rect = pygame.Rect(0, 0, setting.bullet_width, setting.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(ship.rect.y)

    def update(self):
        """更新子弹位置"""
        self.y -= setting.bullet_speed
        self.rect.y = self.y

    def draw(self):
        """绘制子弹"""
        pygame.draw.rect(self.screen, setting.bullet_color, self.rect)
