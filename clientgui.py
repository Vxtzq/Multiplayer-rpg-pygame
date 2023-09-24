import sys
 
import pygame
from pygame.locals import *
from clientsocket import *

 
pygame.init()
 
base_font = pygame.font.Font(None, 32)
fps = 60
run = False
fpsClock = pygame.time.Clock()
xtosend,ytosend = 69,0
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
tiles = []
camx,camy = 0,0

class Player():
    def __init__(self,x, y,ID,name,camx,camy):
        self.camx = camx
        self.camy = camy
        self.x = x
        self.y = y
        self.ID = ID
        self.name = name
    def draw(self):
        global width,height
        self.rect = Rect(width/2,height/2,40,40)
        pygame.draw.rect(screen, (255,255,0), self.rect)
        self.text_surface = base_font.render(self.name, True, (255, 255, 255))
        screen.blit(self.text_surface, (width/2, height/2-40))
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.camx -= 10
            self.x +=10
        if keys[pygame.K_LEFT]:
            self.camx += 10
            self.x -=10
        if keys[pygame.K_UP]:
            self.camy += 10
            self.y-=10
        if keys[pygame.K_DOWN]:
            self.camy -= 10
            self.y +=10
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
        screen.blit(self.text_surface, (self.x+self.camx, self.y-40+self.camy))
    def update(self):
        global entities, camx,camy
        
        self.camx = camx
        self.camy = camy
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
player = Player(0,0,0,"",width/2,height/2)
def run():
    global firstquit
    msgtosend = ""
    
    
    xtosend,ytosend = player.x, player.y
    for event in pygame.event.get():
        if event.type == QUIT:
            msgtosend = "quit"
            
            
            if firstquit == 1:
                firstquit = 0
            else:
                pygame.quit()
                sys.exit()
    

    
    # Update.
    
    
    
    
    # Draw.
    
    pygame.display.flip()
    fpsClock.tick(fps)
    return xtosend,ytosend,msgtosend

