import settings as st
st.init()

import argparse
import os
from util import C2CUtils
from downsampler import Downsampler
import pycolmap
from database import COLMAPDatabase, blob_to_array
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(prog='carla2colmap',usage='%(prog)s [options] <colmap working directory path> <input images path>',\
                    description='Make input data from carla suitable for colmap reconstruction')
parser.add_argument('work_dir', action='store', type=str)
parser.add_argument('img_input', action='store', type=str)
parser.add_argument('-n', action='store', type=int)
parser.add_argument('-c', action='store', type=str)

args = parser.parse_args()

st.COLMAP_PRJ_WD = args.work_dir.strip()
st.IN_IMG_PATH = args.img_input.strip()
st.IN_CAM_PATH = args.c.strip() if args.c is not None else ''
st.USE_CAM = args.c is not None
st.SAMPLE_NUM = args.n if args.n is not None else -1

if not os.path.isdir(st.COLMAP_PRJ_WD):
    raise Exception('The WD path specified does not exist ' + str(st.COLMAP_PRJ_WD))
else:
    st.COLMAP_PRJ_WD = os.path.abspath(st.COLMAP_PRJ_WD)

if not os.path.isdir(st.IN_IMG_PATH):
    raise Exception('The input image path specified does not exist ' + str(st.IN_IMG_PATH))
else:
    st.IN_IMG_PATH = os.path.abspath(st.IN_IMG_PATH)

if st.USE_CAM and not os.path.isdir(st.IN_CAM_PATH):
    print('The input camera path specified does not exist. Camera poses will not be used')
    st.USE_CAM = False
elif st.USE_CAM:
    st.IN_CAM_PATH = os.path.abspath(st.IN_CAM_PATH)

def print_settings():
    print('########## CONFIG ###########')
    print('COLMAP_PRJ_WD:', st.COLMAP_PRJ_WD)
    print('IN_IMG_PATH:', st.IN_IMG_PATH)
    print('IN_CAM_PATH:', st.IN_CAM_PATH)
    print('USE_CAM:', st.USE_CAM)
    print('SAMPLE_NUM:', st.SAMPLE_NUM)
    print('#############################')

print_settings()

# Downsampling images and extracting camera poses if camera info is provided
downsampler = Downsampler()
downsampled_df = downsampler.downsample()

# Creating database
database_path = os.path.join(st.COLMAP_PRJ_WD, 'database.db')
images_path = os.path.join(st.COLMAP_PRJ_WD, 'images')
 # if os.path.exists(database_path):
 #     os.remove(database_path)
 # pycolmap.extract_features(database_path, images_path)

if st.USE_CAM:
    # Desired Output format
    # IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME

    # we need the image_id to match to those in the database
    try:
        db = COLMAPDatabase.connect(database_path)
        images_df = pd.read_sql_query('SELECT * FROM images', db)
        cameras_df = pd.read_sql_query('SELECT * FROM cameras', db)
    except:
        raise Exception('Some problem with the DB')
    finally:
        db.close()
    
    # Creating model files
    # images.txt
    images_df = images_df[['image_id', 'camera_id', 'name']]
    downsampled_df = downsampled_df.merge(images_df, how='left', left_on='image_name', right_on='name')
    downsampled_df = downsampled_df[['image_id', 'qw', 'qx', 'qy', 'qz', 'tx', 'ty', 'tz', 'camera_id', 'image_name']]
    raw_images_path = os.path.join(st.COLMAP_PRJ_WD, 'sparse/model/raw_images.csv')
    downsampled_df.to_csv(raw_images_path, sep=' ', header=False, index=False)
    with open(raw_images_path, 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('\n', '\n\n')
    with open(os.path.join(st.COLMAP_PRJ_WD, 'sparse/model/images.txt'), 'w') as file:
        file.write(filedata)
    if os.path.exists(raw_images_path):
        os.remove(raw_images_path)

    # cameras.txt
    cameras_df = cameras_df[['camera_id', 'model', 'width', 'height', 'params']]
    cameras_df.params = cameras_df.params.apply(lambda x: blob_to_array(x, np.float64))
    params = np.stack(cameras_df.params.to_numpy())
    for i in range(params.shape[1]):
        cameras_df['param_' + str(i)] = params[:, i]
    cameras_df.drop('params', axis=1, inplace=True)
    cameras_df.to_csv(os.path.join(st.COLMAP_PRJ_WD, 'sparse/model/cameras.txt'), sep=' ', header=False, index=False)

    # points3D.txt
    open(os.path.join(st.COLMAP_PRJ_WD, 'sparse/model/points3D.txt'), 'w').close()