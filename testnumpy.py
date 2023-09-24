from numpy import random

# generating a random distribution with a defined probabilty density function
myarray = random.choice([1, 2, 3, 4, 5], p = [0.9, 0.04, 0.02, 0.02, 0.02], size = [1000,1000])

print(myarray)