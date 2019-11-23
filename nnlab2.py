import math
import sys
import random

activations = {"T1": lambda x: x, "T2": lambda x: x if x>0 else 0,"T3": lambda x: 1/(1+math.e**-x)}
derivs = {"T3": lambda y:y*(1-y)}
activ = activations["T3"]
deriv = derivs["T3"]

def dot(s1,s2):
    return sum([s1[i] * s2[i] for i in range(len(s1))])

def setupNN():
    args = sys.argv[1:]
    f = open(args[0],'r')
    lines = f.readlines()
    cases = []
    for line in lines:
        pieces = line.split()
        arrow = False
        inp = []
        out = ''
        for piece in pieces:
            if piece == '=>':
                arrow = True
            elif arrow:
                out = int(piece)
            else:
                inp.append(int(piece))
        cases.append([inp,out])
    inCt = len(cases[0][0]) + 1
    layerct = [inCt,2,1,1]
    nnweights = []
    temp = []
    for t in range(inCt):
        temp.append(random.uniform(-2,2))
        temp.append(random.uniform(-2,2))
    nnweights.append(temp)
    nnweights.append([random.uniform(-2,2),random.uniform(-2,2)])
    nnweights.append([random.uniform(-2,2)])
    return nnweights,cases,layerct

def feed(case,nn,layers):
    nodes = []
    ind = 0
    inp = list(case[0])
    inp.append(1)
    nodes.append(inp)
    for t in range(1,len(layers)):
        nod = layers[t]
        temp = []
        for p in range(nod):
            wei = nn[ind][p::nod]
            ou = dot(inp,wei)
            if t == len(layers)-1:
                temp.append(ou)
            else:
                temp.append(activ(ou))
        nodes.append(temp)
        inp = list(temp)
        ind += 1
    error = case[1] - nodes[len(nodes)-1][0]
    return nodes, error

def back(nn,nodes,layers,expected):
    Enodes = [list(no) for no in nodes]
    grads = [list(n) for n in nn]
    outerror = expected - Enodes[len(Enodes)-1][0]
    Enodes[len(Enodes)-1][0] = outerror
    # Enodes[len(Enodes)-2][0] = outerror * nn[len(nn)-1][0] * deriv(nodes[len(nodes)-2][0])
    for g in range(2,len(Enodes)):
        ind = len(Enodes) - g
        before = ind + 1
        size = layers[ind]
        beforesize = layers[before]
        tempind = 0
        for q in range(size):
            sum = 0
            tem = tempind
            for y in range(beforesize):
                sum += Enodes[before][y] * nn[ind][tem]
                tem += 1
            Enodes[ind][q] = sum * deriv(nodes[ind][q])
            tempind = tem
    grads[len(grads)-1][0] = -1* nodes[len(grads)-1][0] * outerror
    for y in range(len(grads)-1):
        gradind = len(grads) - 2 - y
        gr = len(grads[gradind])
        aftersize = layers[gradind+1]
        tempbefore = 0
        tempafter = 0
        for h in range(gr):
            grads[gradind][h] = -1 * nodes[gradind][tempbefore] * Enodes[gradind+1][tempafter]
            tempafter += 1
            if tempafter % aftersize == 0:
                tempafter = 0
                tempbefore += 1
    for a in range(len(grads)):
        for b in range(len(grads[a])):
            nn[a][b] -= grads[a][b] * .03
    return nn

broken = False
complete = False
while not complete:
    nn, training, layers = setupNN()
    # nn = [[1,1,1,1,1,1],[1,1],[1]]
    error = [10] * len(training)
    for i in range(600000):
        nodes, e = feed(training[i%len(training)],nn,layers)
        error[i%len(training)] = abs(e)
        et = sum(error)
        if i == 50000:
            print('Testnum 50000 has an error of '+str(et))
            if et > .3 and layers[0] == 2:
                broken = True
                break
            if et > .8 and layers[0] == 3:
                broken = True
                # print('Starting over')
                break
            elif layers[0] == 4 and et > 1.6:
                broken = True
                # print('Starting over')
                break
        if i % 10000 == 0:
            print()
            print('Errors: ', end='')
            print(error)
            print('Layer cts: ', end='')
            print(layers)
            print('Weights:')
            for we in nn:
                print(we)
            print()
            for u in range(len(training)):
                case = training[u]
                print(case[0], end='')
                print(': ', end='')
                check, ery = feed(case, nn, layers)
                print(check[len(check) - 1][0])
        # elif i == 599999:
        #     print('Final error: '+str(et))
        nn = back(nn,nodes,layers,training[i%len(training)][1])
    if not broken:
        print()
        print('Errors: ',end='')
        print(error)
        print('Layer cts: ',end='')
        print(layers)
        print('Weights:')
        for we in nn:
            print(we)
        print()
        for u in range(len(training)):
            case = training[u]
            print(case[0],end='')
            print(': ',end='')
            check,ery = feed(case,nn,layers)
            print(check[len(check)-1][0])
        complete = True
    else:
        broken = False