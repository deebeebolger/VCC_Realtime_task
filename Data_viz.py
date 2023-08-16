import pandas as pd
import numpy as np
import os
import pickle5
import sys
from multiprocessing import Pool


data_path = '/Users/bolger/Documents/work/Projects/Visions_ClimateChange/Data'
filesave_path = '/Users/bolger/Documents/work/Projects/Visions_ClimateChange/DataFiles'
path_contents = os.listdir(data_path)

chan = ['Fp1','AF3','F3','F7','FC5','FC1','C3','T7','CP5','CP1','P3','P7','PO3','O1','Oz','Pz','Fp2','AF4','Fz','F4','F8','FC6','FC2','Cz','C4','T8','CP6','CP2','P4','P8','PO4','O2']
nLabel, nTrial, nSuj, nChans, nTime = 4, 40, len(path_contents), len(chan), 8064

fileout_labels0 = open("labels_0.dat",'w')
fileout_labels1 = open("labels_1.dat",'w')
fileout_labels2 = open("labels_2.dat",'w')
fileout_labels3 = open("labels_3.dat",'w')

for i, currfile in enumerate(path_contents):  # Range of user.
    data_curr = os.path.join(data_path, currfile)
    dataIn = pickle5.load(open(data_curr, 'rb'), encoding='latin1')
    print(f'Loading file {currfile}')
    for trl in range(nTrial):  # Trial range
        fileout_data = open(os.path.join(filesave_path, "features_raw.csv", 'w'))
        for ichan, chancurr in enumerate(chan):
            fileout_data.write(chancurr+",")
        fileout_data.write("\n")
        for currdat in range(nTime):
            for ichan2 in range(chan):
                if ichan2 < 32:
                    if ichan2 == 31:
                        fileout_data.write(str(dataIn['data'][trl][ichan2][currdat]))
                    else:
                        fileout_data.write(str(dataIn['data'][trl][ichan2][currdat])+",")
            fileout_data.write("\n")

        fileout_labels0.write(str(dataIn['labels'][trl][0]) + "\n")
        fileout_labels1.write(str(dataIn['labels'][trl][1]) + "\n")
        fileout_labels2.write(str(dataIn['labels'][trl][2]) + "\n")
        fileout_labels3.write(str(dataIn['labels'][trl][3]) + "\n")
        fileout_data.close()
        #os.system('python creating_vector.py')
        # print("user"+ str(i) +"trial" +str(trl))

fileout_labels0.close()
fileout_labels1.close()
fileout_labels2.close()
fileout_labels3.close()
print("\n That's all folks!")






