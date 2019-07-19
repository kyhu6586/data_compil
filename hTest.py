import numpy as np
import math
import random
A0=0.0
B0=0.0
C0=0.0
A1=0.0
B1=0.0
C1=0.0
A=0.0
B=0.0
C=0.0
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

f= open("1MVG_angles.txt","r")
count=0
h=[]
noH=[]
data=[]
length=file_len("1MVG_angles.txt")
for line in f:
    split=line.split()
    if len(split)>1:
        data.append(Data1(split[0],split[1],float(split[2]),float(split[3]),int(split[5])))
        print(data[count].h)
        if data[count].h%2==0:
            noH.append(data[count])
        else:
            h.append(data[count])
        count+=1
index=0

#random.shuffle(data)
in_train=np.zeros([length,1],dtype=np.float32)
out0=np.zeros([length,1],dtype=np.float32)
out1=np.zeros([length,1],dtype=np.float32)
out=np.zeros([length,1],dtype=np.float32)
karplus0=np.zeros([length,3],dtype=np.float32)
karplus1=np.zeros([length,3],dtype=np.float32)
karplus=np.zeros([length,3],dtype=np.float32)
for x in range(len(h)):
    out1[x]=h[x].constant
    karplus1[x][0]=1.0
    karplus1[x][1]=math.cos(float(h[x].angle))
    karplus1[x][2]=math.cos(2*float(h[x].angle))
    print(karplus1[x])
print("--------------------------------")
for x in range(len(noH)):
    out0[x]=noH[x].constant
    karplus0[x][0]=1.0
    karplus0[x][1]=math.cos(float(noH[x].angle))
    karplus0[x][2]=math.cos(2*float(noH[x].angle))
    print(karplus0[x])
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
for x in range(len(data)):
    out[x]=data[x].constant
    karplus[x][0]=1.0
    karplus[x][1]=math.cos(float(data[x].angle))
    karplus[x][2]=math.cos(2*float(data[x].angle))
    print(karplus[x])
print("************************************")
wexact0=np.linalg.pinv(karplus0).dot(out0)
wexact1=np.linalg.pinv(karplus1).dot(out1)
wexact=np.linalg.pinv(karplus).dot(out)
A0=wexact0[0]
B0=wexact0[1]
C0=wexact0[2]
A1=wexact1[0]
B1=wexact1[1]
C1=wexact1[2]
A=wexact[0]
B=wexact[1]
C=wexact[2]
print("ABC "+str(A)+str(B)+str(C))
print(len(data))
print("A1B1C1 "+str(A1)+str(B1)+str(C1))
print(len(h))
print("A0B0C0 "+str(A0)+str(B0)+str(C0))
print(len(noH))



index=0
testRes=0.0
diffGen=0.0
diffRes=0.0
print("~~~~~~~~~~~")
#Run test cases to find deviation
for index in range(len(data)):
    t=data[index]
    genDiff=t.constant-(A+(B*math.cos(t.angle))+(C*math.cos(2*t.angle)))
    if t.h==0:
        resDiff=t.constant-(A0+(B0*math.cos(t.angle))+(C0*math.cos(2*t.angle)))
    else:
        resDiff=t.constant-(A1+(B1*math.cos(t.angle))+(C1*math.cos(2*t.angle)))
    diffGen+=abs(genDiff[0])
    diffRes+=abs(resDiff[0])
    print(abs(genDiff[0]),abs(resDiff[0]))
    if resDiff[0]<genDiff[0]:
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

