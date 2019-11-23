from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
from sklearn import preprocessing
import numpy as np
import pandas as pd
from statistics import median

def getDataLabeled():
    x = []
    y = []
    input = open("training.csv").read().split("\n")
    count = 0
    for i in input:
        if count != 0:
            inputArray = i.split(",")
            if len(inputArray)==9: #number of features + number of labels
                y.append(inputArray.pop(0))
                inputArray.pop(5)
                for p in range(0,7):
                    if inputArray[p] != '':
                        inputArray[p] = float(inputArray[p])
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
            if(len(inputArray)==8): #number of features
                inputArray.pop(5)
                for p in range(0,7):
                    if inputArray[p] != '':
                        inputArray[p] = float(inputArray[p])
                x.append(inputArray)
            else:
                print(len(inputArray))
    return x

def fillinMissingAge(dataset):
    agesdict = {}
    for i in range(1,4):
        for j in range(0,2):
            guess = [x[2] for x in dataset if x[0]==i and x[1] == j and x[2] != '']
            med = median(guess)
            agesdict[(i,j)] = med
    for y in dataset:
        if y[2]=='':
            y[2] = agesdict[(int(y[0]),int(y[1]))]
    return dataset

def generateOutputFile(y_test):
    with open('outer.csv', 'w') as f:
        f.write("id,solution\n")
        for i in range(len(y_test)):
            f.write(str(i+1)+","+str(y_test[i]+"\n"))

x,y = getDataLabeled()
x = fillinMissingAge(x)
x = preprocessing.scale(x)
X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=0.1,random_state=109)
svc = svm.SVC(kernel = 'linear',gamma=.001,C=.01)
# param = {}
# param['kernel'] = ['linear','poly','sigmoid']
# param['gamma'] = [.001,.01,.1,1]
# param['C'] = [.001,.01,.1,1]
# g = GridSearchCV(svc,param)
svc.fit(X_train,y_train)
# print("Score: ",end="")
# print(g.best_score_)
# print(g.best_params_)
# svc.fit(X_train, y_train)
# train_accuracy = round(svc.score(X_train, y_train) * 100, 2)
# validation_accuracy = round(svc.score(X_test, y_test) * 100, 2)
# print(train_accuracy)
# print(validation_accuracy)
xin = fillinMissingAge(getDataUnlabeled())
yf = svc.predict(preprocessing.scale(xin))
generateOutputFile(yf)
# model = svm.SVC()
# model.fit(X_train,y_train)
# y_p = model.predict(X_test)
# print("Accuracy:",metrics.accuracy_score(y_test, y_p))

