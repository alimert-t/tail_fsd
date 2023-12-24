#    START OF EXECUTION CODE

import sys
import math
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from taillib.ktilde import ktilde
from taillib.tail import tail
from taillib.correction import recoilBroad
from taillib.correction import shift_start_energy
from taillib.bin import bin_distribution

def calc(isotopologue, estart, eend, corr, fname):
        
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

    result_data = []

    for i in range(1, int(istep)):
        eprime = enueb - ethrsd
        if eprime <= 0:
            eprime = 1.0e-12
        enueb += enstep 
        enres = enueb * ehinev
        # Calculating probabilities with tail function
        probability = tail(eprime, ethrsd, enueb, enstep)
        # Calculation of fractional recoil momentum with function ktilde
        fracRecoil = ktilde(enres)
        result_data.append([enres, probability, fracRecoil])
    
    header = ["Energy [eV]", "Prob. Density [eV^-1]", "Frac. Rec. Mom. [a_0^(-1)]"]    
    dfResult = pd.DataFrame(result_data, columns=['e', 'p', 'k'])

    # Checking if energy correction (fractional recoil momentum broadening)
    # will be aplied or not
    if corr:
        # Here, correction is applied (broadening)
        dfResult = recoilBroad(isotopologue, dfResult, header)

    else:
        # No correction applied
        fname += "_noCorr"
        print(" ")
        print("Fractional recoil momentum shift is NOT applied!")
        print(" ")
    
    #binned_final_distribution = bin_distribution(dfResult, bin_size)
    #binned_final_distribution['Frac. Rec. Mom. [a_0^-1]'] = binned_final_distribution['Energy [eV]'].apply(ktilde)

    dfResult.to_csv(f"out/{fname}.fsd", sep="\t", index=False, header=header)
    
    print("")
    print(f"Results have been written into {fname}.fsd file. \n")
    print(dfResult)
    print("exe.py and run_tail_ktilde.py executed gracefully.")
    print("")

#   END OF CODE
