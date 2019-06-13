from __future__ import print_function
import mdtraj as md
import numpy as np
#Change this to load in desired file-- must be processed through gromacs
traj = md.load('1igd_processed.pdb')
print(traj)
index=0
indices=[]
names=[]
topology=traj.topology
#Loop through this topology, grabbing the first four atoms from every residue
#(Except glycine and prolyne)
for res in topology.residues:
    mini=[] #We want every residue's atoms to be in its own list
    for num in range(len(list(res.atoms))):
        if num<4 and res.name != 'GLY' and res.name != 'PRO' and res.name != 'HOH':
          #  print(list(res.atoms)[num])
            mini.append(index) #append these indices to an array
            index+=1
            if num==0:
                names.append(res.name) # Build an array with all the res names
        else: #Throw out the rest of the indices (after first 4) til next residue
            index+=1
    if len(mini) > 0:#As long as mini has elements in it, append it to 2D indices
        indices.append(mini)
print("----------------")

#Make our angles :)
angles=[]
for ind in indices:
    print(ind)
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
r=open("couples1igd.txt","r")
for line in r:
    split=line.split()
    if(split[8]=="HA"):
        names2.append(split[7])
        couples.append(split[22])
#Code to ensure the indices of the angles and couples line up using name information
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
        num-=1
    num+=1

if len(names)==len(names2)+1:
    names.pop()

if len(names)!=len(names2): 
    print(len(names))
    print(len(names2))
    print("Look at the output and the coupling file for a one-off error!")

#Last Step!!
#Now let's write this data to a file!!

    #CHANGE THIS CHANGE THIS CHANGE THIS
f=open('1igd_angles.txt','w+')
val=0
if(len(names)>len(names2)):
    val=len(names2)
else:
    val=len(names)
for val in range(val):
    f.write(names[val]+" ")
    f.write((str)(angles[val]))
    f.write(" ")
    f.write(couples[val])
    f.write("\n")
f.close()
    #CHANGE THIS TOO
print("File written to 1igd_angles.txt")
