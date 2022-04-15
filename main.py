import os
import numpy as np
import csv
import statistics

def save_file(fn_path, fn, data):
    fn = os.path.join(fn_path, fn)
    with open(fn, 'w', newline='') as f:
        csv_write = csv.writer(f)
        csv_write.writerows(data)
    f.close()
    print('save: ', fn)


def npy_file(fn_path, fn, data):
    fn = os.path.join(fn_path, fn)
    np.save(fn, data)


def get_data(month, day, type, forecast):
    member_data = []
    for m in range(1, 21, 1):
        member = 'E' + str(m) if m > 9 else 'E0' + str(m)
        file_name = hour_acc + '_member_npy\\' + year + month + '\\' + month + day + '_' + type + '_' + member + '_' + forecast + '.npy'
        data = np.load(file_name)
        data = data.astype(np.float16)
        member_data.append(data.tolist())
    member_data = np.array(member_data)
    return member_data


def ensemble_mean(data, month, day, type, forecast):
    mean = np.zeros((312, 312))
    for i in range(0, 10):
        mean += data[i]
    mean = mean / 20
    save_name = 'mean_' + month + day + '_' + type + '_' + forecast
    save_file(hour_acc + '_mean_csv\\'+ year + month, save_name + '.csv', mean)
    npy_file(hour_acc + '_mean_npy\\'+ year + month, save_name, mean)
    return mean


def ensemble_pm(mean, data, month, day, type, forecast):
    pm = np.zeros(312 * 312)
    mean_flatten = mean.flatten()
    mean_sort = sorted(mean_flatten, reverse=True)

    mem_median = []
    mem_flatten = data.flatten()
    mem_sort = sorted(mem_flatten, reverse=True)

    for i in range(0, len(mem_sort), 20):
        twenty_list = mem_sort[i:i + 20]
        mem_median.append(statistics.median(twenty_list))

    for i in range(0, len(mean_sort)):
        index = np.where(mean_flatten == mean_sort[i])
        if len(index[0]) > 1:
            pm[index[0][0]] = mem_median[i]
            mean_flatten[index[0][0]] = -99999
        else:
            pm[index[0][0]] = mem_median[i]

    pm = np.array(pm).reshape(312, 312)
    save_name = 'pm_' + month + day + '_' + type + '_' + forecast
    save_file(hour_acc + '_pm_csv\\'+ year + month, save_name + '.csv', pm)
    npy_file(hour_acc + '_pm_npy\\'+ year + month, save_name, pm)


def ensemble_npm(mean, data, month, day, type, forecast):

    npm = np.zeros(312 * 312)
    mean_flatten = mean.flatten()
    mean_sort = sorted(mean_flatten, reverse=True)

    mem_flatten = []
    npm_sort = []
    for i in range(0, 10):
        flatten = data[i].flatten()
        flatten = sorted(flatten, reverse=True)
        mem_flatten.append(flatten)

    for i in range(0, (312 * 312)):
        sum = 0
        for j in range(0, 10):
            sum += mem_flatten[j][i]
        npm_sort.append(sum / 10)

    for i in range(0, len(mean_sort)):
        index = np.where(mean_flatten == mean_sort[i])
        if len(index[0]) > 1:
            npm[index[0][0]] = npm_sort[i]
            mean_flatten[index[0][0]] = -99999
        else:
            npm[index[0][0]] = npm_sort[i]

    npm = np.array(npm).reshape(312, 312)
    save_name = 'npm_' + month + day + '_' + type + '_' + forecast
    save_file(hour_acc + '_npm_csv\\'+ year + month, save_name + '.csv', npm)
    npy_file(hour_acc + '_npm_npy\\' + year + month, save_name, npm)
    print('Done: ', save_name)

def make_dirs(hour_acc, year, month):
    sub_folder = year + month + '\\'
    ensemble = ['_mean', '_pm', '_npm']
    type = ['_csv', '_npy']

    for e in ensemble:
        for t in type:
            path = hour_acc + e + t + '\\' + sub_folder
            if not os.path.isdir(path): os.makedirs(path)


hour_acc = '12'

for y in range(18, 22):
    year = str(y)

    for m in range(5, 7):
        month = str(m) if m > 9 else '0' + str(m)
        make_dirs(hour_acc, year, month)
        for d in range(1, 32):
            if y == 18 and m == 5 and d == 1 : pass
            elif m != 6 or (m == 6 and d != 31):
                day = str(d) if d > 9 else '0' + str(d)

                for t in range(0, 19, 6):
                    type = str(t) if t > 9 else '0' + str(t)

                    for f in range(11, 36, int(hour_acc)):
                        forecast = 'F' + str(f) if f > 9 else 'F0' + str(f)
                        file_name = hour_acc + '_member_npy\\'+ year + month + '\\' + month + day + '_' + type + '_' + 'E02' + '_' + forecast + '.npy'
                        if os.path.isfile(file_name):
                            data = get_data(month, day, type, forecast)
                            mean = ensemble_mean(data, month, day, type, forecast)
                            ensemble_pm(mean, data, month, day, type, forecast)
                            ensemble_npm(mean, data, month, day, type, forecast)
                        else:
                            print('Lost:', file_name)