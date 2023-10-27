import sys
import math 
import tail

def overlap(e_start, e_end, e_step):

    a = e_start
    c = e_end
    istep = e_step

    ehinev = 27.2113962

    ethrsd = 0
    b = a 
    enanf = b / ehinev
    enend = c / ehinev
    enstep = (enend - enanf) / istep

    enueb = enanf - enstep
    istep += 1

    for i in range(1, int(istep)):
        eprime = enueb - ethrsd
        if eprime == 0:
            eprime = 1.0e-12
        elif eprime < 0:
            eprime = 0.1e-12

        enueb += enstep 
        enres = enueb * ehinev

        probability = tail.tail(eprime, ethrsd, enueb, enstep)
            
        if eprime == 0.1e-12:
            probability += 0.000277
            
        overlap = math.sqrt(probability)
        return(overlap)
