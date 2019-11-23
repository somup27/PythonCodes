import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
import numpy as np
import csv

rows = []
with open('train.csv', newline='\n') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        rows.append(row)

X = []
y = []
for i in range(len(rows)):
    if i == 0:  # Skip header!
        continue
    X.append(row[30].split(" "))
    y.append(row[0:30])

# split X and y into train and test set
X_train = np.asarray(X[0:4000])
X_test = np.asarray(X[4000:5000])
y_train = np.asarray(y[0:4000])
y_test = np.asarray(y[4000:5000])

model = Sequential()
model.add(Conv2D(60,kernel_size=(3,3),activation='relu',input_shape=(96,96)))
model.add(Conv2D(120,(3,3),activation='relu'))
model.add(Flatten())
model.add(Dense(240,activation='relu'))
model.add(Dense(30,activation='linear'))

model.compile(loss='mean_squared_error',optimizer='adam')
model.fit(X_train,y_train,batch_size = 15,epochs = 10,verbose = 1)
# load in data from test.csv
# generate y_test where y_test is a matrix that is 2049x30 (2049 test images and 30 output features)

output = []
header = []
header.append("ImageID.FeatureID")
header.append("Value")
output.append(header)
for i in range(2049):
    for x in range(30):
        row = []
        row.append(str(i + 1) + "." + str(x + 1))  # We start Ids at 1, so we need to add 1 to each value
        row.append(y_test[i][x])
        output.append(row)

with open('submission.csv', 'w', newline='\n') as f:
    writer = csv.writer(f)
    writer.writerows(output)