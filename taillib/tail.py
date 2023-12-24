import sys
import math
import numpy as np

def tail(eprime, ethrsd, enueb, enstep):

    ehinev = 27.2113962
    pi = np.pi

    rydueb = 2 * eprime
    dnu = math.sqrt(rydueb)

    num = (-8) * math.exp(-(4/dnu) * math.atan(dnu))
    denum = math.sqrt(1 - math.exp(-((4 * pi) / dnu))) * (1+ rydueb) ** 2

    tpryd = (num/denum) ** 2
    tptail = 2 * tpryd

    result = tptail * 2
    prob = result / ehinev

    return prob
