import settings as st
st.init()

import argparse
import os
from util import C2CUtils
from downsampler import Downsampler
import pycolmap


parser = argparse.ArgumentParser(prog='carla2colmap',usage='%(prog)s [options] <colmap working directory path> <input images path>',\
                    description='Make input data from carla suitable for colmap reconstruction')
parser.add_argument('work_dir', action='store', type=str)
parser.add_argument('img_input', action='store', type=str)
parser.add_argument('-n', action='store', type=int)
parser.add_argument('-c', action='store', type=str)

args = parser.parse_args()

st.COLMAP_PRJ_WD = args.work_dir
st.IN_IMG_PATH = args.img_input
st.IN_CAM_PATH = args.c if args.c is not None else ''
st.USE_CAM = args.c is not None
st.SAMPLE_NUM = args.n if args.n is not None else -1


if not os.path.isdir(st.COLMAP_PRJ_WD):
    raise Exception('The WD path specified does not exist')
else:
    st.COLMAP_PRJ_WD = os.path.abspath(st.COLMAP_PRJ_WD)

if not os.path.isdir(st.IN_IMG_PATH):
    raise Exception('The input image path specified does not exist')
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
print(downsampled_df.info())

# Creating database
database_path = os.path.join(st.COLMAP_PRJ_WD, 'database.db')
images_path = os.path.join(st.COLMAP_PRJ_WD, 'images')
os.remove(database_path)
pycolmap.extract_features(database_path, images_path)