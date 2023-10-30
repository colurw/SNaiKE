## v.1 control head coordinate with keypresses
## v.2 make it loop
## v.3 improve keypress latching behaviour with msvcrt
## v.4 add eggs and keep score 

import msvcrt
import numpy as np
import time
import os
import random 

random.seed(13)
egg_xy = np.array([random.randint(0,20), random.randint(0,20)])

head_xy = np.array([10,10])
dir_xy = np.array([0,0])

score = 0
num = 0
count = 0
stop = False
while stop == False:
    time.sleep(1)
    if msvcrt.kbhit():   # if keypress is waiting:
        char = msvcrt.getch()
        num = ord(char)
    if num == 122:       # z
        dir_xy = ([-1,0])
    if num == 120:       # x
        dir_xy = ([1,0])
    if num == 107:       # k
        dir_xy = ([0,1])
    if num == 109:       # m
        dir_xy = ([0,-1])
    if num == 113:       # q
        stop = True
    if np.array_equal(head_xy, egg_xy):
        score += 1
        egg_xy = np.array([random.randint(0,20), random.randint(0,20)])
    head_xy = np.add(head_xy, dir_xy)
    os.system('cls') ## windows only
    print(head_xy)
    print(dir_xy)
    print(egg_xy)
    print(score)
    print(count)
    print("Press 'q' to quit")
    count += 1


