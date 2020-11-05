# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 19:04:50 2020

@author: ASUS
主游戏逻辑
"""

import os,sys,pygame
from pygame import locals
import config,objects

class State:
    def handle(self,event):
        #只处理退出时间的默认事件处理
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type== pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
            sys.exit(0)
            
    def first_display(self,screen):
        screen.fill(config.background_color)
        pygame.display.flip()
        
    def display(self,screen):
    #在后续显示状态时使用
        pass

class Level(State):
    def __init__(self,number=1):
        self.number=number
        #还需躲开多少个
        self.remaining=config.weights_per_level
        
        speed=config.drop_speed
        
        speed+=(self.number-1)*config.speed_increase
        self.weight=objects.Weight(speed)
        self.banana=objects.Banana()
        both=self.weight,self.banana#可包含更多精灵
        self.sprites=pygame.sprite.RenderUpdates(both)
        
    def update(self,game):
        #更新游戏状态
        self.sprites.update()
        if self.banana.touches(self.weight):
            game.next_state=GameOver()
        elif self.weight.landed:
            self.weight.reset()
            self.remaining-=1
            if self.remaining==0:
                game.next_state=LevelCleared(self.number)
                
    def display(self,screen):
        #在第一次清屏后显示状态
        screen.fill(config.background_color)
        updates=self.sprites.draw(screen)
        pygame.display.update(updates)
        
class Paused(State):
    #游戏暂停状态
    finished=0#end?
    image=None#如果要显示文件，将其显示为一个文件名
    text=''#说明性文本
    def handle(self,event):
        State.handle(self,event)
        if event.type in [pygame.MOUSEBUTTONDOWN,pygame.KEYDOWN]:
            self.finished=1
    
    def update(self,game):
        if self.finished:
            game.next_state=self.next_state()
            
    def first_display(self,screen):
        screen.fill(config.background_color)
        #创建一个使用指定外观和字号的Font对象
        font=pygame.font.Font(None,config.font_size)
        #获取文本行
        lines=self.text.strip().splitlines()
        height = len(lines)*font.get_linesize()
        center,top=screen.get_rect().center
        top-=height//2
        
        #如果有图像要显示
        if self.image:
            image=pygame.image.load(self.image).convert()
            r=image.get_rect()
            top+=r.height//2
            r.midbottom=center,top-20
            screen.blit(image,r)
        antialias=1
        black=0,0,0
        
        for line in lines:
            text=font.render(line.strip(),antialias,black)
            r=text.get_rect()
            r.midtop=center,top
            screen.blit(text,r)
            top+=font.get_linesize()
        
        #显示所作的更改
        pygame.display.flip()
        
class Info(Paused):
    next_state=Level
    text='''
    In this game, fuck you'''
    
class Startup(Paused):
    #显示启动图像和欢迎消息的暂停状态
    next_state=Info
    image=config.splash_image
    text='''welcome'''
    
class LevelCleared(Paused):
    #过关
    def __init__(self,number):
        self.number=number
        self.text=''' Level {} cleared
        Click to start next level'''.format(self.number)
    
    def next_state(self):
        return Level(self.number+1)
    
class GameOver(Paused):
        next_state=Level
        text=''' Game Over
        Click to Restart,Esc to Quit'''
        
class Game:
    #主事件循环
    def __init__(self,*args):
        #获取游戏和图像所在的目录
        path = os.path.abspath(args[0])
        dir=os.path.split(path)[0]
        #切换到这个目录，以便后续打开图像文件
        os.chdir(dir)
        #最初不处于任何状态
        self.state=None
        #在第一次事件的循环迭代中切换到Startup
        self.next_state =Startup()
        
    def run(self):
        pygame.init()
        flag=0#默认在窗口中显示游戏
        if config.full_screen:
            flag=pygame.FULLSCREEN
        screen_size=config.screen_size
        screen =pygame.display.set_mode(screen_size,flag)
        
        pygame.display.set_caption('Fruit Self Defense')
        pygame.mouse.set_visible(False)
        
        while True:
            #如果nextState被修改，切换状态并显示
            if self.state!=self.next_state:
                self.state=self.next_state
                self.state.first_display(screen)
            
            #将事件处理并委托给当前状态
            for event in pygame.event.get():
                self.state.handle(event)
            
            #更新当前状态
            self.state.update(self)
            
            #显示
            self.state.display(screen)
            
if __name__=='__main__':
    game=Game(*sys.argv)
    game.run()
                

