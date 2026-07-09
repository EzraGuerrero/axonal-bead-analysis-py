# Axonal Damage Analysis (Python)

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![DOI](https://img.shields.io/badge/DOI-10.1111/ejn.70328-blue)

A Python-based implementation of a high-throughput image analysis workflow to quantify axonal beads relative to neurite area — a biomarker for axonal damage and neurodegeneration. Originally developed in [ImageJ](https://github.com/EzraGuerrero/axonal-damage-analysis/tree/main), this port enables reproducible, scalable analysis with modern Python tools.

> **Used in publication**: [Guerrero Gonzalez, E., et al. (2025). *Development of a Human Preclinical Platform for the Identification of Neuroprotective Compounds.* European Journal of Neuroscience, 62(10), e70328.](https://doi.org/10.1111/ejn.70328)


## Purpose

Quantify axonal bead density and distribution in fluorescent microscopy images of neurons. This metric serves as a sensitive readout for axonal integrity in neurodegenerative disease models.


## Biological Background

Axonal beads (or spheroids) are swellings that form along neuronal axons under stress conditions (e.g., glutamate excitotoxicity).

These beads can be identified on iPSC-derived neurons exposed to excessive glutamate concentrations as accumulation of neurofilament staining (e.g., SMI-31).

This tool:

1. Measures total neurofilament-positive (SMI-31) neurite area
2. Counts axonal beads via intensity thresholding and particle analysis
3. Normalizes bead count per neurite area (beads / 1000 µm²)

This normalized metric serves as a robust, scalable readout for axonal damage in high-content drug screening.

A detailed [protocol](https://github.com/EzraGuerrero/axonal-bead-analysis-py/blob/main/docs/Protocol.md) can be found in the `docs` folder

---

### Requirements

- Python 3.11+
- Packages listed in `requirements.txt`

### Instalation

```bash
# Clone repository
git clone https://github.com/EzraGuerrero/AxonBead.git
cd axonal-bead-analysis-py

# Create environment
conda create -n axonal-bead python=3.11
conda activate axonal-bead

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Basic usage
python src/run_analysis.py --input sample_data

# Custom threshold
python src/run_analysis.py --input sample_data --bead-threshold 200

# Custom output folder
python src/run_analysis.py --input sample_data --output my_results

# Skip QC images (faster)
python src/run_analysis.py --input sample_data --no-qc

# Get help
python src/run_analysis.py --help
```

### CLI arguments

| Argument           | Short | Default          | Description                |
| ------------------ | ----- | ---------------- | -------------------------- |
| `--input`          | `-i`  | required         | Folder with `.czi` files   |
| `--output`         | `-o`  | `example_output` | Results folder             |
| `--scale`          |       | `0.3126`         | µm per pixel               |
| `--bead-threshold` |       | `220`            | Manual threshold for beads |
| `--no-qc`          |       | `False`          | Skip overlay images        |

### Parameters

Configurable thresholds and filters for robustness:

| Parameter            | ImageJ Default | Python Default | Description                              |
| -------------------- | -------------- | -------------- | ---------------------------------------- |
| DoG sigma1           | 5              | 5              | Larger sigma for noise suppression       |
| DoG sigma2           | 1              | 1              | Smaller sigma for filament preservation  |
| Neurite threshold    | Triangle auto  | Triangle auto  | Auto-threshold for neurite mask          |
| Bead threshold       | 200 (manual)   | 220 (manual)   | Manual 8-bit threshold for beads         |
| Bead min size        | 4 px           | 25 px          | Minimum bead area                        |
| Bead max size        | 80 px          | 200 px         | Maximum bead area                        |
| Bead min circularity | 0.3            | 0.3            | Minimum roundness (0 = line, 1 = circle) |

### Output

CSV, Excel, and optional QC images in the specified output folder.

![Neurite Analysis Workflow](../example_output/analysis_workflow.png)

*Figure 1: Analysis workflow. (A) Raw SMI-31 image. (B) Difference of Gaussians filter enhances filaments. (C) Binary mask of neurofilament-positive area. (D) Original image for bead detection. (E) Bead mask (binary) after thresholding. (F) Overlay showing detected beads (red).*


## Important Notes

- Pre-test your bead threshold! Open a representative image, split channels, select green, and use Image > Adjust > Threshold (ImageJ) or inspect intensity histogram (Python) to find a value where only beads are highlighted.
- While Neurite area measurement uses DoG + Triangle auto-threshold in the ImageJ macro version, the Python version uses scikit-image.filters.threshold_triangle.
- Bead detection uses manual thresholding in both versions to ensure user control over this critical parameter.

---

# ImageJ Macro Version

[ImageJ macro version](https://github.com/EzraGuerrero/axonal-damage-analysis/tree/main).

---
## Publication

This tool was used in the analysis pipeline for:

[Guerrero Gonzalez, E., et al. (2025). *Development of a Human Preclinical Platform for the Identification of Neuroprotective Compounds.* European Journal of Neuroscience, 62(10), e70328.](https://doi.org/10.1111/ejn.70328)

## License

MIT License — see [LICENSE](LICENSE)

## Author

Ezra Guerrero González, PhD
