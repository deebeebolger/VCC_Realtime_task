import csv
import numpy as np
import pywt
from matplotlib.pylab import *
from scipy.signal import *
from numpy.fft import *
from scipy import *
from collections import defaultdict

fout_data = open("../Image_classify/train.csv", 'a')
chan = ['Fp1','AF3','F3','F7','FC5','FC1','C3','T7','CP5','CP1','P3','P7','PO3','O1','Oz','Pz','Fp2','AF4','Fz','F4','F8','FC6','FC2','Cz','C4','T8','CP6','CP2','P4','P8','PO4','O2']
cols = defaultdict(list)
vect = []   # Initialize the vector

with open("../Image_classify/features_raw.csv") as f:
    reader = csv.DictReader(f)      # Read the rows of features_raw.csv file as dictionary format.
    for row in reader:              # Read each row as {column1: value1, column2, value2, ...}
        for (k,v) in row.items():   # Loop through each column name and value.
            if k == '':
                print("Current value is None; Skip \n")
            else:
                cols[k].append(v)       # Append the value in the correct list; list corresponding to column of name, k.

for cidx , chancurr in enumerate(chan):
    xarr = np.array(cols[chancurr]).astype(np.double)
    wav_coeffs = pywt.wavedec(xarr, 'db4', level=6)  # 6 coefficients
    cA6, cD6, cD5, cD4, cD3, cD2, cD1 = wav_coeffs   # ordered list of coefficient arrays

    cD5_std = np.mean(cD5)
    cD4_std = np.mean(cD4)
    cD3_std = np.mean(cD3)
    cD2_std = np.mean(cD2)
    cD1_std = np.mean(cD1)
    if chancurr == 'O2':
        fout_data.write(str(cD5_std)+",")
        fout_data.write(str(cD4_std)+",")
        fout_data.write(str(cD3_std)+",")
        fout_data.write(str(cD2_std)+",")
        fout_data.write(str(cD1_std))
    else:
        fout_data.write(str(cD5_std) + ",")
        fout_data.write(str(cD4_std) + ",")
        fout_data.write(str(cD3_std) + ",")
        fout_data.write(str(cD2_std) + ",")
        fout_data.write(str(cD1_std) + ",")

fout_data.write("\n")
fout_data.close()






