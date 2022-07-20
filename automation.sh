set -o xtrace
# command for running:
# ./automation.sh | tee output.log
colmap feature_extractor --project_path ./configs/feature_extractor.ini
colmap exhaustive_matcher --project_path ./configs/exhaustive_matcher.ini
colmap point_triangulator --project_path ./configs/point_triangulator.ini
# mkdir ./sparse
# colmap mapper --project_path ./configs/mapper.ini
mkdir ./dense
colmap image_undistorter --project_path ./configs/image_undistorter.ini
colmap patch_match_stereo --project_path ./configs/patch_match_stereo.ini
colmap stereo_fusion --project_path ./configs/stereo_fusion.ini
#colmap poisson_mesher --project_path ./configs/poisson_mesher.ini
#colmap delaunay_mesher --project_path ./configs/delaunay_mesher.ini