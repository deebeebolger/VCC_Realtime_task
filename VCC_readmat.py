import scipy as scp
import os
import datetime


dir_current = os.getcwd()
data_path = os.path.join(dir_current, 'REC')
dir_contents = os.listdir(data_path)

data_mat = scp.io.loadmat(os.path.join(data_path, dir_contents[3]))

ts = data_mat['trial_time_stamps']
D2 = datetime.datetime.fromtimestamp(ts[0][1]*1000)
D1 = datetime.datetime.fromtimestamp(ts[0][0]*1000)
Dmicrosec_diff = D2.microsecond - D1.microsecond
Dms_diff = Dmicrosec_diff/1000
