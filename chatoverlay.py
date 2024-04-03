import pygame
import sys

pygame.init()

base_font = pygame.font.Font(None, 32)

show = 1

def text_box(coloraround,events,active,rect,text,last_timer,color_active,color_passive,screen):
    global show
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
                    if event.key != pygame.K_RETURN:
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
# Create the window

lastglitter = 0
chatactive= False

def chatoverlay(events,chatactive,lastglitter,text,chats,screen):
    
    #pygame.draw.rect(screen, (255,0,0), (x, y, 100, 100))
    if len(chats)> 6:
        chats.pop(0)
    
    
    # render at position stated in arguments
    
    overlay = pygame.Surface((400,300))  # the size of your rect
    overlay.set_alpha(200)                # alpha level
    overlay.fill((0,0,0))           # this fills the entire surface
    screen.blit(overlay, (0,0))
    for i in range(len(chats)):
        slot = base_font.render(chats[i], True, (255, 255, 255))
        screen.blit(slot, (10,10+i*40))
    input_rect = pygame.Rect(20, 250, 360, 32)
    chatactive, text,lastglitter = text_box((255,255,255),events,chatactive,input_rect,text,lastglitter,(120,120,120),(50,50,50),screen)
    return chatactive, text, lastglitter
    
# Game loop

