import sys
import math
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

def recoilBroad():

    dfT = pd.read_csv("transition" + '.txt', sep='\\s+', header=None)
    dfT.columns = ["e", "p", "k2"]

    dfC = pd.read_csv("amo/"+"energyShift" + '.txt', sep='\\s+', header=None)
    dfC.columns = ["k1","s"]

    ktildeCorr = dfC["k1"]
    energyShift = dfC["s"]

    interpFunc = interp1d(ktildeCorr, energyShift)

    ktildeTail = dfT["k2"]  
    tailCorrection = interpFunc(ktildeTail)

    tailCorrected = dfT["e"] + tailCorrection

    #dfN = np.column_stack([tailCorrected, dfT["p"], dfT["k2"]])
    dfN = pd.DataFrame(np.column_stack([tailCorrected, dfT["p"], dfT["k2"]]), columns=["Energy", "Probability Density", "Ktilde"])
    return dfN



