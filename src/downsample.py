import os
# Changing working direa
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
os.chdir('../')
print("Current working directory:\n", os.getcwd())

import glob
import shutil
from matplotlib import projections
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.insert(1, "../GIT/colmap/scripts/python")
sys.path.insert(1, "/data/colmap/scripts/python") #needed for colmap database reading
from database import COLMAPDatabase
from carla2colmap import DataConverter


dir = './images'
# Check whether the specified path exists or not
if not os.path.exists(dir):
    os.mkdir(dir)
# remove all files in downsampled dir
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

monopoint_path = './monopointcloud/'
# collecting camera and image data file names
files = glob.glob(monopoint_path + '*/semseg/*')
cameras = glob.glob(monopoint_path + '*/camera.txt')
files.sort()
cameras.sort()
length = len(files)

# Constructiong data frames
mp_cams = pd.DataFrame()
for c in cameras:
    mp_cams = pd.concat([mp_cams, pd.read_csv(c, sep=' ', 
                                              names=['x', 'y', 'z', 'pitch', 'yaw', 'roll'])])

mp_cams['img_file'] = files

mp_cams['camera_id'] = 1

image_names = np.arange(0, len(mp_cams))
image_names = image_names.astype('str')
image_names = np.char.zfill(image_names, 5)
image_names = np.char.add(image_names, np.full((len(mp_cams)), '.png'))
mp_cams['image_name'] = image_names

# Sampling
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
try:
    db = COLMAPDatabase.connect('./database.db')
    colmap_df = pd.read_sql_query("SELECT * FROM images", db)
except:
    raise Exception("Some problem with the DB")
finally:
    db.close()
colmap_df = colmap_df[['image_id', 'name']]

selected = selected.merge(colmap_df, how='left', left_on='image_name', right_on='name')

selected.loc[:, ['qw', 'qx', 'qy', 'qz', 'tx', 'ty', 'tz']] \
    = DataConverter.convert(selected.loc[:, ['x', 'y', 'z', 'pitch', 'yaw', 'roll']].to_numpy(copy=True))

# generate csv
selected = selected[['image_id', 'qw', 'qx', 'qy', 'qz', 'tx', 'ty', 'tz', 'camera_id', 'image_name']]
selected.to_csv('./sparse/model/raw_images.csv', sep=' ', header=False, index=False)


