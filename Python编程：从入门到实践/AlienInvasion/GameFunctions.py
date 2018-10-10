# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     GameFunctions
   Description :
   Author :        Liangz
   Date：          2018/10/8
-------------------------------------------------
   Change Activity:
                   2018/10/8:
-------------------------------------------------
"""
__author__ = 'Liangz'

import sys
import pygame
from Bullet import Bullet

def check_keydown_events(event, game_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # # 创建一颗子弹，并将其加入到编组bullets中
        # if len(bullets) < game_settings.bullets_allowed:
        #     new_bullet = Bullet(game_settings, screen, ship)
        #     bullets.add(new_bullet)
        fire_bullet(game_settings, screen, ship, bullets)


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def chech_events(game_settings, screen, ship, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_RIGHT:
            #     # 向右移动飞船
            #     ship.moving_right = True
            # elif event.key == pygame.K_LEFT:
            #     # 向左移动飞船
            #     ship.moving_left = True
            check_keydown_events(event, game_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            # if event.key == pygame.K_RIGHT:
            #     ship.moving_right = False
            # elif event.key == pygame.K_LEFT:
            #     ship.moving_left = False
            check_keyup_events(event, ship)


def update_screen(game_settings, screen, ship, bullets):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(game_settings.bg_color)

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def fire_bullet(game_settings, screen, ship, bullets):
    """如果还没有达到限制，就发射一颗子弹"""
    # 创建新子弹，并将其加入到编组bullets中
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)