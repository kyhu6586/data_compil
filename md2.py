
#now to put it all together
from __future__ import print_function
import numpy as np
import mdtraj as md
traj=md.load('md.xtc',top='1AKI_solv_ions.gro')
topology= traj.topology
#get atoms with specific properties with filtered lists. 
print([atom.index for atom in topology.atoms if atom.element.symbol is 'C' and atom.is_sidechain])

#next is calculating centroids
atom_indices=[a.index for a in traj.topology.atoms if a.element.symbol !='H']
distances = np.empty((traj.n_frames, traj.n_frames))
for i in range(traj.n_frames):
    distances[i]=md.rmsd(traj, traj, i, atom_indices=atom_indices)
beta=1
index=np.exp(-beta*distances/distances.std()).sum(axis=1).argmax()
print(index)
centroid=traj[index]
print(centroid)

