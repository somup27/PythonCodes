from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
from sklearn import preprocessing
import numpy as np

def generateOutputFile(y_test):
    with open('outer.csv', 'w') as f:
        f.write("id,solution\n")
        for i in range(len(y_test)):
            f.write(str(i+1)+","+str(y_test[i]+"\n"))

def getDataLabeled():
    x = []
    y = []
    input = open("training.csv").read().split("\n")
    count = 0
    for i in input:
        if count != 0:
            inputArray = i.split(",")
            if len(inputArray)==6: #number of features + number of labels
                y.append(inputArray.pop(0))
                x.append(inputArray)
            else:
                print(len(inputArray))
        count = count + 1
    return x,y

def getDataUnlabeled():
    x = []
    input = open("testing.csv").read().split("\n")
    for index, i in enumerate(input):
        if index != 0:
            inputArray = i.split(",")
            if(len(inputArray)==5): #number of features
                x.append(inputArray)
            else:
                print(len(inputArray))
    return x

x,y = getDataLabeled()
X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=0.4,random_state=109)
X_train = preprocessing.scale(X_train)
param = {}
param['kernel'] = ['linear','rbf','poly','sigmoid']
param['gamma'] = 10. ** np.arange(-5,4)
param['C'] = 10. ** np.arange(-3,8)
g = GridSearchCV(model,param)
g.fit(X_train,y_train)
print("Score: ",end="")
print(g.best_score_)
print(g.best_params_)
# model.fit(X_train,y_train)
# x = preprocessing.scale(getDataUnlabeled())
# y = model.predict(x)
# generateOutputFile(y)
