## v.1 control head coordinates with keypresses
## v.2 make it loop
## v.3 improve keypress latching behaviour with msvcrt
## v.4 add eggs and keep score
## v.5 wrap head coordinates at board edge
## v.6 graphic output

import msvcrt
import numpy as np
import time
import os
import random 

## define assets and trackers
random.seed(13)
egg_xy = np.array([random.randint(0,12), random.randint(0,12)])
head_xy = np.array([6,6])
dir_xy = np.array([0,0])
score = 0
key = 0
count = 0
stop = False

while stop == False:
    ## reduce speed of while loop
    time.sleep(1)
    ## if keypress is waiting record ascii code
    if msvcrt.kbhit():  
        char = msvcrt.getch()
        key = ord(char)
    ## update direction vector
    if key == 122:       # z
        dir_xy = ([-1,0])
    if key == 120:       # x
        dir_xy = ([1,0])
    if key == 109:       # m
        dir_xy = ([0,1])
    if key == 107:       # k
        dir_xy = ([0,-1])
    if key == 113:       # q
        stop = True
    ## if head meets egg, generate new egg and add score
    if np.array_equal(head_xy, egg_xy):
        score += 1
        egg_xy = np.array([random.randint(0,12), random.randint(0,12)])
    ## update head position
    head_xy = np.add(head_xy, dir_xy)
    ## wrap around board edges
    if head_xy[0] > 12:
        head_xy[0] = 0
    if head_xy[0] < 0:
        head_xy[0] = 12
    if head_xy[1] > 12:
        head_xy[1] = 0
    if head_xy[1] < 0:
        head_xy[1] = 12
    ## display output variables
    os.system('cls') ## windows only
    # print(head_xy)
    # print(dir_xy)
    # print(egg_xy)
    print(score)
    print(count)
    print("Press 'q' to quit")
    count += 1
    ## draw 13x13 graphic output
    for vert in range(0,13):
        for hor in range(0,13):
            ## check cursor position against asset locations
            if vert == head_xy[1] and hor == head_xy[0]:
                symbol = "H"
            elif vert == egg_xy[1] and hor == egg_xy[0]:
                symbol = "e"
            else:
                symbol = "."
            ## create new line after printing 14 symbols
            if hor == 12:
                print(symbol,end='\n')
            else:
                print(symbol,end=' ')

