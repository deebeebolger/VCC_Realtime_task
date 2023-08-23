import os
import pylsl
import numpy as np
import pandas as pd
import scipy
import scipy.io as sio
import threading
import time
import warnings
import pygame
import pickle
from scipy import signal
from VCC_Segment_PSD_calc import *

pygame.init()
VERBOSE = False

def time_str():
    return time.strftime("%H_%M_%d_%m_%Y", time.gmtime())


class NoRecordingDataError(Exception):
    def __init__(self):
        self.value = "Received no data while recording"

    def __str__(self):
        return repr(self.value)


class KillSwitch():
    def __init__(self):
        self.terminate = False

    def kill(self):
        self.terminate = True
        return False

def record(channel_data=[], time_stamps=[], KillSwitch=None, time_vect=[], data_noinc=[]):
    if VERBOSE:
        sio.savemat("recording_" + time_str() + ".mat", {
            "time_stamps"  : [1, 2, 3],
            "channel_data" : [1, 2, 3]
        })
    else:
        print('Hello there Dee!')
        streams = pylsl.resolve_stream('type', 'EEG')
        inlet = pylsl.stream_inlet(streams[0])
        sampcount = 0

        while True:
            try:
                sample, time_stamp = inlet.pull_sample()  # Captures the current data sample and the time of sample on remote machine.
                time_stamp += inlet.time_correction()     # Retrieve an estimated time correction offset for the given stream.This number is added to the time stamp generated via lsl.local_clock()
                curr_samp = sampcount*(1/125)

                time_stamps.append(time_stamp)
                channel_data.append(sample)               # Vector with a column for each channel
                data_noinc.append(sample)

                time_vect.append(curr_samp)
                sampcount += 1

                # first col of one row of the record_data matrix is time_stamp,
                # the following cols are the sampled channels

            except KeyboardInterrupt:
                complete_samples = min(len(time_stamps), len(channel_data))
                sio.savemat("recording_" + time_str() + ".mat", {
                    "time_stamps"  : time_stamps[:complete_samples],
                    "channel_data" : channel_data[:complete_samples]
                })
                break
    if KillSwitch.terminate:
        return False

class RecordData():
    def __init__(self, Fs, sujnom, disptime, pic_number, gender="male", record_func=record):  #define __init__() method.
        # Create instance variables.
        self.trial = []
        self.X = []
        self.trial_time_stamps = []
        self.time_stamps       = []
        self.time_vect         = []
        self.trial_timevect    = []
        self.trial_data        = []
        self.X_noninc          = []
        self.Fs = Fs
        self.disptime = disptime
        self.gender = gender
        self.sujnom = sujnom
        self.add_info = ""
        self.killswitch = KillSwitch()
        self.Y = []
        self.currimage_name = []
        self.image_classes  = []
        self.pic_number = pic_number
        self.data_filt = []
        self.freqband_data = []

        recording_thread = threading.Thread(group=None, target=record_func,
                                            args=(self.X, self.time_stamps, self.killswitch, self.time_vect, self.X_noninc),
                                            )
        recording_thread.daemon = True              # define daemon thread to execute in background.
        self.recording_thread   = recording_thread

    def __iter__(self):
        # Data to return
        yield 'trial'            , self.trial
        yield 'sujnom'           , self.sujnom
        yield 'X'                , self.X
        yield 'time_stamps'      , self.time_stamps
        yield 'trial_time_stamps', self.trial_time_stamps
        yield 'Y'                , self.Y
        yield 'Fs'               , self.Fs
        yield 'gender'           , self.gender
        yield 'add_info'         , self.add_info
        yield 'time_vect'        , self.time_vect
        yield 'trial_data'       , self.trial_data
        yield 'trial_timevect'   , self.trial_timevect
        yield 'disptime'         , self.disptime
        yield 'image_classes'    , self.image_classes
        yield 'pic_number'       , self.pic_number
        yield 'data_filt'        , self.data_filt
        yield 'freqband_data'    , self.freqband_data


    def add_trial(self, label, to_add=[]):

        if label == 0:
            N = self.Fs * (self.disptime * self.pic_number)  #
            curr_data = self.X_noninc
            currd_shape = np.shape(curr_data)
            print(f'N samples {str(int(N))}')
            print(f"The dimensions of current data is {str(currd_shape)}")
            print("Trial length in samples is:" + str(len(curr_data[-int(N):])))
            self.trial_data.append(curr_data[-int(N):])  # Pass only the 15seconds to the frequency analysis.
            to_add = curr_data[-int(N):]
            print("current trial data dimension: " + str(np.shape(curr_data[-int(N):])))
            print("Pause Label: " + str(label))
            self.trial_data.append(to_add)
        else:
            print(f"Trial label: {label}")
            self.image_classes.append(label)

        self.trial_time_stamps.append(pylsl.local_clock())  # Get the time at the start of the trial.
        self.Y.append(label)
        self.trial_timevect.append(self.time_vect[-1])

        return to_add

    def start_recording(self):
        self.recording_thread.start()
        time.sleep(1)
        if len(self.X) == 0:
            raise NoRecordingDataError()

    def set_trial_start_indexes(self):
        i = 0
        for trial_time_stamp in self.trial_time_stamps:
            for j in range(i, len(self.time_stamps)):
                time_stamp = self.time_stamps[j]
                if trial_time_stamp <= time_stamp:
                    self.trial.append(j - 1)
                    i = j
                    break


    def preprocess_data(self):
        '''
        Function to carry out quick pre-processing of the data for the current trial.
        It pre-processes the trial_data variable.
        The dimensions of trial_data is trials X samples X channels (16)
        There should be 60seconds of data per trial == 7500 samples.
        1. Ensure that the channels are in the same order as for training dataset.
        2. Band pass filter.
        :return:
        '''
        DFIn = pd.read_excel('channels_psd_obci.xlsx')
        DeapOrder = DFIn['InDeap']
        ObciOrder = DFIn['InOBCI']
        Chans     = DFIn['Electrode']

        Tdata = self.trial_data
        Tdata = Tdata[0,:,:]
        obci_cidx = np.asarray(ObciOrder)
        chanidx = np.where(obci_cidx>0)[0]
        chans2keep = list(ObciOrder[chanidx])   # The channels to use.
        elecs2keep = Chans[chanidx]
        Tdata_order = np.asarray([Tdata[:,i-1] for i in chans2keep])   # Reordered the channels to correspond to Deap data.

        # Filter the continuous data using a 6-order butterworth filter.
        lowcut = 4
        highcut = 45
        order = 6
        nyq = 0.5 * self.Fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = signal.butter(order, [low, high], btype='band')
        datafilt = signal.filtfilt(b, a, Tdata_order)
        print(f"Size of datafilt is {np.shape(datafilt)}")

        # Rereference to the average reference.
        # chanref_indx = ref
        # drf = datafilt - ref
        # find the mean of the other 15 electrodes and subtract.
        return datafilt

    def freqband_calc(self):
        '''
        Function to calculate the mean power in the frequency bands: alpha, beta and gamma.

        :return:
        '''

        data_znormed = Znormer(self.data_filt)
        zdata_seg = subseg_trial(data_znormed, self.disptime, 0.5, self.Fs)
        zdata_sega = np.asarray(zdata_seg)
        #zdata_seg = trialT_divide(data_znorme, 6, 0.5, 125)
        tnum, channum, sampnum = np.shape(zdata_seg)
        fband_trial = []

        for tcount in range(tnum):
            Freqbands = PSD_trial(zdata_sega[int(tcount),:,:], 125)
            fband_trial.append(Freqbands)

        Freqband_arr = np.asarray(fband_trial)
        self.freqband_data = Freqband_arr
        return Freqband_arr

    def stop_recording_and_dump(self, file_name="session_" + time_str() + ".mat"):
        self.set_trial_start_indexes()
        sio.savemat(file_name, dict(self))

        fnom = self.sujnom +'_'+time_str()
        curr_fnom = os.path.join('../VCC_Realtime_task/Sujets_PSD4Model', fnom + '_PSD_frame.npy')
        np.save(curr_fnom, np.array(self.freqband_data, dtype=object), allow_pickle=True)  # Save as a numpy array.

        return file_name


if __name__ == '__main__':
    record()

