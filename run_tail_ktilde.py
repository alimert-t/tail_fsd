#    run_tail_ktilde.py
#    ======================================================================
#
#    Calculate the atomic tail for beta decay within sudden 
#    approximation using the result in Fukugita+Kubodera, 
#    Z.Phys.9,365(1981) adapted to the molecular case by considering 
#    the different ionisation energies and prefactor 2.0 (for the 
#    two electrons).
#
#    This shell script calls the main script "exe.py" which executes the calculations with
#    python modules "tail.py & correction.py" and "ktilde.py" which calculates
#    the atomic tail and fractional recoil momentums (ktilde) at the atomic tail.
#     
#    This code is originally (tail.f) written by A. Saenz, now modified  
#    for current needs by Ali Mert Turaclar.
#
#    Arguments to be given:
#    ----------------------
#
#           1st Argument: Starting point of atomic tail, in eV. (i.e 240)
#           2nd Argument: End point of atomic tail, in eV. (i.e 1500) 	  
#           3rd Argument: Number of energy steps. (i.e 500 steps of energy in between start - end)
#           4th Argument: 1 or 0. Application of fractional recoil momentum shift. (1 -> Shift
#                         is applied, 0 -> Shift is not applied.) Generally, 1 should be selected. 
#
#    Example command for starting this script:
#    $python3 tail_ktilde.py 240 1000 380 1
#
#    ======================================================================
#
#    Date: 10.02.2023
#    Author: Ali Mert Turaclar
#    Last Change / Update: 10.02.2023
#
#    ======================================================================

#    START OF SCRIPT

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
    
    parser = argparse.ArgumentParser()
    parser.add_argument("e_start", type=float, help="Start energy of atomic tail")
    parser.add_argument("e_end", type=float, help="End energy of atomic tail")
    parser.add_argument("istep", type=int, help="Number of energy points to be calculated, Energy_step_size = (e_end - estart) / istep")
    parser.add_argument("corr", nargs='?', type=str, choices=["Yes", "No"], default="Yes", help="Application of effective fractional recoil momentum shift. Yes => Shift is applied, No => Shift is NOT applied. Default = Yes")
    args = parser.parse_args()
    
    print("Start Energy = ", sys.argv[1], " eV")
    print("End Energy = ", sys.argv[2], " eV")
    print("Number of energy steps = ", sys.argv[3])
    print("")
    
    calc(args.e_start, args.e_end, args.istep, args.corr)
    
if __name__ == "__main__":
    main()
