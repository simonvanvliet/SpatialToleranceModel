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

### `./datafiles`

This folder contains the experimental data files

### `./1_dose_response_curves`: Construct dose response curves of RHL and HQNO fluorescent reporters

Fluorescent intensities of reporters were measured in high throughput for many concentrations with FACS, and at low throughput on a few concentrations in microfluidics. These were combined to fit dose response curves, in two steps.

Substeps are contained in jupyter notebooks, with sequential numbers [#], with one each for HQNO `[#]a_[description]_hqno` and RHL `[#]b_[description]_rhl`.

Intermediate data files are stored in `data` subfolder.

Output figures are stored in `figures` subfolder.

1. `1[a/b]_calibrate_facs_microscope_[hqno/rhl].ipynb`: Converts FACS fluorescent intensity to microscope intensities, using linear regression of FACS and microscopy intensities measured at same inducer concentration.
   - Input:
     - facs data files: `./datafiles/[hqno/rhl]_calibration_facs.csv`
     - microscopy data files: `./datafiles/[hqno/rhl]_calibration_microscopy.csv`
   - Output:
     - FACS intensities converted into equivalent microscope intensities: `./1_dose_response_curves/data/1_[hqno/rhl]_facs_transformed.csv`.
2. `2[a/b]_fit_dose_response_[hqno/rhl].ipynb`: Fits dose response curve (HQNO: Hill function, RHL: combined spline + Hill function) to converted and corrected fluorescent intensities vs inducer concentration. 
   - Input: output from previous notebook: `./1_dose_response_curves/data/1_[hqno/rhl]_facs_transformed.csv`
   - Output: parameters of dose response curves: `./1_dose_response_curves/data/2_[hqno/rhl]_calibration_curve.json`.

