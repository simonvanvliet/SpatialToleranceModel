# Spatial Tolerance Model

Model accompanying the paper:

By:

Model conceptualized and analyzed by Giulia Bottacin, Benjamin Raach, and Simon van Vliet.

Model developed and implemented by Benjamin Raach and Simon van Vliet.

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

1. `1_[hqno/rhl]_preprocess_gradient`: Loads cell-based fluorescent gradient data and bins and plots data.
   - Input: microscopy fluorescent data: `./datafiles/[hqno/rhl]_gradient_microscopy.csv`
   - Output: Binned data: `./2_gradient_inference/data/1_[hqno/rhl]_fluor_gradient_binned.csv`  
2. `2_[hqno/rhl]_concentration_estimate`: Converts fluorescent gradients in estimated concentration gradients and fits diffusion model
   - Input: binned fluorescence values from previous notebook: `./2_gradient_inference/data/1_[hqno/rhl]_fluor_gradient_binned.csv`  
   - Output:
     - Inferred and fitted concentrations profiles: `./2_gradient_inference/data/2_[hqno/rhl]_concentration_profiles.csv`
     - Diffusion model fit parameters: `./2_gradient_inference/data/2_[hqno/rhl]_diffusion_model_fits.csv`
3. `3_plot_concentrations`: Creates dual-axis plots comparing HQNO and RHL concentration gradients with percentile bands.
   - Input: Concentration profiles from previous notebook: `./2_gradient_inference/data/2_[hqno/rhl]_concentration_profiles.csv`
   - Output: Combined concentration gradient figures: `./2_gradient_inference/figures/3_hqno_rhl_dual_axis_fitted_concentration.pdf`

### 3_batch_survival

Notebooks to fit survival model to batch culture antibiotic assay data.

1. `1_fit_batch_survival`: Fits linear logit model to bacterial survival data as function of RHL and HQNO concentrations.
   - Input: Survival assay data: `./datafiles/HQNO_RHL_Survival.csv`
   - Output: Model parameters: `./3_batch_survival/data/survival_model_parameters.json`

### 4_1D_model_predictions

Notebooks containing 1D Reaction - Diffusion model predictions.

1. `1_estimate_flowchannel_conc`: Uses analytical 1D reaction-diffusion model to calculate exogenous concentration needed in PA flow channel to restore PA-WT like gradients in PA double mutant conditions.
   - Input: Diffusion model fit parameters: `./2_gradient_inference/data/2_[hqno/rhl]_diffusion_model_fits.csv`
   - Output: None

