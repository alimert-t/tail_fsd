import numpy as np
from scipy.interpolate import interp1d

def spline(target, ref):
    # Extract R and E values from both datasets
    target_R = target[:,0]
    target_E = target[:,1]
    ref_R = ref[:,0]

    # Find the overlapping range of R values
    overlap_min_R = max(np.min(target_R), np.min(ref_R))
    overlap_max_R = min(np.max(target_R), np.max(ref_R))
    
    # Filter the target data to only include the overlapping range
    overlapping_target_R = target_R[(target_R >= overlap_min_R) & (target_R <= overlap_max_R)]
    overlapping_target_E = target_E[(target_R >= overlap_min_R) & (target_R <= overlap_max_R)]

    # Create the cubic spline interpolator for the overlapping range
    spline = interp1d(overlapping_target_R, overlapping_target_E, kind='cubic')

    # Filter the ref data to only include the overlapping R values
    truncated_ref_R = ref_R[(ref_R >= overlap_min_R) & (ref_R <= overlap_max_R)]
    truncated_ref_E = ref[:,1][(ref_R >= overlap_min_R) & (ref_R <= overlap_max_R)]

    # Interpolate the target E values over the truncated ref R values
    interpolated_E = spline(truncated_ref_R)

    # Combine the truncated ref R values with the interpolated E values
    interpolated_target_data = np.column_stack((truncated_ref_R, interpolated_E))
    truncated_ref_data = np.column_stack((truncated_ref_R, truncated_ref_E))

    return interpolated_target_data, truncated_ref_data
