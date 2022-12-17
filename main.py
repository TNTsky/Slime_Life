import sys
import pygame
import numpy
import json
import random
from collections import deque




with open('map.json') as f:
    map = json.load(f)


pygame.init()

background_img = pygame.image.load('images/map.png')
slime_img = pygame.image.load('images/SlimeBlue.png')
apple_img = pygame.image.load('images/apple.png')


size=[60,40]
apple_pos=[]
reward_time = 50


direct = [(0,-1),(-1,0),(0,1),(1,0)]

class Slime:
    def __init__(self):
        self.x = 30
        self.y = 20
        self.eat = False
        self.rotate = 0
        self.movepath = []
        self.back = []
    
    def move(self):
        for i in apple_pos:
            if (i[0]-self.x)in range(-10,11) and (i[1]-self.y)in range(-10,11) :
                self.go(i)
                return
        direction = direct[self.rotate]
        new_x = self.x + direction[0]
        new_y = self.y + direction[1]
        while map[new_y%40][new_x%60] or (new_y not in range(40)) or (new_x not in range(60)):
            self.rotate = random.randint(0,3)
            direction = direct[self.rotate]
            new_x = self.x + direction[0]
            new_y = self.y + direction[1]
        self.x = new_x
        self.y = new_y

    def go(self,pos):
        if self.movepath :
            self.x,self.y = self.movepath[0]
        else:
            find([self.x,self.y],pos)


def find(start,end):
    arr=[[0 for j in range(60)] for i in range(30)]
        

def paint(slime):
    screen_image.blit(slime_img, (slime.x*16, slime.y*16))

def reward(time):
    x=random.randint(0,59)
    y=random.randint(0,39)
    while(map[y][x] or (x in range(25,35) and y in range(15,25)) or [x,y] in apple_pos):
        x=random.randint(0,59)
        y=random.randint(0,39)
    apple_pos.append([x,y])
    return(random.randint(30,50))










pygame.display.set_caption('窩也不知道是甚麼的遊戲')  # 遊戲標題
screen_image = pygame.display.set_mode((960, 640))  
screen_image.blit(background_img, (0, 0))
screen_image.blit(slime_img, (480, 320))
screen_image.blit(slime_img, (480, 320))

slime_list=[1,2,3,4]
for i in slime_list:
    globals()['slime'+str(i)] = Slime()
# slime1=Slime()
# slime2=Slime()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen_image.blit(background_img, (0, 0))

    for i in slime_list:
        globals()['slime'+str(i)].move()
        paint(globals()['slime'+str(i)])

    # slime1.move()
    # paint(slime1)
    # slime2.move()
    # paint(slime2)
    
    if reward_time==0:
        reward_time=reward(reward_time)
    
    for i in apple_pos:
        screen_image.blit(apple_img, (i[0]*16, i[1]*16))


    reward_time-=1


    pygame.time.wait(100)
    pygame.display.flip()