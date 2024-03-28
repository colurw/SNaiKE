import random
import gym
from gym import spaces 
import numpy as np
from stable_baselines3.common.env_checker import check_env


class SnakeEnv(gym.Env):
    def __init__(self):
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=np.array([0]), high=np.array([1]), shape=(13,13,3), dtype=np.int8)  ## flatten shape?
        self.state = np.zeros(shape=(13,13, 3), dtype=np.int8)
        self.reward = 0
        self.egg_xy = np.array([random.randint(0,12), random.randint(0,12)])
        self.head_xy = np.array([6,6])
        self.dir_xy = np.array([0,-1])
        self.body_xy = np.array([[6, 5], [6, 4], [6, 3]])
        self.body_length = 3
        self.score = 0
        self.rm_ccw_90 = np.array([[0,-1], [1,0]])
        self.rm_cw_90 = np.transpose(self.rm_ccw_90)


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
            self.egg_xy = np.array([random.randint(0,12), random.randint(0,12)])
            # regenerate egg if underneath body
            for segment in self.body_xy:
                if np.array_equal(self.egg_xy, segment):
                    self.egg_xy = np.array([random.randint(0,12), random.randint(0,12)])
            # increase length and score
            self.body_xy = np.insert(self.body_xy, self.body_length, self.head_xy, axis=0)
            self.body_length += 1
            self.score += 1
            
        # body follows head
        self.body_xy = np.insert(self.body_xy, 0, self.head_xy, axis=0)
        self.body_xy = np.delete(self.body_xy, self.body_length, axis=0)
        
        # get next head position
        self.head_xy = np.add(self.head_xy, self.dir_xy)
        
        # wrap around board edges
        if self.head_xy[0] > 12:
            self.head_xy[0] = 0
        
        if self.head_xy[0] < 0:
            self.head_xy[0] = 12
        
        if self.head_xy[1] > 12:
            self.head_xy[1] = 0
        
        if self.head_xy[1] < 0:
            self.head_xy[1] = 12
        
        # detect head hitting body
        for segment in self.body_xy:
            if np.array_equal(self.head_xy, segment) and self.score > 0:
                done = True
            else:
                done = False

        # generate new screen state as 3-channel numpy array
        self.state = np.zeros(shape=(13,13,3), dtype=np.int8)
        self.state[self.egg_xy[1], self.egg_xy[0], 0] = 1
        self.state[self.head_xy[1], self.head_xy[0], 1] = 1
        for segment in self.body_xy:
            self.state[segment[1], segment[0], 2] = 1

        # calculate reward
        if self.score > 0: 
            self.reward = self.score 
        else: 
            self.reward = -10 

        # set placeholder for info
        info = {}

        return self.state, self.reward, done, info


    def render(self):
        """ https://gymnasium.farama.org/tutorials/gymnasium_basics/environment_creation/#sphx-glr-tutorials-gymnasium-basics-environment-creation-py """
        pass
    

    def reset(self):
        self.state = np.zeros(shape=(13,13, 3), dtype=np.int8)
        self.egg_xy = np.array([random.randint(0,12), random.randint(0,12)])
        self.head_xy = np.array([6,6])
        self.dir_xy = np.array([0,-1])
        self.body_xy = np.array([[6, 5], [6, 4], [6, 3]])
        self.body_length = 3
        self.score = 0
        self.reward = 0
        
        return self.state


if __name__ == "__main__":

    check_env(SnakeEnv())