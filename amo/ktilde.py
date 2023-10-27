import sys
import math

def ktilde(enres):
    atomicMass = 931.4940954E06
    alpha = 137.035999139
    spectatorMass = 3.0160492779
    electronMass = 510998.9461
    tritiumMass = spectatorMass
    ehinev = 27.2113962
    pi = math.acos(-1)

    kineticEnergy = 18573.24 - enres
    me = electronMass / atomicMass
    pi_e = math.sqrt(kineticEnergy * (kineticEnergy + 2 * electronMass)) / electronMass
    m = spectatorMass / (spectatorMass + tritiumMass + 2 * me)

    kTilde = alpha * (m) * pi_e
    
    return kTilde
