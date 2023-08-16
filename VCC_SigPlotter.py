import matplotlib.pyplot as plt
import numpy as np
import os

def plot_channels(chandata, srate, channoms, curr_sujet):
    """
    Function to plot the EEG signals given an array of EEG in the
    form trials X channels X time.
    :param chandata: array of EEG data in form trials X channels X time
    :param srate:    sampling frequency (required to build time vector)
    :param channoms: channel titles
    :return:
    """
    n_cols = 2
    n_rows = int(len(channoms)/n_cols)
    fig, ax = plt.subplots(n_rows, n_cols)
    ax = np.array(ax).flatten()
    chan_idx = np.arange(0,len(channoms))
    fig.suptitle(curr_sujet)

    for chancurr, ichan, ax_curr in zip(channoms, chan_idx, ax):

        currdata = chandata[:,ichan,:]      # The data for all trials for the current channel
        currdata_ga = np.mean(currdata, 0)  # Calculate the mean over all trials for the current channel.

        if ichan == 0:
            dsize = np.shape(chandata)
            time  = np.arange(0, dsize[2])/srate

        ax_curr.plot(time[srate*20:srate*25], currdata_ga[srate*20:srate*25])
        ax_curr.set_xlabel('Time')
        ax_curr.grid(True)
        ax_curr.set(title = chancurr)

    sname = curr_sujet.split('.')
    figname = sname[0] + '_EEG'
    figname_path = 'Figures/'+figname
    fig.savefig(figname_path)
    plt.close(fig)
