import sys
import math 
import tail

def overlap(e_start, e_end):

    istep = 1

    ehinev = 27.2113962
    enanf = e_start / ehinev
    enend = e_end / ehinev

    enueb = enanf
    istep += 1

    for i in range(1, int(istep)):
        eprime = enueb
        if eprime <= 0:
            eprime = 1.0e-12

        probability = tail.tail(eprime, 0, enueb, 1)
        
        overlap = math.sqrt(probability)
        return(overlap)
