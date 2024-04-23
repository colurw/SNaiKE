import random
import gymnasium
from gymnasium import spaces 
import numpy as np
from stable_baselines3.common.env_checker import check_env
import math


class SnakeEnv(gymnasium.Env):
    def __init__(self, size=37):
        self.size = size
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0, high=255, shape=(3, self.size, self.size), dtype=np.uint8)  ## flatten shape?
        self.state = np.zeros(shape=(3, self.size ,self.size), dtype=np.uint8)
        self.reward = 0
        self.egg_xy = np.array([random.randint(0, self.size-1), random.randint(0, self.size-1)])
        self.head_xy = np.array([math.floor(self.size/2), math.floor(self.size/2)])
        self.dir_xy = np.array([0,-1])
        self.body_xy = np.array([[math.floor(self.size/2), math.floor(self.size/2)-1], 
                                 [math.floor(self.size/2), math.floor(self.size/2)-2], 
                                 [math.floor(self.size/2), math.floor(self.size/2)-3]])
        self.body_length = 3
        self.score = 0
        self.rm_ccw_90 = np.array([[0,-1], [1,0]])
        self.rm_cw_90 = np.transpose(self.rm_ccw_90)
        self.wrap = False


    def step(self, action):
        if action == 1:  
            # matrix product of direction vector and 90ccw rotation matrix
            self.dir_xy = np.matmul(self.dir_xy, self.rm_ccw_90)
        
        if action == 2: 
            # matrix product of direction vector and 90cw rotation matrix
            self.dir_xy = np.matmul(self.dir_xy, self.rm_cw_90)
        
        action = 0

        # if head touches egg, generate new egg
        if np.array_equal(self.head_xy, self.egg_xy):
            self.egg_xy = np.array([random.randint(0, self.size-1), random.randint(0, self.size-1)])
            # regenerate egg if underneath body
            for segment in self.body_xy:
                if np.array_equal(self.egg_xy, segment):
                    self.egg_xy = np.array([random.randint(0, self.size-1), random.randint(0, self.size-1)])
            # increase length and score
            self.body_xy = np.insert(self.body_xy, self.body_length, self.head_xy, axis=0)
            self.body_length += 1
            self.score += 1
            
        # body follows head
        self.body_xy = np.insert(self.body_xy, 0, self.head_xy, axis=0)
        self.body_xy = np.delete(self.body_xy, self.body_length, axis=0)
        
        # get next head position
        self.head_xy = np.add(self.head_xy, self.dir_xy)
        
        if self.wrap == True:
            # wrap around board edges
            if self.head_xy[0] > self.size-1:
                self.head_xy[0] = 0
            
            if self.head_xy[0] < 0:
                self.head_xy[0] = self.size-1
            
            if self.head_xy[1] > self.size-1:
                self.head_xy[1] = 0
            
            if self.head_xy[1] < 0:
                self.head_xy[1] = self.size-1
        
        else:
            # end game when head exceeds limits
            if self.head_xy[0] > self.size-1:
                self.reward = -5
                terminated = True
            
            if self.head_xy[0] < 0:
                self.reward = -5
                terminated = True
            
            if self.head_xy[1] > self.size-1:
                self.reward = -5
                terminated = True
            
            if self.head_xy[1] < 0:
                self.reward = -5
                terminated = True
        
        # detect head hitting body
        for segment in self.body_xy:
            if np.array_equal(self.head_xy, segment) and self.score > 0:
                terminated = True
            else:
                terminated = False

        # record new screen state as 3-channel numpy array (channels first)
        self.state = np.zeros(shape=(3, self.size, self.size), dtype=np.uint8)
        self.state[0, self.egg_xy[1], self.egg_xy[0]] = 255
        self.state[1, self.head_xy[1], self.head_xy[0]] = 255
        for segment in self.body_xy:
            self.state[2, segment[1], segment[0]] = 255

        # calculate reward
        if self.score > 0: 
            self.reward = self.score 
        else: 
            self.reward = -10 

        # set placeholder for info, truncated
        info = {}
        truncated = False

        return self.state, self.reward, terminated, truncated, info


    def render(self):
        """ https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/#sphx-glr-tutorials-gymnasium-basics-environment-creation-py """
        
        pass
    

    def reset(self, seed=None):
        self.seedNum = seed
        self.state = np.zeros(shape=(self.size ,self.size, 3), dtype=np.uint8)
        self.egg_xy = np.array([random.randint(0, self.size-1), random.randint(0, self.size-1)])
        self.head_xy = np.array([math.floor(self.size/2), math.floor(self.size/2)])
        self.dir_xy = np.array([0,-1])
        self.body_xy = np.array([[math.floor(self.size/2), math.floor(self.size/2)-1], 
                                 [math.floor(self.size/2), math.floor(self.size/2)-2], 
                                 [math.floor(self.size/2), math.floor(self.size/2)-3]])
        self.body_length = 3
        self.score = 0
        self.reward = 0
        info = {}
        
        return self.state, info


if __name__ == "__main__":

    check_env(SnakeEnv()) 



## calculate distance to egg to speed up learning?
## truncate - set time limit / maximum no. of frames for each rollout
## render - use pygame display
## channels first in obsv space and algo 