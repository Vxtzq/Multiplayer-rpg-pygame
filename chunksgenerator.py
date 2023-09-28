import numpy as np


def generate_chunk(startline,startcol,chunkheight,chunkwidth):
    
    chunk = np.zeros((chunkwidth,chunkheight))
    indexline = 0
    indexchar = 0
    indexstartline = 0
    indexstartcol = 0
    f = open("map2.txt", 'r')
    for line in f:
        if indexstartline >= startline:
            if indexline < chunkheight:
                for char in line:
                    if indexstartcol >= startcol:
                        if indexchar < chunkwidth:
                            chunk[indexline,indexchar]= char
                            
                            indexchar += 1
                    else:
                        indexstartcol += 1
                indexline += 1
                indexchar = 0
        else:
            indexstartline += 1
        
        
        
        
    f.close()
    return chunk

