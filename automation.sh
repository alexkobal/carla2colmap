#!/bin/bash

# command for running:
# ./automation.sh | tee output.log
# !!! DON'T FORGET TO USE LF LINE ENDINGS, OR THE SCRIPT WILL NOT RECOGNISE THE PATHS !!!
# CONFIG #


# Disable config as it will be handled in the maing script
# PRJ_WD=/home/sandor/GIT/carla2colmap/project
# IN_IMG=/home/sandor/GIT/carla2colmap/monopointcloud/08_15
# IN_IMG_FOLDER=rgb
# IN_CAM=/home/sandor/GIT/carla2colmap/monopointcloud/08_15
# CONFIGS=/home/sandor/GIT/carla2colmap/configs
# SAMP_NUM=128

CURRENT_DIR=$PWD
mkdir -p $PRJ_WD
./carla2colmap/carla2colmap.sh -n $SAMP_NUM -c $IN_CAM -i $IN_IMG_FOLDER $PRJ_WD $IN_IMG
cd $PRJ_WD
# colmap feature_extractor --project_path $CONFIGS/feature_extractor.ini # already in the previous step
colmap exhaustive_matcher --project_path $CONFIGS/exhaustive_matcher.ini
colmap point_triangulator --project_path $CONFIGS/point_triangulator.ini
# colmap bundle_adjuster --project_path $CONFIGS/bundle_adjuster.ini
# mkdir ./sparse # if camera poses are available, this will already exist
# colmap mapper --project_path $CONFIGS/mapper.ini # needed only when camera poses are unknown
mkdir -p $PRJ_WD/dense
colmap image_undistorter --project_path $CONFIGS/image_undistorter.ini
colmap patch_match_stereo --project_path $CONFIGS/patch_match_stereo.ini
colmap stereo_fusion --project_path $CONFIGS/stereo_fusion.ini
# colmap poisson_mesher --project_path $CONFIGS/poisson_mesher.ini
# colmap delaunay_mesher --project_path $CONFIGS/delaunay_mesher.ini

cd $CURRENT_DIR
