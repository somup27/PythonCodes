import math
import sys

def dot(inp,wei,transfer):
    su = 0.0
    for u in range(len(inp)):
        su += inp[u] * wei[u]
    if transfer == 'T1':
        return su
    elif transfer == 'T2':
        if su > 0:
            return su
        else:
            return 0
    elif transfer == 'T3':
        return 1 / (1 + math.exp(-1 * su))
    elif transfer == 'T4':
        return (2/(1+math.exp(-1 * su))) - 1

args = sys.argv[1:]
weightsfile = open(args[0],'r')
nnweights = [args[2:]]
lines = weightsfile.readlines()
ind = 0
for i in range(len(lines)):
    weights = [float(x) for x in lines[i].split()]
    if i == len(lines) - 1:
        nnweights.append(weights)
    else:
        nodes = int(len(weights)/len(nnweights[ind]))
        temp = []
        oriind = 0
        endind = len(nnweights[ind])
        while endind <= len(weights):
            temp.append(weights[oriind:endind])
            oriind += len(nnweights[ind])
            endind += len(nnweights[ind])
        nnweights.append(temp)
        ind += 1
nnweights.pop(0)
output = []
temp = [float(x) for x in args[2:]]
for p in range(len(nnweights)):
    layer = nnweights[p]
    if p == len(nnweights)-1:
        if len(temp) != len(layer):
            for y in range(len(layer)):
                output.append(temp[0] * layer[y])
        else:
            for y in range(len(layer)):
                output.append(temp[y] * layer[y])
    else:
        inp = list(temp)
        temp = []
        for i in range(len(layer)):
            temp.append(dot(inp,layer[i],args[1]))
print(output)



