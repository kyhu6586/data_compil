from __future__ import print_function
import mdtraj as md
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy
from scipy.spatial.distance import squareform
traj=md.load('md.xtc', top='1AKI_solv_ions.gro')
#This is clustering with outside libraries
distances=np.empty((traj.n_frames, traj.n_frames))
for i in range(traj.n_frames):
    #computing pairwise rmsd between conformations
    distances[i]=md.rmsd(traj, traj, i)
print('Max pairwise rmsd: %f nm' % np.max(distances))
#must reduce  
#scipy.cluster implements the average linkage algorithm (among others)
assert np.all(distances-distances.T<1e-6)
reduced_distances=squareform(distances, checks=False)
linkage=scipy.cluster.hierarchy.linkage(reduced_distances, method='average')
#plotting dendogram
plt.title('RMSD Average linkage hierarchical clustering')
_=scipy.cluster.hierarchy.dendrogram(linkage, no_labels=True, count_sort='descendent')
