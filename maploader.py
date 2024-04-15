import pygame
from sys import exit
import threading
import random
from variables import *
from pygame.locals import *

# Initialize Pygame


# Set the dimensions of the screen

  

TILE_SIZE = 60
map_data = None
finished = 0
# Load the map

def load_tiles(name,count,imagelist):
    for i in range(count):
        img = pygame.image.load("assets/"+name+str(i+1)+".png").convert()
        
        imagelist.append(img)

def load_map(path):
    # Load map data from file
    with open(path) as f:
        map_data = [line.strip().lower() for line in f]
    #print(map_data)
    print("map data loaded")
    
    
    return map_data

    

def render_tiles(map_data, WIDTH, HEIGHT, player_pos, cam_offset,screen):
    global initial
    visible_tiles = []
    
    # Extract player's position
    player_tile_x, player_tile_y = [initial[0]+ 31,initial[1]+20]
    
    # Calculate the visible area based on player's position, camera offset, and screen size
    start_x = max(player_tile_x - (WIDTH // TILE_SIZE) // 2, 0)
    start_y = max(player_tile_y - (HEIGHT // TILE_SIZE) // 2, 0)
    end_x = min(start_x + (WIDTH // TILE_SIZE), len(map_data[0]))
    end_y = min(start_y + (HEIGHT // TILE_SIZE), len(map_data))
    
    # Apply camera offset
    start_x += cam_offset[0]
    start_y += cam_offset[1]
    end_x += cam_offset[0]
    end_y += cam_offset[1]
    
    # Render tiles within the visible area
    for y in range(int(start_y), int(end_y)+2):
        for x in range(int(start_x), int(end_x)+1):
            # Check if the tile indices are within bounds
            if 0 <= y < len(map_data) and 0 <= x < len(map_data[0]):
                tile = map_data[y][x]
                tile_pos = ((x - start_x) * TILE_SIZE-0.1, (y - start_y) * TILE_SIZE-0.1)
                visible_tiles.append((tile, tile_pos))
    
    return visible_tiles

# Render tiles
# Render tiles
class Tile():
    def __init__(self,color,x,y,screen):
        self.x = x
        self.y = y
        self.color = color
         
        pygame.draw.rect(screen, self.color, (self.x, self.y, TILE_SIZE, TILE_SIZE))
class Wall(pygame.sprite.Sprite):
    def __init__(self,color,x,y,screen):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.rect = Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, self.color, (self.x, self.y, TILE_SIZE, TILE_SIZE))

class Goal(pygame.sprite.Sprite):
    def __init__(self,color,x,y,screen,team):
        super().__init__()
        self.x = x
        self.y = y
        self.team = team
        self.color = color
        self.rect = Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, self.color, (self.x, self.y, TILE_SIZE, TILE_SIZE))
            
    
        
        


# Main loop

def drawbg(watercostume,WIDTH,HEIGHT,screen,player_pos,cam_offset,map_data):
    global walls
    TILE_SIZE = 60
    # Load map data
    walls = []
    goals = []
    
    
        
    
    #print("Map loaded successfully:", map_data)
    visible_tiles = render_tiles(map_data,WIDTH,HEIGHT,player_pos,cam_offset,screen)
        
    for tile, pos in visible_tiles:
        if tile == "1":
            t = Tile((255, 255, 255), int(pos[0]), int(pos[1]),screen)
            #pygame.draw.rect(screen, (255, 255, 255), (int(pos[0]), int(pos[1]), TILE_SIZE, TILE_SIZE))
        if tile == "2":
            w = Wall((0, 0, 0), int(pos[0]), int(pos[1]),screen)
            walls.append(w)
            
        if tile == "3":
            t = Tile((200, 200, 200), int(pos[0]), int(pos[1]),screen)
        if tile == "4":
            g = Goal((200, 100, 100), int(pos[0]), int(pos[1]),screen,"red")
            goals.append(g)
        if tile == "5":
            g = Goal((100, 100, 200), int(pos[0]), int(pos[1]),screen,"blue")
            goals.append(g)
            
            
    return walls,goals
# Player's initial position
    
    

    

        
        
    
