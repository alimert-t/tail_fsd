# TAIL_FSD 

The 'tail_fsd' package is a Python package that calculates the atomic tail for beta decay of TS (where S is T, H or D) within sudden approximation using the result in Fukugita+Kubodera, Z.Phys.9,365(1981) adapted to the molecular case by considering the different ionization energies and a prefactor of 2.0 (for the two electrons). 'tail_fsd.py' code initiates the execution script "exe.py" which then runs the neccesary Python modules inside 'taillib'.

'tail_fsd' package also provides a calculation code that calculates the overlaps for final state distribution calculations, using the code 'tail_overlap.py'. This takes potential energy curves of mother and daughter molecule, and calculates the overlaps using the 'taillib' modules.

## tail_fsd

The code takes four arguments:

1. Parent molecule (T2, HT or DT)
2. Starting point of the atomic tail (eV):
    *Important Note*: Please do NOT use this code for starting energies below 100 eV. Below 100 eV, close (and below) to ionization threshold energy, the tail model is NOT a physically sensible model. This model / package only makes sense for calculations with higher starting energy. For energies below 100 eV, please use other programs.
3. End point of the atomic tail (eV)
4. Bin widths:
    The package provides a binned FSD, with a given bin width.
5. Correction:
    The correction flag is by default False, which means that the program APPLIES the energy shift / nuclear broadening by default. It is reccomended to just skip this flag, and use as is.

#### Example usage:

$python3 tail_fsd.py -i T2 -s 240 -n 3000 -b 2 

### Output
The code writes the results to a .fsd file in the "/out" folder. The file is named tail_fsd_TS_<start_point>_<end_point>_<bin_width>.fsd. The file contains three columns:

1. Energy [eV]
2. Binned Probability
3. Frac. Rec. Mom. [a_0^(-1)]

The code also prints the results to the console.

## tail_overlap

The code takes two arguments:

1. Parent molecule potential energy file
2. Daughter molecule potential energy file
3. Flag to indicate R-independent calculation. If set, a single R value is used for all calculations. The default is False, meaning that if this flag is not given, calculation is done as a function of R.
4. The constant R point to use for R-independent calculations. This flag is only neccesary if the flag above is given.
5. File name, extension is set to ".snm" by default.

#### Example Usage:

$python tail_overlap.py -p t2st001Doss.txt -d HeTpst001Mert.pot -n HeTpst001Mert

$python tail_overlap.py -p t2st001Doss.txt -d HeTpst001Mert.pot -n HeTpst001Mert -r -v 1.431

### Output

Output is in the format of other AMO group overlap files (hence the .snm extension). Mainly, in contains two columns:

1. R value (a.u.)
2. Overlaps

## Requirements
The following packages are required to run the package:

- NumPy
- pandas
- scipy


## Disclaimer

The atomic tail calculation code is originally written by A. Saenz. It has been modified by A. M. Turaclar for current needs such as the introduction of fractional recoil momentum and broadening originated from it. 

The last change/update: 08.12.2023
