import sys
import pygame
import json
import random
import copy

with open('map.json') as f:
    map = json.load(f)


# 遊戲速度
speed = 10

# 原始數量
slime = 4

# 食物生成間隔
random_reward = (20, 40)

# 視野距離
sight = 10

# 場上食物數量
apple_max = 5

# 每次吃食物增加生命
apple_lifeadd = 100

# 生出後代所需食物量
need_eat = 2

# 成年預設生命
normal_life = 300

# 新生預設生命
new_life = 200

# 飢餓狀態生命
less_life = 100


pygame.init()

background_img = pygame.image.load('images/map.png')
slime_img = pygame.image.load('images/SlimeBlue.png')
apple_img = pygame.image.load('images/apple.png')


size = [60, 40]
apple_place = [(i, j) for j in range(16, 19) for i in range(26, 29)]+[(i, j) for j in range(21, 24) for i in range(26, 29)] + \
    [(i, j) for j in range(16, 19) for i in range(31, 34)]+[(i, j)
                                                            for j in range(21, 24) for i in range(31, 34)]
apple_pos = []
reward_time = random_reward[1]
apple_home = []
slime_num = slime
death = 0
hungry_num = 0

direct = [(0, -1), (-1, 0), (0, 1), (1, 0)]


class Slime:
    def __init__(self):
        self.x = 30
        self.y = 20
        self.get = False
        self.rotate = 0
        self.move_path = []
        self.back_path = []
        self.get_path = []
        self.must_path = []
        self.life = 250
        self.eat = 0

    def move(self):
        global slime_num
        global hungry_num
        if self.must_path:
            self.x, self.y = self.must_path.pop()
            if self.eat >= need_eat:
                i = 1
                while (i in slime_list):
                    i += 1
                slime_list.append(i)
                globals()['slime'+str(i)] = Slime()
                globals()['slime'+str(i)].rotate = i % 4
                globals()['slime'+str(i)].life = new_life
                slime_num += 1
                self.eat = 0
            return()

        if self.get:
            self.move_path = []
            if self.x not in range(26, 34) or self.y not in range(16, 24):
                pos = (28, 18)
                if self.back_path:
                    self.x, self.y = self.back_path.pop()
                    return()
                else:
                    arr = [[0 for j in range(60)] for i in range(40)]
                    self.back_path = copy.deepcopy(
                        find([self.x, self.y], pos, arr, self.back_path))
                    self.x, self.y = self.back_path.pop()
                    return()
            else:
                for pos in apple_place:
                    if pos not in apple_home:
                        if (self.x, self.y) == pos:
                            self.get = False
                            apple_home.append(pos)
                            arr = [[0 for j in range(60)] for i in range(40)]
                            self.must_path = copy.deepcopy(
                                find([self.x, self.y], [30, 20], arr, self.must_path))
                            return()
                        else:
                            arr = [[0 for j in range(60)] for i in range(40)]
                            self.get_path = copy.deepcopy(
                                find([self.x, self.y], pos, arr, self.get_path))
                            self.x, self.y = self.get_path.pop()
                            return()

        for i in apple_pos:
            if (i[0]-self.x) in range(-sight, sight+1) and (i[1]-self.y) in range(-sight, sight+1):
                self.go(i)
                self.back_path = []
                return()
        self.move_path = []

        if self.life < less_life:
            hungry_num += 1
            if self.x not in range(26, 34) or self.y not in range(16, 24):
                pos = (32, 22)
                if self.back_path:
                    self.x, self.y = self.back_path.pop()
                    return()
                else:
                    arr = [[0 for j in range(60)] for i in range(40)]
                    self.back_path = copy.deepcopy(
                        find([self.x, self.y], pos, arr, self.back_path))
                    self.x, self.y = self.back_path.pop()
                    self.rotate = (self.rotate+1) % 4
                    return()
            elif apple_home:
                for pos in apple_home:
                    if (self.x, self.y) == pos:
                        apple_home.remove(pos)
                        self.life += apple_lifeadd
                        self.eat += 1
                        arr = [[0 for j in range(60)] for i in range(40)]
                        self.must_path = copy.deepcopy(
                            find([self.x, self.y], [30, 20], arr, self.must_path))
                        return()

                    else:
                        arr = [[0 for j in range(60)] for i in range(40)]
                        self.back_path = copy.deepcopy(
                            find([self.x, self.y], pos, arr, self.back_path))
                        self.x, self.y = self.back_path.pop()
                        return()

        self.back_path = []
        direction = direct[self.rotate]
        new_x = self.x + direction[0]
        new_y = self.y + direction[1]
        while map[new_y % 40][new_x % 60] or (new_y not in range(40)) or (new_x not in range(60)):
            self.rotate = random.randint(0, 3)
            direction = direct[self.rotate]
            new_x = self.x + direction[0]
            new_y = self.y + direction[1]
        self.x = new_x
        self.y = new_y

    def go(self, pos):
        if self.move_path:
            self.x, self.y = self.move_path.pop()
        else:
            arr = [[0 for j in range(60)] for i in range(40)]
            self.move_path = copy.deepcopy(
                find([self.x, self.y], pos, arr, self.move_path))
            self.x, self.y = self.move_path.pop()


def find(start, end, arr, path):
    arr[start[1]][start[0]] = -1
    now_pos = [start]
    found = False
    d = 0
    while (not found):
        d += 1
        new_pos = []
        for pos in now_pos:
            for dir in direct:
                if pos[0]+dir[0] in range(60) and pos[1]+dir[1] in range(40):

                    if (pos[0]+dir[0] == end[0] and pos[1]+dir[1] == end[1]):
                        found = True
                    elif (not arr[pos[1]+dir[1]][pos[0]+dir[0]]) and not map[pos[1]+dir[1]][pos[0]+dir[0]]:
                        new_pos.append([pos[0]+dir[0], pos[1]+dir[1]])
                        arr[pos[1]+dir[1]][pos[0]+dir[0]] = d

        now_pos = copy.deepcopy(new_pos)

    pos = copy.deepcopy(end)
    path.append(pos)
    while(d != 1):
        for dir in direct:
            if pos[0]+dir[0] in range(60) and pos[1]+dir[1] in range(40):
                if arr[pos[1]+dir[1]][pos[0]+dir[0]] == d:
                    path.append([pos[0]+dir[0], pos[1]+dir[1]])
                    pos = ([pos[0]+dir[0], pos[1]+dir[1]])
        d -= 1
    return(path)


def paint(slime):
    screen_image.blit(slime_img, (slime.x*16, slime.y*16))


def reward():
    x = random.randint(0, 59)
    y = random.randint(0, 39)
    while(map[y][x] or (x in range(25, 35) and y in range(15, 25)) or [x, y] in apple_pos):
        x = random.randint(0, 59)
        y = random.randint(0, 39)
    apple_pos.append([x, y])
    return(random.randint(random_reward[0], random_reward[1]))


def life_pass():
    global death
    for i in slime_list:
        if globals()['slime'+str(i)].x in range(25, 35) and globals()['slime'+str(i)].y in range(15, 25):
            globals()['slime'+str(i)].life -= 0.5
        else:
            globals()['slime'+str(i)].life -= 1

        if globals()['slime'+str(i)].life <= 0:
            del globals()['slime'+str(i)]
            slime_list.remove(i)
            death += 1


pygame.display.set_caption('窩也不知道這是甚麼')
screen_image = pygame.display.set_mode((1120, 640))
screen_image.blit(background_img, (0, 0))

slime_list = [i+1 for i in range(slime)]
for i in slime_list:
    globals()['slime'+str(i)] = Slime()
    globals()['slime'+str(i)].life = normal_life
    globals()['slime'+str(i)].rotate = i % 4


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen_image.blit(background_img, (0, 0))

    if reward_time <= 0 and len(apple_pos) < apple_max and len(apple_home)+len(apple_pos) < 30:
        reward_time = reward()

    for i in apple_pos:
        screen_image.blit(apple_img, (i[0]*16, i[1]*16))
        for j in slime_list:
            if globals()['slime'+str(j)].x == i[0] and globals()['slime'+str(j)].y == i[1]:
                if i in apple_pos:
                    apple_pos.remove(i)
                    globals()['slime'+str(j)].life += apple_lifeadd
                    globals()['slime'+str(j)].eat += 1
                    globals()['slime'+str(j)].get = True

    for i in apple_home:
        screen_image.blit(apple_img, (i[0]*16, i[1]*16))

    for i in slime_list:
        globals()['slime'+str(i)].move()
        paint(globals()['slime'+str(i)])

    reward_time -= 1

    life_pass()

    alive_image = pygame.font.Font(
        "font/msjh.ttc", 24).render(f'目前數量:{len(slime_list)}', True, (173, 111, 80))
    screen_image.blit(alive_image, (975, 50))
    alive_image = pygame.font.Font(
        "font/msjh.ttc", 24).render(f'飢餓數量:{hungry_num}', True, (173, 111, 80))
    screen_image.blit(alive_image, (975, 150))
    alive_image = pygame.font.Font(
        "font/msjh.ttc", 24).render(f'累計總數:{slime_num}', True, (173, 111, 80))
    screen_image.blit(alive_image, (975, 350))
    alive_image = pygame.font.Font(
        "font/msjh.ttc", 24).render(f'死亡累積:{death}', True, (173, 111, 80))
    screen_image.blit(alive_image, (975, 450))

    hungry_num = 0

    pygame.time.wait(1000//speed)
    pygame.display.flip()
