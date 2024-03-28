import numpy as np

# create control data array
with open("snake_c_data_1671239512", "r") as raw_data:
    raw_control = np.loadtxt(raw_data, dtype='int', delimiter=' ')

# duplicate last entry and shift all values forwards one frame
last_row = raw_control[-1]
extended = np.vstack((raw_control, last_row))
control_data = extended[1:,]
print(control_data.shape)
print()

# create screen data array
with open("snake_s_data_1671239512", "r") as raw_data:
    raw_screen = np.loadtxt(raw_data, dtype='int', delimiter=' ')
print(raw_screen.shape)

# calculate number of frames and reshape array
num_of_frames = int(len(raw_screen)/13)
print(f'{num_of_frames} frames')
screen_data = raw_screen.reshape(num_of_frames,13,13)
print(screen_data.shape)
print()

# combine both datasets
snake_data = np.arange(0,225).reshape(15,15)
for i in range(num_of_frames):
    # pad each screen frame with '1's
    frame = screen_data[i]
    new_frame = np.pad(frame, (1, 1), 'constant', constant_values=(1, 1))
    # update the relevant edge with '4's using direction data
    direction = control_data[i]
    if direction[0] == -1:
        new_frame[:,0] = 4
    if direction[0] == 1:
        new_frame[:,-1] = 4
    if direction[1] == -1:
        new_frame[0,:] = 4
    if direction[1] == 1:
        new_frame[-1,:] = 4
    # append frame to array
    snake_data = np.vstack((snake_data, new_frame))
# remove initial placeholder frame
snake_data = snake_data.reshape(num_of_frames+1, 15, 15)
snake_data = snake_data[1:]
print(snake_data.shape)

# check data
# with np.printoptions(threshold=np.inf):
#     print(snake_data)