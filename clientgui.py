import sys
 
import pygame
from pygame.locals import *
from clientsocket import *
import random
import numpy as np
from chatoverlay import *
from variables import *

width, height = 1200, 800

pygame.init()

TILE_SIZE = 60
clock = pygame.time.Clock()
base_font = pygame.font.Font(None, 32)
fps = 60
run = False
fpsClock = pygame.time.Clock()


screen = pygame.display.set_mode((width, height))



class Player():
    def __init__(self,x, y,ID,name,camx,camy,relx,rely):
        self.camx = camx+x
        self.camy = camy+y
        self.x = x
        self.y = y
        self.offset = [self.x/TILE_SIZE,self.y/TILE_SIZE]
        
        self.ID = ID
        self.name = name
    def draw(self):
        global width,height
        self.rect = Rect(width/2-20,height/2-20,40,40)
        pygame.draw.rect(screen, (255,255,0), self.rect)
        self.text_surface = base_font.render(self.name, True, (255, 255, 255))
        screen.blit(self.text_surface, (width/2-20, height/2-40))
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.camx -= 5
            self.x +=5
            self.offset[0] += 5/TILE_SIZE
           
        if keys[pygame.K_LEFT]:
            self.camx += 5
            self.x -=5
            self.offset[0] -= 5/TILE_SIZE
            
        if keys[pygame.K_UP]:
            self.camy += 5
            self.y-=5
            self.offset[1] -= 5/TILE_SIZE
            
        if keys[pygame.K_DOWN]:
            self.camy -= 5
            self.y +=5
            self.offset[1] += 5/TILE_SIZE
            
    def update(self):
        self.move()
        self.draw()
        
class Entity():
    def __init__(self,x, y,ID,pseudos,ids,entities,camx,camy):
        self.x = x
        self.y = y
        self.camx = camx
        self.camy = camy
        self.ID = ID
        self.pseudo = ""
        self.pseudos = pseudos
        self.ids = ids
        self.entities = entities
        self.delete = 1
    def draw(self):
        self.rect = Rect(self.x+self.camx,self.y+self.camy,40,40)
        pygame.draw.rect(screen, (255,0,0), self.rect)
        self.text_surface = base_font.render(self.pseudo, True, (255, 255, 255))
        screen.blit(self.text_surface, (self.x+self.camx-20, self.y-40+self.camy))
    def update(self):
        global entities
        
        
        self.draw()
        self.delete = 1
        for ID in self.ids:
            if ID == self.ID:
                self.delete = 0
        if self.delete == 1:
            index = 0
            for entity in entities:
                
                if entity.ID == self.ID:
                    del entities[index]
                index += 1
        if self.pseudo == "":
            if self.pseudos != []:
                for pseudo in self.pseudos:
                    
                    
                    if self.ID == int(pseudo[1]):
                        self.pseudo = pseudo[0]
                        print(self.pseudo)

        
      
        
                    
firstquit = 1
# Game loop.
player = Player(25,25,0,"",width/2,height/2,0,0)

def run(chats):
    global firstquit,chat,chatactive,text,lastglitter
    msgtosend = ""
    
    
    xtosend,ytosend = player.x, player.y
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            msgtosend = "quit"
            
            
            if firstquit == 1:
                firstquit = 0
            else:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                if not chatactive:
                    chat = not chat
                    
            if event.key == pygame.K_RETURN:
                
                chattosend.append(text)
                text = ""
    

        
    # Update.
    if chat == True:
        
        chatactive, text,lastglitter =chatoverlay(events,chatactive,lastglitter,text,chats,screen)

    
    
    
    # Draw.
    
    pygame.display.flip()
    fpsClock.tick(fps)
    clock.tick(60)
    return xtosend,ytosend,msgtosend



