#!/usr/bin/env python3
# coding: utf-8

# In[1]:
import pygame
import sys
import os
import os.path as path
from random import randint

# recursive function that takes in arguments (string of binary number, length of string, current position, sum)
# returns string
def bin_to_dec(li, n, s):
    #base condition
    if (n == 0):
        return s
    l = len(li)
    _sum = 0
    if li[n-1] == '1':
        _sum += (2**(l-n))
    return str(bin_to_dec(li, n-1, s + _sum))

#shifts one bit to the right
def right_shift(li):  
    del li[-1]
    li.insert(0, "0")

# shifts one bit to the left
def left_shift(li):
    del li[0]
    li.append("0")

#switches 1 and 0 in li
def switch_digit(index):
    num = li[index]
    if num == "0":
        li[index] = "1"
    elif num == "1":
        li[index] = "0"

# function to print text s with alignment (r or l) at position (x, y) on screen
def print_text(s, text_color, bg_color,size, screen, x, y, side):
    #create font object
    font = pygame.font.Font('freesansbold.ttf', size)
    #create text surface object
    text = font.render(s, True, text_color)
    # text.set_alpha(0)
    #create rect object for text surface object
    textRect = text.get_rect()
    if side == "r":
        textRect.bottomright = (x,y)
    elif side == "l":
        textRect.bottomleft = (x,y)
    elif side == "c":
        textRect.center = (x,y)

    # print onto screen
    screen.blit(text, textRect)
    
def print_question(num, text_color, bg_color ,screen):
    s = "make: " + num
    x = WIDTH/2
    y = 150
    # print_text(s, black, 30, screen, x, y, "l")
    # #create font object
    font = pygame.font.Font('freesansbold.ttf', 30)
    #create text surface object
    text = font.render(s, True, text_color)
    #create rect object for text surface object
    textRect = text.get_rect()
    textRect.center = (x,y) 
    #print onto screen
    screen.blit(text, textRect)

# colors
white = (255, 255, 255)
black = (0, 0, 0)
grey = (240, 240, 240)
dark_grey = (200, 200, 200)
green = (0, 255, 0)

# background color
bg_color = white

#initialize pygame
pygame.init()

page = "menu" # menu, instructions, easy_mode, hard_mode, end_screen, calculator, credits

#list that stores binary digits
li = []  

# dimensions 900x500 
BORDER_W = 50
WIDTH = 800 + 2*BORDER_W        
HEIGHT = 500

# set up drawing window
screen = pygame.display.set_mode([WIDTH,HEIGHT])

# If the code is frozen, use this path:
if getattr(sys, 'frozen', False):
    CurrentPath = sys._MEIPASS
# If it's not use the path we're on now
else:
    CurrentPath = path.dirname(__file__)

spriteFolderPath = path.join(CurrentPath, 'sprites')

# images
img_zero = pygame.image.load(path.join(spriteFolderPath, 'zero.png'))
img_one = pygame.image.load(path.join(spriteFolderPath, 'one.png'))
img_bg = pygame.image.load(path.join(spriteFolderPath, 'snow.jpg'))
        
# ------------ class declarations ------------
class Digit(pygame.sprite.Sprite):
    def __init__(self, num, index, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img_zero.copy()
        self.rect = self.image.get_rect()
        self.num = num
        self.index = index
        self.rect.left = x
        self.rect.top = y

    def update(self):
        self.num = li[self.index]
        if self.num == "0":
            self.image = img_zero.copy()
        elif self.num == "1":
            self.image = img_one.copy()

class Button:
    def __init__(self, s, position, size, link):
        #create font object
        self.name = s
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.bg_color = grey
        #create text surface object
        self.text = self.font.render(s, True, black, self.bg_color)
        #create rect object for text surface object
        self.textRect = self.text.get_rect()
        self.textRect.center = position
        self.size = size
        self.position = position
        self.link = link

        self.button_surface = pygame.Surface(size)
        self.button_surface.fill(self.bg_color)
        self.rect = self.button_surface.get_rect()
        self.rect.center = position

    def draw(self, screen):
        screen.blit(self.button_surface, self.rect)
        screen.blit(self.text, self.textRect)

    def set_bg_color(self, color):
        self.bg_color = color
        self.text = self.font.render(self.name, True, black, self.bg_color)
        self.button_surface.fill(self.bg_color)

# --------------------------------------------

# # create digit sprites group and add Digit objects
digit_sprites = pygame.sprite.Group()
separation = 4          # distance between digits
#if mouse is over button and is clicked, go to next page
def clicked_over_digit(m):
    global digit_sprites
    for _digit in digit_sprites:
        left = _digit.rect.left
        right = left + _digit.rect.width
        top = _digit.rect.top
        bottom = top + _digit.rect.height
        if (left <= m[0] <= right) and (top <= m[1] <= bottom): # is mouse over digit
            switch_digit(_digit.index)
            _digit.update()

# create button sprites group and add Button objects
button_sprites = []
def set_objects(page):
    global button_sprites
    global digit_sprites
    button_sprites.clear()
    for sprite in digit_sprites:
        sprite.kill()
    if page == "menu":
        buttonsize = (200, 40)
        button_sprites.append(Button("Easy mode", (WIDTH/2, HEIGHT/2+10), buttonsize, "easy_mode"))
        button_sprites.append(Button("Hard mode", (WIDTH/2, HEIGHT/2+60), buttonsize, "hard_mode"))
        button_sprites.append(Button("Calculator mode", (WIDTH/2, HEIGHT/2+110), buttonsize, "calculator"))
        button_sprites.append(Button("Quit", (WIDTH/2, HEIGHT/2+160), buttonsize, "quit"))
    elif page == "easy_mode" or page == "hard_mode" or page == "end_screen":
        button_sprites.append(Button("Main Menu", (85, HEIGHT-30), (150,40), "menu"))
    elif page == "calculator":
        button_sprites.append(Button("Main Menu", (85, HEIGHT-30), (150,40), "menu"))
        button_sprites.append(Button(">>", (WIDTH/2+50, HEIGHT/2-100), (80,40), ""))
        button_sprites.append(Button("<<", (WIDTH/2-50, HEIGHT/2-100), (80,40), ""))

# change button color if mouse is hovering over
def mouseover_button(m):
    global button_sprites
    global digit_sprites
    for button in button_sprites:
        left = button.rect.left
        right = left + button.rect.width
        top = button.rect.top
        bottom = top + button.rect.height
        if (left <= m[0] <= right) and (top <= m[1] <= bottom): # is mouse over button
            button.set_bg_color(dark_grey)
        else:
            button.set_bg_color(grey)

#if mouse is over button and is clicked, go to next page
def clicked_over_button(m):
    global page
    global button_sprites
    global digit_sprites
    global li
    for button in button_sprites:
        left = button.rect.left
        right = left + button.rect.width
        top = button.rect.top
        bottom = top + button.rect.height
        if (left <= m[0] <= right) and (top <= m[1] <= bottom): # is mouse over button
            if button.link != "":
                set_objects(button.link)
                page = button.link
            else:
                if button.name == ">>":
                    right_shift(li)
                elif button.name == "<<":
                    left_shift(li)
                digit_sprites.update()


# clock
clock = pygame.time.Clock()
time = 60           # seconds
time_left = time   
FPS = 30
frame = 0           # for timer
dp_time = 2*FPS     # how long to display bonus time for
frame1 = dp_time    # for bonus time
def bonus_time(d):
    if d == "easy_mode":
        return int(4)
    elif d == "hard_mode":
        return int(8)

# generate random number
new_randn = True
maxn = 0
currn = 0
samen = 0

correct = False
score_added = False
score = 0

def reset():
    global time_left
    global time
    global correct
    global score_added
    global score
    global currn
    global samen
    time_left = time
    correct = False
    score_added = False
    score = 0
    while currn == samen:
        currn = str(randint(0,maxn))
    samen = currn

# game loop
running = True
set_objects("menu")
while running:
    pygame.display.set_caption('1000')
    mouse = pygame.mouse.get_pos()
    #print background 
    screen.blit(img_bg, (0,0))

    # ------------- Menu -------------
    if page == "menu":
        print_text("1000", black, bg_color, 100, screen, WIDTH/2, HEIGHT/2 - 100, "c")

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # check if mouse is clicked 
            if event.type == pygame.MOUSEBUTTONUP: 
                for button in button_sprites:
                    left = button.rect.left
                    right = left + button.rect.width
                    top = button.rect.top
                    bottom = top + button.rect.height
                    if (left <= mouse[0] <= right) and (top <= mouse[1] <= bottom): # is mouse over button
                        diff = 0
                        if button.link == "easy_mode":
                            diff = 8
                        elif button.link == "hard_mode":
                            diff = 12
                        elif button.link == "calculator":
                            diff = 16 

                        digits_width = (diff * img_zero.get_width()) + (diff-1) * separation
                        digit_x = WIDTH/2 - digits_width/2 
                        digit_y = HEIGHT/2 - 60

                        maxn = (2**diff) - 1
                        currn = str(randint(1,maxn))
                        samen = currn

                        li.clear()
                        set_objects(button.link)
                        for i in range(diff):
                            li.append("0")
                            new_digit = Digit(li[i], i, digit_x, digit_y)
                            digit_sprites.add(new_digit)
                            digit_x += new_digit.image.get_width() + separation
                        
                        reset()
                        page = button.link

    # ------------- Easy/Hard Mode -------------
    elif page == "easy_mode" or page == "hard_mode":
        # timer
        if time_left < 0:
            page = "end_screen"
        if frame == FPS:
            frame = 0
            time_left -= 1
        frame += 1

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #checks if a mouse is clicked 
            if event.type == pygame.MOUSEBUTTONDOWN: 
                # if correct answer, go to next question
                if correct:
                    correct = False
                    frame1 = 0

                    bt = bonus_time(page)
                    time_left += bt
                    score_added = False
                    while currn == samen:
                        currn = str(randint(1,maxn))
                    samen = currn

                    # set all digits to 0
                    for i in range(len(li)):
                        li[i] = "0"
                    for _digit in digit_sprites:
                        _digit.update()

                else:  
                    # check if mouse is clicked over any button or digit
                    clicked_over_digit(mouse)
                    clicked_over_button(mouse)

        ans = bin_to_dec(li, len(li), 0) 
        # Draw background, print text
        if ans == currn:
            correct = True 
            screen.fill(green)
            if not score_added:
                score += 1
                score_added = True
        print_text("Score: " + str(score), black, bg_color, 30, screen, 15, 40, "l")
        if time_left >= 0:
            print_text("Time: " + str(time_left), black, bg_color, 30, screen, WIDTH-140, 40, "l")
        print_question(currn, black, bg_color, screen)
        print_text(ans, black, bg_color, 80, screen, WIDTH/2, HEIGHT-70, "c")

        if frame1 < (dp_time):
            print_text("+" + str(bt), green, bg_color, 30, screen, WIDTH-53, 70, "l")
            frame1 += 1

        # loop through digit sprites, check if mouse is over any digit
        for sprite in digit_sprites:
            left = sprite.rect.left
            right = left + sprite.rect.width
            top = sprite.rect.top
            bottom = top + sprite.rect.height
            if (left <= mouse[0] <= right) and (top <= mouse[1] <= bottom) and not correct: # is mouse over digit
                pygame.draw.rect(screen, grey, sprite.rect) # draw grey box around digit

        # draw digits
        digit_sprites.draw(screen)

    # ------------- End Screen -------------
    elif page == "end_screen":
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # check if a mouse is clicked over any button
            if event.type == pygame.MOUSEBUTTONUP:
                clicked_over_button(mouse)

        # print score
        print_text("Score: " + str(score), black, white, 90, screen, WIDTH/2, HEIGHT/2, "c")
    
    # ------------- Calculator -------------
    elif page == "calculator":
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                # check if mouse is clicked over any button or digit
                clicked_over_digit(mouse)
                clicked_over_button(mouse)

        # loop through digit sprites, check if mouse is over any digit
        for sprite in digit_sprites:
            left = sprite.rect.left
            right = left + sprite.rect.width
            top = sprite.rect.top
            bottom = top + sprite.rect.height
            if (left <= mouse[0] <= right) and (top <= mouse[1] <= bottom): # is mouse over digit
                pygame.draw.rect(screen, grey, sprite.rect) # draw grey box around digit
        digit_sprites.draw(screen)
        ans = bin_to_dec(li, len(li), 0)
        print_text(ans, black, bg_color, 80, screen, WIDTH/2, HEIGHT-70, "c")

    elif page == "quit":
        running = False

    #print buttons
    for button in button_sprites:   
        button.draw(screen)
    
    mouseover_button(mouse)

    # Flip the display
    pygame.display.flip()
    clock.tick(FPS)

# Done! Time to quit.
pygame.quit()

# %%
