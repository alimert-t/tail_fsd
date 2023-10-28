#    START OF EXECUTION CODE

import sys
import math
import os
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from amo.ktilde import ktilde
from amo.tail import tail
from amo.correction import recoilBroad

def calc(a, c, istep, corr, fname):

    # Hartree to eV conversion
    ehinev = 27.2113962

    # Conversion of threshold energy, start and end energies to eV 
    ethrsd = a / ehinev
    b = a
    enanf = b / ehinev
    enend = c / ehinev
    # Calculating energy steps
    enstep = (enend - enanf) / istep
    enueb = enanf - enstep
    istep += 1

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
            
            print("{:.5f}".format(enres), "             ", "{:.7e}".format(probability), "             ", "{:.5f}".format(fracRecoil), file=fp)
    
    header = ["Energy [eV]", "Prob. Density [eV^-1]", "Frac. Rec. Mom. [a_0^(-1)]"]    
    
    # Checking if energy correction (fractional recoil momentum broadening)
    # will be aplied or not
    if corr:
        # Here, correction is applied (broadening)
        dfResult = recoilBroad()
        # Results are written into generated file_name
        dfResult.columns = ['Energy [eV]', 'Prob. Dist. [eV^-1]', 'Frac. Rec. Mom. [a_0^-1]']
        dfResult.to_csv(f"out/{fname}.fsd", sep="\t", index=False, header=header)
        print("")
        print(f"Results have been written into {fname}.fsd file.")
        print("")
        print(dfResult)
        print("")
        print("exe.py and run_tail_ktilde.py executed gracefully.")
        print("")
    else:
        # No correction applied
        dfResult = pd.read_csv("transition" + '.txt', sep='\\s+', header=None)
        dfResult.columns = ['Energy [eV]', 'Prob. Dist. [eV^-1]', 'Frac. Rec. Mom. [a_0^-1]']
        # Results are written into generated file_name
        dfResult.to_csv(f"out/{fname}_corrNO.fsd", sep="\t", index=False, header=header)
        print("")
        print(f"Results have been written into {fname}_corrNO.fsd file.")
        print("")        
        print(" ")
        print("Fractional recoil momentum shift is NOT applied!")
        print(" ")
        print(dfResult)
        print("")
        print("exe.py and run_tail_ktilde.py executed gracefully.")
        print("")
    
    # Scratch 'transition.txt' is removed, ready to be generated again for next calculations
    scratch = "transition.txt"
    os.remove(scratch)

#   END OF CODE
