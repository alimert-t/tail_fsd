    #  TAIL_FSD.py
    # ======================================================================
    #
    # Calculate the atomic tail for beta decay within sudden 
    # approximation using the result in Fukugita+Kubodera, 
    # Z.Phys.9,365(1981) adapted to the molecular case by considering 
    # the different ionisation energies and prefactor 2.0 (for the 
    # two electrons).
    #
    # This shell script calls the main script "exe.py" which executes the calculations with
    # python modules "tail.py & correction.py" and "ktilde.py" which calculates
    # the atomic tail and fractional recoil momentums (ktilde) at the atomic tail.
    #  
    # This code is originally (tail.f) written by A. Saenz, now modified  
    # for current needs by Ali Mert Turaclar.
    #
    # Arguments to be given:
    # ----------------------
    #         
    #        1st Argument: Isotopologue (T2, HT or DT)
    #        2nd Argument: Starting point of atomic tail, in eV. (i.e 240)
    #        3rd Argument: End point of atomic tail, in eV. (i.e 1500) 	  
    #        4th Argument: Number of energy steps. (i.e 500 steps of energy in between start - end)
    #        5th Argument: Application of energy broadening due to fractional recoil momentum.
    #                      Default: True. If this argument is passed as "-c" broadening will NOT be
    #                      applied. It is reccomended to skip this argument.
    #
    # ======================================================================
    #
    # Date: 10.02.2023
    # Author: A. Mert Turaclar
    # Last Change / Update: 24.11.2023
    #
    # ======================================================================
    #    START OF CODE

import sys
import math
import os
import numpy as np
import pandas as pd
import argparse
from scipy.interpolate import interp1d
from taillib.ktilde import ktilde
from taillib.tail import tail
from taillib.correction import recoilBroad
from exe import calc 

def main():
    print(' ')
    print(' ')
    print('           *****************************')
    print('           ***                       ***')
    print('           ***                       ***')
    print('           ***        TAIL_FSD       ***')
    print('           ***                       ***')
    print('           ***                       ***')
    print('           *****************************')
    print(' ')
    print(' ')

    # Taking arguments to be executed.
    parser = argparse.ArgumentParser(
        description='Calculates the atomic tail final state distribuiton.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--isotopologue", required=True, choices=['T2', 'DT', 'HT'], help="Isotopologue that is to be calculated: T2, DT or HT")
    parser.add_argument("-s", "--energy-start", type=float, required=True, help="Start energy of atomic tail. Note: Even though starting energy of the tail can be chosen freely, energies below 100 eV should not be calculated with the tail model. Since the conventional methods of FSD calculation is physically the sensible way to do so below 100 eV.")
    parser.add_argument("-n", "--energy-end", type=float, required=True, help="End energy of atomic tail")
    parser.add_argument("-e", "--energy-step", type=int, required=True, help="Number of energy steps to be calculated")
    parser.add_argument("-c", "--correction", action='store_true', help="Skip the application of effective fractional recoil momentum shift. If -c flag is given, correction will NOT be applied!")
    #parser.add_argument("-b", "--bin-edges", type=float, required=True, help="Bin edges to bin the final state distribution.")
    args = parser.parse_args()

    print(f"Isotopologue : {args.isotopologue}")    
    print(f"Start Energy =  {args.energy_start} eV")
    print(f"End Energy = {args.energy_end} eV")
    print(f"Number of Steps = {args.energy_step} \n")

    if (args.energy_start < 20):
        print("")
        print("         *** ATTENTION: For energies below 100 eV, the tail model is NOT a suitable way to calculate final state distribution.")
        print("                        tail model should be used for the continuum, energies (at least) above 100 eV.")
        print("                        please use already available final state distributions for energies below 100 eV. \n")
        print("         *** Calculation will NOT proceed, please do not use tail for low energies. \n")
        print("Calculation aborted due to unphysical start energy. Quitting...")
        quit()


    if (args.energy_start < 100):
        print("")
        print("         *** ATTENTION: For energies below 100 eV, the tail model is NOT a suitable way to calculate final state distribution.")
        print("                        tail model should be used for the continuum, energies (at least) above 100 eV.")
        print("                        please use already available final state distributions for energies below 100 eV. \n")
        
        
        answer = input("Proceed with this calculation? (yes/no) ")
        if (answer.lower() == "yes") or (answer.lower() == "y"):
            pass
        if (answer.lower() == "no") or (answer.lower() == "n"):
            print("quitting...")
            quit()
        

    # Generating the file name
    file_name = f"{args.isotopologue}_s{int(args.energy_start)}_n{int(args.energy_end)}-tail"

    # Sending the arguments to calculation script
    should_apply_correction = not args.correction
    calc(args.isotopologue, args.energy_start, args.energy_end, args.energy_step, should_apply_correction, file_name) #args.energy_step, should_apply_correction, file_name)
    
if __name__ == "__main__":
    main()

#   END OF CODE
