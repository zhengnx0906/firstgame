# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 18:32:32 2020

@author: ZNX
包含squish使用的游戏对象
"""
import pygame,config,os
from random import randrange

class SquishSprite(pygame.sprite.Sprite):
    """
    本游戏中所有精灵（sprite）的超类，构造函数加载一副图像,设置精灵的外接矩形
    和移动范围，移动范围取决于屏幕尺寸和边距
    """
    def __init__(self,image):
        super().__init__()
        self.image=pygame.image.load(image).convert()
        self.rect=self.image.get_rect()
        screen=pygame.display.get_surface()
        shrink=-config.margin*2
        self.area=screen.get_rect().inflate(shrink,shrink)
        
class Weight(SquishSprite):
    def __init__(self,speed):
        super().__init__(config.weight_image)
        self.speed=speed
        self.reset()
        
    def reset(self):
        #"将锤子移到屏幕顶端的一个随机位置"
        x=randrange(self.area.left,self.area.right)
        self.rect.midbottom=x,0
        
    def update(self):
        #更新下一帧中的铅锤
        self.rect.top+=self.speed
        self.landed=self.rect.top>=self.area.bottom
        
class Banana(SquishSprite):
    def __init__(self):
        super().__init__(config.banana_image)
        self.rect.bottom=self.area.bottom
        #这些内边距表示图像中不属于香蕉的部分
        #如果铅锤进入这些区域，并不认为它砸到了香蕉
        self.pad_top=config.banana_pad_top
        self.pad_size=config.banana_pad_size
        
    def update(self):
        #将香蕉的中心x设置为鼠标的当前的x，
        #再使用矩形的方法clamp确保香蕉位于允许范围
        self.rect.centerx=pygame.mouse.get_pos()[0]
        self.rect=self.rect.clamp(self.area)
        
    def touches(self,other):
        """
        判断香蕉是否与另一个精灵发生碰撞，这里没有直接使用矩形的方法colliderect
        而是先用inflat以及pad_side和pad_top计算出一个新的矩形，这个矩形步包含
        香蕉顶部和两边的空白区域
        """
        #通过剔除内边距来计算bounds
        bounds=self.rect.inflate(-self.pad_size,-self.pad_top)
        #底部对齐
        bounds.bottom=self.rect.bottom
        #检查是否与另一个对象的rect重叠
        return bounds.colliderect(other.rect)
    
