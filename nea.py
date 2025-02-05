import pygame
import math
import copy
from maze import mazes

pygame.init()

# Constants
WIDTH = 900
HEIGHT = 950
FPS = 60
PLAYER_SPEED = 2
GHOST_SPEEDS = [2, 2, 2, 2]
POWERUP_DURATION = 600

# Colors
COLOR_BLUE = 'blue'
COLOR_WHITE = 'white'

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 20)

# Load images
player_images = [pygame.transform.scale(pygame.image.load(f'pngs/{i}.png'), (45, 45)) for i in range(0, 2)]
blinky_img = pygame.transform.scale(pygame.image.load(f'ghosts/red.png'), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load(f'ghosts/pink.png'), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load(f'ghosts/blue.png'), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load(f'ghosts/orange.png'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(f'ghosts/powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'ghosts/dead.png'), (45, 45))

# Game variables
level = copy.deepcopy(mazes)
score = 0
lives = 2
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
game_over = False
game_won = False
moving = False
direction_command = 0
counter = 0
flicker = False
startup_counter = 0

# Player position
player_x = 450
player_y = 663
direction = 0

# Ghost positions
blinky_x, blinky_y, blinky_direction = 56, 58, 0
inky_x, inky_y, inky_direction = 440, 388, 2
pinky_x, pinky_y, pinky_direction = 440, 438, 2
clyde_x, clyde_y, clyde_direction = 440, 438, 2

# Ghost dead status
blinky_dead = inky_dead = pinky_dead = clyde_dead = False

# Ghost home status
blinky_box = inky_box = pinky_box = clyde_box = False

# Revival counters for ghosts
blinky_revival_counter = 0
inky_revival_counter = 0
pinky_revival_counter = 0
clyde_revival_counter = 0
REVIVAL_TIME = 300  # Adjust this value as needed

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction in [2, 3]:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction in [0, 1]:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_clyde(self):
        return self.move_generic()

    def move_blinky(self):
        return self.move_generic()

    def move_inky(self):
        return self.move_generic()

    def move_pinky(self):
        return self.move_generic()

    def move_generic(self):
        # r, l, u, d
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos -= 30
        return self.x_pos, self.y_pos, self.direction


    def revive(self, x, y, direction):
        self.x_pos = x
        self.y_pos = y
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.direction = direction
        self.dead = False
        self.in_box = True
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

def draw_misc():
    score_text = font.render(f'Score: {score}', True, COLOR_WHITE)
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives+1):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))

def check_collisions(scor, power, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scor, power, power_count, eaten_ghosts

def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, COLOR_WHITE, (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, COLOR_WHITE, (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, COLOR_BLUE, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, COLOR_BLUE, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, COLOR_BLUE, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, math.pi / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, COLOR_BLUE,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], math.pi / 2, math.pi, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, COLOR_BLUE, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], math.pi,
                                3 * math.pi / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, COLOR_BLUE,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * math.pi / 2,
                                2 * math.pi, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, COLOR_WHITE, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    image_index = (counter // 5) % len(player_images)
    if direction == 0:
        screen.blit(player_images[image_index], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[image_index], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[image_index], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[image_index], 270), (player_x, player_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

def move_player(play_x, play_y):
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += PLAYER_SPEED
    elif direction == 1 and turns_allowed[1]:
        play_x -= PLAYER_SPEED
    if direction == 2 and turns_allowed[2]:
        play_y -= PLAYER_SPEED
    elif direction == 3 and turns_allowed[3]:
        play_y += PLAYER_SPEED
    return play_x, play_y

def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not blinky_dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky_dead and eaten_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky_dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky_dead and eaten_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky_dead:
            pink_target = (player_x, runaway_y)
        elif not pinky_dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde_dead and not eaten_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde_dead and eaten_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        if not blinky_dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky_dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky_dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde_dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]

def draw_menu():
    screen.fill('black')
    title_font = pygame.font.Font('freesansbold.ttf', 50)
    menu_font = pygame.font.Font('freesansbold.ttf', 30)

    title_text = title_font.render('Pac-Man', True, COLOR_WHITE)
    start_text = menu_font.render('1. Start Game', True, COLOR_WHITE)
    instructions_text = menu_font.render('2. Instructions', True, COLOR_WHITE)
    quit_text = menu_font.render('3. Quit', True, COLOR_WHITE)

    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 100))

    pygame.display.flip()

def menu():
    in_menu = True
    while in_menu:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    in_menu = False  # Start the game
                if event.key == pygame.K_2:
                    show_instructions()
                if event.key == pygame.K_3:
                    pygame.quit()
                    exit()

def show_instructions():
    showing_instructions = True
    while showing_instructions:
        screen.fill('black')
        instructions_font = pygame.font.Font('freesansbold.ttf', 20)
        instructions_text = [
            "Use arrow keys to move Pac-Man.",
            "Avoid the ghosts, they will kill you if they touch you.",
            "Eat all the dots to win.",
            "Eat the large power-up dots to temporarily scare the ghosts.",
            "Press 'ESC' to return to the menu."
        ]

        for i, line in enumerate(instructions_text):
            instruction_surface = instructions_font.render(line, True, COLOR_WHITE)
            screen.blit(instruction_surface, (50, 100 + i * 30))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    showing_instructions = False

# Initialize targets
targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)

# Run the menu first
menu()

# Main game loop
run = True
while run:
    clock.tick(FPS)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < POWERUP_DURATION:
        power_counter += 1
    elif powerup and power_counter >= POWERUP_DURATION:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill('black')
    draw_board()
    center_x = player_x + 23
    center_y = player_y + 24
    if powerup:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]
    if eaten_ghost[0]:
        ghost_speeds[0] = 2
    if eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3]:
        ghost_speeds[3] = 2
    if blinky_dead:
        ghost_speeds[0] = 4
    if inky_dead:
        ghost_speeds[1] = 4
    if pinky_dead:
        ghost_speeds[2] = 4
    if clyde_dead:
        ghost_speeds[3] = 4

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)
    draw_player()
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_img, blinky_direction, blinky_dead, blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_img, inky_direction, inky_dead, inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_img, pinky_direction, pinky_dead, pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_img, clyde_direction, clyde_dead, clyde_box, 3)
    draw_misc()
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)  # Update targets

    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)

    if powerup:
        if player_circle.colliderect(blinky.rect) and not eaten_ghost[0]:
            blinky_dead = True
            eaten_ghost[0] = True
            score += (2 ** eaten_ghost.count(True)) * 100
            blinky_revival_counter = 0
        if player_circle.colliderect(inky.rect) and not eaten_ghost[1]:
            inky_dead = True
            eaten_ghost[1] = True
            score += (2 ** eaten_ghost.count(True)) * 100
            inky_revival_counter = 0
        if player_circle.colliderect(pinky.rect) and not eaten_ghost[2]:
            pinky_dead = True
            eaten_ghost[2] = True
            score += (2 ** eaten_ghost.count(True)) * 100
            pinky_revival_counter = 0
        if player_circle.colliderect(clyde.rect) and not eaten_ghost[3]:
            clyde_dead = True
            eaten_ghost[3] = True
            score += (2 ** eaten_ghost.count(True)) * 100
            clyde_revival_counter = 0

    if blinky_dead:
        blinky_revival_counter += 1
        if blinky_revival_counter > REVIVAL_TIME:
            blinky.revive(440, 388, 2)  # Revive at the ghost house position
            blinky_dead = False

    if inky_dead:
        inky_revival_counter += 1
        if inky_revival_counter > REVIVAL_TIME:
            inky.revive(440, 388, 2)  # Revive at the ghost house position
            inky_dead = False

    if pinky_dead:
        pinky_revival_counter += 1
        if pinky_revival_counter > REVIVAL_TIME:
            pinky.revive(440, 388, 2)  # Revive at the ghost house position
            pinky_dead = False

    if clyde_dead:
        clyde_revival_counter += 1
        if clyde_revival_counter > REVIVAL_TIME:
            clyde.revive(440, 388, 2)  # Revive at the ghost house position
            clyde_dead = False

    if not powerup:
        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or (player_circle.colliderect(inky.rect) and not inky.dead) or (player_circle.colliderect(pinky.rect) and not pinky.dead) or (player_circle.colliderect(clyde.rect) and not clyde.dead):
            if lives != 0:
                lives = lives -1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                powerup = False
                power_counter = 0
                lives = 2
                startup_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                score = 0
                level = copy.deepcopy(mazes)
                game_over = False
                game_won = False

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    pygame.display.flip()

pygame.quit()
