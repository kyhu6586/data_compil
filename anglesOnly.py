from __future__ import print_function
import mdtraj as md
import numpy as np
#Change this to load in desired file-- must be processed through gromacs
traj = md.load('1igd_processed.pdb')
print(traj)
index=0
indices=[]
nums=[]
topology=traj.topology
#Loop through this topology, grabbing the first four atoms from every residue
#(Except glycine and prolyne)
for res in topology.residues:
    mini=[] #We want every residue's atoms to be in its own list
    for num in range(len(list(res.atoms))):
        if num<4 and res.name != 'GLY' and res.name != 'PRO' and res.name != 'HOH':
           # print(list(res.atoms)[num])
            mini.append(index) #append these indices to an array
            index+=1
            if num==0:
                nums.append(res) # Build an array with all the res names
        else: #Throw out the rest of the indices (after first 4) til next residue
            index+=1
    if len(mini) > 0:#As long as mini has elements in it, append it to 2D indices
        indices.append(mini)
print("----------------")

#Make our angles :)
angles=[]
for ind in indices:
    #print(ind)
    if len(ind)==4:
        newlist=np.array([ind[1], ind[0], ind[2], ind[3]])
        newlist=np.reshape(newlist,(1,4))
        angles.append(md.compute_dihedrals(traj, newlist)[0][0])

f=open('1igd_angles.txt','w+')
for val in range(len(nums)):
    f.write((str)(nums[val]))
    f.write(" ")
    f.write((str)(angles[val]))
    f.write(" ")
    f.write("\n")
f.close()
    #CHANGE THIS TOO
print("File written to 1igd_angles.txt")

