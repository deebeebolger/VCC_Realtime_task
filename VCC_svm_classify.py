from sklearn import svm
from sklearn.impute import SimpleImputer
import numpy as np

train_y = []
train_a = []
train_x = np.genfromtxt('../Image_classify/train.csv', delimiter=',')
f = open("../Image_classify/labels_0.dat", "r")
for i in f:
	train_y.append(i)

train_y = np.array(train_y).astype(float)
train_y = train_y.astype(int)
train_x = np.array(train_x)

imp_x = SimpleImputer(missing_values=np.nan, strategy='mean')
imp_x = imp_x.fit(train_x)
Xtrain_imp = imp_x.transform(train_x)

clf = svm.SVC()
clf.fit(Xtrain_imp, train_y)

f = open("../Image_classify/labels_1.dat", "r")
for i in f:
	train_a.append(i)
train_a = np.array(train_a).astype(float)
train_a = train_a.astype(int)
#print "arousal",train_a[1040:1280]
#print "train_x",len(train_x[0:26])
clf1 = svm.SVC()
clf1.fit(train_x, train_a)
#print test_a
predict_al = clf1.predict(train_x)
#print "alrosal",predict_al
predict_val = clf.predict(np.transpose(Xtrain_imp))
#print "valence",predict_val
val_count = al_count = 0
for i in range(len(train_y)):
	if train_y[i] == predict_val[i]:
		val_count = val_count+1
	if train_a[i] == predict_al[i]:
		al_count = al_count+1

print(f"predicted valence is {(float(val_count)/len(train_y))*100}")
print(f"predicted arousal is {(float(al_count)/len(train_y))*100}")