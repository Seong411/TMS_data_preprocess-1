"""
1. zephyr의 각 파일 이름을 ECG, BREATHING으로 바꾸고 zephyr 데이터가 있는 폴더에 넣는다
2. 이 파일은 통합 하려는 데이터 상위 디렉토리에 존재해야한다.
3. LABEL.csv 파일에서 인풋으로 넣을 셀 말고 다른 셀 잘못 건드리면 NULL값이 행으로 추가돼서 에러 뜰 수 있음

NOTHING: N / SAD: S / ANGER: A / FEAR: F

ADDED_TIME + end_time이 다음 start_time보다 큰 경우는 고려하지 않았음

csv 파일 보면 null이 없는데 이게 중간에 데이터를 못 받으면 null로 표기한 게 아니라 아예 써놓지를 않은 것 같다.
EDA 0값 어떻게 할지
"""
import pandas
import os
import time
import datetime
import math
import statistics
import numpy
from naming import Change_All_Datafiles_Name as Change

ADDED_TIME = 0 # added to label.end_time
count = {}
count_total = 0

# cur_time ex) 0728121132 (no year) 한국시간 기준으로 넣으면 됨
def get_UTC_time(cur_time):
	time_obj = datetime.datetime.strptime(cur_time, '%m%d%H%M%S')
	time_obj = time_obj.replace(year = 2020)
	UTC_time = time.mktime(time_obj.timetuple())
	return int(UTC_time)

# cur_time ex) 03/05/2020 19:24:58.435 (zephyr form -> empatica form)
def get_UTC_time_from_zephyr(cur_time):
	time_obj = datetime.datetime.strptime(cur_time.split('.')[0], '%d/%m/%Y %H:%M:%S')
	UTC_time = time.mktime(time_obj.timetuple())
	return UTC_time

def get_start_idx(UTC_time, latest_time, HZ):
	return int((UTC_time - latest_time) * HZ)

def get_start_RR_idx(start_time, zephyr_time, cnt):
	start_idx = -1
	sum_column = zephyr_time
	while True:
		start_idx = start_idx + 1
		if start_idx>=cnt:
			break
		sum_column = sum_column + int(rr_df[column_name['RtoR']][start_idx])/1000
		if start_time < sum_column:
			break
	return start_idx

def get_end_RR_idx(start_time, time_window, start_idx, zephyr_time, cnt):
	end_idx = start_idx
	sum_column = 0
	while True:
		end_idx = end_idx + 1
		if end_idx>=cnt:
			break
		sum_column = sum_column + int(rr_df[column_name['RtoR']][end_idx])/1000
		if time_window < sum_column:
			break
	return end_idx

def get_HRV(start_idx, end_idx):
	cnt = end_idx - start_idx
	sum_diff_square = 0
	for idx in range(start_idx, end_idx + 1):
		sum_diff_square = sum_diff_square + (int(rr_df[column_name['RtoR']][idx+1])-int(rr_df[column_name['RtoR']][idx]))*(int(rr_df[column_name['RtoR']][idx+1])-int(rr_df[column_name['RtoR']][idx]))/1000000
	return math.sqrt(sum_diff_square/cnt)


def check_noise(STFW, latest_time):
    #TODO:
    # 일단은 그냥 0값 있으면 time window 패스하는걸로 했는데, 있으면 그 record만 지우는 방식을 쓸 수도 있고, 그 time window의 평균 값을 집어넣어주는 방법도 있음
    ################################### finding noise ####################################
    ######################################################################################
    idx = get_start_idx(STFW, latest_time, hz['hr'])
    if hr_df[column_name['hr']][idx:idx + hz['hr'] * time_window].min() == 0:
        if noise_mode == 1 and 'hr' in count:
            count['hr'] += 1
            return True
        elif noise_mode == 1:
            count['hr'] = 1
            return True
        else:
            mean = hr_df[column_name['hr']][idx:idx + hz['hr'] * time_window].sum() / (time_window * hz['hr'])
            for i in range(idx, idx + hz['hr'] * time_window):
                if hr_df[column_name['hr']][i] == 0:
                    hr_df[column_name['hr']][i] = mean

    idx = get_start_idx(STFW, latest_time, hz['eda'])
    if eda_df[column_name['eda']][idx:idx + hz['eda'] * time_window].min() == 0:
        if noise_mode == 1 and 'eda' in count:
            count['eda'] += 1
            return True
        elif noise_mode == 1:
            count['eda'] = 1
            return True
        else:
            mean = hr_df[column_name['eda']][idx:idx + hz['eda'] * time_window].sum() / (time_window * hz['eda'])
            for i in range(idx, idx + hz['eda'] * time_window):
                if hr_df[column_name['eda']][i] == 0:
                    hr_df[column_name['eda']][i] = mean

    idx = get_start_idx(STFW, latest_time, hz['breathing'])
    if breathing_df[column_name['breathing']][idx:idx + hz['breathing'] * time_window].min() == 0:
        if noise_mode == 1 and 'breathing' in count:
            count['breathing'] += 1
            return True
        elif noise_mode == 1:
            count['breathing'] = 1
            return True
        else:
            mean = hr_df[column_name['breathing']][idx:idx + hz['breathing'] * time_window].sum() / (time_window * hz['breathing'])
            for i in range(idx, idx + hz['breathing'] * time_window):
                if hr_df[column_name['breathing']][i] == 0:
                    hr_df[column_name['breathing']][i] = mean


    idx = get_start_idx(STFW, latest_time, hz['ecg'])
    if ecg_df[column_name['ecg']][idx:idx + hz['ecg'] * time_window].min() == 0:
        if noise_mode == 1 and 'ecg' in count:
            count['ecg'] += 1
            return True
        elif noise_mode == 1:
            count['ecg'] = 1
            return True
        else:
            mean = hr_df[column_name['ecg']][idx:idx + hz['ecg'] * time_window].sum() / (time_window * hz['ecg'])
            for i in range(idx, idx + hz['ecg'] * time_window):
                if hr_df[column_name['ecg']][i] == 0:
                    hr_df[column_name['ecg']][i] = mean

    ################################## address noise #####################################
    # 1. mediate the noise data
    # 2. just delete
    ######################################################################################
    return False


# set data from each file from start_time to end_time
# if (start_time - end_time) % time_window != 0: just ignore the tail
def set_data(start_time, end_time, zephyr_time, time_window, emotion):
	global count_total
	for STFW in range(start_time, end_time, time_window): # STFW: start time for window
		if STFW + time_window > end_time: # time-window size is not enough
			break

		count_total += 1

		if check_noise(STFW, latest_time): # TODO
			continue

		labeling.append(emotion)

		# hr
		idx = get_start_idx(STFW, latest_time, hz['hr'])
		hr_max.append(hr_df[column_name['hr']][idx:idx + hz['hr']*time_window].max())
		hr_min.append(hr_df[column_name['hr']][idx:idx + hz['hr']*time_window].min())
		hr_avg.append(hr_df[column_name['hr']][idx:idx + hz['hr']*time_window].sum() / (time_window * hz['hr']))
		hr_med.append(statistics.median(hr_df[column_name['hr']][idx:idx + hz['hr']*time_window]))
		hr_std.append(numpy.std(hr_df[column_name['hr']][idx:idx + hz['hr']*time_window]))

		# eda
		idx = get_start_idx(STFW, latest_time, hz['eda'])
		eda_max.append(eda_df[column_name['eda']][idx:idx + hz['eda']*time_window].max())
		eda_min.append(eda_df[column_name['eda']][idx:idx + hz['eda']*time_window].min())
		eda_avg.append(eda_df[column_name['eda']][idx:idx + hz['eda']*time_window].sum() / (time_window * hz['eda']))
		eda_med.append(statistics.median(eda_df[column_name['eda']][idx:idx + hz['eda']*time_window]))
		eda_std.append(numpy.std(eda_df[column_name['eda']][idx:idx + hz['eda']*time_window]))
		
		# breathing
		idx = get_start_idx(STFW, latest_time, hz['breathing'])
		breathing_max.append(breathing_df[column_name['breathing']][idx:idx + hz['breathing']*time_window].max())
		breathing_min.append(breathing_df[column_name['breathing']][idx:idx + hz['breathing']*time_window].min())
		breathing_avg.append(breathing_df[column_name['breathing']][idx:idx + hz['breathing']*time_window].sum() / (time_window * hz['breathing']))
		breathing_med.append(statistics.median(breathing_df[column_name['breathing']][idx:idx + hz['breathing']*time_window]))
		breathing_std.append(numpy.std(breathing_df[column_name['breathing']][idx:idx + hz['breathing']*time_window]))
		
		# ecg
		idx = get_start_idx(STFW, latest_time, hz['ecg'])
		ecg_max.append(ecg_df[column_name['ecg']][idx:idx + hz['ecg']*time_window].max())
		ecg_min.append(ecg_df[column_name['ecg']][idx:idx + hz['ecg']*time_window].min())
		ecg_avg.append(ecg_df[column_name['ecg']][idx:idx + hz['ecg']*time_window].sum() / (time_window * hz['ecg']))
		ecg_med.append(statistics.median(ecg_df[column_name['ecg']][idx:idx + hz['ecg']*time_window]))
		ecg_std.append(numpy.std(ecg_df[column_name['ecg']][idx:idx + hz['ecg']*time_window]))

		# hrv
		rr_cnt = int(rr_df['RtoR'].count())
		start_idx = get_start_RR_idx(STFW, zephyr_time, rr_cnt)
		end_idx = get_end_RR_idx(STFW, time_window, start_idx, zephyr_time, rr_cnt)
		hrv.append(get_HRV(start_idx, end_idx))

		# sbp
		idx = get_start_idx(STFW, latest_time, hz['bvp'])
		sbp.append(bvp_df[column_name['bvp']][idx:idx + hz['bvp']*time_window].max())

Change()
		
##################################### get inputs #####################################
# folder name
dir_name = input("Input your folder name: ")

# time_window
time_window = input("Input time_window as seconds: ")
time_window = int(time_window)

# labeling flag
labeling_flag = input("\nWill you label the file? [y/n]: ");

# get label as file
#if labeling_flag: 

# pad_time: label 양 옆으로 쓰지 않을 데이터를 몇초 구간으로 잡을 건지
pad_time = int(input("Input pad_time as seconds: "))

noise_mode = input("\n ===================================================== \n"
	+ "    1. just delete the data. \n"
	+ "    2. mediate the data before getting statistics. \n"
	+ " ===================================================== \n"
	+ "    Press the number how you will address noise: ")

###################################### setting #######################################
# open csv files
this_dir = os.path.dirname(os.path.abspath( __file__ ))
this_dir = this_dir[:-4] + 'Data'
output_file = os.path.join(os.path.dirname(os.path.abspath( __file__ )), dir_name + '_output.csv')
label = pandas.read_csv(os.path.join(this_dir, dir_name, 'LABEL.csv'))
hr = pandas.read_csv(os.path.join(this_dir, dir_name, 'HR.csv'))
eda = pandas.read_csv(os.path.join(this_dir, dir_name, 'EDA.csv'))
ibi = pandas.read_csv(os.path.join(this_dir, dir_name, 'IBI.csv'))
breathing = pandas.read_csv(os.path.join(this_dir, dir_name, 'BREATHING.csv'))
ecg = pandas.read_csv(os.path.join(this_dir, dir_name, 'ECG.csv'))
rr = pandas.read_csv(os.path.join(this_dir, dir_name,'RR.csv'))	# zephyr랑 empatica data_directory sync 문제
bvp = pandas.read_csv(os.path.join(this_dir, dir_name, 'BVP.csv'))

all_dataFrame = []
labeling = [] # NOTHING: N / SAD: S / ANGER: A / FEAR: F
hr_max = []
hr_min = []
hr_avg = []
hr_med = []
hr_std = []
eda_max = []
eda_min = []
eda_avg = []
eda_med = []
eda_std = []
breathing_max = []
breathing_min = []
breathing_avg = []
breathing_med = []
breathing_std = []
ecg_max = []
ecg_min = []
ecg_avg = []
ecg_med = []
ecg_std = []
hrv = []
sbp = []

# read data as dataFrame
#hr_df = pandas.DataFrame(hr)
#eda_df = pandas.DataFrame(eda)
#ibi_df = pandas.DataFrame(ibi)
hr_df = hr
eda_df = eda
ibi_df = ibi
breathing_df = breathing
ecg_df = ecg
rr_df = rr
bvp_df = bvp

# get the column name
column_name = {}
column_name['hr'] = list(hr_df)[0]
column_name['eda'] = list(eda_df)[0]
column_name['ibi'] = list(ibi_df)[0]
column_name['breathing'] = list(breathing_df)[1]
column_name['ecg'] = list(ecg_df)[1]
column_name['RtoR'] = list(rr_df)[1]
column_name['BVP'] = list(bvp_df)[1]

########################### Adjusting the START & END time ###########################

# get the start time of all the data as Empatica form(UNIX UTC)
start_time = {}
start_time['hr'] = float(list(hr_df)[0])
start_time['eda'] = float(list(eda_df)[0])
start_time['ibi'] = float(list(ibi_df)[0])
start_time['breathing'] = float(get_UTC_time_from_zephyr(breathing_df['Time'][0]))
start_time['ecg'] = float(get_UTC_time_from_zephyr(ecg_df['Time'][0]))
start_time['bvp'] = float(list(bvp_df)[0])

# get HZ
hz = {}
hz['hr'] = 1
hz['eda'] = 4
hz['ibi'] = 1
hz['breathing'] = 25
hz['ecg'] = 250
hz['bvp'] = 64

# get the latest start time in sec
latest_time = max(start_time['hr'], start_time['eda'], start_time['ibi'], start_time['breathing'], start_time['ecg'], start_time['bvp'])
zephyr_time = max(start_time['breathing'], start_time['ecg'])

######################## drop the data before latest time ############################

# get the difference between latest time as seconds
time_diff = {}
time_diff['hr'] = latest_time - start_time['hr']
time_diff['eda'] = latest_time - start_time['eda']
time_diff['ibi'] = latest_time - start_time['ibi']
time_diff['breathing'] = latest_time - start_time['breathing']
time_diff['ecg'] = latest_time - start_time['ecg']
time_diff['bvp'] = latest_time - start_time['bvp']

# get the number of rows that should be deleted
del_num = {}
del_num['hr'] = time_diff['hr'] * hz['hr']
del_num['eda'] = time_diff['eda'] * hz['eda']
del_num['ibi'] = time_diff['ibi'] * hz['ibi']
del_num['breathing'] = time_diff['breathing'] * hz['breathing']
del_num['ecg'] = time_diff['ecg'] * hz['ecg']
del_num['bvp'] = time_diff['bvp'] * hz['bvp']

# delete rows as much as the difference (also row for Hz)
hr_df.drop([i for i in range(int(del_num['hr']) + 1)], inplace=True)
eda_df.drop([i for i in range(int(del_num['eda']) + 1)], inplace=True)
ibi_df.drop([i for i in range(int(del_num['ibi']) + 1)], inplace=True)
breathing_df.drop([i for i in range(int(del_num['breathing']))], inplace=True)
ecg_df.drop([i for i in range(int(del_num['ecg']))], inplace=True)
bvp_df.drop([i for i in range(int(del_num['bvp']))], inplace=True)

# get the fastest end time in sec
min_recorded_time_in_sec = min(len(hr_df)/hz['hr'], len(eda_df)/hz['eda'], len(ibi_df)/hz['ibi'], len(breathing_df)/hz['breathing'], len(ecg_df)/hz['ecg'], len(bvp_df)/hz['bvp'])
fastest_end_time = int(latest_time) + math.trunc(min_recorded_time_in_sec)


################################# data extracting ####################################

for i in range(-1, len(label)):
	# catch exception for LABEL.csv
	if get_UTC_time(str(label['start'][max(i, 0)])) < latest_time:
		print("Your LABEL.csv row[", i, "] is invalid. (start time is out of range)")
		exit(0)
	elif get_UTC_time(str(label['end'][max(i, 0)])) > fastest_end_time:
		print("Your LABEL.csv row[", i, "] is invalid. (end time is out of range)")
		exit(0)
	elif get_UTC_time(str(label['start'][max(i, 0)])) > get_UTC_time(str(label['end'][max(i, 0)])):
		print("Your LABEL.csv row[", i, "] is invalid. (start time is later than end time)")
		exit(0)
	zephyr_time = int(zephyr_time)
	# time interval before the first cell in LABEL.csv
	if i == -1:
		start_time = int(latest_time)
		end_time = get_UTC_time(str(label['start'][0])) - pad_time
		emotion = 'N'
		set_data(start_time, end_time, zephyr_time, time_window, emotion)
		continue
	
	# time interval for one cell in LABEL.csv
	start_time = get_UTC_time(str(label['start'][i]))
	end_time = get_UTC_time(str(label['end'][i])) + 1 + ADDED_TIME
	emotion = label['label'][i]
	set_data(start_time, end_time, zephyr_time, time_window, emotion)
	
	# time interval between cells in LABEL.csv
	if i < len(label) - 1:
		start_time = get_UTC_time(str(label['end'][i])) + 1 + pad_time
		end_time = get_UTC_time(str(label['start'][i + 1])) - pad_time
		emotion = 'N'
		set_data(start_time, end_time, zephyr_time, time_window, emotion)
	
	# time interval after the last cell in LABEL.csv
	elif i == len(label) - 1:
		start_time = get_UTC_time(str(label['end'][i])) + 1 + pad_time
		end_time = fastest_end_time
		emotion = 'N'
		set_data(start_time, end_time, zephyr_time, time_window, emotion)

######################### Merge all the data into one file ###########################

data = {'labeling': labeling,
		'hr_max': hr_max, 'hr_min': hr_min, 'hr_avg': hr_avg, 'hr_med': hr_med, 'hr_std': hr_std,
		'eda_max': eda_max, 'eda_min': eda_min, 'eda_avg': eda_avg, 'eda_med': eda_med, 'eda_std': eda_std,
		'breathing_max': breathing_max, 'breathing_min': breathing_min, 'breathing_avg': breathing_avg, 'breathing_med': breathing_med, 'breathing_std': breathing_std,
		'ecg_max': ecg_max, 'ecg_min': ecg_min, 'ecg_avg': ecg_avg, 'ecg_med': ecg_med, 'ecg_std': ecg_std, 'hrv':hrv}

all_dataFrame.append(pandas.DataFrame(data=data))

All_data = pandas.concat(all_dataFrame, axis=0, ignore_index=True) # merge dataframe
All_data.to_csv(output_file, index=False)

print('Total number of records: ', count_total)
print('The number of zero time-windows of each feature', count)