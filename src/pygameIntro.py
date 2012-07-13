'''
Created on Jul 12, 2012

@author: catapult
'''
import pygame
import random
import time

black = (0, 0, 0)
white = (255, 255, 255)
red   = (255, 0, 0)
blue  = (0, 0, 255)

framePerSecond = 30
playerSpeed = 6

screen_width = 700
screen_height = 400

class Block(pygame.sprite.Sprite):
    
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20, 15])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.dx = 0
        self.dy = 0
        
    def update(self):
        self.rect.move_ip(self.dx, self.dy)
        
        
class Player(Block):
    
    def __init__(self):
        Block.__init__(self, blue)
        self.image_down = pygame.image.load("../resource/down.png")
        self.image_up = pygame.image.load("../resource/up.png")
        self.image_right = pygame.image.load("../resource/right.png")
        self.image_left = pygame.image.load("../resource/left.png")
        self.image = self.image_down
        
        
    def update(self):
        Block.update(self)
        
        if self.dx < 0:
            self.image = self.image_left
        elif self.dx > 0:
            self.image = self.image_right 
            
        if self.dy < 0:
            self.image = self.image_up
        elif self.dy > 0:
            self.image = self.image_down    
                      
        
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > screen_width - self.rect.width:
            self.rect.x = screen_width - self.rect.width
        
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > screen_height - self.rect.height:
            self.rect.y = screen_height - self.rect.height
        
    
class PointBlock(Block):
    
    def __init__(self, dx, dy):
        Block.__init__(self, black)
        self.image = pygame.image.load("../resource/sprite.png")
        self.dx = dx
        self.dy = dy
        
    def update(self):
        Block.update(self)
        if self.rect.x < 0:
            self.dx = -self.dx
            self.rect.x = 0
        elif self.rect.x > screen_width - self.rect.width:
            self.dx = -self.dx
            self.rect.x = screen_width - self.rect.width
        
        if self.rect.y < 0:
            self.dy = -self.dy
            self.rect.y = 0
        elif self.rect.y > screen_height - self.rect.height:
            self.dy = -self.dy
            self.rect.y = screen_height - self.rect.height
            
class KillBlock(Block):
    
    def __init__(self, dx, dy):
        Block.__init__(self, red)
        self.image = pygame.image.load("../resource/killSprite.png")
        self.dx = dx
        self.dy = dy
        
    def update(self):
        Block.update(self)
        if self.rect.x < 0:
            self.dx = -self.dx
            self.rect.x = 0
        elif self.rect.x > screen_width - self.rect.width:
            self.dx = -self.dx
            self.rect.x = screen_width - self.rect.width
        
        if self.rect.y < 0:
            self.dy = -self.dy
            self.rect.y = 0
        elif self.rect.y > screen_height - self.rect.height:
            self.dy = -self.dy
            self.rect.y = screen_height - self.rect.height
        
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load("../resource/bgd.png")

block_list = pygame.sprite.Group()
kill_block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

for i in range(10):
    
    dx = random.randrange(-playerSpeed, playerSpeed)
    dy = random.randrange(-playerSpeed, playerSpeed)
    
    block = PointBlock(dx, dy)
    
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)
    
    block_list.add(block)
    all_sprites_list.add(block)
    
for i in range(3):
    dx = random.randrange(1, int(.6 * playerSpeed))
    dy = random.randrange(1, int(.6 * playerSpeed))
    
    block = KillBlock(dx, dy)
    
    block.rect.x = random.randrange(int(.5*(screen_width)), screen_width)
    block.rect.y = random.randrange(int(.5*(screen_width)),screen_height)
    
    kill_block_list.add(block)
    all_sprites_list.add(block)
    
    
player = Player()
all_sprites_list.add(player)

clock = pygame.time.Clock()

score = 0

score_font = pygame.font.SysFont("arial", 20)
win_font = pygame.font.SysFont("arial",40)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.dy -= playerSpeed
            if event.key == pygame.K_DOWN:
                player.dy += playerSpeed
            if event.key == pygame.K_LEFT:
                player.dx -= playerSpeed
            if event.key == pygame.K_RIGHT:
                player.dx += playerSpeed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.dy -= -playerSpeed
            if event.key == pygame.K_DOWN:
                player.dy += -playerSpeed
            if event.key == pygame.K_LEFT:
                player.dx -= -playerSpeed
            if event.key == pygame.K_RIGHT:
                player.dx += -playerSpeed
    
    #screen.fill(white)        
    screen.blit(background, (0,0))    
    all_sprites_list.update()
    all_sprites_list.draw(screen)
    
    
    
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)
    kill_hit_list = pygame.sprite.spritecollide(player, kill_block_list, True)
    if len(kill_hit_list) > 0:
        text_win = win_font.render("Lose! ", True, red) 
        win_pos = (300,180,370,180)
        screen.blit(text_win, win_pos)
        pygame.display.flip()#similar to pygame.display.update()
        while True:
           for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit() 
    
    
    one_score = len(blocks_hit_list)
    if one_score > 0:
        score +=  one_score  
        print(score)
 
        
     
    text = score_font.render("score:"+str(score), True, red)   
    text_pos = text.get_rect()
    screen.blit(text, text_pos)
    
          
    if score == 10:
        text_win = win_font.render("Win!", True, red) 
        win_pos = (350,200,370,220)
        screen.blit(text_win, win_pos)
        pygame.display.flip()#similar to pygame.display.update()
        while True:
           for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit() 
    
    pygame.display.flip()#similar to pygame.display.update()
    
    clock.tick(framePerSecond)
    
                
    
    