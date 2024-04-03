import os 
import wandb
from gymnasium import spaces
from snake_gym import SnakeEnv
from wandb.integration.sb3 import WandbCallback
from stable_baselines3 import PPO
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
import torch
import torch.nn as nn


class CustomCNN(BaseFeaturesExtractor):
    """
    :param observation_space: (gym.Space)
    :param features_dim: (int) Number of features extracted.
        This corresponds to the number of unit for the last layer.
    """

    def __init__(self, observation_space: spaces.Box, features_dim: int = 256):
        super().__init__(observation_space, features_dim)
        # We assume CxHxW images (channels first)
        # Re-ordering will be done by pre-preprocessing or wrapper
        n_input_channels = observation_space.shape[0]
        self.cnn = nn.Sequential(
            nn.Conv2d(n_input_channels, 32, kernel_size=8, stride=4, padding=0),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=4, stride=2, padding=0),
            nn.ReLU(),
            nn.Flatten(),
        )

        # Compute shape by doing one forward pass
        with torch.no_grad():
            n_flatten = self.cnn(
                torch.as_tensor(observation_space.sample()[None]).float()
            ).shape[1]

        self.linear = nn.Sequential(nn.Linear(n_flatten, features_dim), nn.ReLU())

    def forward(self, observations: torch.Tensor) -> torch.Tensor:
        return self.linear(self.cnn(observations))


policy_kwargs = dict(features_extractor_class=CustomCNN,
                     features_extractor_kwargs=dict(features_dim=128))

run = wandb.init(project="snake_PPO",
                 config={"policy_type": "MlpPolicy", 
                         "total_timesteps": 25000,
                         "env_name": "snake_PPO"},
                 sync_tensorboard=True,  
                 monitor_gym=True,  
                 save_code=True,)

env = SnakeEnv()
env = Monitor(env)
env = DummyVecEnv([lambda:env])

model = PPO("CnnPolicy", env, policy_kwargs=policy_kwargs, verbose=1, tensorboard_log=f"runs/{run.id}")

callback = WandbCallback(gradient_save_freq=10,
                         model_save_path=f"models/{run.id}",
                         verbose=2,)

model.learn(total_timesteps=25000, callback=callback)

PPO_path = os.path.join('Training', 'Saved Models', 'snake_PPO_25k')
model.save(PPO_path)

evaluate_policy(model, env, n_eval_episodes=10)
run.finish()
