import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation
import settings as st
import os
import glob
import shutil

class C2CUtils:
    @staticmethod
    def convert_cam_pos(data): 
        """
        Converts data from carla to colmap camera position data

        Parameters
        -------
        data: ndarray (structured or homogeneous), Iterable, dict, or DataFrame (same as data in pandas.DataFrame)
            it shoud have a shape of (N, 6) as ['x', 'y', 'z', 'pitch', 'yaw', 'roll'] columns

        Returns
        -------
        ndarray of shape (N, 7) with ['qw', 'qx', 'qy', 'qz', 'tx', 'ty', 'tz'] columns ready to use in colmap
        """
        df = pd.DataFrame(data, columns=('z', 'x', 'y', 'pitch', 'yaw', 'roll')) # xyz -> zxy world coordinate conversion
        df.loc[:, ['pitch', 'yaw', 'roll']] = -df.loc[:, ['pitch', 'yaw', 'roll']] # negate rotation
        df.y = -df.y #y axes should be inverted
        ret_df = pd.DataFrame() # creating return DataFrame

        # convert from euler angles to quaternions
        euler_angles = np.array([df.pitch, df.yaw, df.roll]).transpose()
        r = Rotation.from_euler('xyz', euler_angles, degrees=True)
        
        ret_df['qx'], ret_df['qy'], ret_df['qz'], ret_df['qw'] = r.as_quat().transpose()

        # converting translation vector
        T = df.loc[:, ['x', 'y', 'z']].to_numpy()
        T = r.apply(T) # apply inverse of inverse rotation (fix carla : rotation->translation vs. colmap : translation->rotation)
        T = -T # the final translation vector needs to be negated (colmap input requirenment)

        ret_df['tx'], ret_df['ty'], ret_df['tz'] = T.transpose()

        return ret_df.loc[:, ['qw', 'qx', 'qy', 'qz', 'tx', 'ty', 'tz']].to_numpy(copy=True)

    @staticmethod
    def downsample_images():
        # Creating ./images for images
        images_dir = os.path.join(st.COLMAP_PRJ_WD, 'images')
        # Check whether the specified path exists or not
        if not os.path.exists(images_dir):
            os.mkdir(images_dir)
        # remove all files in ./images directory
        for f in os.listdir(images_dir):
            os.remove(os.path.join(images_dir, f))

        # collecting image data file names
        images = glob.glob(st.IN_IMG_PATH + '/**/semseg/**') #TODO Clarify how the folder structure will look like in the final pipeline
        images.sort()
        images = np.array(images, dtype=str)

        # check if sample number was specified
        if st.SAMPLE_NUM > 0:
            ids = np.around(np.linspace(0, images.shape[0]-1, int(round(st.SAMPLE_NUM, 0))))
            ids = ids.astype("int")
        else:
            ids = np.arange(0, len(images))

        image_names = np.arange(0, ids.shape[0])
        image_names = image_names.astype('str')
        image_names = np.char.zfill(image_names, 5)
        image_names = np.char.add(image_names, np.full((ids.shape[0]), '.png'))

        selected_images = np.dstack((images[ids], image_names))
        selected_images = np.squeeze(selected_images)

        #print(selected_images[:, :10])

        # copy sampled images to images folder
        for row in selected_images:
            shutil.copy(row[0], os.path.join(images_dir, str(row[1])))
            

    @staticmethod
    def downsample_cameras():
        # --- CAMERA --- #

        # Creating ./sparse/model/ for downsampled camera poses
        cam_model_dir = os.path.join(st.COLMAP_PRJ_WD, 'sparse/model')
        cam_model_fname = os.path.join(st.COLMAP_PRJ_WD, 'raw_images.csv')
            # Check whether the specified path exists or not
        if not os.path.exists(cam_model_dir):
            os.mkdir(cam_model_dir)
        # remove all files in ./sparse/model directory
        for f in os.listdir(cam_model_dir):
            os.remove(os.path.join(cam_model_dir, f))
        print(cam_model_dir)

        cameras = glob.glob(st.IN_CAM_PATH + '*/camera.txt')
        cameras = np.array(cameras.sort())


        mp_cams = pd.DataFrame()
        for c in cameras:
            mp_cams = pd.concat([mp_cams, pd.read_csv(c, sep=' ', names=['x', 'y', 'z', 'pitch', 'yaw', 'roll'])])




