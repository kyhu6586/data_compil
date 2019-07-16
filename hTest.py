import numpy as np
import math
import random
A0=0.0
B0=0.0
C0=0.0
A1=0.0
B1=0.0
C1=0.0
overA=0.0
overB=0.0
overC=0.0
class Data1:
    resName=""
    neiName=""
    angle=0.0
    constant=0.0
    h=0
    def __init__(self,m,n,a,c,hh):
        self.resName=m
        self.neiName=n
        self.angle=a
        self.constant=c
        self.h=hh
        
    def __str__(self):
        return self.resName+" "+str(self.angle)

def file_len(fname):
    f= open(fname,"r")
    count=0
    for line in f:
        if line!="" and len(line.split())>1:
            count+=1

    return count+1

f= open("C_Final.txt","r")
count=0
h=[]
noH=[]
data=[]
length=file_len("C_Final.txt")
for line in r:
    split=line.split()
    if len(split)>1:
        data.append(Data1(split[0],split[1],float(split[2]),float(split[3]),split[5]))
        if data[count].h==0:
            noH.append(data[count])
        else:
            H.append(data[count])
        count+=1
index=0

#random.shuffle(data)
in_train=np.zeros([length,1],dtype=np.float32)
out_train=np.zeros([length,1],dtype=np.float32)
karplus=np.zeros([length,3],dtype=np.float32)
while index<len(data):
    in_train[index]=data[index].angle
    out_train[index]=data[index].constant
    karplus[index][0]=1.0
    karplus[index][1]=math.cos(float(in_train[index]))
    karplus[index][2]=math.cos(2*float(in_train[index]))
    index+=1
wexact=np.linalg.pinv(karplus).dot(out_train)
overA=wexact[0]
overB=wexact[1]
overC=wexact[2]
index=0
testRes=0.0
diffGen=0.0
diffRes=0.0
print("ABC")
print(overA)
print(overB)
print(overC)
print("~~~~~~~~~~~")

for index in range(len(data)):
    t=data[index]
    here=dictionary[t.resName]
    genDiff=t.constant-(overA+(overB*math.cos(t.angle))+(overC*math.cos(2*t.angle)))
    resDiff=t.constant-(din[1][here]+(din[2][here]*math.cos(t.angle))+(din[3][here]*math.cos(2*t.angle)))
    diffGen+=abs(genDiff[0])
    diffRes+=abs(resDiff)
    print(abs(genDiff[0]),abs(resDiff))
    if resDiff<genDiff[0]:
        testRes+=1

testRes/=len(data)
testRes*=100
print(diffGen)
print(diffRes)
diffGen/=len(data)
diffRes/=len(data)
print("test results, res-specific better than general: "+str(testRes))
print("average diff, general: "+str(diffGen))
print("average diff, res-specific: "+str(diffRes))

