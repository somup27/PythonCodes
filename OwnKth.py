import math

def dist(a, b):
    sum = 0
    for i in range(len(a)):
        temp = a[i] - b[i]
        sum = sum + temp ** 2
    return math.sqrt(sum)


class KNN():
    def fit(self, xtrain, ytrain):
        self.xtrain = xtrain
        self.ytrain = ytrain

    def predict(self, xtest):
        return self.neigh(xtest)

    def neigh(self, dat):
        bestdist = dist(dat, self.xtrain[0])
        bestindex = 0
        for i in range(1, len(self.xtrain)):
            dis = dist(dat, self.xtrain[i])
            if dis < bestdist:
                bestdist = dis
                bestindex = i
        return self.ytrain[bestindex]

#dataset [cash,type(3),color(3)]
#0 - sedan, blue
#1 - SUV, red
#2 - van, green
#Wanted - (SUV or Green) and <=30000
xtrain = [[4,0,2],[2,1,1],[1,1,2],[3,0,2],[2,2,0]]
ytrain = ["No","Yes","Yes","Yes","No"]

clas = KNN()
clas.fit(xtrain,ytrain)

xtest = [int(x) for x in input().split()]
print(clas.predict(xtest))