from scipy.interpolate import interp1d
import numpy as np
import argparse

def spline(target, ref):
#parser = argparse.ArgumentParser(
#    description='''Performs spline interpolation to potential energy curves to
#    match R points of two potential energy curves. These potential energy
#    curves then to be used as input for tail_overlap.py.''',
#    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#parser.add_argument('-t', '--target-potential', type=str, required=True, help='Target potential energy file to be interpolated.')
#parser.add_argument('-r', '--refference-potential', type=str, required=True, help'Refference potential energy, the R points of this file will be used as a refference for interpolation.')

#args = parsser.parse_args()
#target = args.target_potential
#ref = args.refference_potential

    target_data = target #np.genfromtxt(target)
    ref_data = ref #np.genfromtxt(ref)

    target_R = target_data[:,0]
    target_E = target_data[:,1]
    ref_R = ref_data[:,0]
    ref_E = ref_data[:,1]

    spline = interp1d(target_R, target_E, kind='cubic')

    target_R_interp = spline(ref_R)
    return target_R_interp
