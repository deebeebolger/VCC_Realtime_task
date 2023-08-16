import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import os
import math

xlfile_path = '/Users/bolger/Documents/work/Projects/Visions_ClimateChange/DEAP/metadata_csv'
xlfile_nom = 'participant_ratings.csv'
xlfullfile = os.path.join(xlfile_path, xlfile_nom)

vidxl_path = '/Users/bolger/Documents/work/Projects/Visions_ClimateChange/DEAP/metadata_csv'
vidxl_nom  = 'video_list.csv'
vidxl_fullfile = os.path.join(vidxl_path, vidxl_nom)

# Extract the meta-data information.
dfxl = pd.read_csv(xlfullfile)
valence_all = list(dfxl['Valence'])
arousal_all = list(dfxl['Arousal'])
domin_all   = list(dfxl['Dominance'])
ExpID_all   = list(dfxl['Experiment_id'])   # Look to the video to find related video
SujID_all   = list(dfxl['Participant_id'])  # The participant labels
Trials_all  = list(dfxl['Trial'])           # The trial number.

# Extract the video data information.
vidxl = pd.read_csv(vidxl_fullfile)
vid_ExpID   = list(vidxl['Experiment_id'])
vid_Artist  = list(vidxl['Artist'])
vid_Title   = list(vidxl['Title'])
vid_ValAvg  = list(vidxl['AVG_Valence'])
vid_ArslAvg = list(vidxl['AVG_Arousal'])
vid_DomAvg  = list(vidxl['AVG_Dominance'])

# Find the index of non-empty Experiment id.
notnan_idx = [nan_idx for nan_idx, vcurr in enumerate(vid_ExpID) if math.isnan(vcurr)==False]
VidExp_all = np.take(vid_ExpID, notnan_idx)
Artist_all = np.take(vid_Artist, notnan_idx)
Title_all  = np.take(vid_Title, notnan_idx)
Valence_avg = np.take(vid_ValAvg, notnan_idx)
Arousal_avg = np.take(vid_ArslAvg, notnan_idx)
Dominance_avg = np.take(vid_DomAvg, notnan_idx)

Vidlist_expID = []
Vidlist_title = []
Vidlist_artiste = []
Vidlist_valence = []
Vidlist_arousal = []
Vidlist_dominance = []
Vidlist_sujnums   = []
Vidlist_vallabel  = []
Vidlist_arousallabel = []
Vidlist_dominancelabel = []
Vidlist_valclass  = []
Vidlist_arousalclass = []
Vidlist_dominanceclass = []
Vidlist_VAD = []

for vidx, vcurr in enumerate(VidExp_all):

    Eindx    = [cnt for cnt, expcurr in enumerate(ExpID_all) if expcurr == vcurr]
    Val_sel  = np.take(valence_all, Eindx)
    Val_mean = np.mean(Val_sel)                # Calculate the mean valence for current video.
    Arousal_sel = np.take(arousal_all, Eindx)
    Arousal_mean = np.mean(Arousal_sel)        # Calculate the mean arousal for current video
    Dominance_sel = np.take(domin_all, Eindx)
    Dominance_mean = np.mean(Dominance_sel)    # Calculate the mean dominance for current video.
    Vidsuj = np.take(SujID_all, Eindx)
    numsuj = len(Eindx)                        # The number of subjects that rated current video.
    vidcurr_suj = " ".join(str(x) for x in Vidsuj)

    vadcurr = []

    if Val_mean <= 5:
        Vallabel = 'Neg'
        Valclass = 0
        vadcurr.append(Valclass)
    elif Val_mean > 5:
        Vallabel = 'Pos'
        Valclass = 1
        vadcurr.append(Valclass)

    if Arousal_mean <= 5:
        Arousal_label = 'Low'
        Arousal_class = 0
        vadcurr.append(Arousal_class)
    elif Arousal_mean > 5:
        Arousal_label = 'High'
        Arousal_class = 1
        vadcurr.append(Arousal_class)

    if Dominance_mean <= 5:
        Dominance_label = 'Low'
        Dominance_class = 0
        vadcurr.append(Dominance_class)
    elif Dominance_mean > 5:
        Dominance_label = 'High'
        Dominance_class = 1
        vadcurr.append(Dominance_class)

    vidcurr_vad = " ".join(str(x1) for x1 in vadcurr)

    Vidlist_sujnums.append(vidcurr_suj)
    Vidlist_expID.append(vcurr)
    Vidlist_artiste.append(Artist_all[vidx])
    Vidlist_title.append(Title_all[vidx])
    Vidlist_valence.append(Val_mean)
    Vidlist_arousal.append(Arousal_mean)
    Vidlist_dominance.append(Dominance_mean)

    Vidlist_vallabel.append(Vallabel)
    Vidlist_arousallabel.append(Arousal_label)
    Vidlist_dominancelabel.append(Dominance_label)

    Vidlist_valclass.append(Valclass)
    Vidlist_arousalclass.append(Arousal_class)
    Vidlist_dominanceclass.append(Dominance_class)
    Vidlist_VAD.append(vidcurr_vad)

VideoDF_data = {'ExperimentID': list(Vidlist_expID), 'Video_Artist': Vidlist_artiste, 'Video_title': Vidlist_title, 'ParticipantsID': Vidlist_sujnums,
                'Average_Valence': Vidlist_valence, 'Average_Arousal': Vidlist_arousal, 'Average_dominance': Vidlist_dominance, 'Valence_label': Vidlist_vallabel,
                'Valence_class': Vidlist_valclass, 'Arousal_label': Vidlist_arousallabel, 'Arousal_class': Vidlist_arousalclass, 'Dominance_label': Vidlist_dominancelabel,
                'Dominance_class': Vidlist_dominanceclass, 'VAD_model': Vidlist_VAD}
VideoDF = pd.DataFrame(VideoDF_data)
VideoInfo_title = 'Video_VAD_info_corrige.csv'
VideoDF.to_csv(os.path.join(xlfile_path, VideoInfo_title))

#%% Create a scatterplot of the VAD model.
fig = plt.figure()
ax  = fig.add_subplot(projection='3d')

ax.scatter(Vidlist_valence, Vidlist_arousal, Vidlist_dominance)
ax.set_xlabel('Mean Valence')
ax.set_ylabel('Mean Arousal')
ax.set_zlabel('Mean Dominance')
figname = 'VAD_scatterplot'
figname_path = 'Figures/'+figname
fig.savefig(figname_path)
plt.close(fig)

#%% Create a plot of the VAD model.

axhi_max = np.ceil(np.max([np.max(Vidlist_valence), np.max(Vidlist_arousal), np.max(Vidlist_dominance)]))

be = mpl.pyplot.get_backend()
print(f'The current backend is {be}')

plt.figure()
plt.xlim((0,9))    # Set x-axis range
plt.ylim((0,9))    # Set y-axis range
plt.plot([5,5], [0,9], linewidth=3, color='black')
plt.plot([0,9], [5,5], linewidth=3, color='black')
plt.grid(True)
# ax1.set_xlabel([2.5, 7.5], labels=['Low', 'High'])
# ax1.set_ylabel([2.5, 7.5], labels=['Low', 'High'])
plt.xlabel('Mean Valence')
plt.ylabel('Mean Arousal')
plt.title('Valence-Arousal Model (2D)')
plt.scatter(Vidlist_valence, Vidlist_arousal)
plt.show()

plt.figure()
plt.xlim((0,9))    # Set x-axis range
plt.ylim((0,9))    # Set y-axis range
plt.plot([5,5], [0,9], linewidth=3, color='black')
plt.plot([0,9], [5,5], linewidth=3, color='black')
plt.grid(True)
# ax1.set_xlabel([2.5, 7.5], labels=['Low', 'High'])
# ax1.set_ylabel([2.5, 7.5], labels=['Low', 'High'])
plt.xlabel('Mean Valence')
plt.ylabel('Mean Dominance')
plt.title('Valence-Dominance Model (2D)')
plt.scatter(Vidlist_valence, Vidlist_dominance)
plt.show()

plt.figure()
plt.xlim((0,9))    # Set x-axis range
plt.ylim((0,9))    # Set y-axis range
plt.plot([5,5], [0,9], linewidth=3, color='black')
plt.plot([0,9], [5,5], linewidth=3, color='black')
plt.grid(True)
# ax1.set_xlabel([2.5, 7.5], labels=['Low', 'High'])
# ax1.set_ylabel([2.5, 7.5], labels=['Low', 'High'])
plt.xlabel('Mean Arousal')
plt.ylabel('Mean Dominance')
plt.title('Arousal-Dominance Model (2D)')
plt.scatter(Vidlist_arousal, Vidlist_dominance)
plt.show()