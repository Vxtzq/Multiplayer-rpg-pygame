import sys
 
import pygame
from pygame.locals import *
from clientsocket import *

 
 
pygame.init()


snowimg = pygame.image.load("ressources/snow.png")
snowimg = pygame.transform.scale(snowimg,((50,50)))
grassimg = pygame.image.load("ressources/grass.png")
grassimg = pygame.transform.scale(grassimg,((50,50)))
grass2img = pygame.image.load("ressources/grass2.png")
grass2img = pygame.transform.scale(grass2img,((50,50)))
sandimg = pygame.image.load("ressources/sand.png")
sandimg = pygame.transform.scale(sandimg,((50,50)))
waterimg = pygame.image.load("ressources/water.png")
waterimg = pygame.transform.scale(waterimg,((50,50)))
treeimg = pygame.image.load("ressources/tree.png")
treeimg = pygame.transform.scale(treeimg,((50,50)))
mountainsimg = pygame.image.load("ressources/mountains.png")
mountainsimg = pygame.transform.scale(mountainsimg,((50,50)))

base_font = pygame.font.Font(None, 32)
fps = 60
run = False
fpsClock = pygame.time.Clock()
xtosend,ytosend = 69,0
width, height = 640, 480
screen = pygame.display.set_mode((width, height))



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
        self.rect = Rect(width/2-20,height/2-20,40,40)
        pygame.draw.rect(screen, (255,255,0), self.rect)
        self.text_surface = base_font.render(self.name, True, (255, 255, 255))
        screen.blit(self.text_surface, (width/2-20, height/2-40))
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.camx -= 15
            self.x +=15
        if keys[pygame.K_LEFT]:
            self.camx += 15
            self.x -=15
        if keys[pygame.K_UP]:
            self.camy += 15
            self.y-=15
        if keys[pygame.K_DOWN]:
            self.camy -= 15
            self.y +=15
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

def generate_map(surf):
    
    
    f = open("map2.txt", 'r')
    length = 0
    for line in f:
        length = len(line)
    f.close()
    spacex = length/2*50
    spacey = length/2*50
    spacex = -spacex
    spacey = -spacey
    color = (0,0,0)
    
    f = open("map2.txt", 'r')
    for line in f:
        spacex = length/2*50
        spacex = -spacex
        
        for char in line:
            if char == "0":
                rect = grass2img.get_rect()            
                surf.blit(grass2img,(spacex,spacey))
            if char == "1":
                rect = snowimg.get_rect()            
                surf.blit(snowimg,(spacex,spacey))
            if char == "2":
                
                rect = treeimg.get_rect()
            
                surf.blit(treeimg,(spacex,spacey))
            if char == "3":
                rect = grassimg.get_rect()
            
                surf.blit(grassimg,(spacex,spacey))
            if char == "4":
                rect = sandimg.get_rect()
            
                surf.blit(sandimg,(spacex,spacey))
            if char == "5":
                rect = waterimg.get_rect()
            
                surf.blit(waterimg,(spacex,spacey))
            if char == "6":
                rect = mountainsimg.get_rect()
            
                surf.blit(mountainsimg,(spacex,spacey))
                
            
            spacex+= 50
            
        spacey += 50
    spacey = 0     
        
    f.close()
    return spacex,spacey,surf

