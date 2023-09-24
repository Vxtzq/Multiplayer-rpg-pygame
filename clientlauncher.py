# import sys module
import pygame
import sys
from clientsocket import *
from tilemap import *
  
camx,camy = 0,0
launcherend = True
# pygame.init() will initialize all
# imported module
pygame.init()
  
clock = pygame.time.Clock()

# it will display on screen
screen = pygame.display.set_mode([width, height])
  
# basic font for user typed
base_font = pygame.font.Font(None, 32)
little_font = pygame.font.Font(None, 24)
username_text = ''
password_text = ''
  
# create rectangle
input_rect = pygame.Rect(175, 100, 250, 32)
input_rectpassword = pygame.Rect(175, 200, 250, 32)

buttonrect = pygame.Rect(230, 350, 150, 45)
buttonrect2 = pygame.Rect(100, 270, 300, 32)
buttonrect3 = pygame.Rect(230, 350, 100, 45)
# color_active stores color(lightskyblue3) which
# gets active when input box is clicked by user
color_active = pygame.Color('lightskyblue3')
black = pygame.Color('black')
color1 = pygame.Color('lightskyblue2')
color2 = pygame.Color('chartreuse3')
color3 = (0,125,0)
white = (255,255,255)
success = True
register = 1
# color_passive store color(chartreuse4) which is
# color of input box.
color_passive = pygame.Color('chartreuse4')
color = color_passive
useractive= False
passwordactive = False
login = False
buttontext = "login"
buttonchangetext = ""

client = None
lastglitter = 0
show = 1

def generate_map():
    global tiles
    
    f = open("map2.txt", 'r')
    length = 0
    for line in f:
        length = len(line)
    f.close()
    spacex = length/2*40
    spacey = length/2*40
    spacex = -spacex
    spacey = -spacey
    
    f = open("map2.txt", 'r')
    for line in f:
        spacex = length/2*40
        spacex = -spacex
        print("line")
        for char in line:
            tile = Tile(spacex,spacey,0,0,str(char))
            tiles.append(tile)
            spacex+= 40
            print("char")
        spacey += 40
    spacey = 0     
        
    f.close()

def text_box(coloraround,events,active,rect,text,last_timer):
    global color_active,color_passive,show
    mycolor = None
    for event in events:
  
      # if user types QUIT then the screen will close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
  
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                active = True
            else:
                active = False
        if active == True:
                
            if event.type == pygame.KEYDOWN:
      
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
      
                    # get text input from 0 to -1 i.e. end.
                    text = text[:-1]
      
                # Unicode standard is used for string
                # formation
                else:
                    text += event.unicode
    if active:
        mycolor = color_active
    else:
        mycolor = color_passive
    pygame.draw.rect(screen, mycolor, rect)
    pygame.draw.rect(screen, coloraround, rect,3)
    # it will set background color of screen
    text_surface = base_font.render(text, True, (255, 255, 255))
    textrect = text_surface.get_rect()
    # render at position stated in arguments
    screen.blit(text_surface, (rect.x+5, rect.y+5))
    
    
    if active:
        
        now = pygame.time.get_ticks()
        if now - last_timer >= 500:
            show = -show
            last_timer = now
            
           
        # render at position stated in arguments
        if show== 1:
            
            cursor_surface = base_font.render("|", True, (255, 255, 255))
            screen.blit(cursor_surface, (rect.x+textrect.width+5, rect.y+5))
        else:
            pass
    
          
    # draw rectangle and argument passed which should
    # be on screen
    
    
    if textrect.width >= rect.width-10:
        text = text[0:-1] 
    
    # set width of textfield so that text cannot get
    # outside of user's text input
    
    return active, text,last_timer

class Tile():
    def __init__(self,x, y,camx,camy,name):
        self.x = x
        self.y = y
        self.camx = camx
        self.camy = camy
        self.name =  name
        self.transmit = 0
        self.color = (0,0,200)
        if name == "0":
            self.color = (0,120,0)
        if name == "1":
            self.color = (0,200,0)
        if name == "2":
            self.color = (101,67,33)
        if name == "3":
            self.color = (0,120,0)
        if name == "4":
            self.color = (200,200,0)
        if name == "5":
            (100,100,255)
        
    def draw(self):
        self.rect = Rect(self.x+self.camx,self.y+self.camy,40,40)
        pygame.draw.rect(screen, self.color, self.rect)
        
    def update(self):
        global camx,camy
        self.camx = camx
        self.camy = camy
        self.draw()  

def button(success,rect,coloractive,colorpassive,coloraround,text,textcolor,font=base_font,new=None):
    global register,client
    
    for event in events:
  
      # if user types QUIT then the screen will close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
  
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                if new == "new":
                    
                    if register == 1:
                        success,client = newplayer(username_text,password_text,"r")
                    else:
                        success,client = newplayer(username_text,password_text,"l")
                elif new == "play":
                    success = "play"
                else:
                    if register == 1:
                        register = -1
                    else:
                        register = 1
                            
    x,y = pygame.mouse.get_pos()
    mousepos = (x,y)
    if rect.collidepoint(mousepos):
        pygame.draw.rect(screen, coloractive, rect)
    else:
        pygame.draw.rect(screen, colorpassive, rect)
        pygame.draw.rect(screen, coloraround, rect,5)
    text_surface = font.render(text, True, textcolor)
    textrect = text_surface.get_rect()
    # render at position stated in arguments
    screen.blit(text_surface, (rect.x+45, rect.y+10))
    return success,client

launcher = True
while launcher:
    screen.fill((255, 255, 255))
        # display.flip() will update only a portion of the
    # screen to updated, not full area
    events = pygame.event.get()
    for event in events:
  
      # if user types QUIT then the screen will close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    username_surface = base_font.render("username :", True, (0,0,0))
    # render at position stated in arguments
    screen.blit(username_surface, (200, 60))
    if success != None:
        if success == "invalid":
            error_surface = little_font.render("Invalid username or password", True, (200,0,0))
            # render at position stated in arguments
            screen.blit(error_surface, (200, 250))
        if success == "quit":
            launcher = False
        if success == "internal":
            error_surface = little_font.render("An internal error occured, try again.", True, (200,0,0))
            # render at position stated in arguments
            screen.blit(error_surface, (200, 250))
        if success == "notfound":
            error_surface = little_font.render("No server found", True, (200,0,0))
            # render at position stated in arguments
            screen.blit(error_surface, (200, 250))
        if success == True:
            pass
        else:
            
            error_surface = little_font.render(str(success), True, (200,0,0))
            # render at position stated in arguments
            screen.blit(error_surface, (200, 250))
            if success == "loginvalid":
                
                connected = True
                launcher = False
     
    password_surface = base_font.render("password :", True, (0,0,0))
    # render at position stated in arguments
    screen.blit(password_surface, (200, 160))
    
    passwordactive, password_text,lastglitter = text_box(black,events,passwordactive,input_rectpassword,password_text,lastglitter)
    if register == 1:
        buttontext = "register"
        buttonchangetext = "Already have an account ? Login"
    else:
        buttontext = "login"
        buttonchangetext = "Don't have an account ? Register"
    useractive, username_text,lastglitter = text_box(black,events,useractive,input_rect,username_text,lastglitter)
    success,client = button(success,buttonrect,color1,color3,color2,buttontext,white,new="new")
    login = button(login,buttonrect2,white,white,white,buttonchangetext,black,font=little_font)
 
    pygame.display.flip()
    
    
    
    # clock.tick(60) means that for every second at most
    # 60 frames should be passed.
    clock.tick(60)
nouse = None    
while launcherend:

    screen.fill((255, 255, 255))
    # display.flip() will update only a portion of the
    # screen to updated, not full area
    events = pygame.event.get()
    for event in events:
  
      # if user types QUIT then the screen will close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    text_surface = base_font.render("Login successful", True, (0,0,0))
    # render at position stated in arguments
    screen.blit(text_surface, (200, 150))
    success,nouse = button(success,buttonrect3,color1,color3,color2,"Play",white,new="play")
    if success == "play":
        launcherend = False
    pygame.display.flip()
pseudosent = 0
entities = []
pseudos = []
idsbackup = []
change = 0
entitychange = 0
entitiesbackup = []

generate_map()
while True:
    
    
    camx = player.camx
    camy = player.camy
    tiletransmitter = tiles[0]
    tiletransmitter.camx = camx
    tiletransmitter.camy = camy
    tiletransmitter.transmit = 1
    
    for entity in entities:        
        if pseudos != entity.pseudos:
            entity.pseudos = pseudos
    if change == 1:
        for entity in entities:
            entity.ids = ids
        change = 0
    if entitychange == 1:
         for entity in entities:
            entity.entities = entities
         entitychange = 0
    print(pseudos)
    if player.name == "":
        for pseudo in pseudos:
            if pseudo[1] == player.ID:
                player.name = pseudo[0]
        
        
    if pseudosent == 0:
        msg = "p"+username_text
        client.send(msg.encode(FORMAT))
        pseudosent = 1
    else:
        pass
    xtosend, ytosend, msgtosend = run()
    msg = 'c' + str([xtosend,ytosend])
    screen.fill((0, 0, 0))
#    
    if msgtosend == "":
        client.send(msg.encode(FORMAT))
    else:
        client.send("quit".encode(FORMAT))
    

    if msg == "quit":
        connected = False
    else:
        msg = client.recv(SIZE).decode(FORMAT)
        if msg[0] != "f":
            if msg[0] != "p":
                res = ast.literal_eval(msg)
                
                counter = 0
                ids = []
                idsreceived = []
                
                            
                for clientpos in res:
                    pos = clientpos
                    clientid = pos[0]
                    clientxy = ast.literal_eval(pos[1])
                    ids.append(clientid)
                    index = 0
                    dontadd = 0
                    if idsbackup != ids:
                        idsbackup = ids
                        change = 1
                    for entity in entities:
                        if entity.ID == clientid:
                            entity.x = clientxy[0]
                            entity.y = clientxy[1]
                            index += 1
                            dontadd = 1
                    
                    if dontadd == 0:
                        if clientid != globalid:
                            entity = Entity(clientxy[0],clientxy[1],clientid,pseudos,ids,entities,0,0)
                            entities.append(entity)
                            msg = "p"+username_text
                            client.send(msg.encode(FORMAT))
            else:
                
                msg = msg.replace("pseudos","")
                test = ast.literal_eval(msg.replace("pseudos",""))
                pseudos = test
                                   
        else:
            globalid = int(msg.replace("first",""))
            player.ID = globalid
            #print("global" +str(globalid))
    for tile in tiles:
        #print("test")
        tile.update()
    for entity in entities:
        #print("test")
        entity.update()
    
    player.update()
    if entities != entitiesbackup:
        entitychange = 1
    entitiesbackup = entities
    clock.tick(60)
    print(clock.get_fps())
    
    pygame.display.flip()
    
    
    #print(f"[SERVER] {msgtosend}")
pygame.quit()