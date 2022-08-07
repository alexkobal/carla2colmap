# command for running:
# ./automation.sh | tee output.log
# !!! DON'T FORGET TO USE LF LINE ENDINGS, OR THE SCRIPT WILL NOT RECOGNISE THE PATHS !!!
# CONFIG #
PRJ_WD=/home/sandor/GIT/carla2colmap/project
IN_IMG=/home/sandor/GIT/carla2colmap/monopointcloud
IN_CAM=/home/sandor/GIT/carla2colmap/monopointcloud
CONFIGS=/home/sandor/GIT/carla2colmap/configs
SAMP_NUM=512
./carla2colmap/carla2colmap.sh -n $SAMP_NUM -c $IN_CAM $PRJ_WD $IN_IMG
#colmap feature_extractor --project_path ./configs/feature_extractor.ini # already in the previous step
colmap exhaustive_matcher --project_path ./configs/exhaustive_matcher.ini --database_path $PRJ_WD/database.db 
colmap point_triangulator --project_path ./configs/point_triangulator.ini --database_path $PRJ_WD/database.db \
                            --image_path $PRJ_WD/images --input_path $PRJ_WD/sparse/model --output_path $PRJ_WD/sparse
# mkdir ./sparse # if camera poses are available, this will already exist
# colmap mapper --project_path ./configs/mapper.ini # needed only when camera poses are unknown
mkdir ./dense
colmap image_undistorter --project_path ./configs/image_undistorter.ini --image_path $PRJ_WD/images \
--input_path $PRJ_WD/sparse --output_path $PRJ_WD/dense
colmap patch_match_stereo --project_path ./configs/patch_match_stereo.ini --workspace_path $PRJ_WD/dense
colmap stereo_fusion --project_path ./configs/stereo_fusion.ini --workspace_path $PRJ_WD/dense
#colmap poisson_mesher --project_path ./configs/poisson_mesher.ini
#colmap delaunay_mesher --project_path ./configs/delaunay_mesher.ini