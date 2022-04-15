import os
import struct
import numpy as np
import datetime as dt
import csv


def csv_file(fn_path, fn, data):
    fn = os.path.join(fn_path, fn)
    with open(fn, 'w', newline='') as f:
        csv_write = csv.writer(f)
        csv_write.writerows(data)
    f.close()
    print('save: ', fn)


def npy_file(fn_path, fn, data):
    fn = os.path.join(fn_path, fn)
    np.save(fn, data)


def read_file(year, month, month_d, ense, type, fore, time):
    file_path = 'F:\\Ensemble_Data\\bQPF' + year + month + '\\'
    file_name = 'WEPS_' + ense + '_' + year + month_d + type + '_' + fore + '_' + time + '.dat'
    file = file_path + file_name

    if os.path.isfile(file):
        return open_file(file)
    else:
        print(type([]))
        return []


def open_file(file):
    with open(file, 'rb') as fr:
        data = fr.read()
        member = struct.unpack(561 * 441 * 'h', data[-561 * 441 * 2:])
        member = np.array(member).reshape(561, 441).astype(np.float16) / 10
        member = member[155:467, 75:387]
        fr.close()
    return member


start_month = 5
start_day = 1
end_month = 6
end_day = 30
hour_acc = '6'
hour_acc_num = 6


for y in range(19, 22):
    year = str(y)
    int_year = 2000 + y
    start_date = dt.datetime(int_year, start_month, start_day, 0)
    end_date = dt.datetime(int_year, end_month, end_day, 0)
    total_days = (end_date - start_date).days + 1
    date_string = start_date + dt.timedelta(days=0)
    date_string = date_string + dt.timedelta(hours=0)

    for d in range(total_days):

        for t in range(0, 19, 6):
            type = str(t) if t > 9 else '0' + str(t)
            month_d = date_string.strftime("%m%d")
            month = date_string.strftime("%m")

            csv_path = hour_acc + '_member_csv\\' + year + month + '\\'
            npy_path = hour_acc + '_member_npy\\' + year + month + '\\'
            if not os.path.isdir(csv_path): os.makedirs(csv_path)
            if not os.path.isdir(npy_path): os.makedirs(npy_path)

            for e in range(1, 21):
                ensemble = e
                for f in range(11, 35, hour_acc_num):
                    sum = np.zeros((312, 312))
                    fore = 'F' + str(f) if f > 9 else 'F0' + str(f)
                    ense = 'E' + str(ensemble) if ensemble > 9 else 'E0' + str(ensemble)
                    save_name = month_d + '_' + type + '_' + ense + '_' + fore
                    shut_down = False

                    for i in range(0, hour_acc_num):
                        time = year + (date_string + dt.timedelta(hours=(f + i))).strftime("%m%d%H")
                        fore = 'f' + str(f + i) if (f + i) > 9 else 'f0' + str(f + i)
                        while True:
                            ense = 'E' + str(ensemble) if ensemble > 9 else 'E0' + str(ensemble)
                            member = read_file(year, month, month_d, ense, type, fore, time)
                            if not member.any():
                                ensemble = ensemble + 1 if ensemble < 20 else ensemble - 19
                                if e == ensemble:
                                    shut_down = True
                                    break
                            else:
                                sum += member
                                break

                    if not shut_down:
                        csv_file(csv_path, save_name + '.csv', sum)
                        npy_file(npy_path, save_name, sum)
                    else: print('Not Save: ', save_name)

            date_string = date_string + dt.timedelta(hours=6)
