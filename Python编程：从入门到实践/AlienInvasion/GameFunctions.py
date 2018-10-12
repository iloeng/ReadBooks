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
from Alien import Alien
from time import sleep


def check_keydown_events(event, game_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    # 空格键发射子弹
    elif event.key == pygame.K_SPACE:
        # # 创建一颗子弹，并将其加入到编组bullets中
        # if len(bullets) < game_settings.bullets_allowed:
        #     new_bullet = Bullet(game_settings, screen, ship)
        #     bullets.add(new_bullet)
        fire_bullet(game_settings, screen, ship, bullets)

    #
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def chech_events(game_settings, screen, status, play_button, ship, bullets):
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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(status, play_button, mouse_x, mouse_y)


def check_play_button(status, play_button, mouse_x, mouse_y):
    """在玩家单击Play按钮是开始新游戏"""
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        status.game_active = True


def update_screen(game_settings, screen, status, ship, aliens, bullets, play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(game_settings.bg_color)

    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not status.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(game_settings, screen, ship, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(game_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(game_settings, screen, ship, aliens, bullets):
    """相应子弹和外星人的碰撞"""
    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        create_fleet(game_settings, screen, ship, aliens)


def fire_bullet(game_settings, screen, ship, bullets):
    """如果还没有达到限制，就发射一颗子弹"""
    # 创建新子弹，并将其加入到编组bullets中
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(game_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可容纳多少个外星人

    alien = Alien(game_settings, screen)
    number_aliens_x = get_number_aliens_x(game_settings, alien.rect.width)
    number_rows = get_number_rows(game_settings, ship.rect.height, alien.rect.height)

    # 创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 创建一个外星人并将其加入当期行
            create_alien(game_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(game_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = game_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(game_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)


def get_number_rows(game_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = game_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(game_settings, status, screen, ship, aliens, bullets):
    """更新外星人群中所有外星人的位置"""
    check_fleet_edges(game_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        # print("Ship Hit !!!")
        ship_hit(game_settings, status, screen, ship, aliens, bullets)


def check_aliens_bottom(game_settings, status, screen, ship, aliens, bullets):
    """检查是否有外形人到达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(game_settings, status, screen, ship, aliens, bullets)
            break

    check_aliens_bottom(game_settings, status, screen, ship, aliens, bullets)

def check_fleet_edges(game_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break


def change_fleet_direction(game_settings, aliens):
    """将整体外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


def ship_hit(game_settings, status, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    # 将ships_left减1
    if status.ships_left > 0:
        status.ships_left -= 1

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕的低端中央
        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:
        status.game_active = False

