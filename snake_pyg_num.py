import numpy as np
import time
import os
import random 
import pygame

# define assets, trackers, rotation matrices, variables
egg_xy = np.array([random.randint(0,36), random.randint(0,36)])
head_xy = np.array([18,18])
dir_xy = np.array([0,-1])
body_xy = np.array([[18,17], [18,16], [18,15]])
body_length = 3
score = 0
key = 0
period = 0.3
capture = False
rm_ccw_90 = np.array([[0,-1], [1,0]])
rm_cw_90 = np.transpose(rm_ccw_90)
cw, ccw = 0, 0
screen = np.zeros(shape=(37,37,3), dtype=np.int8)

head_colour = (0,0,255)
body_colour = (0,255,0)
egg_colour = (255,0,0)
scale = 6

# start pygame
pygame.init()
disp = pygame.display.set_mode((37*scale, 37*scale))
pygame.display.set_caption('SNaiKE')

game_over=False
while not game_over:

    # slow down loop when shorter 
    time.sleep(period*pow(0.85,score))

    # map keypress to direction
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dir_xy = np.matmul(dir_xy, rm_ccw_90)
                ccw = 1
            elif event.key == pygame.K_RIGHT:
                dir_xy = np.matmul(dir_xy, rm_cw_90)
                cw = 1

    # if head touches egg, generate new egg
    if np.array_equal(head_xy, egg_xy):
        egg_xy = np.array([random.randint(0,36), random.randint(0,36)])
        # regenerate egg if underneath body
        for segment_xy in body_xy:
            if np.array_equal(egg_xy, segment_xy):
                egg_xy = np.array([random.randint(0,36), random.randint(0,36)])
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
    if head_xy[0] > 36:
        head_xy[0] = 0
    
    if head_xy[0] < 0:
        head_xy[0] = 36
    
    if head_xy[1] > 36:
        head_xy[1] = 0
    
    if head_xy[1] < 0:
        head_xy[1] = 36
    
    # detect head hitting body then break loop
    for segment in body_xy:
        if np.array_equal(head_xy, segment) and score > 0:
            gameover = True

    # generate new screen state as 3-channel numpy array
    os.system('cls')
    print(f"Score: ",score)
    # update egg
    screen[egg_xy[1], egg_xy[0], 0] = 255
    # update head
    screen[head_xy[1], head_xy[0], 1] = 255
    # update body
    for segment in body_xy:
        screen[segment[1], segment[0], 2] = 255

    # generate pygame screen
    disp.fill((0,0,0))
    for segment in body_xy:
        pygame.draw.rect(disp, body_colour, [segment[0]*scale, segment[1]*scale, 1*scale, 1*scale])
    pygame.draw.rect(disp, head_colour, [head_xy[0]*scale, head_xy[1]*scale, 1*scale, 1*scale])
    pygame.draw.rect(disp, egg_colour, [egg_xy[0]*scale, egg_xy[1]*scale, 1*scale, 1*scale])
    pygame.display.update()
    
pygame.quit()
quit()
print()
print("Press 'c,n' to control, 'q' to quit")

print("GAME OVER")
