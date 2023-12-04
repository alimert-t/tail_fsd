import numpy as np
import pandas as pd

def bin_distribution(df, bin_size):
    """
    Bins a combined probability distribution based on a specified bin size.

    Parameters:
    df (DataFrame): DataFrame with columns 'Energy [eV]' and 'Combined Prob. Dist. [eV^-1]'
    bin_size (float): The size of each bin in eV.

    Returns:
    DataFrame: Binned distribution with columns 'Bin Center [eV]' and 'Binned Probability'
    """
    # Determine the range of energy values
    min_energy = df['Energy [eV]'].min()
    max_energy = df['Energy [eV]'].max()

    # Create bin edges
    bin_edges = np.arange(min_energy, max_energy + bin_size, bin_size)

    # Compute the bin centers
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    # Initialize an array to store binned probabilities
    binned_probabilities = np.zeros(len(bin_centers))

    # Iterate over each bin and sum the probabilities
    for i in range(len(bin_centers)):
        # Find indices of df['Energy [eV]'] that fall into the current bin
        in_bin = (df['Energy [eV]'] >= bin_edges[i]) & (df['Energy [eV]'] < bin_edges[i + 1])
        # Sum up the probabilities in this bin
        binned_probabilities[i] = df.loc[in_bin, 'Prob. Dist. [eV^-1]'].sum()
    
    # Create a new DataFrame for the binned distribution
    binned_df = pd.DataFrame({'Energy [eV]': bin_centers, 'Binned Probability': binned_probabilities})

    return binned_df
