# -*- coding: utf-8 -*-
"""
@author: Jakub Cholewa

Music by StrangeZero:

https://www.jamendo.com/artist/3799/strangezero
https://www.jamendo.com/track/1378740/burnin-star
https://www.jamendo.com/track/1378739/you-pushed-the-button-for-me
https://www.jamendo.com/track/1378742/synthia
https://www.jamendo.com/track/1378743/rapidly-unexpected
https://www.jamendo.com/track/1378741/plastic-console
https://www.jamendo.com/track/536419/ikebana
https://www.jamendo.com/track/536420/different-feelings

"""

import pygame
from pygame.locals import *
import time
import os
import getpass

SCORE = 0
LIFE = 3

BLOCK_WIDTH = 50
BLOCK_HEIGHT = 20
BALL_SIZE = 10
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 10
PLAYFIELD_SIZE = (650, 700)
ADD_AREA = 100
RIGHT_AREA = 650
SCREEN_SIZE = (1300,800)
CLOCK = pygame.time.Clock()
WHITE = (255,255,255)
RED = (200,0,0)
RED_LIGHT = (255,0,0)
GREEN = (34,177,76)
GREEN_LIGHT = (0,255,0)
YELLOW = (200, 200, 0)
YELLOW_LIGHT = (255,255,0)
BLACK = (0,0,0)
PURPLE = (150,0,205)
PURPLE_LIGHT = (236, 71, 233)

class Block:
    def __init__(self, x_coord, y_coord, block_color, block_life):
        self.block_x = x_coord
        self.block_y = y_coord
        self.block_color = block_color
        self.block_life = block_life
        self.block = None
        
        if block_color == 1:
            self.block = pygame.image.load("img/block_solid.png").convert()
        elif block_color == 2:
            self.block = pygame.image.load("img/block_red.png").convert()
        elif block_color == 3:
            self.block = pygame.image.load("img/block_yellow.png").convert()
        elif block_color == 4:
            self.block = pygame.image.load("img/block_blue.png").convert()
        elif block_color == 5:
            self.block = pygame.image.load("img/block_pink.png").convert()
        elif block_color == 6:
            self.block = pygame.image.load("img/block_green.png").convert()
        return
        
def generate_level(level):
    file = None
    data = None
    if level == 1:
        file = open("levels/level1.txt", "r")
    elif level == 2:
        file = open("levels/level2.txt", "r")
    elif level == 3:
        file = open("levels/level3.txt", "r")
    elif level == 4:
        file = open("levels/level4.txt", "r")
    data = file.readlines()
    file.close()
    i=0
    blocks = []
    while i<len(data)-3:
        block_x = int(data[i].rstrip())
        block_y = int(data[i+1].rstrip())
        block_color = int(data[i+2].rstrip())
        block_life = int(data[i+3].rstrip())
        block = Block(block_x, block_y, block_color, block_life)
        blocks.append(block)
        i+=5
    return blocks
                

class ArkanoidGame(object):
    def __init__(self, score = SCORE, life = LIFE, cont = False, level = 1):
        #pygame.mixer.pre_init(44100, -16, 2, 2048)
        #pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        #pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.display.set_caption("Arkanoid")
        icon = pygame.image.load("img/ball.png")
        pygame.display.set_icon(icon)
        self.surface = pygame.display.set_mode(SCREEN_SIZE)
        self.surface.fill(BLACK)
        self.score = score
        self.life = life
        self.level=level
        self.cont = cont
        self.blocks = generate_level(self.level)
        self.smallfont = pygame.font.SysFont(None, 25)
        self.mediumfont = pygame.font.SysFont(None, 50)
        self.largefont = pygame.font.SysFont(None, 80)
        self.game_intro()
       
        
    def game_intro(self):
    
        
        menu = pygame.image.load("img/menu.jpg")
        pygame.mixer.music.load("sounds/music_menu.ogg")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
    
        self.draw_player()
        self.draw_ball()
        if self.cont == True:
            self.gamestate = 1
            self.game_loop()
        
        while True:
            self.surface.fill(BLACK)
            self.surface.blit(menu,(0,0))
            
            self.put_button(200,400,250,100,"Play", PURPLE, PURPLE_LIGHT, "play")
            self.put_button(850,400,250,100,"Controls", PURPLE, PURPLE_LIGHT, "controls")
            self.put_button(850,600,250,100,"Quit", PURPLE, PURPLE_LIGHT, "quit")
            self.put_button(200,600,250,100,"Scores", PURPLE, PURPLE_LIGHT, "high")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_exit()
                    
            pygame.display.update()
            
    def game_exit(self):
        pygame.quit()
        
    def load_images(self):
        self.playfield = pygame.image.load("img/playfield.png").convert()
        self.frame = pygame.image.load("img/frame.png").convert()
        self.player = pygame.image.load("img/player.png")
        self.ball = pygame.image.load("img/ball.png").convert()
        self.level1 = pygame.image.load("img/level1.jpg").convert()
        self.game_frame1 = pygame.image.load("img/game_frame1.png")
        self.game_frame2 = pygame.image.load("img/game_frame2.png")
        self.game_frame3 = pygame.image.load("img/game_frame3.png")
        
    def load_sounds(self):
        self.hit = pygame.mixer.Sound("sounds/hit.ogg")
        self.destroy = pygame.mixer.Sound("sounds/destroy.wav")
             
    def draw_player(self):
        self.player_speed = 10
        self.player_x = PLAYFIELD_SIZE[0]/2 - PLAYER_WIDTH/2 + ADD_AREA
        self.player_y = PLAYFIELD_SIZE[1] - 50 + ADD_AREA

    def move_player(self, direction):
        self.player_x += direction*self.player_speed
        
    def draw_ball(self):
        self.ball_x_speed = 5
        self.ball_y_speed = 5
        self.ball_x = self.player_x + PLAYER_WIDTH/2 - BALL_SIZE/2
        self.ball_y = self.player_y - BALL_SIZE
        self.dir_x = 0
        self.dir_y = 0
        self.ball_active = False
        
    def move_ball(self):
        self.ball_x += self.dir_x*self.ball_x_speed
        self.ball_y += self.dir_y*self.ball_y_speed
        
    def check_borders(self):
        if self.ball_x < ADD_AREA:
            self.dir_x *= -1
            self.hit.play()
        if self.ball_x > PLAYFIELD_SIZE[0]+ADD_AREA-BALL_SIZE:
            self.dir_x *= -1
            self.hit.play()
        if self.ball_y < ADD_AREA:
            self.dir_y *= -1
            self.hit.play()
        if self.ball_y > PLAYFIELD_SIZE[1]+ADD_AREA:
            self.ball_active = False
            self.life -= 1
            
    def check_collission_player(self):

         #if self.ball_y + BALL_SIZE == self.player_y and self.ball_x+BALL_SIZE/2 >= self.player_x and self.ball_x+BALL_SIZE/2<=self.player_x+PLAYER_WIDTH:
         #    self.dir_y = -1
         #    self.hit.play()
         #    if self.dir_x > -2 and self.ball_x+BALL_SIZE/2<=self.player_x+25:
         #        self.dir_x -= 1
         #    if self.dir_x < 2 and self.ball_x+BALL_SIZE/2 >= self.player_x+55:
         #        self.dir_x +=1
                 
        if self.ball_y + BALL_SIZE >= self.player_y and self.ball_y + BALL_SIZE <= self.player_y+PLAYER_HEIGHT and self.ball_x >= self.player_x-BALL_SIZE and self.ball_x<=self.player_x+PLAYER_WIDTH:
             self.dir_y = -1
             self.hit.play()
             if self.dir_x >= -2.5 and self.ball_x+BALL_SIZE/2<=self.player_x+17:
                 self.dir_x -= 0.3
             if self.dir_x >= -2.5 and self.ball_x+BALL_SIZE/2>self.player_x+17 and self.ball_x+BALL_SIZE/2<=33:
                 self.dir_x -= 0.2
             if self.dir_x <= 2.5 and self.ball_x+BALL_SIZE/2>=self.player_x+50 and self.ball_x+BALL_SIZE/2 < 66:
                 self.dir_x += 0.2
             if self.dir_x <= 2.5 and self.ball_x+BALL_SIZE/2 > self.player_x+66:
                 self.dir_x += 0.3
             
       
            
    def check_collission_block(self, block_x, block_y):
        if self.ball_x+BALL_SIZE/2 >= block_x and self.ball_x+BALL_SIZE/2 <= block_x+BLOCK_WIDTH and self.ball_y == block_y+BLOCK_HEIGHT:
            self.dir_y *= -1
            if self.dir_y >= 1.3:
                self.dir_y -= 0.1
            return True
        if self.ball_x+BALL_SIZE/2 >= block_x and self.ball_x+BALL_SIZE/2 <= block_x+BLOCK_WIDTH and self.ball_y+BALL_SIZE == block_y:
            self.dir_y *= -1
            return True
        if self.ball_x+BALL_SIZE/2 == block_x + BLOCK_WIDTH and self.ball_y+BALL_SIZE/2 >=block_y and self.ball_y+BALL_SIZE/2 <= block_y+BLOCK_HEIGHT:
            self.dir_x *= -1
            return True
        if self.ball_x+BALL_SIZE/2 == block_x and self.ball_y+BALL_SIZE/2 >= block_y and self.ball_y+BALL_SIZE/2 <= block_y+BLOCK_HEIGHT:
            self.dir_x *= -1
            return True
        return False
        
    def text_objects(self, text, color, font):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()
        
    def message_to_screen(self, text, color, y_change = 0, size="small"):
        if size == "small":
            textSurf, textRect = self.text_objects(text, color, self.smallfont)
        if size == "medium":
            textSurf, textRect = self.text_objects(text, color, self.mediumfont)
        if size == "large":
            textSurf, textRect = self.text_objects(text, color, self.largefont)
            
        textRect.center = int((SCREEN_SIZE[0] / 2)), int((SCREEN_SIZE[1] /2) + y_change)
        self.surface.blit(textSurf, textRect)
        
    def text_to_button(self, text, color, button_x, button_y, button_width, button_height, size):
        textSurf, textRect = self.text_objects(text, color, size)
        textRect.center = (button_x+(button_width/2)), (button_y+button_height/2)
        self.surface.blit(textSurf, textRect)
        
    def put_button(self,button_x, button_y, button_width, button_height, text, color, color_light, action = None):
        button_select = pygame.mixer.Sound("sounds/button_select.wav")
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if button_x+button_width > cur[0] > button_x and button_y+button_height > cur[1] > button_y:
            pygame.draw.rect(self.surface, color_light, (button_x, button_y, button_width, button_height))
            if click[0] == 1 and action != None:
                button_select.play()
                if action == "quit":
                    self.game_exit()
                if action == "controls":
                    self.game_controls()
                if action == "play":
                    self.gamestate = 1
                    self.game_loop()
                if action == "menu":
                    ArkanoidGame()
                if action == "next":
                    ArkanoidGame(self.score, self.life, True, self.level)
                if action == "high":
                    self.highscores()
                    
        else:
            pygame.draw.rect(self.surface, color, (button_x, button_y, button_width, button_height))
        self.text_to_button(text, BLACK, button_x, button_y, button_width, button_height, self.largefont)
            
    def game_controls(self):
        controls = pygame.image.load("img/controls.jpg").convert()
        controls_frame = pygame.image.load("img/ramka_controls.png")
        self.surface.blit(controls,(0,0))
        self.surface.blit(controls_frame,(250,290))
        self.message_to_screen("Move player : Left and Right arrows", WHITE, -40, "medium")
        self.message_to_screen("Shoot ball: Spacebar", WHITE, 40, "medium")
        self.message_to_screen("Pause: P", WHITE, 120, "medium")
        while True:   
            self.put_button(150,650,250,100,"Play", PURPLE, PURPLE_LIGHT, "play")
            self.put_button(900,650,250,100,"Quit", PURPLE, PURPLE_LIGHT, "quit")
            pygame.display.update()
            CLOCK.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_exit()
        
    def game_over_screen(self):
       gameover = pygame.image.load("img/gameover.jpg").convert()
       gameover_frame = pygame.image.load("img/gameover_frame.png")
       
       self.surface.blit(gameover,(0,0))
       self.surface.blit(gameover_frame,(400,410))
       self.message_to_screen("Your score: "+str(self.score), WHITE, 100, "large")
       
       self.check_score()
   
       while True:
            
            self.put_button(150,650,250,100,"Menu", PURPLE, PURPLE_LIGHT, "menu")
            self.put_button(900,650,250,100,"Quit", PURPLE, PURPLE_LIGHT, "quit")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_exit()
              
                
            
                        
    def continue_screen(self):
    
        continue_background = pygame.image.load("img/continue.jpg").convert()
        continue_frame = pygame.image.load("img/gameover_frame.png")
        
        self.surface.blit(continue_background,(0,0))
        self.surface.blit(continue_frame,(400,410))
        self.message_to_screen("Your score: "+str(self.score), WHITE, 100, "large")
        
        while True:
  
            self.put_button(150,650,250,100,"Menu", PURPLE, PURPLE_LIGHT, "menu")
            self.put_button(900,650,250,100,"Next", PURPLE, PURPLE_LIGHT, "next")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_exit() 
                
    def finish_screen(self):
        finish = pygame.image.load("img/finish.jpg").convert()
        finish_frame = pygame.image.load("img/gameover_frame.png")
        pygame.mixer.music.stop()
        pygame.mixer.music.load("sounds/music_finish.ogg")
        pygame.mixer.music.set_volume(2)
        pygame.mixer.music.play(-1)
        
        self.surface.blit(finish,(0,0))
        self.surface.blit(finish_frame,(400,410))
        self.message_to_screen("Your score: "+str(self.score), WHITE, 100, "large")
        
        self.check_score()
    
        
        while True:
            self.put_button(150,650,250,100,"Menu", PURPLE, PURPLE_LIGHT, "menu")
            self.put_button(900,650,250,100,"Quit", PURPLE, PURPLE_LIGHT, "quit")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_exit()
                
    def check_score(self):
        file = open("highscore.txt", "r")
        data = file.readlines()
        file.close()
        user = getpass.getuser()
        i=0
        for j in range(10):
            if self.score >= int(data[i].rstrip()):
                break
            i+=2
        if i<18:
            file = open("highscore.txt", "w")
            for x in range(i):
                file.write(str(data[x]))
            file.write(str(self.score)+"\n")
            file.write(user+"\n")
            while i<=17:
                file.write(str(data[i]))
                i+=1
            file.close()
                    
        
    def pause(self):
        
        pause = True
        self.message_to_screen("PAUSE", WHITE, -100, "medium")
        self.message_to_screen("Press P to continue the game", WHITE, 0, "small")
        pygame.display.update()
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pause = False
            CLOCK.tick(15)
        
    def highscores(self):
        
        highscores_background = pygame.image.load("img/highscores.jpg").convert()
        highscores_frame = pygame.image.load("img/highscores_frame.png")
        
        self.surface.blit(highscores_background,(0,0))
        self.surface.blit(highscores_frame,(550,270))
        
        file = open("highscore.txt", "r")
        data = file.readlines()
        file.close()
        i=0
        j=1
        while i<=19:
            
            self.message_to_screen(str(j)+". "+data[i].rstrip()+" "+data[i+1].rstrip(), WHITE, i*20-50, "small")
            i+=2
            j+=1
        
        
        while True:
            self.put_button(150,650,250,100,"Menu", PURPLE, PURPLE_LIGHT, "menu")
            self.put_button(900,650,250,100,"Quit", PURPLE, PURPLE_LIGHT, "quit")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_exit()
            
        
    def game_loop(self):
        myfont = pygame.font.Font(None, 20)
        self.load_images()
        self.load_sounds()
        
        pygame.mixer.music.stop()
        if self.level==1:
            pygame.mixer.music.load("sounds/music_level1.ogg")
        elif self.level==2:
            pygame.mixer.music.load("sounds/music_level2.ogg")
        elif self.level==3:
            pygame.mixer.music.load("sounds/music_level3.ogg")
        elif self.level==4:
            pygame.mixer.music.load("sounds/music_level4.ogg")
            
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()
        
        while self.gamestate == 1:
            button = pygame.key.get_pressed()
            
            if button[pygame.K_RIGHT] == True:  
                if self.player_x < PLAYFIELD_SIZE[0]+ ADD_AREA - PLAYER_WIDTH - 5:
                    self.move_player(1)
                else: self.player_x = PLAYFIELD_SIZE[0]+ADD_AREA - PLAYER_WIDTH
                
            elif button[pygame.K_LEFT] == True:
                if self.player_x > ADD_AREA + 5:
                    self.move_player(-1)
                else:
                    self.player_x = ADD_AREA
                    
            elif button[pygame.K_a] == True:
                self.level+=1
                if self.level != 5:
                    self.continue_screen()
                else:
                    self.finish_screen()
                
            if button[pygame.K_SPACE] == True and self.ball_active == False:
                self.hit.play()
                self.ball_active = True
                self.dir_y = -1
            if self.ball_active == True:
                self.move_ball()
                self.check_borders()
                self.check_collission_player()
            if button[pygame.K_p] == True:
                self.pause()
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gamestate = 0
                    
            self.surface.fill(BLACK)
            self.surface.blit(self.level1,(0,0))
            self.surface.blit(self.frame,(ADD_AREA/2,ADD_AREA/2))
            self.surface.blit(self.playfield,(ADD_AREA,ADD_AREA))
            self.surface.blit(self.game_frame1,(910,60))
            self.surface.blit(self.game_frame2,(910,290))
            self.surface.blit(self.game_frame3,(910,590))
            self.surface.blit(self.player,(self.player_x,self.player_y))
            if self.ball_active == False:
                self.draw_ball()
            self.surface.blit(self.ball,(self.ball_x, self.ball_y))
        
           
            for block in self.blocks:
                if self.check_collission_block(block.block_x, block.block_y) == True:
                    self.score += 1
                    block.block_life-=1
                    if block.block_life == 0:
                        self.destroy.play()
                        self.blocks.remove(block)
                    else:
                        self.hit.play()
                        block.block = pygame.image.load("img/block_solid_broken.png")
                
            for block in self.blocks:
                self.surface.blit(block.block, (block.block_x, block.block_y))
            
            
            level_text = self.largefont.render("Level "+str(self.level), True, YELLOW)            
            score_text = self.largefont.render("SCORE:", True, YELLOW)
            score_points = self.largefont.render(str(self.score), True, YELLOW)
            lives_text = self.largefont.render("LIVES:", True, YELLOW)
            lives_points = self.largefont.render(str(self.life), True, YELLOW)
            
            self.surface.blit(level_text,(ADD_AREA+PLAYFIELD_SIZE[0]+200, ADD_AREA))
            self.surface.blit(score_text,(ADD_AREA+PLAYFIELD_SIZE[0]+200, ADD_AREA+220))
            self.surface.blit(score_points,(ADD_AREA+PLAYFIELD_SIZE[0]+200, ADD_AREA+300))
            self.surface.blit(lives_text,(ADD_AREA+PLAYFIELD_SIZE[0]+200, ADD_AREA+520))
            self.surface.blit(lives_points,(ADD_AREA+PLAYFIELD_SIZE[0]+200, ADD_AREA+600))
            
            
            pygame.display.update()
            CLOCK.tick(60)
            
            if self.life == 0:
                self.gamestate = 0
            if not any(self.blocks):
                self.level+=1
                if self.level != 5:
                    self.continue_screen()
                else:
                    self.finish_screen()
        
        self.game_over_screen()
        
ArkanoidGame()