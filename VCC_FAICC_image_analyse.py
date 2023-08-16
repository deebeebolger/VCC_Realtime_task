import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from kneed import KneeLocator
import shutil
from PIL import Image

"""
This script groups the images of the FAICC database according to their ratings of:
- Valence
- Arousal
These ratings will decide which images will be presented together for the 60second interval.
The FAICC database is a database comprising 301 images related to climate change.
The images were given ratings of valence, arousal and relevance by 106 participants.
For these ratings a 9-point Likert scale was used.
Arousal: 1 ==> calming feeling, 9 ==> exciting feeling
Valence: 1 ==> negative feeling, 9 ==> positive feeling 
Relevance: 1 ==> irrelevant to climate change, 9 ==> relevant to climate change.
Reference: Ottavi, S., Roussel, S. & Airelle, S. 2021, The French affective images of climate change (FAICC): A Dataset with Relevance and Affective Ratings, 
           Frontiers in Psychology, 12. DOI=10.3389/fpsyg.2021.650650. 

In our presentation, we focus on Valence and arousal as these descriptors were also used to construct the DEAP database.
"""

def FindClustNum_elbow(fscaled):

    kmeans_kwargs = { "init": "random", "n_init": 10, "max_iter": 300, "random_state": 42 }
    # A list holds the SSE values for each k
    sse = []

    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(fscaled)
        sse.append(kmeans.inertia_)

    plt.style.use("fivethirtyeight")
    plt.plot(range(1, 11), sse)
    plt.xticks(range(1, 11))
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")
    plt.show()

def image_save(dir_pics):
    Idir_contents = os.listdir((dir_pics))
    pjpg = [jpgcurr for jpgcurr in Idir_contents if '.jp' in jpgcurr]

    for pcnt, pcurr in enumerate(pjpg):
        currpath = os.path.join(dir_pics, pcurr)
        im = Image.open(currpath)
        pbis = pcurr.split('.')
        new_title = pbis[0]+'.png'
        im.save(os.path.join(dir_pics, new_title),"PNG")

data_path = '/Users/bolger/Documents/work/Projects/Visions_ClimateChange/FAICC_Database'
fname     = 'DataBase - FAICC.xlsx'
fullpath  = os.path.join(data_path, fname)

dfIn = pd.read_excel(fullpath, sheet_name='Rating data')
ImageID = list(dfIn['Image ID'])
Arousal_mean = list(dfIn['Arousal Mean'])
Valence_mean = list(dfIn['Valence Mean'])
Relevance_mean = list(dfIn['Relevance Mean'])

Arousal_mean = Arousal_mean[1:-1]   # take out the beginning nan value
Valence_mean = Valence_mean[1:-1]
Relevance_mean = Relevance_mean[1:-1]
ImageID = ImageID[1:-1]

sns.displot(Arousal_mean)
sns.displot(Valence_mean)
sns.displot(Relevance_mean)
sns.displot(x=Arousal_mean, y=Valence_mean)

##%% Carry out Kmeans clustering of the images based on Arousal, Valence and Relevance features

features = np.transpose(np.vstack((Arousal_mean, Valence_mean, Relevance_mean)))
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)  # scale features values to have 0 mean and std =1

FindClustNum_elbow(features_scaled)

clusterN = 6
kmeans = KMeans(init="random", n_clusters=clusterN, n_init=10, max_iter=300, random_state=42)
kmeans.fit(features_scaled)

##% Scatter-plot of the features and the final centroids.

feature_class = kmeans.labels_
colors = ['red' if ft == 0 else 'green' if ft == 1 else 'blue' if ft == 2 else 'yellow' if ft == 3 else
            'orange' if ft == 4 else'black' for ft in list(feature_class)]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(features_scaled[:,0], features_scaled[:,1], features_scaled[:,2], s=50, c=colors)
ax.set_xlabel('Mean Arousal')
ax.set_ylabel('Mean Valence')
ax.set_zlabel('Mean Relevance')
plt.show()

##%% Divide the images into cluster groups.
dir_orig = '/Users/bolger/Documents/work/Projects/Visions_ClimateChange/FAICC_Database/Pictures'
diro_contents = os.listdir((dir_orig))
class_unique = np.unique(feature_class)

for classcurr in class_unique:
    CIndx = [classIndx for classIndx, ccurr in enumerate(feature_class) if ccurr==classcurr]
    Image_curr = [ImageID[index] for index in CIndx]
    dirname = 'Images_Class'+str(classcurr+1)
    newpath = os.path.join('../Image_classify/FAICC_Images', dirname)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    dir_dest = newpath

    # Files to move
    for fcount, Icurr in enumerate(Image_curr):
        x_png =  str(int(Icurr))+'.png'
        pic2move = [piccur for piccur in diro_contents if x_png == piccur]
        if pic2move == []:
            print(f'Current image {x_png} does not exist.')
        else:
            old_file = os.path.join(dir_orig, pic2move[0])
            shutil.copy(old_file, dir_dest)


