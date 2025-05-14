"""飞船模块"""

from typing import Literal
import pygame
import setting

MoveAction = Literal["left", "right", "up", "down", "stop"]


class Ship:
    def __init__(self, screen: pygame.Surface):
        # 屏幕宽高
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # 飞船信息
        self.image = pygame.image.load("./image/ship.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # 飞船移动
        self.move_action: MoveAction = "stop"
        # rect对象的centerx只存整数
        self.centerx = float(self.rect.centerx)

    def update(self):
        """更新飞船位置"""
        if self.move_action == "left" and self.rect.left > 0:
            self.centerx -= setting.move_speed
        if self.move_action == "right" and self.rect.right < self.screen_rect.right:
            self.centerx += setting.move_speed
        self.rect.centerx = self.centerx

    def draw(self):
        """绘制飞船"""
        self.screen.blit(self.image, self.rect)
