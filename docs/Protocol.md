# Protocol: Quantification of Axonal Bead Formation as a Readout of Neurite Damage

## 1. Background and Rationale

Axonal loss is a key driver of clinical progression in multiple sclerosis and other neurodegenerative diseases (Reynolds et al., 2011). Glutamate excitotoxicity is a major contributor to neuronal death and axonal damage (Woo et al., 2021). This protocol describes an in vitro assay to quantify axonal damage induced by glutamate treatment, using axonal beads (spheroids) as a morphological readout.

Axonal beads are focal swellings that form along neurofilament-positive (SMI-31+) filaments under excitotoxic stress. These structures are characterised by high-intensity neurofilament staining and can be quantified relative to total neurite area to provide a robust, normalised metric of axonal damage suitable for drug screening.

**Key advantages of this assay:**
- Compatible with high-content screening platforms
- Normalised readout (beads per neurite area) controls for neurite density variations
- Responds to neuroprotective compounds (demonstrated with IL-4, minocycline, pioglitazone, sPIF)

**Publication:** Guerrero Gonzalez, E., et al. (2025). *Development of a Human Preclinical Platform for the Identification of Neuroprotective Compounds.* European Journal of Neuroscience, 62(10), e70328. [https://doi.org/10.1111/ejn.70328](https://doi.org/10.1111/ejn.70328)

---

## 2. Materials

### 2.1 Cell Culture
- Human induced neurons (hiNs) differentiated to mature neuronal morphology
- Maturation: 22 days in vitro (DIV 22) before treatment

### 2.2 Reagents
- L-Glutamate (1 mM final concentration)
- HCl vehicle control (equivalent volume, pH-matched)

### 2.3 Immunofluorescence
- Primary antibody: anti-SMI-31 (unphosphorylated neurofilament H)
- Secondary antibody: Alexa Fluor 488 anti-mouse (Goat)
- Nuclear stain: DAPI

---

## 3. Image Acquisition

| Parameter | Specification |
|-----------|---------------|
| Microscope | Confocal laser scanning microscope |
| Objective | 20× air |
| Channels | 2 (blue: DAPI; green: SMI-31) |
| Z-stack | Single optical section (snapshot) |
| Resolution | 1024 × 1024 pixels |
| Pixel size | 0.3126 µm/pixel |

**Critical notes:**
- Acquire images at consistent laser power and gain settings across all conditions
- Include untreated and vehicle-only controls in every experiment
- Capture representative fields with dense but non-overlapping neurite networks
- Acquire image snaps or generate Z-stack Maximum Intensity Projection

---

## 4. Image Analysis Workflow

### 4.1 Overview

The analysis pipeline consists of three main steps:
1. **Neurite area measurement** — total SMI-31+ filamentous area
2. **Axonal bead detection** — bright, round swellings along filaments
3. **Normalisation** — bead count per 1000 µm² neurite area

### 4.2 Step-by-Step

#### Step 1: Channel Extraction
Extract the green channel (SMI-31) from the CZI file. The blue channel (DAPI) is not used for quantification.

#### Step 2: Neurite Area Segmentation

**Biological goal:** Measure the total area occupied by neurofilament-positive neurites.

**Method:** Difference of Gaussians (DoG) filtering enhances filamentous structures by subtracting a narrow Gaussian blur (σ=1) from a broad Gaussian blur (σ=5). This suppresses uniform background while preserving filament edges.

**Thresholding:** The Triangle auto-threshold method automatically determines the optimal intensity cutoff for separating neurites from background based on the histogram of the DoG-filtered image.

**Output:** Binary mask where white pixels = neurite area, black = background.

![Neurite Analysis Workflow](../example_output/analysis_workflow.png)

*Figure 1: Analysis workflow. (A) Raw SMI-31 image. (B) Difference of Gaussians filter enhances filaments. (C) Binary mask of neurofilament-positive area. (D) Original image for bead detection. (E) Bead mask (binary) after thresholding. (F) Overlay showing detected beads (red).*

#### Step 3: Axonal Bead Detection

**Biological goal:** Count focal swellings (beads) that indicate axonal damage.

**Method:** Beads are characterised by high SMI-31 intensity and round morphology. A manual intensity threshold (pre-tested on representative images) isolates bright bead cores. Connected component analysis identifies individual beads, which are then filtered by size (25–200 pixels) and circularity (&gt;0.3) to exclude filament fragments and noise.

**Critical:** The threshold must be validated manually on a representative image before batch processing. In ImageJ: `Image > Adjust > Threshold`.

**Output:** Binary mask of detected beads + overlay on original image.

#### Step 4: Normalisation

To control for variations in neurite density between fields, normalise bead count to total neurite area:
- Beads per 1000 µm² = (Bead count / Neurite area in µm²) × 1000

This metric is robust across experiments and correlates with neuroprotective compound efficacy.

---

## 5. Expected Results

| Condition | Expected Bead Density | Interpretation |
|-----------|----------------------|----------------|
| Untreated | Low baseline (~1–2 beads/1000 µm²) | Healthy axons |
| Vehicle (HCl) | Similar to untreated | No toxic effect of vehicle |
| Glutamate (1 mM, 24 h) | High (~5–10 beads/1000 µm²) | Axonal damage |
| Glutamate + neuroprotectant | Reduced vs. glutamate alone | Compound efficacy |

---

## 6. Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| No beads detected | Threshold too high | Lower bead threshold; validate on representative image |
| Too many beads | Threshold too low | Increase bead threshold; check for background fluorescence |
| Neurite mask incomplete | Weak SMI-31 staining | Check antibody concentration; ensure consistent laser power |
| Beads counted on filaments | Circularity filter too permissive | Increase minimum circularity (e.g., 0.5) |
| High variability between replicates | Inconsistent imaging | Standardise laser power, gain, and focus across sessions |

---

## 7. References

- [Reynolds, R., et al. (2011). The neuropathological basis of clinical progression in multiple sclerosis.](https://pubmed.ncbi.nlm.nih.gov/21626034/)
- [Woo, M.S., et al. (2021). Neuronal metabotropic glutamate receptor 8 protects against neurodegeneration in CNS inflammation.](https://pubmed.ncbi.nlm.nih.gov/33661276/)
- [Guerrero Gonzalez, E., et al. (2025). Development of a Human Preclinical Platform. *EJN*, 62(10), e70328.](https://doi.org/10.1111/ejn.70328)

---

## 8. Implementation

This protocol is implemented as:

- **ImageJ macro:** [axonal-damage-analysis](https://github.com/EzraGuerrero/axonal-damage-analysis)
- **Python pipeline:** [axonal-bead-analysis-py](https://github.com/EzraGuerrero/axonal-bead-analysis-py)
