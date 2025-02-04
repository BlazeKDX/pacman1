#importing the correct modules and externaal files from the project to program the game
import pygame
import math
from maze import mazes

pygame.init()

#setting up the window dimensions
window = pygame.display.set_mode((900, 950))
#setting up the title
title = pygame.display.set_caption("Pacman")
#setting up the game speed and fps limit
clock = pygame.time.Clock()
fps = 60
#setting up the maze variables
score = 0
level = mazes
maze = mazes
colour_b = 'blue'
colour_w = 'white'
pellet_effect=False
can_face = [False,False,False,False]
ghost_dead=[False,False,False,False]
initial_timer = 0
#retrieving ghost images from external folder
redpng = pygame.transform.scale(pygame.image.load(f'ghosts/red.png'),(45,45))
pinkpng = pygame.transform.scale(pygame.image.load(f'ghosts/pink.png'),(45,45))
cyanpng = pygame.transform.scale(pygame.image.load(f'ghosts/blue.png'),(45,45))
orangepng = pygame.transform.scale(pygame.image.load(f'ghosts/orange.png'),(45,45))
scaredpng = pygame.transform.scale(pygame.image.load(f'ghosts/powerup.png'),(45,45))
deathpng = pygame.transform.scale(pygame.image.load(f'ghosts/dead.png'),(45,45))
#setting up ghost variables 
position_x=450
position_y=663
red_x = 56
red_y = 58
red_y = 58
xred= 56
yred = 58
redfacing = 0
xcyan = 440
ycyan = 388
cyanfacing = 2
xpink = 440
ypink = 438
pinkfacing = 2
xorange = 440
yorange = 438
orangefacing = 2
deadred = False
deadcyan = False
deadpink = False
deadorange = False
redhome = False
cyanhome = False
pinkhome = False
orangehome = False
active = False
ghost_speed = [2, 2, 2, 2]
begin_count = 0
moves = False
#pacman variables 
facing_change = 0
facing=0
rate=0
pacman_speed = 2
pwerup=False
pwer_timer=0
life=3
target = [(position_x, position_y), (position_x, position_y), (position_x, position_y), (position_x, position_y)]
pacman_png=[]
for x in range(0,2):
#appending the images to the list rescaling the image 
    pacman_png.append(pygame.transform.scale(pygame.image.load(f'pngs/{x}.png'),(45,45)))

#defining the display maze function
def display_maze(maze):
    row1 = ((950-50)//32)
    row2 = (900//30)
#defining the maze values by assigning each value a shape 
    for x in range(len(maze)):
        for y in range(len(maze[x])):
            if maze[x][y]==1:
                pygame.draw.circle(window,colour_w,(y*row2+(row2*0.5),x*row1+(row1*0.5)),4)
            if maze[x][y]==2 and not pellet_effect:
                 pygame.draw.circle(window,colour_w,(y*row2+(row2*0.5),x*row1+(row1*0.5)),10)
            if maze[x][y]==3:
                 pygame.draw.line(window,colour_b,(y*row2+(row2*0.5),row1*x),(row2*y+(row2*0.5),row1*x+row1),3)
            if maze[x][y]==4:
                 pygame.draw.line(window,colour_b,(y*row2,row1*x+(row1*0.5)),(y*row2+row2,row1*x+(row1*0.5)),3)
            if maze[x][y]==5:
                pygame.draw.arc(window,colour_b,[(row2*y-(row2*0.4))-2,(row1*x+(row1*0.5)),row2,row1],0,math.pi/2,3)
            if maze[x][y]==6:
                pygame.draw.arc(window,colour_b,[(row2*y+(row2*0.5)),(row1*x+(row1*0.5)),row2,row1],math.pi/2,math.pi,3)
            if maze[x][y]==7:
                pygame.draw.arc(window,colour_b,[(row2*y+(row2*0.5)),(row1*x-(row1*0.4)),row2,row1],math.pi,3*math.pi/2,3)
            if maze[x][y]==8:
                pygame.draw.arc(window,colour_b,[(row2*y-(row2*0.4))-2,(row1*x-(row1*0.44)),row2,row1],3*math.pi/2,math.pi*2,3)
            if maze[x][y]==9:
                 pygame.draw.line(window,colour_w,(y*row2,row1*x+(row1*0.5)),(y*row2+row2,row1*x+(row1*0.5)),3)

#creating the ghosts class
class ghost:
    def __init__(self, coord_x, coord_y, targets, speed, png, face, dead, home, type):
        self.x_pos = coord_x
        self.y_pos = coord_y
        self.x_middle = self.x_pos + 22
        self.y_middle = self.y_pos + 22
        self.targets = targets
        self.speed = speed
        self.png = png
        self.facing = face
        self.dead = dead
        self.home = home
        self.type = type
        self.faces, self.home = self.collisions()
        self.rect = self.draw()

    def draw(self):
        if (not pwerup and not self.dead) or (ghost_dead[self.type] and pwerup and not self.dead):
            window.blit(self.png, (self.x_pos, self.y_pos))
        elif pwerup and not self.dead and not ghost_dead[self.type]:
            window.blit(scaredpng, (self.x_pos, self.y_pos))
        else:
            window.blit(deathpng, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.x_middle - 18, self.y_middle - 18), (36, 36))
        return ghost_rect

    def collisions(self):
        height = 900//32
        width = 900//30
        constant = 15
        self.faces = [False, False, False, False]
        if 0 < self.x_middle // 30 < 29:
            if level[(self.y_middle - constant) // height][self.x_middle // width] == 9:
                self.faces[2] = True
            if level[self.y_middle // height][(self.x_middle - constant) // width] < 3 \
                    or (level[self.y_middle // height][(self.x_middle - constant) // width] == 9 and (
                    self.home or self.dead)):
                self.faces[1] = True
            if level[self.y_middle // height][(self.x_middle + constant) // width] < 3 \
                    or (level[self.y_middle // height][(self.x_middle + constant) // width] == 9 and (
                    self.home or self.dead)):
                self.faces[0] = True
            if level[(self.y_middle + constant) // height][self.x_middle // width] < 3 \
                    or (level[(self.y_middle + constant) // height][self.x_middle // width] == 9 and (
                    self.home or self.dead)):
                self.faces[3] = True
            if level[(self.y_middle - constant) // height][self.x_middle // width] < 3 \
                    or (level[(self.y_middle - constant) // height][self.x_middle // width] == 9 and (
                    self.home or self.dead)):
                self.faces[2] = True

            if self.facing == 2 or self.facing == 3:
                if 12 <= self.x_middle % width <= 18:
                    if level[(self.y_middle + constant) // height][self.x_middle // width] < 3 \
                            or (level[(self.y_middle + constant) // height][self.x_middle // width] == 9 and (
                            self.home or self.dead)):
                        self.faces[3] = True
                    if level[(self.y_middle - constant) // height][self.x_middle // width] < 3 \
                            or (level[(self.y_middle - constant) // height][self.x_middle // width] == 9 and (
                            self.home or self.dead)):
                        self.faces[2] = True
                if 12 <= self.y_middle % height <= 18:
                    if level[self.y_middle // height][(self.x_middle - width) // width] < 3 \
                            or (level[self.y_middle // height][(self.x_middle - width) // width] == 9 and (
                            self.home or self.dead)):
                        self.faces[1] = True
                    if level[self.y_middle // height][(self.x_middle + width) // width] < 3 \
                            or (level[self.y_middle // height][(self.x_middle + width) // width] == 9 and (
                            self.home or self.dead)):
                        self.faces[0] = True

            if self.facing == 0 or self.facing == 1:
                if 12 <= self.x_middle % width <= 18:
                    if level[(self.y_middle + constant) // height][self.x_middle // width] < 3 \
                            or (level[(self.y_middle + constant) // height][self.x_middle // width] == 9 and (
                            self.home or self.dead)):
                        self.faces[3] = True
                    if level[(self.y_middle - constant) // height][self.x_middle // width] < 3 \
                            or (level[(self.y_middle - constant) // height][self.x_middle // width] == 9 and (
                            self.home or self.dead)):
                        self.faces[2] = True
                if 12 <= self.y_middle % height <= 18:
                    if level[self.y_middle // height][(self.x_middle - constant) // width] < 3 \
                            or (level[self.y_middle // height][(self.x_middle - constant) // width] == 9 and (
                            self.home or self.dead)):
                        self.faces[1] = True
                    if level[self.y_middle // height][(self.x_middle + constant) // width] < 3 \
                            or (level[self.y_middle // height][(self.x_middle + constant) // width] == 9 and (
                            self.home or self.dead)):
                        self.faces[0] = True
        else:
            self.faces[0] = True
            self.faces[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.home = True
        else:
            self.home = False
        return self.faces, self.home

    def orange_movement(self):
        if self.facing == 0:
            if self.targets[0] > self.x_pos and self.faces[0]:
                self.x_pos += self.speed
            elif not self.faces[0]:
                if self.targets[1] > self.y_pos and self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.targets[1] < self.y_pos and self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.targets[0] < self.x_pos and self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
            elif self.faces[0]:
                if self.targets[1] > self.y_pos and self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                if self.targets[1] < self.y_pos and self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.facing == 1:
            if self.targets[1] > self.y_pos and self.faces[3]:
                self.facing = 3
            elif self.targets[0] < self.x_pos and self.faces[1]:
                self.x_pos -= self.speed
            elif not self.faces[1]:
                if self.targets[1] > self.y_pos and self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.targets[1] < self.y_pos and self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.targets[0] > self.x_pos and self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
            elif self.faces[1]:
                if self.targets[1] > self.y_pos and self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                if self.targets[1] < self.y_pos and self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.facing == 2:
            if self.targets[0] < self.x_pos and self.faces[1]:
                self.facing = 1
                self.x_pos -= self.speed
            elif self.targets[1] < self.y_pos and self.faces[2]:
                self.facing = 2
                self.y_pos -= self.speed
            elif not self.faces[2]:
                if self.targets[0] > self.x_pos and self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.targets[0] < self.x_pos and self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.targets[1] > self.y_pos and self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
            elif self.faces[2]:
                if self.targets[0] > self.x_pos and self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.targets[0] < self.x_pos and self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.facing == 3:
            if self.targets[1] > self.y_pos and self.faces[3]:
                self.y_pos += self.speed
            elif not self.faces[3]:
                if self.targets[0] > self.x_pos and self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.targets[0] < self.x_pos and self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.targets[1] < self.y_pos and self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
            elif self.faces[3]:
                if self.targets[0] > self.x_pos and self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.targets[0] < self.x_pos and self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.facing

    def red_movement(self):
        if self.facing == 0:
            if self.targets[0] > self.x_pos and self.faces[0]:
                self.x_pos += self.speed
            elif not self.faces[0]:
                if self.targets[1] > self.y_pos and self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.targets[1] < self.y_pos and self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.targets[0] < self.x_pos and self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
            elif self.faces[0]:
                self.x_pos += self.speed
        elif self.facing == 1:
            if self.targets[0] < self.x_pos and self.faces[1]:
                self.x_pos -= self.speed
            elif not self.faces[1]:
                if self.targets[1] > self.y_pos and self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.targets[1] < self.y_pos and self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.targets[0] > self.x_pos and self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
            elif self.faces[1]:
                self.x_pos -= self.speed
        elif self.facing == 2:
            if self.targets[1] < self.y_pos and self.faces[2]:
                self.facing = 2
                self.y_pos -= self.speed
            elif not self.faces[2]:
                if self.targets[0] > self.x_pos and self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.targets[0] < self.x_pos and self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.targets[1] > self.y_pos and self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
            elif self.faces[2]:
                self.y_pos -= self.speed
        elif self.facing == 3:
            if self.targets[1] > self.y_pos and self.faces[3]:
                self.y_pos += self.speed
            elif not self.faces[3]:
                if self.targets[0] > self.x_pos and self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.targets[0] < self.x_pos and self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.targets[1] < self.y_pos and self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
            elif self.faces[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.facing

    def cyan_movement(self):
        if self.facing == 0:
            if self.targets[0] > self.x_pos and self.faces[0]:
                self.x_pos += self.speed
            elif not self.faces[0]:
                if self.targets[1] > self.y_pos and self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.targets[1] < self.y_pos and self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.targets[0] < self.x_pos and self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
            elif self.faces[0]:
                if self.targets[1] > self.y_pos and self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                if self.targets[1] < self.y_pos and self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.facing == 1:
            if self.targets[1] > self.y_pos and self.faces[3]:
                self.facing = 3
            elif self.targets[0] < self.x_pos and self.faces[1]:
                self.x_pos -= self.speed
            elif not self.faces[1]:
                if self.targets[1] > self.y_pos and self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.targets[1] < self.y_pos and self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.targets[0] > self.x_pos and self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
            elif self.faces[1]:
                if self.targets[1] > self.y_pos and self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                if self.targets[1] < self.y_pos and self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.facing == 2:
            if self.targets[1] < self.y_pos and self.faces[2]:
                self.facing = 2
                self.y_pos -= self.speed
            elif not self.faces[2]:
                if self.targets[0] > self.x_pos and self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.targets[0] < self.x_pos and self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.targets[1] > self.y_pos and self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
            elif self.faces[2]:
                self.y_pos -= self.speed
        elif self.facing == 3:
            if self.targets[1] > self.y_pos and self.faces[3]:
                self.y_pos += self.speed
            elif not self.faces[3]:
                if self.targets[0] > self.x_pos and self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.targets[0] < self.x_pos and self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.targets[1] < self.y_pos and self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
            elif self.faces[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.facing

    def pink_movement(self):
        if self.facing == 0:
            if self.targets[0] > self.x_pos and self.faces[0]:
                self.x_pos += self.speed
            elif not self.faces[0]:
                if self.targets[1] > self.y_pos and self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.targets[1] < self.y_pos and self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.targets[0] < self.x_pos and self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
            elif self.faces[0]:
                self.x_pos += self.speed
        elif self.facing == 1:
            if self.targets[1] > self.y_pos and self.faces[3]:
                self.facing = 3
            elif self.targets[0] < self.x_pos and self.faces[1]:
                self.x_pos -= self.speed
            elif not self.faces[1]:
                if self.targets[1] > self.y_pos and self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.targets[1] < self.y_pos and self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.targets[0] > self.x_pos and self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
            elif self.faces[1]:
                self.x_pos -= self.speed
        elif self.facing == 2:
            if self.targets[0] < self.x_pos and self.faces[1]:
                self.facing = 1
                self.x_pos -= self.speed
            elif self.targets[1] < self.y_pos and self.faces[2]:
                self.facing = 2
                self.y_pos -= self.speed
            elif not self.faces[2]:
                if self.targets[0] > self.x_pos and self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.targets[0] < self.x_pos and self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.targets[1] > self.y_pos and self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.faces[3]:
                    self.facing = 3
                    self.y_pos += self.speed
                elif self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
            elif self.faces[2]:
                if self.targets[0] > self.x_pos and self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.targets[0] < self.x_pos and self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.facing == 3:
            if self.targets[1] > self.y_pos and self.faces[3]:
                self.y_pos += self.speed
            elif not self.faces[3]:
                if self.targets[0] > self.x_pos and self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.targets[0] < self.x_pos and self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.targets[1] < self.y_pos and self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.faces[2]:
                    self.facing = 2
                    self.y_pos -= self.speed
                elif self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                elif self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
            elif self.faces[3]:
                if self.targets[0] > self.x_pos and self.faces[0]:
                    self.facing = 0
                    self.x_pos += self.speed
                elif self.targets[0] < self.x_pos and self.faces[1]:
                    self.facing = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.facing


target = [(position_x,position_y),(position_x,position_y),(position_x,position_y),(position_x, position_y)]

#defining the display pacman function
def display_pacman():
    #depending on the facing pacman is facing this will display pacman in that facing
    if facing == 0:
        window.blit(pacman_png[(rate//10)],(position_x,position_y))
    elif facing == 1:
        window.blit(pygame.transform.flip(pacman_png[rate//10],True,False),(position_x,position_y))
    elif facing == 2:
        window.blit(pygame.transform.rotate(pacman_png[rate//10],90),(position_x,position_y))
    elif facing == 3:
        window.blit(pygame.transform.rotate(pacman_png[rate//10],270),(position_x,position_y))

def collision(points,pwerup,pwer_timer,ghost_dead):
    height = 900 // 32
    width = 900 // 30
    if 0 < position_x < 870:
        if level[y_middle//height][x_middle//width] == 1:
            level[y_middle//height][x_middle//width] = 0
            points = points+10
        if level[y_middle//height][x_middle//width] == 2:
            level[y_middle//height][x_middle//width]=0
            points = 50 +points
            pwerup = True
            pwer_timer = 0
            ghost_dead = [False, False, False, False]
    return points,pwerup,pwer_timer,ghost_dead

def display_external():
        score_txt = pygame.font.SysFont(None,20,True).render(f'Score:{score}',True,'white')
        if pwerup:
            pygame.draw.circle(window,'blue',(600   ,930),15)
        window.blit(score_txt, (800,920))
        for i in range(life):
            window.blit(pygame.transform.scale(pacman_png[0],(30,30)),(650+i*40,915))

def border_control(c_x,c_y):
    face = [False,False,False,False]
    height = 900//32
    width = 900// 30
    checking_condition = 15
    if c_x//30 < 29:
        if facing == 2:
            if level[c_y // height][(c_x-checking_condition)//width]<3:
                face[1] = True
        if facing == 3:
            if level[c_y//height][(c_x+checking_condition)//width]<3:
                face[0] = True
        if facing == 0:
            if level[(c_y+checking_condition)//height][c_x//width]<3:
                face[3] = True
        if facing == 1:
            if level[(c_y-checking_condition)//height][c_x//width]<3:
                face[2] = True

        if facing==2 or facing == 3:
            if 12 <= c_x % width<= 18:
                if level[(c_y+checking_condition)//height][c_x//width]< 3:
                    face[3] = True
                if level[(c_y-checking_condition)//height][c_x//width]< 3:
                    face[2] = True
            if 12 <= c_y % height <=18:
                if level[c_y//height][(c_x-width)//width]<3:
                    face[1] = True
                if level[c_y//height][(c_x+width)//width]<3:
                    face[0] = True
        if facing == 0 or facing == 1:
            if 12 <= c_x%width<=18:
                if level[(c_y+height)//height][c_x//width]<3:
                    face[3] = True
                if level[(c_y-height) // height][c_x//width]<3:
                    face[2] = True
            if 12 <= c_y % height <= 18:
                if level[c_y//height][(c_x-checking_condition)//width]<3:
                    face[1] = True
                if level[c_y//height][(c_x+checking_condition)//width]<3:
                    face[0] = True
    else:
        face[0] = True
        face[1] = True

    return face

#defining function pacman_controls to enable his movement based on condtions
def pacman_movement(pacman_horizontal, pacman_vertical):
    if facing == 0 and can_face[0]:
        pacman_horizontal = pacman_speed+pacman_horizontal
    elif facing == 1 and can_face[1]:
        pacman_horizontal = pacman_horizontal-pacman_speed
    if facing == 2 and can_face[2]:
        pacman_vertical = pacman_vertical-pacman_speed
    elif facing == 3 and can_face[3]:
        pacman_vertical = pacman_speed+pacman_vertical
    return pacman_horizontal,pacman_vertical

#game loop
play = True
while play:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    #setting the speed of the cycle of pacmans state 
    if rate<19:
        rate=rate+1
        if rate >10:
            pellet_effect=False
    else:
        rate=0
        pellet_effect=True
    if pwerup and pwer_timer<600:
        pwer_timer=pwer_timer+1
    elif pwerup and pwer_timer>=600:
        ghost_dead=[False,False,False,False]
        pwerup=False
        pwer_timer=0
    if initial_timer<180:
        moves = False
        initial_timer=initial_timer+1
    else:
        moves = True


    window.fill((0, 0, 0))
    display_external()
    display_maze(maze)
    display_pacman()
    red = ghost(xred, yred, target[0], ghost_speed[0], redpng, redfacing, deadred, redhome, 0)
    cyan = ghost(xcyan, ycyan, target[1], ghost_speed[1], cyanpng, cyanfacing, deadcyan, cyanhome, 1)
    pink = ghost(xpink, ypink, target[2], ghost_speed[2], pinkpng, pinkfacing, deadpink, pinkhome, 2)
    orange = ghost(xorange, yorange, target[3], ghost_speed[3], orangepng, orangefacing, deadorange, orangehome, 3)
    x_middle = position_x+23
    y_middle = position_y+24
    can_face = border_control(x_middle, y_middle)
    if moves:
        position_x,position_y=pacman_movement(position_x,position_y) 
        redx, redy, redfacing = red.red_movement()
        cyanx, cyany, cyanfacing = cyan.cyan_movement()
        pinkx, pinky, pinkfacing = pink.pink_movement()
        orangex, orangey, orangefacing = orange.orange_movement()
    score,pwerup,pwer_timer,ghost_dead = collision(score,pwerup,pwer_timer,ghost_dead)
    for x in range(4):
        if facing == x and can_face[x]:
            facing=x
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play=False
#up=2,down=3,right=0,left=1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                facing=2
            if event.key == pygame.K_DOWN:
                facing=3
            if event.key == pygame.K_RIGHT:
                facing=0
            if event.key == pygame.K_LEFT:
                facing=1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and facing_change == 0:
                facing_change = facing
            if event.key == pygame.K_LEFT and facing_change == 1:
                facing_change = facing
            if event.key == pygame.K_UP and facing_change == 2:
                facing_change = facing
            if event.key == pygame.K_DOWN and facing_change == 3:
                facing_change = facing
    if facing_change == 0 and can_face[0]:
        facing = 0
    if facing_change == 1 and can_face[1]:
        facing = 1
    if facing_change == 2 and can_face[2]:
        facing = 2
    if facing_change == 3 and can_face[3]:
        facing = 3

    pygame.display.update()
pygame.quit()