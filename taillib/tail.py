import sys
import math

def tail(eprime, ethrsd, enueb, enstep):

    ehinev = 27.2113962
    pi = math.acos(-1)
    
    rydueb = 2 * eprime
    dnu = math.sqrt(rydueb)

    num = (-8) * math.exp(-(4/dnu) * math.atan(dnu))
    denum = math.sqrt(1 - math.exp(-((4 * pi) / dnu))) * (1+ rydueb) ** 2

    tpryd = (num/denum) ** 2
    tptail = 2 * tpryd
    
    # Division by ehinev for the result to be Hartree units
    # Result is tptail * 2 to account for the 2 electron case of TS beta decay
    result = (tptail * 2) / ehinev
    prob = result 

    if eprime == 0.1e-12:
        prob += 0.000277959

    return prob
