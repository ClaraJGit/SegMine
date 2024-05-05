import os
import numpy as np 

def save_median_morphometry(cells, site_id, well_id, output_file):
    # Calculate median metrics for all cells
    nb_cells = len(cells)
    areas = [cell.morphometry['area'] for cell in cells]
    min_diameters = [cell.morphometry['min_diam'] for cell in cells]
    max_diameters = [cell.morphometry['max_diam'] for cell in cells]
    median_area = np.median(areas)
    median_min_diameter = np.median(min_diameters)
    median_max_diameter = np.median(max_diameters)
    intensities = [cell.morphometry['intensities'] for cell in cells]
    #median_intensities = np.median(np.array(intensities), axis=0).tolist()
    
    # Write median metrics to the output file
    with open(output_file, "a") as file:  # Use "a" for append mode
        file.write(f"{well_id},{site_id},{nb_cells},{median_area},{median_min_diameter},{median_max_diameter}\n")
#,{','.join(map(str, median_intensities)}}

def calculate_compound_weight(row):
    # Conversion factors
    nanoliter_to_liter = 1e-9
    micromole_to_mole = 1e-6
    mole_to_gram = 1e-3
    microgram_to_picogram = 1e6

    # Extract values from the row
    volume = row['cmpd_vol'] * nanoliter_to_liter  # Convert volume to liters
    concentration = row['cmpd_conc'] * micromole_to_mole  # Convert concentration to moles
    concentration_unit = row['cmpd_conc_unit']  # Concentration unit

    # Check if concentration unit is a percentage
    if concentration_unit == 'perc':
        # If concentration unit is percentage, assume volume is total volume (e.g., 100% of total volume)
        # Adjust concentration to micromoles per liter
        concentration *= 1e-6  # Convert percentage to fraction
        volume = 1.0  # Total volume is 1 liter

    # Calculate compound weight in grams
    compound_weight = volume * concentration

    # Convert compound weight to picograms
    compound_weight_picograms = compound_weight * mole_to_gram * microgram_to_picogram

    return compound_weight_picograms

def dmso_percentage_to_microMoles(percentage):
    # Density of DMSO (grams per milliliter)
    density_g_per_ml = 1.1
    
    # Molar mass of DMSO (grams per mole)
    molar_mass_g_per_mol = 78.13
    
    # Convert density to grams per liter (g/L)
    density_g_per_L = density_g_per_ml * 1000
    
    # Convert grams per liter to moles per liter (mol/L)
    moles_per_L = density_g_per_L / molar_mass_g_per_mol
    
    # Convert moles per liter to micromoles per liter (µmol/L)
    micromoles_per_L = moles_per_L * 1e6
    
    # Calculate the microMoles for the given percentage (%v/v)
    microMoles = (percentage / 100) * micromoles_per_L
    
    return microMoles


def calculate_stock_in_mM(row):
    concentration_unit = row['stock_conc_unit']  # Concentration unit
    if concentration_unit == 'perc':
        dmso_micromole = dmso_percentage_to_microMoles(row['stock_conc'])
    elif concentration_unit == 'mM':
        dmso_micromole = row['stock_conc']
    return dmso_micromole00