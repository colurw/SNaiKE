## v.1 control head coordinate with keypresses
## v.2 make it loop

import keyboard
import numpy as np
import time
import os

head_xy = np.array([10,10])
dir_xy = np.array([0,0])
count = 0

stop = False
while count != 100:
    # if keyboard.is_pressed("z"):
    #     dir_xy = ([-1,0])
    # if keyboard.read_key() == "x":
    #     dir_xy = ([1,0])
    # if keyboard.read_key() == "k":
    #     dir_xy = ([0,1])
    # if keyboard.read_key() == "m":
    #     dir_xy = ([0,-1])
    # if keyboard.read_key() == "q":
    #     stop = True
    head_xy = np.add(head_xy, dir_xy)
    os.system('cls') ## windows only
    print(head_xy)
    print(dir_xy)
    print(count)
    count += 1
    

