from __future__ import print_function
import mdtraj as md
import numpy as np
#Change this to load in desired file-- must be processed through gromacs
traj = md.load('1igd_processed.pdb')
print(traj)
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

f=open('1IGD_angles.txt','w+')
for val in range(len(names)):
    f.write(names[val]+" ")
    f.write(prevs[val]+" ")
    f.write((str)(angles[val]))
    f.write("\n")
f.close()
    #CHANGE THIS TOO
print("File written to 1IGD_angles.txt")
