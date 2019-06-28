from __future__ import print_function
import mdtraj as md
import numpy as np
#Change this to load in desired file-- must have hydrogens
#code for residue specific karplus models

loadfile = "comb_angles.txt"
prot=loadfile[:4]
traj = md.load(loadfile)
print(traj) 
res_lengths=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

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
    a=0.0
    b=0.0
    c=0.0
    def __init__(self,aa,bb,cc):
        self.a=aa
        self.b=bb
        self.c=cc



def file_len(fname):
    f= open(fname,"r")
    count=0
    for line in f:
        split=line.split()
        if len(split)>1:
            res_lengths[dictionary[split[0]]]+=1

angles_karplus=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
couples_karplus=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
mini_karplus=[]
f=open(fname,"r")
for line in f:
    split=line.split()
    if len(split)>1:
        angles_karplus[dictionary[split[0]]].append(split[2])
        couples_karplus[dictionary[split[0]]].append(split[3])
for i in range(len(angles_karplus)):
    wexact=np.linalg.pinv(angles_karplus[i]).dot(couples_karplus[i])


print("----------------")

#Make our angles :)
angles=[]
for ind in indices:
    if len(ind)==4:
        newlist=np.array([ind[1], ind[0], ind[2], ind[3]])
        newlist=np.reshape(newlist,(1,4))
        angles.append(md.compute_dihedrals(traj, newlist)[0][0])
for name in names:
    print(name)

#Grab coupling info from file
names2=[]
couples=[]
#Put a different file name here
r=open("couples"+prot.lower()+".txt","r")
for line in r:
    if line!="":
        split=line.split() 
        if len(split)>0:
            names2.append(split[7])
            couples.append(split[22])
#Code to ensure the indices of the angles and couples line up using name information
print(names2)
print(len(names2))
print(len(couples))
print(len(names))
print(len(angles))
num=0
while num<len(names) and num<len(names2):
    print("num: %d name1: %s name2: %s" % (num,names[num],names2[num]))
    if names2[num]=='GLY' or names2[num]=='PRO':
        print("Deleting from names2 at num %d"%num)
        names2.pop(num)
        couples.pop(num)
        num-=1
    if names2[num]!=names[num]:
        print("Deleting from names1 at num %d"%num)
        names.pop(num)
        angles.pop(num)
        prevs.pop(num)
        num-=1
    num+=1

if len(names)==len(names2)+1:
    names.pop()
    angles.pop()
    prevs.pop()

if len(names)!=len(names2): 
    print(len(names))
    print(len(names2))
    print("Look at the output and the coupling file for a one-off error!")

#Last Step!!
#Now let's write this data to a file!!
f=open(prot.upper()+'_angles.txt','w+')
val=0
if(len(names)>len(names2)):
    val=len(names2)
else:
    val=len(names)
for val in range(val):
    f.write(names[val]+" ")
    f.write(prevs[val]+" ")
    f.write((str)(angles[val]))
    f.write(" ")
    f.write(couples[val])
    f.write("\n")
f.close()
print("File written to "+prot+"_angles.txt")
