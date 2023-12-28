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
from taillib.constants import ehinev

def calc(isotopologue, estart, eend, iStep, corr, fname):
        
    ionization_energies = {"T2":15.486, "DT":15.470, "HT":15.433} # T2: Phs.Rev. A 60(4).3013 (1999)
                                                                  # HT and DT are actually given as D2 and H2 in the paper.
                                                                  # They need re-calculation. (?)

    startingEnergy = estart / ehinev
    endingEnergy = eend / ehinev

    if isotopologue in ionization_energies:
        energyThreshold = ionization_energies[isotopologue] / ehinev

    energyStep = (endingEnergy - startingEnergy) / iStep 
    enueb = startingEnergy - energyStep

    result_data = []

    for i in range(1, iStep + 1):
        ePrime = enueb - energyThreshold
        if ePrime <= 0:
            ePrime = 1.0e-12
        enueb += energyStep 
        energyResult = enueb * ehinev
        # Calculating probabilities with tail function
        probability = tail(ePrime, energyThreshold, enueb, energyStep)
        # Calculation of fractional recoil momentum with function ktilde
        fracRecoil = ktilde(energyResult)
        result_data.append([energyResult, probability, fracRecoil])
    
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
        print("Fractional recoil momentum shift is NOT applied! \n \n")
    
    #binned_final_distribution = bin_distribution(dfResult, bin_size)
    #binned_final_distribution['Frac. Rec. Mom. [a_0^-1]'] = binned_final_distribution['Energy [eV]'].apply(ktilde)

    dfResult.to_csv(f"out/{fname}.fsd", sep="\t", index=False, header=header)

    #pd.set_option('display.max_rows', None) # Print the data without truncating the lines
    # Should we print the full result on the terminal? Or not? I'm note sure. So, for now, it is printed but will be truncated
    print(f"Results have been written into {fname}.fsd file. \n")
    print(dfResult) #.to_string(index=False)) # If we truncate it, index part is neccessary. If not, removing the index is good idea, I think
    print("\n \n")
    print("exe.py and tail_fsd.py executed gracefully. \n")

#   END OF CODE
