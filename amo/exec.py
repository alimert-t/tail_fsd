
#    START OF EXECUTION SCRIPT

import sys
import math
import os
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import ktilde
import tail
import recoilBroad

def calc(a, c, istep, corr):
        
    print("Calculation starts.")
    
    ehinev = 27.2113962

    ethrsd = a / ehinev
    b = a
    enanf = b / ehinev
    enend = c / ehinev
    enstep = (enend - enanf) / istep

    enueb = enanf - enstep
    istep += 1

    with open("transition.txt", "w") as fp:
        for i in range(1, int(istep)):
            eprime = enueb - ethrsd
            if eprime == 0:
                eprime = 1.0e-12
            elif eprime < 0:
                eprime = 0.1e-12

            enueb += enstep 
            enres = enueb * ehinev

            probability = tail(eprime, ethrsd, enueb, enstep)
            
            if eprime == 0.1e-12:
                probability += 0.000277

            fracRecoil = ktilde(enres)
            
            print("{:.5f}".format(enres), "             ", "{:.7e}".format(probability), "             ", "{:.5f}".format(fracRecoil), file=fp)
    
    header = ["Energy [eV]", "Prob. Density [eV^-1]", "Frac. Rec. Mom. [a_0^(-1)]"]    
    
    if corr == 1:
        dfResult = recoilBroad()
        dfResult.to_csv("out/" + 'tail_fsd' + "_" + sys.argv[1] + "_" + sys.argv[2]  + ".txt", sep="\t", index=False, header=header)
        print("")
        print("Results have been written into tail_fsd"+ "_" + sys.argv[1] + "_" + sys.argv[2]  + ".txt file.")
        print("")
        print(dfResult)
        print("")
        print("tail_ktilde.py is executed gracefully.")
        print("")
    else:
        dfResult = pd.read_csv("transition" + '.txt', sep='\\s+', header=None)
        dfResult.to_csv("out/" + 'tail_fsd'+ "_" + sys.argv[1] + "_" + sys.argv[2] + "_corr0" + '.txt', sep="\t", index=False, header=header)
        print("")
        print("Results have been written into tail_fsd"+ "_" + sys.argv[1] + "_" + sys.argv[2] + "_corr0" + ".txt file.")
        print("")        
        print(" ")
        print("Fractional recoil momentum shift is NOT applied!")
        print(" ")
        print(dfResult)
        print("")
        print("tail_ktilde.py is executed gracefully.")
        print("")
    
    scratch = "transition.txt"
    os.remove(scratch)

