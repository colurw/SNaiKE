# snake_PPO

Proximal Policy Optimisation is a state-of-the-art reinforcement learning algorithm designed to allow Q-learning methods (_ie._ where an 'intelligent' agent is released into an environment) to be applied to a neural network.  
Its main benefit (other than multi-threading many simultaneous environments) is that it permits a back-propogation of the environment's gradients through the network for each time-step.  
This speeds up the learning process when compared to gradient-free methods, such as Genetic Algorithms like <a href="https://github.com/colurw/flight_sim_GNN" title="colurw/flight_sim_GNN">flight_sim_GNN</a> - which suffer through a more randomised exploration of the environment's manifold.  

### snake_cli.py
Is an ascii version of the classic Nokia mobile game, playable using in the terminal using keyboard controls, that captures screen and keypress datastreams - intended for a supervised learning project, that was abandoned after realising that I didn't want to spend hours playing it to create the data.  Hence...

### snake_pyg_num.py
Transforms the ascii display into a RGB numpy array, and uses pygame to get keypress data and generate a display window.

### snake_gym.py
Converts the game into a Gymnasium Environment() class for use with gradient-based reinforcement learning algorithms.

### PPO.py
Initialises a convolutional neural network that learns how to use the control inputs, based on its interpretation the RGB screen array.