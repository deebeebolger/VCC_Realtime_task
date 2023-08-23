from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import numpy as np
from VCC_SigPlotter import plot_channels

def subseg_trial(tdataIn, ftimes, olap, srate):
    """
       :param tdataIn: channel X ntime data for current trial
       :param ftimes : the length of each frame in seconds.
       :param olap:    the overlap when dividing the trial into frames
       :return:        list of start and end samples for each frame (length = 10)
       """
    enum, nsamps = np.shape(tdataIn)
    lentotal = nsamps / srate  # The total length of the trial in seconds
    lenframe = lentotal / ftimes  # The length of each frame in seconds
    nsamps_frame = lenframe * srate  # The number of samples in each frame
    nsamps_olap = nsamps_frame * olap  # The number of samples in overlap

    # Generate the start samples.
    # Length nsamps and in steps of nsamps * olap
    start_last = (lentotal - lenframe) * srate
    samps_start = np.arange(0, start_last + nsamps_olap, nsamps_olap)
    samps_end = samps_start + nsamps_frame
    startend_samps = np.vstack((samps_start, samps_end))
    startend_samps = np.transpose(startend_samps)

    data_frames = []

    for fcnt, fcurr in enumerate(startend_samps):
        print(f'Current start and end samples are {int(fcurr[0])} and {int(fcurr[1])} respectively')
        framecurr = tdataIn[:, int(fcurr[0]):int(fcurr[1])]
        data_frames.append(framecurr)

    return data_frames

def Znormer(arr):
    """
    Programmé par Gilles Pouchoulin (2023)
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

def PSD_trial(data, fsamp):
    freqs, Pxx_den = signal.welch(data, fsamp, nperseg=128)
    fidx = [fcnt for fcnt, fcurr in enumerate(freqs) if fcurr >= 4 and fcurr <= 45]

    plt.plot(freqs[fidx], 20 * np.log10(Pxx_den[6, fidx]))
    plt.title('PSD of Cz electrode (all videos)')
    plt.ylabel('PSD (dB)')
    plt.xlabel('Frequency (Hz)')
    plt.xlim([4, 45])

    Allbands = []

    alpha_indx = [aindx for aindx, fcurr1 in enumerate(freqs) if fcurr1 >= 8 and fcurr1 <= 13]
    beta_indx = [bindx for bindx, fcurr2 in enumerate(freqs) if fcurr2 > 13 and fcurr2 <= 30]
    gamma_indx = [gindx for gindx, fcurr3 in enumerate(freqs) if fcurr3 > 30 and fcurr3 <= 45]

    alpha_pow = Pxx_den[:, alpha_indx]
    alphapow_mean = np.mean(alpha_pow, 1)  # Find the mean alpha power

    beta_pow = Pxx_den[:, beta_indx]
    betapow_mean = np.mean(beta_pow, 1)  # Find the mean beta power

    gamma_pow = Pxx_den[:, gamma_indx]
    gammapow_mean = np.mean(gamma_pow, 1)  # Find the mean gamma power.

    Allbands = np.vstack((alphapow_mean, betapow_mean, gammapow_mean))
    Allbands = np.transpose(Allbands)

    return Allbands
