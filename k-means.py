import PIL
from PIL import Image
import urllib.request
import io
import sys
import random
import time

def setupClusters(pix,img,means):
    clusters = {}
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            rgb = pix[x, y]
            if rgb not in clusters:
                temp = []
                for j in range(len(means)):
                    rgbr = means[j]
                    dis = ((rgb[0] - rgbr[0]) ** 2 + (rgb[1] - rgbr[1]) ** 2 + (rgb[2] - rgbr[2]) ** 2)
                    temp.append((dis, j))
                clusters[rgb] = min(temp)[1]
    return clusters

def createNewClusters(oldclusters,means):
    newclus = {}
    for rgb in oldclusters:
        temp = []
        for j in range(len(means)):
            rgbr = means[j]
            dis = ((rgb[0] - rgbr[0]) ** 2 + (rgb[1] - rgbr[1]) ** 2 + (rgb[2] - rgbr[2]) ** 2)
            temp.append((dis, j))
        newclus[rgb] = min(temp)[1]
    return newclus

def calculateMean(clusters,k,colors):
    sums = [[0,0,0] for i in range(k)]
    counts = [0 for i in range(k)]
    for cluster in clusters:
        clu = clusters[cluster]
        sums[clu][0] += cluster[0] * colors[cluster]
        sums[clu][1] += cluster[1] * colors[cluster]
        sums[clu][2] += cluster[2] * colors[cluster]
        counts[clu] += colors[cluster]
    for t in range(len(counts)):
        if counts[t] == 0:
            counts[t] += 1
    return [(sums[i][0]/(counts[i]+1),sums[i][1]/(counts[i]+1),sums[i][2]/(counts[i]+1)) for i in range(k)]

def checkClusters(cluster,newcluster):
    changed = False
    for key in cluster:
        if cluster[key] != newcluster[key]:
            changed = True
            break
    return changed

def Complete(means):
    if len(means) == 0:
        return False
    count = {}
    for mean in means:
        if mean in count:
            count[mean] += 1
        else:
            count[mean] = 1
    return count[max(count,key=count.get)] == 1

def inRange(pos,img):
    if pos[0] >= 0 and pos[0] < img.size[0] and pos[1] >= 0 and pos[1] < img.size[1]:
        return True
    return False

def floodfill(ned,explored,meandict,img):
    stack = [ned]
    while stack:
        pos = stack.pop(len(stack)-1)
        explored.add(pos)
        children = [(pos[0], pos[1] - 1), (pos[0], pos[1] + 1), (pos[0] - 1, pos[1]), (pos[0] + 1, pos[1]),
                    (pos[0] - 1, pos[1] - 1), (pos[0] + 1, pos[1] - 1), (pos[0] + 1, pos[1] + 1),
                    (pos[0] - 1, pos[1] + 1)]
        for child in children:
            if inRange(child, img) and child not in explored and meandict[child] == meandict[pos]:
                stack.append(child)
    return explored


k, URL = sys.argv[1:]
k = int(k)
f = ''
img = ''
if 'http' not in URL:
    img = Image.open(URL)
else:
    f = io.BytesIO(urllib.request.urlopen(URL).read())
    img = Image.open(f)
pix = img.load()
print('Size: ',img.size[0],' x ',img.size[1])
print('Pixels: ',img.size[0]*img.size[1])
colors = {}
for x in range(img.size[0]):
    for y in range(img.size[1]):
        pixel = pix[x,y]
        if pixel not in colors:
            colors[pixel] = 1
        else:
            colors[pixel] += 1
print('Distinct pixel count: ',len(colors))
mau = max(colors,key = colors.get)
print('Most common pixel: ',mau,' => ',colors[mau])
means = []
while not Complete(means):
    means = [pix[random.randint(0,img.size[0]-1),random.randint(0,img.size[1]-1)] for u in range(k)]
print()
clusters = setupClusters(pix,img,means)
means = list(calculateMean(clusters,k,colors))
while True:
    newclusters = createNewClusters(clusters,means)
    if not checkClusters(clusters,newclusters):
        break
    newmeans = calculateMean(newclusters,k,colors)
    means = list(newmeans)
    clusters = dict(newclusters)
counts = [0 for i in range(k)]
for x in range(img.size[0]):
    for y in range(img.size[1]):
        counts[clusters[pix[x,y]]] += 1
# print('Final Counts: ',counts)
print('Final means: ')
for t in range(k):
    print(str(t+1)+': ',means[t],' => ',counts[t])
print()
meandict = {}
for x in range(img.size[0]):
    for y in range(img.size[1]):
        pi = pix[x,y]
        mean = means[clusters[pi]]
        meandict[(x,y)] = clusters[pi]
        pix[x,y] = (int(mean[0]),int(mean[1]),int(mean[2]))
img.save("kmeans/{}.png".format('2021spatil'), "PNG")
explored = set()
regioncounts = [0 for i in range(k)]
for pixel in meandict:
    if pixel not in explored:
        explored = floodfill(pixel,explored,meandict,img)
        regioncounts[meandict[pixel]] += 1
print('Region Counts: ', regioncounts)