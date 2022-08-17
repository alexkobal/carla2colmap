import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation


class C2CUtils:
    @staticmethod
    def convert_cam_pos(data): 
        """
        Converts data from carla to colmap camera position data

        Parameters
        -------
        data: ndarray of shape (N, 6) as ['x', 'y', 'z', 'pitch', 'yaw', 'roll'] columns

        Returns
        -------
        ndarray of shape (N, 7) with ['qw', 'qx', 'qy', 'qz', 'tx', 'ty', 'tz'] columns ready to use in colmap
        """
        df = pd.DataFrame(data, columns=('z', 'x', 'y', 'pitch', 'yaw', 'roll')) # xyz -> zxy world coordinate conversion
        df.loc[:, ['pitch', 'yaw', 'roll']] = -df.loc[:, ['pitch', 'yaw', 'roll']] # negate rotation
        df.y = -df.y #y axis should be inverted
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

