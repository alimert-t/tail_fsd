import sys
import math
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from taillib.ktilde import ktilde

def recoilBroad(isotopologue):

    path = "input/correction/"
    
    dfT = pd.read_csv("transition" + '.txt', sep='\\s+', header=None)
    dfT.columns = ["e", "p", "k2"]
    
    if isotopologue == "T2":
        dfC = pd.read_csv(path+"hetp_shift_interpolated.dat", sep='\t', header=None)
    elif isotopologue == "DT":
        dfC = pd.read_csv(path+"hedp_shift_interpolated.dat", sep='\t', header=None)
    elif isotopologue == "HT":
        dfC = pd.read_csv(path+"hehp_shift_interpolated.dat", sep='\t', header=None)
    else:
        print(f"Unkown isotopologue: {istopologue}")
    
    dfC.columns = ["k1","s"]

    ktildeCorr = dfC["k1"]
    energyShift = dfC["s"]

    interpFunc = interp1d(ktildeCorr, energyShift)

    ktildeTail = dfT["k2"]  
    tailCorrection = interpFunc(ktildeTail)

    tailCorrected = dfT["e"] + tailCorrection

    dfN = pd.DataFrame(np.column_stack([tailCorrected, dfT["p"], dfT["k2"]]), columns=["Energy", "Probability Density", "Ktilde"])
    return dfN

def shift_start_energy(estart, isotopologue):

    ktilde_start = ktilde(estart)

    path = "input/correction/"

    # Select the appropriate file based on isotopologue
    if isotopologue == "T2":
        dfC = pd.read_csv(path+"hetp_shift_interpolated.dat", sep='\t', header=None)
    elif isotopologue == "DT":
        dfC = pd.read_csv(path+"hedp_shift_interpolated.dat", sep='\t', header=None)
    elif isotopologue == "HT":
        dfC = pd.read_csv(path+"hehp_shift_interpolated.dat", sep='\t', header=None)
    else:
        raise ValueError(f"Unknown isotopologue: {isotopologue}")

    dfC.columns = ["k1", "s"]

    # Interpolation
    interpFunc = interp1d(dfC["k1"], dfC["s"], fill_value="extrapolate")

    # Calculate the energy shift for ktilde_start
    energy_shift = interpFunc(ktilde_start)
    
    estart -= energy_shift

    return estart
