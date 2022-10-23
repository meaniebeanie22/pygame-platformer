import pygame
from pygame.locals import *
import sys
import random
import time

pygame.init()
vec = pygame.math.Vector2 #2 for two dimensional

HEIGHT = 600
WIDTH = 600
FPS = 7
SPEED = 20
APPLES = 2 

FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("An Abomination of Snake")

class Player(pygame.sprite.Sprite):
    def __init__(self): ## 
        super().__init__()
        self.surf = pygame.Surface((20,20))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect()
        self.pos = vec(WIDTH//2, HEIGHT//2)
        self.score = 1
        self.direction = 'up'
        all_sprites.add(self)
        self.cells = []
        


    def move(self, events): ## 
        c_dir = self.direction
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP and c_dir != 'down':
                    self.direction = 'up'
                if event.key == K_RIGHT and c_dir != 'left':
                    self.direction = 'right'
                if event.key == K_DOWN and c_dir != 'up':
                    self.direction = 'down'
                if event.key == K_LEFT and c_dir != 'right':
                    self.direction = 'left'

        if self.direction == 'up':
            self.pos.y -= SPEED
        elif self.direction == 'right':
            self.pos.x += SPEED
        elif self.direction == 'down':
            self.pos.y += SPEED
        elif self.direction == 'left':
            self.pos.x -= SPEED
        
        self.rect.topleft = self.pos
        # deal with cells
        self.cells.insert(0, vec(self.pos)) ## these three lines are no longer fricked - was apparently inserting a vector id that can change, not the data itself
        while len(self.cells) > self.score + 3:
            bob = self.cells.pop()
            
    def update(self):
        hits = pygame.sprite.spritecollide(self, apples, False)
        if hits:
            for apple in hits:
                self.score += 1
                apple.kill()
        


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255,0,0))
        C = True
        while C:
            apx = round(random.randint(10, WIDTH-10), -1)
            apy = round(random.randint(10, HEIGHT-10), -1)
            apx -= apx % 20
            apy -= apy % 20
            if not(vec(apx,apy) in P1.cells):
                C = False
                
        self.rect = self.surf.get_rect(topleft = (apx, apy))
        all_sprites.add(self)
    
    def move(self, events):
        pass

all_sprites = pygame.sprite.Group()
apples = pygame.sprite.Group()
def apple_gen():
    while len(apples) < APPLES:
        ap = Apple()
        apples.add(ap) 

P1 = Player()

while True:
    P1.update()
    print('pos:', P1.pos)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: sys.exit()
    apple_gen()

    if P1.pos.x >= WIDTH:
        P1.pos.x = 0
        
    if P1.pos.y >= HEIGHT:
        P1.pos.y = 0

    if P1.pos.x < 0:
        P1.pos.x = WIDTH

    if P1.pos.y < 0:
        P1.pos.y = HEIGHT

    elif P1.pos in P1.cells[1:]:
        print('failure, score =', P1.score)
        break

    displaysurface.fill((0,0,0))

    for entity in all_sprites:
        if isinstance(entity, Player):
            for cell in entity.cells:
                sur = pygame.Surface((20,20))
                sur.fill((0,255,0))
                rec = sur.get_rect()
                rec.topleft = cell
                displaysurface.blit(sur, rec)
        else:
            displaysurface.blit(entity.surf, entity.rect)
        
        entity.move(events)
    FPS = round(7 + P1.score ** (1/2), 1)

    f = pygame.font.SysFont("Verdana", 20)     
    g  = f.render(str(P1.score), True, (123,255,0))   
    displaysurface.blit(g, (WIDTH/2, 10)) 

    pygame.display.update()
    FramePerSec.tick(FPS)
