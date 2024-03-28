# v.1 control head coordinates with keypresses
# v.2 run inside loop
# v.3 improve keypress behaviour with msvcrt
# v.4 add eggs and keep score
# v.5 wrap head coordinates at board edge
# v.6 graphic output
# v.7 add trailing body
# v.8 prevent single width u-turn, add collision detection for game over
# v.9 speed up after eating
# v.10 prevent egg from regenerating underneath body
# v.11 capture direction vector and output datastream
# v.12 rotate head direction using two keys only
# v.13 better random seed generator, integer datastream
# v.14 datastreams split to two files

import msvcrt
import numpy as np
import time
import os
import random 

# random number generator
rng = str(time.time())[:-3:-1]
random.seed(rng)

# define assets, trackers, rotation matrices
egg_xy = np.array([random.randint(0,12), random.randint(0,12)])
head_xy = np.array([6,6])
dir_xy = np.array([0,-1])
body_xy = np.array([[6, 5], [6, 4], [6, 3]])
body_length = 3
score = 0
key = 0
stop = False
period = 0.5
capture = False
rm_ccw_90 = np.array([[0,-1], [1,0]])
rm_cw_90 = np.transpose(rm_ccw_90)
cw, ccw = 0, 0

# create unique file for data capture
if capture == True:
    s_file = open(f'snake_s_data_{int(time.time())}', 'w')
    c_file = open(f'snake_c_data_{int(time.time())}', 'w')

# clear screen
os.system('cls')

while stop == False:
    # set delay in loop, higher scores give faster movement
    time.sleep(period*pow(0.85,score))
    
    # if keypress is waiting record ascii code
    if msvcrt.kbhit():  
        char = msvcrt.getch()
        key = ord(char)
    if key == 113:  # q
        stop = True
    if key == 99:   # c
        # matrix product of direction vector and 90ccw rotation matrix
        dir_xy = np.matmul(dir_xy, rm_ccw_90)
        ccw = 1
    if key == 110:  # n
        # matrix product of direction vector and 90cw rotation matrix
        dir_xy = np.matmul(dir_xy, rm_cw_90)
        cw = 1
    key = 0
    
    if capture == True:
        # capture direction vector and rotation flags and write to file
        positive_dir = np.add(dir_xy, [2,2])
        c_file.write(f"{dir_xy[0]} {dir_xy[1]} {cw} {ccw}\n")
        cw, ccw = 0, 0

    # if head touches egg, generate new egg
    if np.array_equal(head_xy, egg_xy):
        egg_xy = np.array([random.randint(0,12), random.randint(0,12)])
        # regenerate egg if underneath body
        for segment_xy in body_xy:
            if np.array_equal(egg_xy, segment_xy):
                egg_xy = np.array([random.randint(0,12), random.randint(0,12)])
        # increase length and score
        body_xy = np.insert(body_xy, body_length, head_xy, axis=0)
        body_length += 1
        score += 1
        
    # body follows head
    body_xy = np.insert(body_xy, 0, head_xy, axis=0)
    body_xy = np.delete(body_xy, body_length, axis=0)
    
    # get next head position
    head_xy = np.add(head_xy, dir_xy)
    
    # wrap around board edges
    if head_xy[0] > 12:
        head_xy[0] = 0
    
    if head_xy[0] < 0:
        head_xy[0] = 12
    
    if head_xy[1] > 12:
        head_xy[1] = 0
    
    if head_xy[1] < 0:
        head_xy[1] = 12
    
    # detect head hitting body then break loop
    for segment in body_xy:
        if np.array_equal(head_xy, segment) and score > 0:
            stop = True

    # draw 13x13 graphic output
    os.system('cls')
    print(f"Score: ",score)
    for vert in range(0, 13):
        for hor in range(0, 13):
            
            # check cursor position against asset coordinates and get relevant symbol
            if vert == head_xy[1] and hor == head_xy[0]:
                symbol = "O"
                data = "3"
            
            elif vert == egg_xy[1] and hor == egg_xy[0]:
                symbol = "e"
                data = "4"
            
            else:
                symbol = "."      
                data = "0"      
            
            for segment in body_xy:
                if vert == segment[1] and hor == segment[0]:
                    symbol = "S"
                    data = "2"
            
            # return new line after printing 13 symbols
            if hor == 12:   
                print(symbol, end='\n')
                if capture == True:
                    # write data symbol to file
                    s_file.write(f'{data}\n')
            else:
                # print next symbol in line
                print(symbol, end=' ') 
                if capture == True:
                    # write data symbol to file
                    s_file.write(f'{data} ')
    print()
    print("Press 'c,n' to control, 'q' to quit")

print("GAME OVER")
if capture == True:
    s_file.close()
    c_file.close()