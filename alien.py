from typing import Literal
import pygame
import setting


class Alien(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # 外星人位置信息
        self.image = pygame.image.load("./image/alien.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # 左右移动方向
        self.direction_x: Literal[1, -1] = 1

    def check_edge(self):
        """外星人是否超出屏幕"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def update(self):
        """更新外星人位置"""
        self.x += setting.alien_speed_x * setting.alien_move_direction
        self.rect.x = self.x

    def draw(self):
        """绘制外星人"""
        self.screen.blit(self.image, self.rect)
