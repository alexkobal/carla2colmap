# Global variables used across modueles (mostly for storing input parameters)

def init():
    global COLMAP_PRJ_WD    # Colmap project working directory
    global IN_IMG_PATH      # Path to input images (can be structured in folders)
    global IN_IMG_FOLDER    # Folder in which the images are within the image path
    global IN_CAM_PATH      # Path to input camera poses (can be structured in folders, structure should be the same as for images)
    global SAMPLE_NUM       # Number of output image samples (0 if not provided)
    global USE_CAM       # Use camera poses for reconstruction of not (false if not provided)
