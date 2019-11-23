import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
import numpy as np
import csv
import pandas as pd

# rows = []
# with open('training.csv', newline='\n') as csvfile:
#     reader = csv.reader(csvfile, delimiter=',')
#     for row in reader:
#         rows.append(row)
#
# X = []
# y = []
# for i in range(len(rows)):
#     if i == 0:  # Skip header!
#         continue
#     X.append(np.asarray(row[30].split(" "),dtype=np.float32).reshape(96,96))
#     y.append(row[0:30])
X = []
y = []
data = pd.read_csv('training.csv')
for i in range(0,5000):
    row = data.loc[i].tolist()
    X.append(np.asarray(row[30].split(" "),dtype=np.float64).reshape(96,96))
    y.append(np.asarray(row[0:30],dtype=np.float64))
#print(data.columns)
#print(data.values)
X_train = np.asarray(X[0:4000])
X_train = X_train.reshape(4000,96,96,1).astype('float64')
X_test = np.asarray(X[4000:5000])
y_train = np.asarray(y[0:4000]).astype('float64')
y_test = np.asarray(y[4000:5000])

model = Sequential()
model.add(Conv2D(60,kernel_size=(3,3),activation='relu',input_shape=(96,96,1)))
model.add(Conv2D(120,(3,3),activation='relu'))
model.add(Flatten())
model.add(Dense(240,activation='relu'))
model.add(Dense(30,activation='linear'))

model.compile(loss='mean_squared_error',optimizer='adam')
model.fit(X_train,y_train,batch_size = 15,epochs = 10,verbose = 1)