import numpy as np
import os
from visualize.visualized_pred import visualized_area_with_map

save_path = '6_member_npy\\OBS_1805\\photo\\'
file_path = '6_member_npy\\OBS_1805\\'

if not os.path.isdir(save_path):
    os.makedirs(save_path)

for day in range(5, 6, 1):
    for type in range(0, 19, 6):
        for forecast in range(11, 35, 6):
            d = str(day) if day > 9 else '0' + str(day)
            t = str(type) if type > 9 else '0' + str(type)
            f = 'F' + str(forecast) if forecast > 9 else 'F0' + str(forecast)

            obs_file = 'OBS_test_21_06' + d + '_' + t + '_' + f
            ob = file_path + obs_file + '.npy'

            if os.path.isfile(ob):
                land_data = np.load('312_312_land.npy')
                # obs = np.loadtxt(open(ob, "rb"), delimiter=",", skiprows=0)
                obs = np.load(ob)
                obs = obs * land_data
                visualized_area_with_map(obs, 'Sun_Moon_Lake', shape_size=[312, 312],title='{}'.format(obs_file), savepath=save_path)