# *** TAIL_OVERLAP.py ***
#
# Author: A. Mert Turaclar
# Date: 27.10.2023
# Latest Update: 27.10.2023
# Changes: -
#
# This code calculates the overlap between two moleculues using their potential energy curves.
# The calculation is done by atomic tail model (M. Fukugita, Zeitschrift für Physik C 9(4):365
# –367, 1981). 
#
# Use -h flag for help about using the program.
#
#
#   START OF CODE

import sys
import os
import argparse
import pandas as pd
sys.path.append('./taillib')
from exe import calc
from taillib import overlap
from taillib import interpolate
from taillib.constants import ehinev

def process_potentials(parent_file, daughter_file, r_independent, r_value):
    daughter_data_raw = pd.read_csv('input/' + daughter_file, header=None, delim_whitespace=True)
    parent_data_raw = pd.read_csv('input/' + parent_file, header=None, delim_whitespace=True)

    if len(daughter_data_raw) != len(parent_data_raw):
        if len(daughter_data_raw) < len(parent_data_raw):
            ref_data = daughter_data_raw.to_numpy()
            target_data = parent_data_raw.to_numpy()
        else:
            ref_data = parent_data_raw.to_numpy()
            target_data = daughter_data_raw.to_numpy()

        interpolated_data, truncated_data = interpolate.spline(target_data, ref_data)

        if len(daughter_data_raw) < len(parent_data_raw):
            parent_data = pd.DataFrame(interpolated_data)
            daughter_data = pd.DataFrame(truncated_data)
        else:
            daughter_data = pd.DataFrame(interpolated_data)
            parent_data = pd.DataFrame(truncated_data)
    else:
        daughter_data = daughter_data_raw
        parent_data = parent_data_raw

    return daughter_data, parent_data, calculate_pot_diff(daughter_data, parent_data, r_independent, r_value)

def calculate_pot_diff(daughter_data, parent_data, r_independent, r_value):
    # Calculate the absolute potential differences for both cases of R dependence
    pot_diff = (daughter_data[1] - parent_data[1]).abs()

    # Calculate the absolute potential differences, if R is specified
    if r_independent:
        if r_value is None:
            print("Error: --r-independent requires --r-value!")
            sys.exit()
        else:
            idx = (daughter_data[0] - args.r_value).abs().idxmin()
            uniform_pot_diff = pot_diff[idx]
            pot_diff = pd.Series([uniform_pot_diff] * len(pot_diff))

    # Convert from Hartree to eV and calculate overlap matrix elements
    pot_diff_ev = pot_diff * ehinev
    return pot_diff_ev

def calculate_overlaps(pot_diff_ev):
    overlap_matrix_elements = [overlap.overlap(energy, energy) for energy in pot_diff_ev]
    return overlap_matrix_elements

def save_results(file_path, daughter_data, overlap_matrix_elements):
    num_points = len(overlap_matrix_elements)
    header = """*
*
*      Electronic coupling matrix elements (mixed overlaps)
*      S_n (R) calculated from atomic tail formula.
*
       Number of points:     {num_points}
*
*      R [a.u.]      Coupling [a.u.]
*      --------     -----------------
*
""".format(num_points=num_points)

    save_data = pd.DataFrame({'R [a.u.]': daughter_data[0], 'Coupling [a.u.]': overlap_matrix_elements})
    with open(file_path, 'w') as f:
        f.write(header)
        save_data.to_csv(f, sep='\t', index=False, header=False, float_format='%f')
    return save_data, header, num_points

def main():
    print(' ')
    print(' ')
    print('           *****************************')
    print('           ***                       ***')
    print('           ***                       ***')
    print('           ***      TAIL_OVERLAP     ***')
    print('           ***                       ***')
    print('           ***                       ***')
    print('           *****************************')
    print(' ')
    print(' ')

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

    # Check if the file exists, if it does, ask what to do.
    if os.path.exists(file_path):
        # Prompt the user to confirm overwriting
        response = input(f"     The file {file_name} already exists. Do you want to overwrite it? (yes/no): ")
    
        if response.lower() not in ['yes', 'y']:
            print("     Calculation cancelled. The existing file will not be overwritten.")
            print("     quitting...")
            sys.exit()

    daughter_data, parent_data, pot_diff_ev = process_potentials(args.parent_potential_file, args.daughter_potential_file, args.r_independent, args.r_value)
    overlap_matrix_elements = calculate_overlaps(pot_diff_ev)
    save_data, header, num_points = save_results(file_path, daughter_data, overlap_matrix_elements)

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        print(f"     Tail overlaps have been calculated successfully and saved to {file_name}")
    else:
        print(f"    *** Error: Tail overlap file {file_name} was not created or is empty. Please check for issues.")

    print("\n")
    print(save_data.to_string(index=False)) # Print the result to the console

    # Save the overlaps to a file, this part is a 3 line of codes instead of a single line
    # because of the header format. df.to_csv doesn't accept this type of header
    # thus, doing it using `with open`.
    with open('out/' + file_name, 'w') as f:
        f.write(header.format(num_points=num_points))
        save_data.to_csv(f, sep='\t', index=False, header=False, float_format='%f')

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        print(" ")
        print("     Tail overlaps have been calculated successfully! Overlaps have been saved to the file: \n")
        print(f"                {file_name} \n")
        print("tail_overlap exiting gracefully. \n")
    else:
        print(f"    ***Error: Tail overlap {file_name} was not created or is empty. Please check for issues. \n")

if __name__ == '__main__':
    main()

#   END OF CODE
