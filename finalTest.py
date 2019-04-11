import numpy as np
import re
import csv
import math
import datetime

starttime = datetime.datetime.now()
fp = open('E:/finalTest/test5')
fp.readline()

movieId = []
title = []
times = []
genres = []

while True:
    info = fp.readline()
    if info != '':
        info = list(info.split(','))
        if info[2] != '2014' :
            continue
        else:
            movieId.append(info[0])
            title.append(info[1])
            times.append(info[2])
            genres.append(info[3])
    else:
        break

genresBak = []
for claBlo in genres:
    cToNum = []
    tmp = list(claBlo.split('|'))
    #print(tmp)
    for i in tmp:
        if i == 'Action' or i == 'Action\n':
            cToNum.append(1)
        if i == 'Adventure' or i == 'Adventure\n':
            cToNum.append(2)
        if i == 'Animation' or i == 'Animation\n':
            cToNum.append(3)
        if i == 'Children' or i == 'Children\n':
            cToNum.append(4)
        if i == 'Crime' or i ==  'Crime\n':
            cToNum.append(5)
        if i == 'Comedy' or i == 'Comedy\n':
            cToNum.append(6)
        if i == 'Documentary' or i == 'Documentary\n':
            cToNum.append(7)
        if i == 'Drama' or i == 'Drama\n':
            cToNum.append(8)
        if i == 'Fantasy' or i == 'Fantasy\n':
            cToNum.append(9)
        if i == 'Horror' or i == 'Horror\n':
            cToNum.append(10)
        if i == 'Musical' or i == 'Musical\n':
            cToNum.append(11)
        if i == 'Mystery' or i == 'Mystery\n':
            cToNum.append(12)
        if i == 'Romance' or i == 'Romance\n':
            cToNum.append(13)
        if i == 'Sci-Fi' or i == 'Sci-Fi\n':
            cToNum.append(14)
        if i == 'Thriller' or i == 'Thriller\n':
            cToNum.append(15)
        if i == 'War' or i == 'War\n':
            cToNum.append(16)
        if i == 'Western' or i == 'Western\n':
            cToNum.append(17)
    genresBak.append(cToNum)
for i in genresBak:
    if i == []:
        i.append(18)

for i in genresBak:
    while True:
        if len(i) > 4:
            i.pop(-1)
        if len(i) < 4:
            i.append(i[-1] + 1)#this part is a question for the cluster,it have to be proof for it usage
        if len(i) == 4:
            break
fp.close()

def getDistance(a=[],b=[]):
    dis = 0
    for i in range(len(a)):
        dis = dis + pow(a[i] - b[i],2)
    return float(np.sqrt(dis))

disMatrix = np.arange(pow(len(genresBak),2)).reshape(len(genresBak),len(genresBak))
for i in range(len(genresBak)):
    for j in range(len(genresBak)):
        if i < j:
            disMatrix[i,j] = getDistance(genresBak[i],genresBak[j])
        else:
            disMatrix[i,j] = 1000

bakMatrix = disMatrix
n = len(genresBak)
#print(n)
for ii in range(n):
    x = 0
    y = 0
    #the kernel algorithm
    a = True
    for i in range(n):
        if a == False:
            break
        for j in range(i+1,n):
            if bakMatrix[i,j] == bakMatrix.min():
                x = i
                y = j
                a = False
                break
    reNewMatrix = np.arange(pow(n-1,2)).reshape(n-1,n-1)
    #print(disMatrix)
    p = 0
    for i in range(n-2):
        q = 0
        if i == x or i == y:
            p += 1
        for j in range(n-2):
            if j == x or j == y:
                q += 1
            reNewMatrix[i,j] = bakMatrix[p,q]
            q = q + 1
        p = p + 1
    p = 0
    for i in range(n-1):
        if i == x or i == y:
            p = p + 1
            continue
        reNewMatrix[p,n-2] = min(bakMatrix[p,x],bakMatrix[x,p],bakMatrix[p,y],bakMatrix[y,p])
        reNewMatrix[n-2,p] = bakMatrix[n-2,p]
        p = p + 1
    bakMatrix = np.arange(pow(n-1,2)).reshape(n-1,n-1)
    bakMatrix = reNewMatrix
    n -= 1
    #print(x,y,ii)
    if ii != n:
        tmp = []
        tmp.append(movieId[x])
        tmp.append(movieId[y])
        movieId.pop(y)
        movieId.pop(x)
        movieId.append(tmp)
print(movieId)

endtime = datetime.datetime.now()
print (endtime - starttime)
