import os
import glob
import shutil
from matplotlib import projections
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from conversion_util import get_quaternion_from_euler
import sys
sys.path.insert(1, "/home/sandor/GIT/colmap/scripts/python")
from database import COLMAPDatabase

dir = './images'
# Check whether the specified path exists or not
if not os.path.exists(dir):
    os.mkdir(dir)
# remove all files in downsampled dir
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

mypath = './monopointcloud/'
files = glob.glob(mypath + '*/semseg/*')
cameras = glob.glob(mypath + '*/camera.txt')
files.sort()
cameras.sort()
length = len(files)

#print(ids[-1], length)

#for f in files:
#    print(f)

#for c in cameras:
#    cam_file = open(c, 'r')
#    lines = cam_file.readlines()
#    for l in lines:
#        print(l)

#for i in ids:
#    shutil.copy(files[i], dir + '/' + str(i).zfill(10) + '.jpg')
#    print("Copied", files[i])
#

# Constructiong data frames
colmap_imgs = pd.read_csv("./sparse/model/images.txt", sep=' ', comment='#', 
                          names=['image_id', 'qw', 'qx', 'qy', 'qz', 'tx', 'ty', 'tz', 'camera_id', 'name'])
#print(colmap_imgs.info())
mp_cams = pd.DataFrame()
for c in cameras:
    mp_cams = pd.concat([mp_cams, pd.read_csv(c, sep=' ', 
                                              names=['x', 'y', 'z', 'pitch', 'yaw', 'roll'])])

mp_cams['img_file'] = files
euler_angles = np.array([mp_cams.roll, mp_cams.pitch, mp_cams.yaw])
mp_cams['qx'], mp_cams['qy'], mp_cams['qz'], mp_cams['qw'] \
    = np.apply_along_axis(get_quaternion_from_euler, 0, euler_angles) 
mp_cams['camera_id'] = 1

image_names = np.arange(0, len(mp_cams))
image_names = image_names.astype('str')
image_names = np.char.zfill(image_names, 5)
image_names = np.char.add(image_names, np.full((len(mp_cams)), '.png'))
mp_cams['image_name'] = image_names

print(mp_cams.info())
print(mp_cams.head())



# Plotting 3D trajectory
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(mp_cams.x, mp_cams.y, mp_cams.z, marker='o')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.savefig("./trajectory_3d.png")

# Plotting 2D trajectory
fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(mp_cams.x, mp_cams.y, marker='o')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
plt.savefig("./trajectory.png")

# Plotting 2D trajectory
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(colmap_imgs.tx, colmap_imgs.ty, colmap_imgs.tz, marker='o')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.savefig("./trajectory_colmap.png")

result_sample_num = 32 * 16 # we have 16 folders. This would mean 16 loops each with 32 images
ids = np.around(np.linspace(0, mp_cams.shape[0]-1, int(round(result_sample_num, 0))))
ids = ids.astype("int")

# sample and write raw image data
selected = mp_cams.iloc[ids].copy()

# copy sampled images to images folder
for index, row in selected.iterrows():
    shutil.copy(row['img_file'], dir + '/' + row['image_name'])

# IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
#selected['image_id'] = np.arange(1, result_sample_num+1)

# we need the image_id to match to those in the database
db = COLMAPDatabase.connect('./database.db')
colmap_df = pd.read_sql_query("SELECT * FROM images", db)
colmap_df = colmap_df[['image_id', 'name']]

selected = selected.merge(colmap_df, how='left', left_on='image_name', right_on='name')
print(selected.head())

selected = selected[['image_id', 'qw', 'qx', 'qy', 'qz', 'x', 'y', 'z', 'camera_id', 'image_name']]
selected.to_csv('./sparse/model/raw_images.csv', sep=' ', header=False, index=False)

