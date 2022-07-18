#! /usr/bin/env python3
 
# This program converts Euler angles to a quaternion.
# Author: AutomaticAddison.com
 
import numpy as np # Scientific computing library for Python
from scipy.spatial.transform import Rotation
 
def get_quaternion_from_euler(euler_angles):
  """
  Convert an Euler angle to a quaternion.
   
  Input
  roll, pitch, yaw
    :param roll: The roll (rotation around x-axis) angle in radians.
    :param pitch: The pitch (rotation around y-axis) angle in radians.
    :param yaw: The yaw (rotation around z-axis) angle in radians.
 
  Output
    :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
  """
  # yaw = np.radians(yaw)
  # pitch = np.radians(pitch)
  # roll = np.radians(roll)
  
  r = Rotation.from_euler('XYZ', euler_angles, degrees=True)
  
  
  # qx = np.cos(yaw/2) * np.cos(pitch/2) * np.cos(roll/2) + np.sin(yaw/2) * np.sin(pitch/2) * np.sin(roll/2)
  # qy = np.sin(yaw/2) * np.cos(pitch/2) * np.cos(roll/2) - np.cos(yaw/2) * np.sin(pitch/2) * np.sin(roll/2)
  # qz = np.cos(yaw/2) * np.sin(pitch/2) * np.cos(roll/2) + np.sin(yaw/2) * np.cos(pitch/2) * np.sin(roll/2)
  # qw = np.cos(yaw/2) * np.cos(pitch/2) * np.sin(roll/2) - np.sin(yaw/2) * np.sin(pitch/2) * np.cos(roll/2)
 
  return r.as_quat()