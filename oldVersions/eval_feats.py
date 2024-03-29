import numpy as np
import math
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from keras.models import model_from_json
from scipy.stats import pearsonr
import sys
inputfile = sys.argv[1]

#load dataset
f = open(inputfile, 'r')
data = f.readlines()
f.close()
dataset = []
for line in data:
	if '#LGA' in line:
		continue
	dataset.append(line.split(' '))


features = len(dataset[0])-2
X = []
Y = []
for i in range(len(dataset)):
	
	x = []
	for j in range(0,1+features):
		if j ==  0:
			Y.append(float(dataset[i][0]))
			
		else:
			s = dataset[i][j]
			x.append(float(s[(1+s.index(":")):]))
		
	X.append(x)
#determine indices of different sequences
firstS = dataset[0][features+1]
firstID = firstS[1:firstS.index(":")]
dict = {firstID:[0]}
for i in range (1,len(dataset)):
	s = dataset[i][features+1]
	id = s[1:(s.index(":"))]
	if id in dict:
		dict[id] = dict[id] + [i]
	else:
		dict[id] = [i]



# Fit the model

X = np.asarray(X)
#print(X[0,:])
#print(X.shape)

Y = np.asarray(Y)
#print(Y[0])
#print(Y.shape)







#determining loss and correlation coefficient
loss = []
IDs = []
predicted = []
actualYs = []
maxY = float("-inf")
maxYind = 0
for ID in dict:
	IDs.append(ID)
	p = []
	a = []
	l = []
	maxFeats = np.zeros(features)
	maxFeatsind = [0] * features
	maxY = float("-inf")
	maxYind = 0
	for i in dict[ID]:#for each index for that ID
		for j in range(features): #for each feature
			if X[i][j]>maxFeats[j]:
 				maxFeats[j] = X[i][j]
				maxFeatsind[j] = i
			
		p.append(X[i])
	
		if Y[i]>maxY:
			maxY = Y[i]
			maxYind = i
		a.append(Y[i])
	for i in range(features):
		l.append(abs(maxY-Y[maxFeatsind[i]]))
	

	loss.append(l)
	predicted.append(np.asarray(p))
	actualYs.append(np.asarray(a))

correlation_scipy = []
for i in range(len(IDs)):#for each ID
	c = []
	for j in range(features):
		corr, p_value = pearsonr(predicted[i][:,j],actualYs[i])
		c.append(corr)
	correlation_scipy.append(c)


npL = np.asarray(loss)
npC = np.asarray(correlation_scipy)	

avgL = np.sum(npL,axis = 0)/len(IDs)
avgC = np.sum(npC,axis = 0)/len(IDs)


for i in range(len(IDs)):
	for j in range(features):
		print(IDs[i]+", feature "+ str(j+1)+"  - loss: %.2f, correlation: %f" %(loss[i][j], correlation_scipy[i][j]))

for i in range(len(avgL)):
	print("feature "+ str(i+1) + " - average loss: %f, average correlation: %f" %(avgL[i],avgC[i]))
#print(correlation_scipy)
