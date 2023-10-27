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

    if len(sys.argv) != 5:
        print(" ")
        print("Incorrect number of arguments. 4 arguments are expected.")
        print("")
        print("Usage: python3 run_tail_ktilde.py StartEnergy EndEnergy NumberOfSteps 1")
        print("")
        print("tail_ktilde.py is terminated with error.")
        print("")
        sys.exit()
    
    a = float(sys.argv[1])
    c = float(sys.argv[2])
    istep = float(sys.argv[3])
    corr = int(sys.argv[4])
    
    print("Start Energy = ", sys.argv[1], " eV")
    print("End Energy = ", sys.argv[2], " eV")
    print("Number of energy steps = ", sys.argv[3])
    print("")
    
    calc(a, c, istep, corr)
    
if __name__ == "__main__":
    main()
