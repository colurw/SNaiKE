## v.1 control head coordinate with keypresses

import keyboard
import numpy as np

if keyboard.read_key() == "z":
    dir_xy = np.array([-1,0])
if keyboard.read_key() == "x":
    dir_xy = np.array([1,0])
if keyboard.read_key() == "k":
    dir_xy = np.array([0,1])
if keyboard.read_key() == "m":
    dir_xy = np.array([0,-1])
if keyboard.read_key() == "q":
    stop = True

origin_xy = np.array([10,10])
head_xy = np.add(origin_xy, dir_xy)
print(head_xy)

