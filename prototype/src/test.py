import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation
from carla2colmap import DataConverter

# creating empty data
n_cameras = 100
T = np.zeros((n_cameras, 3))
eR = np.zeros((n_cameras, 3))
data = np.hstack((T, eR))
df = pd.DataFrame(data, columns=('z', 'x', 'y', 'pitch', 'yaw', 'roll')) #zxy coordinate order (colmap)

#data manipulation
# translation (spiral)
a = 1
t = np.linspace(0, 6 * np.pi, n_cameras)
df.z = a*t*np.cos(t)
df.x = a*t*np.sin(t)
# angle (rotation based on the spiral)
df.yaw = np.rad2deg(t) + 90
test_input = df.loc[:, ['z', 'x', 'y', 'pitch', 'yaw', 'roll']].to_numpy(copy=True)
#filling out required data with none
df['image_id'] = np.arange(n_cameras)
df['camera_id'] = 1
df['image_name'] = 'image.png'
df.loc[:, ['qw', 'qx', 'qy', 'qz', 'tx', 'ty', 'tz']] = 0

selected = df[['image_id', 'qw', 'qx', 'qy', 'qz', 'tx', 'ty', 'tz', 'camera_id', 'image_name']].copy()

result = DataConverter.convert(test_input)
selected.loc[:, ['qw', 'qx', 'qy', 'qz', 'tx', 'ty', 'tz']] = result
selected.to_csv('./raw_images_test_framework.csv', sep=' ', header=False, index=False)





