import pandas as pd
import numpy as np
import os
import pickle5
import sys
from multiprocessing import Pool
import matplotlib as mpl
import matplotlib.pyplot as plt
from VCC_SigPlotter import plot_channels
from VCC_Extract_FreqBands import PSD_calc

be = mpl.pyplot.get_backend()
print(f'The current backend is {be}')


def trialT_divide(tdataIn, ftimes, olap, srate):
    """

    :param tdataIn: channel X ntime data for current trial
    :param fnumber: the number of frames into which to divide the current trial
    :param olap:    the overlap when dividing the trial into frames
    :return:        list of start and end samples for each frame (length = 10)
    """
    enum, nsamps = np.shape(tdataIn)
    lentotal     = nsamps/srate        # The total length of the trial in seconds
    lenframe     = lentotal/ftimes     # The length of each frame in seconds
    nsamps_frame = lenframe * srate    # The number of samples in each frame
    nsamps_olap  = nsamps_frame * olap # The number of samples in overlap

    # Generate the start samples.
    # Length nsamps and in steps of nsamps * olap
    start_last = (lentotal - lenframe)*srate
    samps_start = np.arange(0, start_last+nsamps_olap, nsamps_olap)
    samps_end   = samps_start + nsamps_frame
    startend_samps = np.vstack((samps_start, samps_end))
    startend_samps = np.transpose(startend_samps)

    data_frames = []

    for fcnt, fcurr in enumerate(startend_samps):
        print(f'Current start and end samples are {int(fcurr[0])} and {int(fcurr[1])} respectively')
        framecurr = tdataIn[:,int(fcurr[0]):int(fcurr[1])]
        data_frames.append(framecurr)

    return data_frames


def normalize_Znorme(arr):
    """
    # Programmé par Gilles Pouchoulin (2023)
    Normalisation d'un tenseur de type par rapport à la moyenne et à la variance (centrer-réduire)
    i.e. où chaque vecteur de l'axe 0 est normalisé  pour obtenir une distribution de moyenne 0 et
    de variance 1.
    Parameters
    ----------

    arr : numpy.ndarray shape (row, col) par exemple (19, 7680)

        Tenseur de dimension 2 à normaliser.

    Returns

    -------

    new_arr : numpy.ndarray shape (row, col) par exemple (19, 7680)

        Tenseur de dimension 2 normalisé.

    """

    assert arr.ndim == 2, "Erreur "

    row_means = arr.mean(axis=1)

    row_stds = arr.std(axis=1)

    new_arr = np.zeros(arr.shape)

    for i, (row, row_mean, row_std) in enumerate(zip(arr, row_means, row_stds)):
        new_arr[i, :] = (row - row_mean) / row_std

    return new_arr


data_path = '/Users/bolger/Documents/work/Projects/Visions_ClimateChange/DEAP/Data/'
filesave_path = '/Users/bolger/Documents/work/Projects/Visions_ClimateChange/DEAP/DataFiles'
path_contents = os.listdir(data_path)
datFiles = [datcurr for datIndx, datcurr in enumerate(path_contents) if '.dat' in datcurr]

srate = 128
chan = ['Fp1','AF3','F3','F7','FC5','FC1','C3','T7','CP5','CP1','P3','P7','PO3','O1','Oz','Pz','Fp2','AF4','Fz','F4','F8','FC6','FC2','Cz','C4','T8','CP6','CP2','P4','P8','PO4','O2']
nLabel, nTrial, nSuj, nChans, nTime = 4, 40, len(path_contents), len(chan), 8064


Fbands_alltrls = []
num_frame = 10
overlap   = 0.5
Tdrop = 3    # Time to drop from the start of each trial (in seconds)
Tdrop_samps= srate * Tdrop

for i, currfile in enumerate(datFiles):  # Range of user.

    data_curr = os.path.join(data_path, currfile)
    dataIn = pickle5.load(open(data_curr, 'rb'), encoding='latin1')
    AllData = dataIn['data']
    AllLabels = dataIn['labels']
    print(f'Loading file {currfile}')

    PSD_alltrials = []

    for trl in range(nTrial):  # Trial range

        currtrl_data = AllData[trl, 0:32, Tdrop_samps-1:-1]  # Taking out the first 3 seconds of the trial data
        # Z-norm data here.
        currtrl_znorm = normalize_Znorme(currtrl_data)
        F = trialT_divide(currtrl_znorm, num_frame, overlap, srate)
        tnum, channum, sampnum = np.shape(F)

        psd_trial = []

        for tcnt, tcurrent in enumerate(F):
            print(f'Trial number {tcnt}...')
            fband_trl = PSD_calc(tcurrent, srate)  # takes in channel-level data for each trial.
            psd_trial.append(fband_trl)

        PSD_alltrials.append(psd_trial)
        PSD_swop = np.moveaxis(PSD_alltrials, 1,1)   # Change order of dimensions to yield 40 X 32 X 19 X 3

        fnom1 = currfile.split('.')
        curr_fnom = os.path.join('../VCC_Realtime_task/Sujet_PSD_znorm', fnom1[0] + '_PSD_frame.npy')
        np.save(curr_fnom, np.array(PSD_swop, dtype=object), allow_pickle=True)   # Save as a numpy array.