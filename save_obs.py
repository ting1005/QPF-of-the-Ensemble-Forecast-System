import os
import numpy as np
import datetime as dt
import csv
import struct


def save_file(fn_path, fn, data):
    fn = os.path.join(fn_path, fn)
    with open(fn, 'w', newline='') as f:
        csv_write = csv.writer(f)
        csv_write.writerows(data)
    f.close()


def npy_file(fn_path, fn, data):
    fn = os.path.join(fn_path, fn)
    np.save(fn, data)
    print('save: ', fn)


def read_file(year, month, month_day, fore):
    file_path = 'F:\\Ensemble_Data\\OBS'+ year + month + '\\'
    file_name = 'CB_GC_PCP_1H_RAD.20' + year + month_day + '.' + fore + '00'
    file = file_path + file_name

    if os.path.isfile(file):
        return open_file(file)
    else:
        return []


def open_file(file):
    with open(file, 'rb') as fr:
        data = fr.read()
        member = struct.unpack(561 * 441 * 'h', data[-561 * 441 * 2:])
        member = np.array(member).reshape(561, 441).astype(np.float16) / 4
        member = member[155:467, 75:387]
        fr.close()
    return member


start_month = 5
start_day = 1
end_month = 6
end_day = 30
hour_acc = '6'
hour_acc_num = 6

for y in range(18, 22):
    year = str(y)
    int_year = 2000 + y
    start_date = dt.datetime(int_year, start_month, start_day, 0)
    end_date = dt.datetime(int_year, end_month, end_day, 0)
    total_days = (end_date - start_date).days + 1

    date_string = start_date + dt.timedelta(days=0)
    date_string = date_string + dt.timedelta(hours=0)

    # CB_GC_PCP_1H_RAD.20200501.0000

    for d in range(total_days):
        print('-----------------------')
        month_d = date_string.strftime("%m%d")
        month = date_string.strftime("%m")

        csv_path = hour_acc + '_member_csv\\OBS_' + year + month + '\\'
        npy_path = hour_acc + '_member_npy\\OBS_' + year + month + '\\'
        if not os.path.isdir(csv_path): os.makedirs(csv_path)
        if not os.path.isdir(npy_path): os.makedirs(npy_path)

        for f in range(1, 20, 6):
            str_forecast = '_F' + str(f) if f > 9 else '_F0' + str(f)
            save_name = 'OBS_' + month_d + str_forecast
            sum = np.zeros((312, 312))
            shut_down = False

            for i in range(0, 6):
                obs_sum = f + i + 10
                while True:
                    if obs_sum > 23:
                        obs_sum = obs_sum % 24
                        month_day = (date_string + dt.timedelta(days=1)).strftime("%m%d")
                    else:
                        month_day = (date_string + dt.timedelta(days=0)).strftime("%m%d")
                    fore = str(obs_sum) if (obs_sum) > 9 else '0' + str(obs_sum)
                    member = read_file(year, month, month_day, fore)

                    if not np.array(member).any():
                        obs_sum = obs_sum - 1 if obs_sum > 1 else obs_sum + 23
                        if obs_sum == (f + i + 10) % 24:
                            shut_down = True
                            break
                    else:
                        sum += member
                        break

            if not shut_down:
                save_file(csv_path , save_name + '.csv', sum)
                npy_file(npy_path , save_name, sum)

        date_string = date_string + dt.timedelta(days=1)