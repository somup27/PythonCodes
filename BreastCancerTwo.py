import random
import math

class Node():
    def __init__(self,left,right,col,num,data):
        self.left_child = left
        self.right_child = right
        self.bestcol = col
        self.bestnum = num
        self.label = data

        def left(self):
            return self.left_child

        def right(self):
            return self.right_child

        def QueC(self):
            return self.bestcol

        def QueN(self):
            return self.bestnum

class Leaf():
    def __init__(self,rows):
        self.label = [rows[x][len(rows[x])-1] for x in range(len(rows))]

#for testing data (no labels)
def getDataUnlabeled():
    x = []
    input = open("testing.csv").read().split("\n")
    for index, i in enumerate(input):
        if index == 0: continue
        inputArray = i.split(",")
        if(len(inputArray)==7): #number of features
            x.append(inputArray)
        else:
            print(len(inputArray))
    return x

def countLabels(data):
    zero = 0
    one = 0
    for x in data:
        label = x[len(x)-1]
        if label == "0": zero = zero + 1
        if label == "1": one = one + 1
    return zero,one

#for training data (with labels)
def getDataLabeled():
    x = []
    input = open("training.csv").read().split("\n")
    count = 0
    for i in input:
        if count != 0:
            inputArray = i.split(",")
            if len(inputArray)==8: #number of features + number of labels
                x.append(inputArray)
            else:
                print(len(inputArray))
        count = count + 1
    train = []
    v = []
    for i in range(160):
        f = random.randint(0,len(x)-1)
        train.append(x[f])
    for s in range(50):
        t = random.randint(0,len(x)-1)
        v.append(x[s])
    return train,v

#pass array of labels and method will generate output txt
def generateOutputFile(y_test):
    with open('outer.csv', 'w') as f:
        f.write("id,Survived\n")
        for i in range(len(y_test)):
            f.write(str(i+1)+","+str(y_test[i]+"\n"))

def gini_impurity(data):
    impurity = 0
    z,o = countLabels(data)
    temp = float(z)/len(data)
    impurity = impurity + temp ** 2
    temp = float(o) / len(data)
    impurity = impurity + temp ** 2
    return 1-impurity

def information_gain(current,left,right):
    current_impurity = gini_impurity(current)
    proportion = float(len(left))/(len(left)+len(right))
    return current_impurity - proportion*gini_impurity(left)-(1-proportion)*gini_impurity(right)

def split(data,col,num):
    left = []
    right = []
    for i in data:
        numb = i[col]
        if numb<=num:
            left.append(i)
        else:
            right.append(i)
    return left,right

def best_split(dataset):
    bestig = 0
    bestnum = 0
    bestcol = 0
    for dat in dataset:
        for i in range(len(dat)-1):
            templeft,tempright = split(dataset,i,dat[i])
            if len(templeft)==0 or len(tempright)==0:
                continue
            tempig = information_gain(dataset,templeft,tempright)
            if tempig>bestig:
                bestig = tempig
                bestcol = i
                bestnum = dat[i]
    return bestig,bestcol,bestnum

def generate_tree(dataset,count):
    if count ==8 : return Leaf(dataset)
    if len(dataset) == 0: return None
    ig,col,num = best_split(dataset)
    if ig < 0.01:
        return Leaf(dataset)
    left,right = split(dataset,col,num)
    lefttree = generate_tree(left,count+1)
    righttree = generate_tree(right,count+1)
    return Node(lefttree,righttree,col,num,dataset)

def predict(data,tree):
    if isinstance(tree,Leaf):
        return checker(tree.label)
    if data[tree.bestcol]<=tree.bestnum:
        return predict(data,tree.left_child)
    else:
        return predict(data,tree.right_child)

def checker(data):
    onecounter = 0
    zerocounter = 0
    for dat in data:
        if dat == "1":
            onecounter = onecounter+1
        else: zerocounter = zerocounter +1
    if onecounter > zerocounter: return "1"
    elif zerocounter>onecounter: return "0"
    else: return str(random.randint(0,1))

def calcAcc(tree, valida):
    true = 0
    false = 0
    for x in valida:
        label = predict(x,tree)
        if label == x[len(x)-1]: true += 1
        else: false += 1
    total = true + false
    return true/total

X_train,v = getDataLabeled()
X_test = getDataUnlabeled()

tree = generate_tree(X_train,0)
print(calcAcc(tree,v))

y_test = []
for x in X_test:
    y_test.append(predict(x,tree))



# TODO: Write some ML for gini_impurity, information_gain, best_split, split, generate_tree
# TODO: use model to generate y_test from X_test
generateOutputFile(y_test)