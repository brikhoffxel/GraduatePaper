#coding:utf-8
import re
import csv
import numpy as np

fp = open('/home/briky/Tmp/test')
fp.readline()

worldRand = [i for i in range(100)]
institution = [i for i in range(100)]
county = [i for i in range(100)]
nationalRank = [i for i in range(100)]
qualityOfEducation = [i for i in range(100)]
alumiEmployment = [i for i in range(100)]
qualityOfFaculty = [i for i in range(100)]
publications = [i for i in range(100)]
influences = [i for i in range(100)]
citations = [i for i in range(100)] #引用
broadImpact = [i for i in range(100)]
patents = [i for i in range(100)]
score = [i for i in range(100)]
line = [i for i in range(100)]

i = 0
while True:
    info = fp.readline()
    if info != '':
        info = info.split('\t')
        line[i] = info;
        line[i] = line[i][:10]+line[i][11:]
        worldRand[i] = info[0]
        institution[i] = info[1]
        county[i] = info[2]
        nationalRank[i] = info[3]
        qualityOfEducation[i] = info[4]
        alumiEmployment[i] = info[5]
        qualityOfFaculty[i] = info[6]
        publications[i] = info[7]
        influences[i] = info[8]
        citations[i] = info[9]
        broadImpact[i] = info[10]
        patents[i] = info[11]
        score[i]  =  info[12]
        i += 1
    else:
        break

for i in range(100):
    worldRand[i] = int(worldRand[i])

def getAverge(data=[]):
    sum = 0
    for i in range(len(data)):
        sum = sum + round(float(data[i]))
    ave = sum/len(data)
    return ave

qualityOfEducationAve = getAverge(qualityOfEducation)
alumiEmploymentAve = getAverge(alumiEmployment)
qualityOfFacultyAve = getAverge(qualityOfFaculty)
publicationsAve = getAverge(publications)
influencesAve = getAverge(influences)
citationsAve = getAverge(citations)
#broadImpactAve = getAverge(broadImpact)  #this line is not number
patentsAve = getAverge(patents)
scoreAve = getAverge(score)
xAve = [qualityOfEducationAve,alumiEmploymentAve,qualityOfFacultyAve,publicationsAve,influencesAve,citationsAve,patentsAve,scoreAve]

#cal the cov
def calCov(a=[],b=[],c=[]):
    #print(a,b,c)
    cov = 0
    for i in range(8):
        cov = cov + (a[i] - c[i])*(b[i] - c[i])
    return cov

#get the main part to take it into float
for i in range(100):
    line[i] = line[i][-8:]
    for j in range(8):
        line[i][j] = round(float(line[i][j]))


#cal the matrix of cov
mCov = np.arange(pow(8,2)).reshape(8,8)
for i in range(len(line[1])):
    for j in range(len(line[1])):
        mCov[i][j] = calCov(line[i],line[j],xAve)

#use the Mahalanobis distance
invMCov = np.linalg.inv(mCov)

def getDistance(x=[],y=[]):
    X = np.matrix(x)
    Y = np.matrix(y)
    Z = X - Y
    dis = Z*invMCov*(Z.T)
    return dis

#kernel cal processing
disMatrix = np.arange(pow(100,2)).reshape(100,100)
for i in range(100):
    for j in range(100):
        if j <= i:
            disMatrix[i,j] = 100000
        else:
            disMatrix[i,j] = getDistance(line[i],line[j])

#try to recreate the matrix
bakDisMatrix = disMatrix
n = 100
result = [i for i in range(n)]

for ii in range(n):
    x = 0
    y = 0
    for i in range(n):
        for j in range(i,n):
            if bakDisMatrix[i,j] == bakDisMatrix.min():
                x = i;
                y = j;
                break

    reNewMatrix = np.arange(pow(n-1,2)).reshape(n-1,n-1)
    p = 0
    for i in range(n-2):
        q = 0
        if i == x or i == y:
            p = p + 1
        for j in range(n-2):
            if j == x or j == y:
                q = q + 1
            reNewMatrix[i,j] = bakDisMatrix[p,q]
            q = q + 1
        p = p + 1
    #for the final c and h
    for i in range(n-1):
        if i == x or i == y:
            continue
        reNewMatrix[i,n-2] = min(bakDisMatrix[x,i],bakDisMatrix[i,x],bakDisMatrix[y,i],bakDisMatrix[i,y])
        reNewMatrix[n-2,i] = bakDisMatrix[n-2,i]
    bakDisMatrix = np.arange(pow(n-1,2)).reshape(n-1,n-1)
    bakDisMatrix = reNewMatrix
    n -= 1

#take it as the same change
    if ii != 99:
        tmp = []
        tmp.append(result[x])
        tmp.append(result[y])
        result.pop(y)
        result.pop(x)
        result.append(tmp)

print(result)