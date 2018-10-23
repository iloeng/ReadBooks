# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     RandomWalkVisual
   Description :
   Author :        Liangz
   Date：          2018/10/23
-------------------------------------------------
   Change Activity:
                   2018/10/23:
-------------------------------------------------
"""
__author__ = 'Liangz'


import matplotlib.pyplot as plt
from RandomWalk import RandomWalk


# 只要程序处于活动状态，就不断地模拟随机漫步
while True:
    # 创建一个RandomWalk实例，并将其包含的点都绘制出来
    random_walk = RandomWalk()
    random_walk.fill_walk()
    plt.scatter(random_walk.x_values, random_walk.y_values, s=15)
    plt.show()

    keep_running = input("Make another walk?(y/n)")
    if keep_running == 'n':
        break
