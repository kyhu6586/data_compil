import numpy as np
import math
import random
overA=0.0
overB=0.0
overC=0.0
class Data1:
    resName=""
    neiName=""
    angle=0.0
    constant=0.0
    def __init__(self,m,n,a,c):
        self.resName=m
        self.neiName=n
        self.angle=a
        self.constant=c
    def __str__(self):
        return self.resName+" "+str(self.angle)

def file_len(fname):
    f= open(fname,"r")
    count=0
    for line in f:
        if line!="" and len(line.split())>1:
            count+=1

    return count+1

def give_file_nam(s,i):
    if os.path.isfile(s+".png"):
        i+=1
        return give_file_nam(s[:-1]+str(i),i)
    else:
        print(s)
        return s
din=[["ALA","GLY","THR","TYR","VAL","LEU","ILE","TRP","GLU","ASP","SER","ASN","GLN","PRO","PHE","ARG","CYS","HIS","LYS","MET"],[],[],[]]
dictionary={}
x="ALA"
dictionary[x]=0
x="GLY"
dictionary[x]=1
x="THR"
dictionary[x]=2
x="TYR"
dictionary[x]=3
x="VAL"
dictionary[x]=4
x="LEU"
dictionary[x]=5
x="ILE"
dictionary[x]=6
x="TRP"
dictionary[x]=7
x="GLU"
dictionary[x]=8
x="ASP"
dictionary[x]=9
x="SER"
dictionary[x]=10
x="ASN"
dictionary[x]=11
x="GLN"
dictionary[x]=12
x="PRO"
dictionary[x]=13
x="PHE"
dictionary[x]=14
x="ARG"
dictionary[x]=15
x="CYS"
dictionary[x]=16
x="HIS"
dictionary[x]=17
x="LYS"
dictionary[x]=18
x="MET"
dictionary[x]=19
class Data:
    name=""
    a=0.0
    b=0.0
    c=0.0
    def __init__(self,n,aa,bb,cc):
        self.a=aa
        self.b=bb
        self.c=cc
        self.name=n
f= open("C_Final.txt","r")
count=0
for line in f:
    split=line.split()
    din[1].append(float(split[0]))
    din[2].append(float(split[1]))
    din[3].append(float(split[2]))
    count+=1
r=open("1IGD_angles.txt", "r")
data=[]
length=file_len("1IGD_angles.txt")
for line in r:
    split=line.split()
    if len(split)>1:
        data.append(Data1(split[0],split[1],float(split[2]),float(split[3])))
print(din)
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

