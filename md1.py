from __future__ import print_function
import mdtraj as md
traj=md.load('md.xtc',top='1AKI_solv_ions.gro')
#n_atoms param returns number of atoms. n_residues returns number of residues
print(traj)

#Also move atoms around with the NumPy array. (3D) (frame, atom, 3)
frame_idx=4
atom_idx=9
print('Where is the fifth atom at the tenth frame?')
print('x: %s\ty: %s\tz: %s' % tuple(traj.xyz[frame_idx, atom_idx,:]))

#topology object stores connectivity information
#Also contains specific chain, residue, and atom information
topology=traj.topology
print(topology)

#select specific atom or loop through them all (0 indexed)
print('Fifth atom: %s' % topology.atom(4))
print('All atoms: %s' % [atom for atom in topology.atoms])

#same for residues
print('Second residue: %s' % traj.topology.residue(1))
print('All residues: %s' % [residue for residue in traj.topology.residues])

#All atoms are objects with indeces, names, element names, number of bonds, and
#residue name (with other more complicated ones)

#All residues are objects too

