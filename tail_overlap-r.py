import sys
sys.path.append('./amo')
import numpy as np
from exe import calc
from amo import overlap

# Ensure that the necessary arguments are provided
if len(sys.argv) < 4:
    print("Usage: python tail_overlap.py daughter_filename parent_filename overlap_filename R_dependence")
    sys.exit(1)

# Get the filenames from command line arguments
daughter_filename = sys.argv[1]
parent_filename = sys.argv[2]
overlap_filename = sys.argv[3]
r_dependence = sys.argv[4]

# Load the potential data
daughter_data = np.genfromtxt('input/' + daughter_filename + '.txt')
parent_data = np.genfromtxt('input/' + parent_filename + '.txt')

# Calculate the absolute potential differences
pot_diff = np.abs(daughter_data[:, 1] - parent_data[:, 1])

# Convert from Hartree to eV
hartree_to_ev = 27.211386
pot_diff_ev = pot_diff * hartree_to_ev

# Calculate overlap matrix elements using the tail function
overlap_matrix_elements = []

for e in pot_diff_ev:
    e_start = e 
    e_end = e   
    e_step = 1  
    no_shift = 0
    overlap_ME = overlap.overlap(e_start, e_end, e_step)
    overlap_matrix_elements.append(overlap_ME)

num_points = len(overlap_matrix_elements)

# Create the header string
header = """
*
*
*      Electronic coupling matrix elements (mixed overlaps)
*      S_n (R) calculated from atomic tail formula using
*      subroutines overlap.py and tail.py (atomic tail). 
*
*
*
       Number of points:     {num_points}
*
*      R (a.u.)      Coupling (a.u.)
*      --------     -----------------
*
"""

save_data = np.column_stack((daughter_data[:, 0], overlap_matrix_elements))

# Save the overlap matrix elements to a file
#np.savetxt('out/' + 'he3tppst001T002.snm', save_data, fmt='%f', delimiter='\t', header=header)
with open('out/' + overlap_filename + '.snm', 'w') as f:
    f.write(header.format(num_points=num_points))
    np.savetxt(f, save_data, fmt='%f', delimiter='\t')
