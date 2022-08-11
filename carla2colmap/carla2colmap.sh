# ./carla2colmap.sh -n 512 -c ../project/monopointcloud ../project ../project/monopointcloud
dir=$(dirname $0)
python3 $dir/src/main.py "$@"