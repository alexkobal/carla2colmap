import os
import subprocess
import pandas as pd
import time

gen_path = '/home/sandor/GIT/carla2colmap/project_test' # TODO: change to a new project location (root directory)

stats_df = pd.DataFrame(columns=['sample_num', 'time_start', 'time_end', 'pt_cloud_fn'])
input_paths = [ # TODO: add correct input paths
    '/home/sandor/GIT/carla2colmap/monopointcloud/03_31', 
    '/home/sandor/GIT/carla2colmap/monopointcloud/10_10/10_10_09_34_16'
    ]
for input_path in input_paths:
    s_num = 2**9 # 512
    input_name = input_path.split('/')[-1]
    current_prj = os.path.join(gen_path, input_name)
    os.environ['PRJ_WD'] = current_prj
    os.environ['IN_IMG'] = input_path
    os.environ['IN_IMG_FOLDER'] = 'masked_rgb' # TODO: change if needed
    os.environ['IN_CAM'] = input_path
    os.environ['CONFIGS'] = '/home/sandor/GIT/carla2colmap/configs'
    os.environ['SAMP_NUM'] = str(s_num)
    t_start = time.time()
    rc = subprocess.call('./automation.sh')
    t_end = time.time()
    print('t_start:', t_start)
    print('t_end:', t_end)
    fused_old = os.path.join(current_prj, 'dense/fused.ply')
    fused_new = os.path.join(current_prj, 'dense/fused_' + str(s_num) + '_' + input_name + '.ply')
    try:
        os.rename(fused_old, fused_new)
    except:
        print('fused.ply not found')

    stats_df.loc[len(stats_df.index)] = [s_num, t_start, t_end, fused_new]
    stats_df.to_csv(os.path.join(gen_path, 'sample_num_stats.csv'))



def generateSampleNum(): # Used for result generation for different sample numbers (legacy code)
    gen_path = '/home/sandor/GIT/carla2colmap/project_sample_num'
    
    stats_df = pd.DataFrame(columns=['sample_num', 'time_start', 'time_end', 'pt_cloud_fn'])
    for p in range(2, 11):
        s_num = 2**p
        current_prj = os.path.join(gen_path, 'sample_num_'+ str(s_num))
        os.environ['PRJ_WD'] = current_prj
        os.environ['IN_IMG'] = '/home/sandor/GIT/carla2colmap/monopointcloud/03_31'
        os.environ['IN_IMG_FOLDER'] = 'semseg'
        os.environ['IN_CAM'] = '/home/sandor/GIT/carla2colmap/monopointcloud/03_31'
        os.environ['CONFIGS'] = '/home/sandor/GIT/carla2colmap/configs'
        os.environ['SAMP_NUM'] = str(s_num)
        t_start = time.time()
        rc = subprocess.call('./automation.sh') # TODO: change to the automation script
        t_end = time.time()
        print('t_start:', t_start)
        print('t_end:', t_end)
        fused_old = os.path.join(current_prj, 'dense/fused.ply')
        fused_new = os.path.join(current_prj, 'dense/fused_' + str(s_num) + '.ply')
        try:
            os.rename(fused_old, fused_new)
        except:
            print('fused.ply not found')
    
        stats_df.loc[len(stats_df.index)] = [s_num, t_start, t_end, fused_new]
        stats_df.to_csv(os.path.join(gen_path, 'sample_num_stats.csv'))