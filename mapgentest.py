#Imports
import numpy as np
import matplotlib.pyplot as plt
import math
import cv2
import time

# Generate random map
def generate ( map_size = 10, start_point = 0, extra_layers=[] ):
    
    size = 2**map_size
    
    # Choose what layers you want
    _ranges = list(range(start_point,map_size))
    _ranges.extend(extra_layers)
    
    # The output map
    a = np.zeros((size,size))
    
    # Compute layers
    for layer in _ranges:
        l = 2**layer
        rand = np.random.rand(l,l) /l
        a += cv2.resize( rand, (size,size) )   
        
    # Return
    return (a-a.min())/(a.max()-a.min())
def select (a, v, r):
    _r = np.logical_and(a > (v-r), a < (v+r))
    a[_r] = 0
    a[a < (v-r)] *= 0.8
    return a



# Output
def show(a):
    plt.figure(figsize = (10,10))
    plt.imshow(a)
    plt.show()

# Apply some borders
_ = generate( map_size=7, start_point=3 )
_ = select(_,0.4, 0.01)
_ = select(_,0.2, 0.01)
_ = select(_,0.8, 0.01)

show( _ )
_ = _*10

f = open("map2.txt", 'w')
buffer = ""
for line in _:
    for val in line:
        buffer = buffer + str(round(val)).replace(".","")
    f.write(buffer+ "\n")
    buffer = ""
f.close()
print(_)