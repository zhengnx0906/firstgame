# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 15:23:05 2020

@author: ZNX
the first time I try to create the game
"""

import sys,pygame
from pygame import locals
from random import randrange

class Weight(pygame.sprite.Sprite):
    def __init__(self,speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed=speed
        #绘制sprite对象时要用到的图像和矩阵
        self.image=weight_image
        self.rect=self.image.get_rect()
        self.reset()
        
    def reset(self):
        #"将锤子移到屏幕顶端的一个随机位置"
        self.rect.top=-self.rect.height
        self.rect.centerx=randrange(screen_size[0])
        
    def update(self):
        #更新下一帧中的铅锤
        self.rect.top+=self.speed
        if self.rect.top>screen_size[1]:
            self.reset()
            
#初始化
pygame.init()
screen_size=800,600
pygame.display.set_mode(screen_size,pygame.FULLSCREEN)
pygame.mouse.set_visible(0)

#加载铅锤图像
weight_image=pygame.image.load('1.gif')
weight_image=weight_image.convert()#匹配显示

#设置不同速度
speed=5

#创建一个sprite对象数组，并在其中添加一个weight实例
sprites=pygame.sprite.RenderUpdates()
sprites.add(Weight(speed))

#获取并填充表面
screen =pygame.display.get_surface()
bg=(255,255,255)#white
screen.fill(bg)
pygame.display.flip()

#用于清除sprite对象
def clear_callback(surf,rect):
    surf.fill(bg,rect)

while True:
    #检查退出事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type== pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
            sys.exit()
    #清除以前的位置
    sprites.clear(screen,clear_callback)
    #更新所有的sprite对象
    sprites.update()
    updates=sprites.draw(screen)
    pygame.display.update(updates)