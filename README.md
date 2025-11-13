# Spatial Tolerance Model

Model accompanying the paper:

By:

Model conceptualized and analyzed by Giulia Bottacin, Benjamin Raach, and Simon van Vliet.

Model developed and implemented by Benjamin Raach.

## Installation

To set up the required Python environment, use the provided `environment.yml` file with conda:

```bash
conda env create -f environment.yml
```

This will create a new conda environment named `diffmodel_env` with all required dependencies.

To activate the environment:

```bash
conda activate diffmodel_env
```

## Content

### datafiles

This folder contains the experimental data files

### 1_dose_response_curves

Notebooks to construct dose response curves of RHL and HQNO fluorescent reporters.

Substeps are contained in jupyter notebooks, with sequential numbers [#], with one each for HQNO `[#]_hqno_[description]` and RHL `[#]_rhl_[description]`.

Outputs are stored in the subfolders `data` (intermediate data files) and `figures` (manuscript figures).

Fluorescent intensities of reporters were measured in high throughput for many concentrations with FACS, and at low throughput on a few concentrations in microfluidics. These were combined to fit dose response curves, in two steps:

1. `1_[hqno/rhl]_calibrate_facs_microscope.ipynb`: Converts FACS fluorescent intensity to microscope intensities, using linear regression of FACS and microscopy intensities measured at same inducer concentration.
   - Input:
     - facs data files: `./datafiles/[hqno/rhl]_calibration_facs.csv`
     - microscopy data files: `./datafiles/[hqno/rhl]_calibration_microscopy.csv`
   - Output:
     - FACS intensities converted into equivalent microscope intensities: `./1_dose_response_curves/data/1_[hqno/rhl]_facs_transformed.csv`.
2. `2_[hqno/rhl]_fit_dose_response.ipynb`: Fits dose response curve (HQNO: Hill function, RHL: combined spline + Hill function) to converted and corrected fluorescent intensities vs inducer concentration.
   - Input: output from previous notebook: `./1_dose_response_curves/data/1_[hqno/rhl]_facs_transformed.csv`
   - Output: parameters of dose response curves: `./1_dose_response_curves/data/2_[hqno/rhl]_calibration_curve.json`.

### 2_gradient_inference

Notebooks to infer RHL and HQNO concentration as function of distance to PA in microfluidic chambers.

Substeps are contained in jupyter notebooks, with sequential numbers [#], with one each for HQNO `[#]_hqno_[description]` and RHL `[#]_rhl_[description]`.

Outputs are stored in the subfolders `data` (intermediate data files) and `figures` (manuscript figures).
