from clientlauncher import *


def generate_map(surf):
    
    
    f = open("map2.txt", 'r')
    length = 0
    for line in f:
        length = len(line)
    f.close()
    spacex = length/2*40
    spacey = length/2*40
    spacex = -spacex
    spacey = -spacey
    color = (0,0,0)
    
    f = open("map2.txt", 'r')
    for line in f:
        spacex = length/2*40
        spacex = -spacex
        print("line")
        for char in line:
            if char == "0":
                color = (0,120,0)
            if char == "1":
                color = (0,200,0)
            if char == "2":
                color = (101,67,33)
            if char == "3":
                color = (0,120,0)
            if char == "4":
                color = (200,200,0)
            if char == "5":
                color =(100,100,255)
            rect = Rect(spacex,spacey,40,40)
            
            pygame.draw.rect(surf, color, rect)
            spacex+= 40
            print("char")
        spacey += 40
    spacey = 0     
        
    f.close()
    return spacex,spacey,surf


