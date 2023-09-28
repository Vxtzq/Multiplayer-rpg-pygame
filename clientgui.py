import sys
 
import pygame
from pygame.locals import *
from clientsocket import *
import random
import numpy as np

width, height = 1200, 800

pygame.init()

imgs = []
imgsjunction = []
grasses = []
dirts = []
dirtimg = pygame.image.load("ressources/snow.png")
dirtimg = pygame.transform.scale(dirtimg,((50,50)))
dirt2img = pygame.image.load("ressources/dirt2.png")
dirt2img = pygame.transform.scale(dirt2img,((50,50)))
dirts.append(dirtimg)
dirts.append(dirt2img)
imgs.append(("1",dirts))
grassimg = pygame.image.load("ressources/grass.png")
grassimg = pygame.transform.scale(grassimg,((50,50)))

grass2img = pygame.image.load("ressources/grass2.png")
grass2img = pygame.transform.scale(grass2img,((50,50)))
grass3img = pygame.image.load("ressources/grass3.png")
grass3img = pygame.transform.scale(grass3img,((50,50)))
grass4img = pygame.image.load("ressources/grass4.png")
grass4img = pygame.transform.scale(grass4img,((50,50)))
grasses.append(grassimg)
grasses.append(grass2img)
grasses.append(grass3img)
grasses.append(grass4img)
imgs.append(("0",grasses))
imgs.append(("3",grasses))
sands = []
sandimg = pygame.image.load("ressources/sand.png")
sandimg = pygame.transform.scale(sandimg,((50,50)))
sand2img = pygame.image.load("ressources/sand2.png")
sand2img = pygame.transform.scale(sand2img,((50,50)))
sands.append(sandimg)
sands.append(sand2img)
imgs.append(("4",sands))
waterimg = pygame.image.load("ressources/water.png")
waterimg = pygame.transform.scale(waterimg,((50,50)))
imgs.append(("5",waterimg))
treeimg = pygame.image.load("ressources/tree.png")
treeimg = pygame.transform.scale(treeimg,((50,50)))
imgs.append(("2",treeimg))
mountainsimg = pygame.image.load("ressources/tree2.png")
mountainsimg = pygame.transform.scale(mountainsimg,((50,50)))
imgs.append(("6",mountainsimg))

base_font = pygame.font.Font(None, 32)
fps = 60
run = False
fpsClock = pygame.time.Clock()
xtosend,ytosend = 69,0

screen = pygame.display.set_mode((width, height))



class Player():
    def __init__(self,x, y,ID,name,camx,camy,relx,rely):
        self.camx = camx
        self.camy = camy
        self.x = x
        self.y = y
        self.relx = relx
        self.rely = rely
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
            self.relx +=5
        if keys[pygame.K_LEFT]:
            self.camx += 5
            self.x -=5
            self.relx -=5
        if keys[pygame.K_UP]:
            self.camy += 5
            self.y-=5
            self.rely -=5
        if keys[pygame.K_DOWN]:
            self.camy -= 5
            self.y +=5
            self.rely +=5
    def update(self):
        self.move()
        self.draw()
        if self.relx > 100*50:
            self.relx = 0
        if self.relx < 0:
            self.relx = 100*50
        if self.rely > 100*50:
            self.rely = 0
        if self.rely < 0:
             self.rely = 100*50
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
player = Player(0,0,0,"",width/2,height/2,0,0)
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

def generate_map(chunk):
    global imgs, imgsjunction
    
    
    length = 100
    print(np.shape(chunk))
    spacex = length/2*50
    spacey = length/2*50
    spacex = -spacex
    spacey = -spacey
    color = (0,0,0)
    backupchar = ""
    surf = pygame.Surface((100*50, 100*50))
    backgroundwidth = surf.get_width()
    backgroundheight = surf.get_height()
    #f = open("map2.txt", 'r')
    f = chunk
    for line in f:
        spacex = length/2*50
        spacex = -spacex
        
        for char in line:
            char = int(char)
            for name in imgs:
                if name[0] == str(char):
                    if str(char) != "3" and str(char) != "0" and str(char) != "4"and str(char) != "1":
                        img = name[1]
                        
                        rect = img.get_rect()            
                        surf.blit(img,(spacex,spacey))
                    else:
                        img = random.choice(name[1])
                        rect = img.get_rect()            
                        surf.blit(img,(spacex,spacey))
            if backupchar != str(char):
                if backupchar == "4":
                    if str(char) == "5":
                        char = "0"
                        for name in imgsjunction:
                            if name[0] == str(char):
                                img = name[1]
                                rect = img.get_rect()            
                                surf.blit(img,(spacex,spacey))
            
            backupchar = str(char)
            
            spacex+= 50
            
        spacey += 50
    spacey = 0     
        
    #f.close()
    return spacex,spacey,surf

