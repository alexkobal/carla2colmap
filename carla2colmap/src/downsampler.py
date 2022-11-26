import pandas as pd
import numpy as np
import settings as st
import os
import glob
import shutil
from util import C2CUtils

class Downsampler:
    def __init__(self):
        self.__df = pd.DataFrame()
        # Creating ./images for images
        self.__images_dir = os.path.join(st.COLMAP_PRJ_WD, 'images')
        self.__init_images_folder()
        # Creating ./sparse/model/ for downsampled camera poses if camera data is to be used
        if st.USE_CAM:
            self.__cam_model_dir = os.path.join(st.COLMAP_PRJ_WD, 'sparse/model')
            self.__cam_model_fname = os.path.join(st.COLMAP_PRJ_WD, 'raw_images.csv')
            self.__init_model_folder()
    
    def __init_images_folder(self):
        # Check whether the specified path exists or not
        if not os.path.exists(self.__images_dir):
            os.mkdir(self.__images_dir)
        # remove all files in ./images directory
        for f in os.listdir(self.__images_dir):
            os.remove(os.path.join(self.__images_dir, f))

    def __init_model_folder(self):
        # Check whether the specified path exists or not
        print("DIR:", [self.__cam_model_dir])
        if not os.path.exists(self.__cam_model_dir):
            os.makedirs(self.__cam_model_dir)
        # remove all files in ./sparse/model directory
        for f in os.listdir(self.__cam_model_dir):
            os.remove(os.path.join(self.__cam_model_dir, f))

    def __read_images(self):
        # collecting image data file names
        images = glob.glob(st.IN_IMG_PATH + '/**/'+ st.IN_IMG_FOLDER +'/**')
        if len(images) == 0: 
            raise Exception('No images found in the specified folder with the specified path')
        images.sort()
        images = np.array(images, dtype=str)
        self.__df['in_image'] = images

    def __read_cameras(self):
        cameras = glob.glob(st.IN_CAM_PATH + '/**/camera.txt')
        cameras.sort()
        cameras = np.array(cameras)
        focals = glob.glob(st.IN_CAM_PATH + '/**/focal.txt')
        focals.sort()
        focals = np.array(focals)


        cam_df = pd.DataFrame()
        for c, f in zip(cameras, focals):
            cam_file_df = pd.read_csv(c, sep=' ', names=['x', 'y', 'z', 'pitch', 'yaw', 'roll'])
            focal_f = .0
            with open(f, 'r') as fp:
                focal_f = float(fp.readline().strip())
            cam_file_df['focal'] = focal_f
            cam_df = pd.concat([cam_df, cam_file_df])


        self.__df.loc[:, ['qw', 'qx', 'qy', 'qz', 'tx', 'ty', 'tz']] = C2CUtils.convert_cam_pos(cam_df.loc[:, ['x', 'y', 'z', 'pitch', 'yaw', 'roll']].to_numpy(copy=True))
        self.__df['focal'] = cam_df['focal'].to_numpy(copy=True)


    def downsample(self, strategy='linspace'):
        # TODO: add a parameter for the sampling function. 
        self.__read_images()
        if st.USE_CAM: self.__read_cameras()

        # check if sample number was specified
        if st.SAMPLE_NUM > 0:

            ids = np.around(np.linspace(0, len(self.__df)-1, int(round(st.SAMPLE_NUM, 0))))
            ids = ids.astype("int")
        else:
            ids = np.arange(0, len(self.__df))
        selected_images = self.__df.iloc[ids].copy()

        image_names = np.arange(0, ids.shape[0])
        image_names = image_names.astype('str')
        image_names = np.char.zfill(image_names, 5)
        image_names = np.char.add(image_names, np.full((ids.shape[0]), '.png'))
        selected_images['image_name'] = image_names

        # copy sampled images to images folder
        for index, row in selected_images.iterrows():
            shutil.copy(row['in_image'], os.path.join(self.__images_dir, row['image_name']))

        return selected_images.copy()