#    START OF EXECUTION CODE

import sys
import math
import os
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from taillib.ktilde import ktilde
from taillib.tail import tail
from taillib.correction import recoilBroad
from taillib.correction import shift_start_energy
from taillib.bin import bin_distribution

def calc(isotopologue, estart, eend, corr, fname, bin_size):
        
    print("Calculation starts.")
    print("")

    ionization_energies = {"T2":15.486, "DT":15.470, "HT":15.433} # T2: Phs.Rev. A 60(4).3013 (1999)
                                                                  # HT and DT are actually given as D2 and H2 in the paper.
                                                                  # They need re-calculation. (?)

    ehinev = 27.2113962
    enanf = estart / ehinev
    enend = eend / ehinev

    if isotopologue in ionization_energies:
        ethrsd = ionization_energies[isotopologue] / ehinev

    enstep = 0.5 / ehinev 

    enueb = enanf - enstep

    istep = int((enend-enanf) / enstep) + 1

    # Starting the calculation, results will be written into 'transition.txt'
    # 'transition.txt' is a scratch file, it will be deleted
    with open("transition.txt", "w") as fp:
        for i in range(1, int(istep)):
            eprime = enueb - ethrsd
            if eprime == 0:
                eprime = 1.0e-12
            elif eprime < 0:
                eprime = 0.1e-12

            enueb += enstep 
            enres = enueb * ehinev
            
            # Calculating probabilities with tail function
            probability = tail(eprime, ethrsd, enueb, enstep)
            
            if eprime == 0.1e-12:
                probability += 0.000277

            # Calculation of fractional recoil momentum with function ktilde
            fracRecoil = ktilde(enres)
            
            print("{:.5f}".format(enres), "\t", "{:.7e}".format(probability), "\t", "{:.5f}".format(fracRecoil), file=fp)
    
    header = ["Energy [eV]", "Binned Prob.", "Frac. Rec. Mom. [a_0^(-1)]"]    

    # Checking if energy correction (fractional recoil momentum broadening)
    # will be aplied or not
    if corr:
        # Here, correction is applied (broadening)
        dfResult = pd.read_csv("transition" + '.txt', sep='\\s+', header=None)
        dfResult = recoilBroad(isotopologue)
        dfResult.columns = ['Energy [eV]', 'Prob. Dist. [eV^-1]', 'Frac. Rec. Mom. [a_0^-1]']

    else:
        # No correction applied
        dfResult = pd.read_csv("transition" + '.txt', sep='\\s+', header=None)
        dfResult.columns = ['Energy [eV]', 'Prob. Dist. [eV^-1]', 'Frac. Rec. Mom. [a_0^-1]']
        fname += "_noCorr"
        print(" ")
        print("Fractional recoil momentum shift is NOT applied!")
        print(" ")
    
    binned_final_distribution = bin_distribution(dfResult, bin_size)
    binned_final_distribution['Frac. Rec. Mom. [a_0^-1]'] = binned_final_distribution['Energy [eV]'].apply(ktilde)
    binned_final_distribution.to_csv(f"out/{fname}.fsd", sep="\t", index=False, header=header)
    
    print("")
    print(f"Results have been written into {fname}.fsd file. \n")
    print(binned_final_distribution)
    print("exe.py and run_tail_ktilde.py executed gracefully.")
    print("")

    # Scratch 'transition.txt' is removed, ready to be generated again for next calculations
    scratch = "transition.txt"
    os.remove(scratch)

#   END OF CODE
