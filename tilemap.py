from clientsocket import *


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

