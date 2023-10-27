"""
     RUN_TAIL_KTILDE.py
    ======================================================================

    Calculate the atomic tail for beta decay within sudden 
    approximation using the result in Fukugita+Kubodera, 
    Z.Phys.9,365(1981) adapted to the molecular case by considering 
    the different ionisation energies and prefactor 2.0 (for the 
    two electrons).

    This shell script calls the main script "exe.py" which executes the calculations with
    python modules "tail.py & correction.py" and "ktilde.py" which calculates
    the atomic tail and fractional recoil momentums (ktilde) at the atomic tail.
     
    This code is originally (tail.f) written by A. Saenz, now modified  
    for current needs by Ali Mert Turaclar.

    Arguments to be given:
    ----------------------

           1st Argument: Starting point of atomic tail, in eV. (i.e 240)
           2nd Argument: End point of atomic tail, in eV. (i.e 1500) 	  
           3rd Argument: Number of energy steps. (i.e 500 steps of energy in between start - end)
           4th Argument: 1 or 0. Application of fractional recoil momentum shift. (1 -> Shift
                         is applied, 0 -> Shift is not applied.) Generally, 1 should be selected. 

    ======================================================================

    Date: 10.02.2023
    Author: A. Mert Turaclar
    Last Change / Update: 27.10.2023

    ======================================================================
"""
#    START OF CODE

import sys
import math
import os
import numpy as np
import pandas as pd
import argparse
from scipy.interpolate import interp1d
from amo.ktilde import ktilde
from amo.tail import tail
from amo.correction import recoilBroad
from exe import calc 

def main():
    print(' ')
    print(' ')
    print('           *****************************')
    print('           ***                       ***')
    print('           ***                       ***')
    print('           ***     RUN_TAIL_KTILDE   ***')
    print('           ***                       ***')
    print('           ***                       ***')
    print('           *****************************')
    print(' ')
    print(' ')
    
    parser = argparse.ArgumentParser(
        description='Calculates the atomic tail final state distribuiton.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--energy-start", type=float, required=True, help="Start energy of atomic tail")
    parser.add_argument("-n", "--energy-end", type=float, required=True, help="End energy of atomic tail")
    parser.add_argument("-i", "--energy-step", type=int, required=True, help="Number of energy points to be calculated, Energy_step_size = (e_end - estart) / istep")
    parser.add_argument("-c", "--correction", action='store_true', help="Application of effective fractional recoil momentum shift. If -c flag is given, correction will be applied!")
    args = parser.parse_args()
    
    print("Start Energy = ", sys.argv[1], " eV")
    print("End Energy = ", sys.argv[2], " eV")
    print("Number of energy steps = ", sys.argv[3])
    print("")
    
    start_energy = args.energy_start
    end_energy = args.energy_end
    num_steps = args.energy_step

    # Now, use these variables in your file name
    file_name = f"tail_fsd-{start_energy}_{end_energy}_i{num_steps}"

    should_apply_correction = args.correction
    calc(args.energy_start, args.energy_end, args.energy_step, should_apply_correction, file_name)
    
if __name__ == "__main__":
    main()
