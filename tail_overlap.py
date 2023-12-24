"""

*** TAIL_OVERLAP.py ***

Author: A. Mert Turaclar
Date: 27.10.2023
Latest Update: 27.10.2023
Changes: -

This code calculates the overlap between two moleculues using their potential energy curves.
The calculation is done by atomic tail model (M. Fukugita, Zeitschrift für Physik C 9(4):365
–367, 1981). 

Use -h flag for help about using the program.

"""

#   START OF CODE

import sys
import os
import argparse
import numpy as np
sys.path.append('./taillib')
from exe import calc
from taillib import overlap
from taillib import interpolate

# Taking and parsing arguments
parser = argparse.ArgumentParser(
    description='Calculates the tail overlaps for FSD calculations.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-p', '--parent-potential-file', type=str, required=True, help='File with parent molecule poential')
parser.add_argument('-d', '--daughter-potential-file', type=str, required=True, help='File with daughter molecule potential')
parser.add_argument('-r', '--r-independent', action='store_true', help='Flag to indicate R-independent calculation. If set, a single R value is used for all calculations.')
parser.add_argument('-v', '--r-value', type=float, help='The R value to use for R-independent calculations. Required if --r-independent is set.')
parser.add_argument('-n', '--file-name', type=str, help='Name of the calculated overlap file, recomended fashion: <DaughterMolecule>+<ElectronicState><T00X>, i.e., HeTppst001T001. Do NOT include file extension.')

args = parser.parse_args()

file_name = args.file_name + ".snm"
file_path = 'out/' + file_name

print("")
print(" *** tail_fsd ***    \n")

# Check if the file exists, if it does, ask what to do.
if os.path.exists(file_path):
    # Prompt the user to confirm overwriting
    response = input(f"     The file {file_name} already exists. Do you want to overwrite it? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("     Operation cancelled. The existing file will not be overwritten.")
        print("     quitting...")
        sys.exit()

daughter_data_raw = np.genfromtxt('input/' + args.daughter_potential_file)
parent_data_raw = np.genfromtxt('input/' + args.parent_potential_file)

if len(daughter_data_raw) != len(parent_data_raw):
    if len(daughter_data_raw) < len(parent_data_raw):
        ref_data = daughter_data_raw
        target_data = parent_data_raw
        file_to_save = 'parent_interpolated.pot'
    else:
        ref_data = parent_data_raw
        target_data = daughter_data_raw
        file_to_save = 'daughter_interpolated.pot'

#   interpolated_data, truncated_data = interpolate.spline(daughter_data_raw, parent_data_raw)
    interpolated_data, truncated_data = interpolate.spline(target_data, ref_data)

    np.savetxt('out/' + file_to_save, interpolated_data, fmt='%f', delimiter='\t')

    if len(daughter_data_raw) < len(parent_data_raw):
        parent_data = interpolated_data
        daughter_data = truncated_data
        print("")
        print("     Parent potential curve has been interpolated with respect to parent potential curve.")
        print(f"     Interpolated daughter data has been saved to /out/{file_to_save}. \n")
    else:
        daughter_data = interpolated_data
        print("")
        print("     Daughter potential curve has been interpolated with respect to daughter potential curve.")
        print(f"     Interpolated parent data has been saved to /out/{file_to_save}. \n")
        parent_data = truncated_data

else:
    daughter_data = daughter_data_raw
    parent_data = parent_data_raw

# Calculate the absolute potential differences for both cases of R dependence
pot_diff = np.abs(daughter_data[:, 1] - parent_data[:, 1])

# Calculate the absolute potential differences, if R is specified
if args.r_independent:
    if args.r_value is None:
        parser.error("--r-independent requires --r-value!")
    else:
        idx = (np.abs(daughter_data[:,0] - args.r_value)).argmin()
        uniform_pot_diff = pot_diff[idx]
        pot_diff = np.full(pot_diff.shape, uniform_pot_diff)

# Convert from Hartree to eV
hartree_to_ev = 27.211386
pot_diff_ev = pot_diff * hartree_to_ev
print(f"pot_diff_ev = {pot_diff_ev}")
# Calculate overlap matrix elements using the tail module
overlap_matrix_elements = []

for overlap_energy in pot_diff_ev:
    e_start =  overlap_energy
    e_end = overlap_energy  
    overlap_ME = overlap.overlap(e_start, e_end)
    print(overlap_ME)
    overlap_matrix_elements.append(overlap_ME)

num_points = len(overlap_matrix_elements)

# Create the header string, conventinal file type for amo group codes
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
with open('out/' + file_name, 'w') as f:
    f.write(header.format(num_points=num_points))
    np.savetxt(f, save_data, fmt='%f', delimiter='\t')

if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    print(" ")
    print("     Tail overlaps calculated successfully! Overlaps have been saved to file: \n")
    print(f"                {file_name} \n")
    print("     tail_overlap exiting gracefully. \n")
else:
    print(f"    ***Error: Tail overlap {file_name} was not created or is empty. Please check for issues. \n")

#   END OF CODE
