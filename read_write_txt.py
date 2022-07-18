import sys
sys.path.insert(1, "/home/sandor/GIT/colmap/scripts/python")
import read_write_model as rw

model_path = "./sparse/model"
camera_path = model_path + "/cameras.bin"
images_path = model_path + "/images.bin"

rw.write_cameras_text(rw.read_cameras_binary(camera_path), model_path + "/cameras.txt")
rw.write_images_text(rw.read_images_binary(images_path), model_path + "/images.txt")