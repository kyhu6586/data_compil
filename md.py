from __future__ import print_function
import mdtraj as md
import numpy as np
#Change this to load in desired file-- must be processed through gromacs
loadfile = "1FZT_processed.pdb"
prot=loadfile[:4]
traj = md.load(loadfile)
print(traj)

class Data:
    res=""
    neighbor=""
    atoms=[]
    couple=0.0
    def __init__(self,r,n,a,c):
        self.res=r
        self.neighbor=n
        self.atoms=a
        self.couple=c
    def __init__(self,r,n,a):
        self.res=r
        self.neighbor=n
        self.atoms=a
    def __init__(self,r,a):
        self.res=r
        self.atoms=a
    def couple(self,c):
        self.couple=c

index=0
indices=[]
names=[]
prevs=[]
topology=traj.topology
resid=[]
for res in topology.residues:
    resid.append(res)
#Loop through this topology, grabbing the first four atoms from every residue
#(Except glycine and prolyne)
for res in range(len(resid)):
    mini=[] #We want every residue's atoms to be in its own list
    for num in range(len(list(resid[res].atoms))):
        if num<4 and resid[res].name != 'GLY' and resid[res].name != 'PRO' and resid[res].name != 'HOH':
            if res>0 and num==0:
                prevs.append(resid[res-1].name)
            elif res==0 and num==0:
                prevs.append("")
                print("empty string appended")
            print(list(resid[res].atoms)[num])
            mini.append(index) #append these indices to an array
            index+=1
            if num==0:
                names.append(resid[res].name) # Build an array with all the res names
        else: #Throw out the rest of the indices (after first 4) til next residue
            index+=1
    if len(mini) > 0:#As long as mini has elements in it, append it to 2D indices
        indices.append(mini)
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
f=open(prot+'_angles.txt','w+')
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
