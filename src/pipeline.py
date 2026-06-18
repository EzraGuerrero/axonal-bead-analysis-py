"""
Axonal Damage Analysis Pipeline
Functions for neurite area and bead detection from CZI images.
"""

# IMPORTS
import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from skimage import filters, measure, util
from scipy import ndimage
import czifile

# FUNCTIONS
def read_czi(file_path):
    """
    Read CZI file and extract green channel (SMI-31)
    """
    img = czifile.imread(file_path)
    # Squeeze and extract channel 1 (green)
    green = np.squeeze(img)[1]
    return green

def measure_neurite_area(green, sigma1=5, sigma2=1, scale_um_per_px=0.3126):
    """
    Measure neurofilament-positive area using Difference of Gaussians and
    Triangle auto-threshold.
    """
    # Difference of Gaussians (inverted)
    green_float = green.astype(float)
    gauss1 = ndimage.gaussian_filter(green_float, sigma=sigma1)
    gauss2 = ndimage.gaussian_filter(green_float, sigma=sigma2)
    dog = gauss2 - gauss1

    # Triangle auto-threshold
    neurite_thresh = filters.threshold_triangle(dog)
    neurite_mask = dog > neurite_thresh

    # Measure area
    area_pixels = np.sum(neurite_mask)
    area_um2 = area_pixels * (scale_um_per_px **2)

    # Get results
    return {
        'area_um2': area_um2,
        'area_pixels': area_pixels,
        'neurite_threshold': neurite_thresh,
        'mask': neurite_mask,
        'DoG': dog
    }

def count_beads(green, area_um2, percentile=98, min_size=25, max_size=200, min_circularity=0.3):
    """
    Count axonal beads using percentile-based threshold and shape filtering.
    """
    # Percentile-based threshold
    # bead_thresh = np.percentile(green, percentile)
    bead_thresh = 220 # Has to be set manually based on a picture with beads
    bead_mask = green > bead_thresh

    # Label connected components
    labeled = measure.label(bead_mask)
    regions = measure.regionprops(labeled)

    bead_count = 0
    for reg in regions:
        
        # Size filter
        if reg.area < min_size or reg.area > max_size:
            continue

        # Circularity
        if reg.perimeter > 0:
            circularity = 4 * np.pi * reg.area / (reg.perimeter ** 2)
        else:
            circularity = 0
        if circularity < min_circularity:
            continue

        bead_count += 1

    # Normalization
    beads_per_1000um2 = (bead_count / area_um2 * 1000) if area_um2 > 0 else 0

    # Get results
    return{
        'bead_count': bead_count,
        'bead_threshold': bead_thresh,
        'beads_per_1000um2': beads_per_1000um2,
        'bead_mask': bead_mask
    }

def process_image(file_path, scale_um_per_px=0.3126, save_qc=False, output_dir=None):
    """
    Process a single CZI image: neurite area + bead counting.
    """
    print(f"\nProcessing: {os.path.basename(file_path)}")

    # Read image
    green = read_czi(file_path)
    print(f" Image shape: {green.shape}")

    # Neurite area
    neurite = measure_neurite_area(green, scale_um_per_px=scale_um_per_px)
    print(f" Neurite area: {neurite['area_um2']:.2f} µm² (Neurite threshold: {neurite['neurite_threshold']:.2f})")

    # Bead counting
    beads = count_beads(green, neurite['area_um2'])
    print(f" Bead count: {beads['bead_count']} (Bead threshold: {beads['bead_threshold']:.2f})")
    print(f" Beads/1000µm²: {beads['beads_per_1000um2']:.4f}")

    # Save QC images if requested
    if save_qc and output_dir:
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(file_path))[0]

        # Neurite mask
        plt.imsave(f"{output_dir}/NeuriteMask_{base_name}.png", neurite['mask'], cmap='gray')

        # Bead overlay
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(green, cmap='gray')
        ax.imshow(beads['bead_mask'], cmap='Reds', alpha=0.5)
        ax.set_title(f"Beads: {beads['bead_count']}")
        ax.axis('off')
        plt.savefig(f"{output_dir}/BeadOverlay_{base_name}.png", dpi=150, bbox_inches='tight')
        plt.close()

    # Get results
    return{
        'filename': os.path.basename(file_path),
        'neurite_area_um2': neurite['area_um2'],
        'bead_count': beads['bead_count'],
        'beads_per_1000um2': beads['beads_per_1000um2'],
        'scale_um_per_pixel': scale_um_per_px,
        'neurite_threshold': neurite['neurite_threshold'],
        'bead_threshold': beads['bead_threshold']
    }

# BATCH PROCESSING

# C:/Users/ezra.gonzalez/axonal-bead-analysis-py/sample_data/sample_output
# C:/Users/pinap/github_projects/axonal-bead-analysis-py/sample_data/sample_output
    
def process_folder(input_dir, output_dir='C:/Users/pinap/github_projects/axonal-bead-analysis-py/sample_data/sample_output', scale_um_per_px=0.3126):
    """
    Process all CZI files in a folder and save summary CSV.
    """
    # Find all CZI files
    czi_files = glob.glob(os.path.join(input_dir, '*.czi'))
    print(f"Found {len(czi_files)} CZI files")

    # Process each
    results = []
    for file_path in sorted(czi_files):
        result = process_image(file_path, scale_um_per_px=scale_um_per_px, save_qc=True, output_dir=output_dir)
        results.append(result)

    # Cerate a summary DataFrame
    df = pd.DataFrame(results)

    # CSV export
    csv_path = os.path.join(output_dir, 'Summary_Results.csv')
    df.to_csv(csv_path, index=False)
    print(f"\nSummary saved (csv): {csv_path}")

    # Excel export
    excel_path = os.path.join(output_dir, 'Summary_Results.xlsx')
    df.to_excel(excel_path, index=False, sheet_name='Results')
    print(f"Excel saved: {excel_path}")
    
    return df