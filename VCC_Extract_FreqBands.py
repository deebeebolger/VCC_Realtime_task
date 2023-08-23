from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

def PSD_calc(data, fsamp):

    freqs, Pxx_den = signal.welch(data, fsamp, nperseg=128)
    fidx = [fcnt for fcnt, fcurr in enumerate(freqs) if fcurr >= 4 and fcurr <= 45]

    plt.plot(freqs[fidx], 20*np.log10(Pxx_den[6, fidx]))
    plt.title('PSD of Cz electrode (all videos)')
    plt.ylabel('PSD (dB)')
    plt.xlabel('Frequency (Hz)')
    plt.xlim([4, 45])

    Allbands = []

    alpha_indx = [aindx for aindx, fcurr1 in enumerate(freqs) if fcurr1 >= 8 and fcurr1 <= 13]
    beta_indx  = [bindx for bindx, fcurr2 in enumerate(freqs) if fcurr2 > 13 and fcurr2 <= 30]
    gamma_indx = [gindx for gindx, fcurr3 in enumerate(freqs) if fcurr3 > 30 and fcurr3 <= 45]

    alpha_pow = Pxx_den[:, alpha_indx]
    alphapow_mean = np.mean(alpha_pow, 1)      # Find the mean alpha power

    beta_pow = Pxx_den[:, beta_indx]
    betapow_mean = np.mean(beta_pow, 1)       # Find the mean beta power

    gamma_pow = Pxx_den[:, gamma_indx]
    gammapow_mean = np.mean(gamma_pow, 1)      # Find the mean gamma power.

    Allbands = np.vstack((alphapow_mean, betapow_mean, gammapow_mean))
    Allbands = np.transpose(Allbands)

    return Allbands
