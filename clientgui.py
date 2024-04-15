import sys
 
import pygame
from pygame.locals import *
from clientsocket import *
from chatoverlay import *
from variables import *
import math


width, height = 1200, 800

pygame.init()

TILE_SIZE = 60
clock = pygame.time.Clock()
base_font = pygame.font.Font(None, 32)
fps = 60
run = False



screen = pygame.display.set_mode((width, height))


def line_length(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

class Player():
    def __init__(self,x, y,ID,name,camx,camy):
        self.camx = camx-20-x
        self.camy = camy-20-y
        self.x = x
        self.y = y
        self.offset = [0,0]
        self.speed = 6
        self.ID = ID
        self.name = name
        self.change_x = 0
        self.change_y = 0
        self.rect = Rect(width/2-20,height/2-20,40,40)
        self.vx = 0
        self.vy = 0
        self.backup_x,self.backup_y = 0,0
    def draw(self):
        global width,height
        self.rect = Rect(width/2-20,height/2-20,40,40)
        pygame.draw.rect(screen, (255,255,0), self.rect)
        self.text_surface = base_font.render(self.name, True, (0, 0, 0))
        screen.blit(self.text_surface, (width/2-20, height/2-40))
    def move(self):
        self.vx,self.vy = 0,0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            self.speed = 6*0.7071
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            self.speed = 6*0.7071
        elif keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            self.speed = 6*0.7071
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            self.speed = 6*0.7071
        else:
            self.speed = 6
        self.change_x = 0
        self.change_y = 0
        if keys[pygame.K_RIGHT]:
        
            self.change_x = 1 * self.speed
            self.vx= self.speed
            self.camx -= self.speed
            self.x +=self.speed
            self.offset[0] += self.speed/TILE_SIZE
           
        if keys[pygame.K_LEFT]:
            self.change_x = -1 * self.speed
            self.vx = -self.speed
            self.camx += self.speed
            self.x -=self.speed
            self.offset[0] -= self.speed/TILE_SIZE
            
        if keys[pygame.K_UP]:
            self.change_y = -1 * self.speed
            self.vy = self.speed
            
            self.camy += self.speed
            self.y-=self.speed
            self.offset[1] -= self.speed/TILE_SIZE
            
        if keys[pygame.K_DOWN]:
            
            self.change_y = 1 * self.speed
            self.vy = -self.speed
            self.camy -= self.speed
            self.y +=self.speed
            self.offset[1] += self.speed/TILE_SIZE
    def collide_test(self,walls,direction):
        
            
        
        
        
        hits = pygame.sprite.spritecollide(self, walls, False)
        if hits:
            
                self.x -= self.change_x
                self.camx -= -self.change_x
                self.offset[0] -= self.change_x/TILE_SIZE
                 
            
            
                self.y -= self.change_y
                self.camy -= -self.change_y
                self.offset[1] -= self.change_y/TILE_SIZE
                    
                
                    
                
                
            
    def update(self,walls):
        
        
        
        self.collide_test(walls,"y")
        
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
        self.text_surface = base_font.render(self.pseudo, True, (0, 0, 0))
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

        
      
        
infos = False           
firstquit = 1
# Game loop.
player = Player(initial[0]*TILE_SIZE,initial[1]*TILE_SIZE,0,"",width/2,height/2)
def info_screen(x,y,fps,screen):
    text_surface = base_font.render("x"+str(round(x/TILE_SIZE)), True, (0, 0, 0))
    screen.blit(text_surface, (width-100, 10))
    text_surface = base_font.render("y"+str(round(y/TILE_SIZE)), True, (0, 0, 0))
    screen.blit(text_surface, (width-200, 10))
    text_surface = base_font.render("fps"+str(fps), True, (0, 0, 0))
    screen.blit(text_surface, (width-300, 10))
def run(chats):
    global firstquit,chat,chatactive,text,lastglitter,infos
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
            if event.key == pygame.K_p:
                infos = not infos
                    
            if event.key == pygame.K_RETURN:
                
                chattosend.append(text)
                text = ""
    

    if infos == True:
        info_screen(player.x,player.y,int(clock.get_fps()),screen)
    # Update.
    if chat == True:
        
        chatactive, text,lastglitter =chatoverlay(events,chatactive,lastglitter,text,chats,screen)

    
    
    
    # Draw.
    
    pygame.display.flip()
    clock.tick(60)
    return xtosend,ytosend,msgtosend,chat



