# Tail Ktilde 

## Introduction
This is a Python code that calculates the atomic tail for beta decay within sudden approximation using the result in Fukugita+Kubodera, Z.Phys.9,365(1981) adapted to the molecular case by considering the different ionization energies and a prefactor of 2.0 (for the two electrons). run\_tail\_ktilde.py script initiates the execution script "exe.py" which calls three other Python modules: tail.py, correction.py, and ktilde.py, which calculate the atomic tail and fractional recoil momentums (ktilde) at the atomic tail.

## Requirements
The following packages are required to run the code:

- NumPy
- pandas
- scipy

## Usage
The code takes four arguments:

1. Starting point of the atomic tail (eV)
2. End point of the atomic tail (eV)
3. Number of energy steps
4. 1 or 0, whether to apply the fractional recoil momentum shift (1: Apply, 0: Do not apply), ("1" is advised for physically correct result)

### Example usage:

$python3 run\_tail\_ktilde.py 240 1000 380 1

## Output
The code writes the results to a .txt file in the "out" folder. The file is named tail\_fsd_<start_point>_<end_point>.txt for the case where the fractional recoil momentum shift is applied, and tail_fsd_<start_point>_<end_point>_corr0.txt for the case where it is not applied. The file contains three columns:

1. Energy [eV]
2. Prob. Density [eV^-1]
3. Frac. Rec. Mom. [a\_0^(-1)]

The code also prints the results to the console.

##
The atomic tail calculation code is originally written by A. Saenz. It has been modified by Ali Mert Turaclar for current needs such as the introduction of fractional recoil momentum and broadening originated from it. 

The last change/update: 10.02.2023
