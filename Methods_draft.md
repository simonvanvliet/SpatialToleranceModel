# Methods

## Fluorescent Reporter Calibration and Dose-Response Curves

To quantify HQNO and RHL concentrations in microfluidic experiments, we constructed calibration curves relating fluorescent reporter intensities to inducer concentrations. Fluorescent intensities were measured using flow cytometry (FACS) for a wide range of concentrations and microscopy for selected concentrations in microfluidic chambers.

**Background correction**: Background fluorescence was determined as the modal intensity of control samples with zero HQNO or RHL induction for microfluidics and as median value for flow cytometry. 

**FACS to microscopy conversion**: FACS intensities were converted to equivalent microscopy intensities using linear regression between the two measurement modalities at matched inducer concentrations.

**Dose-response fitting**: 
Both HQNO and RHL dose-response curves were fitted using a hybrid model combining two approaches, for RHL we fitted to flow cytometry data only, for HQNO reporetr levels were belwo LOD for flowcytometry for HQNO< 40 we pooled flow cytometry (FACS) and microscopy measurements after conversion to common microscopy units:
- **Low-concentration region** (HQNO: ≤160 ng/ml; RHL: ≤100 μg/ml): A monotonic PCHIP (Piecewise Cubic Hermite Interpolating Polynomial) spline interpolator on log₁₀-transformed concentration values (scipy.interpolate.PchipInterpolator) to accurately capture the highly nonlinear dose-response relationship at low concentrations
- **High-concentration region** (above cutoff): A three-parameter Hill function of the form $y = \frac{y_{max} \cdot x^n}{K^n + x^n}$ fitted to the full concentration range, where $y$ is fluorescent intensity, $x$ is concentration, $y_{max}$ is maximum intensity, $K$ is the half-maximal concentration, and $n$ is the Hill coefficient
- **Hybrid evaluation**: For prediction, the PCHIP spline is used for concentrations ≤ cutoff, and the Hill function is used for concentrations > cutoff, ensuring accurate interpolation across the entire concentration range while maintaining proper asymptotic behavior at high concentrations

## Concentration Gradient Inference

Concentration gradients of HQNO and RHL emanating from PA producers were inferred from fluorescent reporter measurements in microfluidic chambers.

**Data preprocessing**: Cell-level fluorescent intensity measurements were spatially binned in fixed 1.5 μm bins in both x and y directions as a function of distance from the PA-SA interface and background-corrected using the calibrations described above.

**Concentration estimation**: Fluorescent intensities were converted to molecular concentrations using the inverse of the calibrated hybrid dose-response curves. For intensities corresponding to concentrations ≤ cutoff (HQNO: 160 ng/ml; RHL: 100 μg/ml), the inverse PCHIP spline was used; for higher concentrations, the inverse Hill function was applied. This ensures accurate concentration estimation across the full range of observed fluorescent intensities.

**Diffusion model fitting**: A one-dimensional steady-state reaction-diffusion model was fitted to the inferred concentration profiles to estimate effective diffusion coefficients (D_eff), production rates (S), and uptake rates (k). The model assumes:
- Steady-state conditions: $\frac{\partial C}{\partial t} = 0$
- Diffusion follows Fick's second law: $D_{eff} \frac{\partial^2 C}{\partial x^2}$
- Production occurs uniformly in the producer region at rate S
- Uptake/degradation in the consumer region follows first-order kinetics: $-k \cdot C$
- Reflective boundary at the interface and absorbing boundary at the far end

## Survival Model

We developed a quantitative model relating SA survival to HQNO and RHL concentrations using batch culture survival assays.

**Model structure**: A logistic regression model was fitted to survival data, with the form:

$$P(survival) = \sigma(m_{RHL} \cdot [RHL] + m_{HQNO} \cdot [HQNO] + b)$$

where $\sigma(z) = \frac{1}{1 + e^{-z}}$ is the logistic function, $m_{RHL}$ and $m_{HQNO}$ are coefficients quantifying the effect of each molecule on survival, and $b$ is the intercept term.

**Data preprocessing and model fitting**:
- Survival was calculated as the fraction of colony-forming units (CFU) at 2h relative to initial CFU at time 0
- Growth during early antibiotic treatment could lead to survival >1; all survival values were normalized by dividing by the maximum observed survival to ensure survival ≤ 1
- Data points below the limit of detection (LOD) were excluded from fitting, where LOD was calculated per replicate as LOD = 1/CFU_t0
- To optimize model performance for microfluidic experiment conditions, models were fitted over three HQNO concentration ranges: 0-40 ng/ml, 0-60 ng/ml, and 0-80 ng/ml
- The 60 ng/ml limit was selected as the primary model as it best captured the concentration range observed in microfluidic chambers
- Model parameters were estimated using least-squares regression on logit-transformed survival values, with goodness of fit evaluated using R²

**Assumption**: The model assumes that the effects of RHL and HQNO on survival are additive on the logit scale, representing independent protective (RHL) and toxic (HQNO) effects.

## One-Dimensional Reaction-Diffusion Model

To predict survival in linear microfluidic geometries, we implemented a one-dimensional reaction-diffusion model.

**Governing equations**: The model solves the steady-state reaction-diffusion equations for both HQNO and RHL:

$$D_i \frac{d^2 C_i}{dx^2} + S_i(x) - k_i(x) \cdot C_i = 0$$

where subscript $i$ denotes either HQNO or RHL, $S_i(x)$ is the spatially-dependent production term (non-zero in producer regions), and $k_i(x)$ is the spatially-dependent uptake rate (non-zero in consumer regions).

**Boundary conditions**: 
- Absorbing boundaries at channel ends ($C = 0$)
- Reflective boundary at the producer-consumer interface

**Parameter estimation**: Production rates were estimated by fitting the model to experimental concentration profiles while using independently measured diffusion coefficients and uptake rates.

**Survival prediction**: Predicted concentration profiles were combined with the logistic survival model to estimate spatially-resolved survival probabilities.

## Two-Dimensional Reaction-Diffusion Model

For complex spatial arrangements, we extended the model to two dimensions to simulate:
1. Colony growth with open boundaries
2. Mixed chambers with various spatial patterns of producers and consumers

**Numerical implementation**: The 2D model was solved numerically using an explicit finite-difference scheme:
- Spatial discretization: dx = dy = 1.0 μm on a grid sized according to channel geometry (typically 50 μm producer + 3 μm corridor + 50 μm consumer in x-direction, 50 μm in y-direction)
- Laplacian operator computed using a 5-point stencil
- Time-stepping with adaptive time step satisfying CFL stability criterion: $\Delta t \leq \frac{\Delta x^2 \Delta y^2}{2D(∆x^2 + \Delta y^2)}$ with safety factor of 0.9
- Maximum simulation time: t_max = 10,000 seconds
- Simulation run until convergence (maximum concentration change < 10⁻⁶ per time step)
- Implementation optimized using Numba JIT compilation

**Boundary conditions**:
- Channel simulations: Absorbing boundaries at longitudinal ends, reflective boundaries on sides, internal walls (width 3 μm) represented as NaN with reflecting boundary conditions to model physical barriers in experimental setup
- Colony simulations: Open boundaries implemented as specified per geometry

**Spatial patterns**: For mixed chamber simulations, we tested:
- Checkerboard patterns with varying patch sizes
- Horizontal stripe patterns with varying stripe widths
- Random patchy patterns (see Pattern Analysis section)

## Pattern Analysis and Segregation Quantification

To quantify spatial segregation between producers and consumers, we implemented a multiscale segregation scoring approach adapted from Dogsa & Mandic-Mulec (2023).

**Segregation score calculation**: For each focal cell of type 1, we calculated:

$$S_i(w) = \left|\frac{\frac{N_{focal,L}}{N_{focal,G}} - \frac{N_{other,L}}{N_{other,G}}}{\frac{N_{focal,L}}{N_{focal,G}} + \frac{N_{other,L}}{N_{other,G}}}\right|$$

where $N_{focal,L}$ and $N_{other,L}$ are counts of focal and other cell types within distance $w$ (window size) from the focal cell, and $N_{focal,G}$ and $N_{other,G}$ are the global counts of each type. The absolute value ensures the score measures segregation magnitude regardless of which type forms the patch.

**Multiscale Spatial Segregation Level (MSSL)**: To capture segregation across spatial scales, we computed segregation scores across multiple window sizes (w = 1 to 25 pixels for synthetic grids with 1-pixel increments; w = 2 to 25 μm for experimental data with 1-μm increments) and calculated MSSL as the area under the segregation-window size curve, normalized by the window size range:

$$MSSL = \frac{\int_{w_{min}}^{w_{max}} S(w) \, dw}{w_{max} - w_{min}}$$

where the integral was computed using the trapezoidal rule (scipy.integrate.trapezoid).


**Experimental pattern analysis**: For experimental mixed chamber data, we:
1. Converted cell positions from pixels to micrometers (0.065 μm/pixel)
2. Calculated segregation scores for each replicate chamber using point-based distance method (Euclidean distance) rather than grid-based approach to account for discrete cell positions
3. Determined survival fraction per chamber as number of PA cells showing regrowth divided by total PA cells, with per-chamber limit of detection defined as LOD = 1/n_PA
4. Assessed correlation between MSSL and survival fraction using Spearman rank correlation (ρ), which does not assume linearity and is robust to outliers

**Model-experiment integration**: We simulated 2D reaction-diffusion dynamics for the generated synthetic patterns to predict survival as a function of segregation level, allowing comparison with experimental observations.

## Statistical Analysis

All analyses were performed in Python using standard scientific libraries (NumPy, SciPy, pandas, statsmodels). Model fitting used non-linear least squares (scipy.optimize) and logistic regression (statsmodels). Statistical comparisons employed Spearman rank correlation for non-parametric associations. Uncertainty estimates represent standard deviations across biological replicates or bootstrapped confidence intervals as indicated.

## Code Availability

All analysis code is available in Jupyter notebooks organized by analysis step, with detailed inline documentation. The computational pipeline is fully reproducible given the provided environment specification (environment.yml) and raw data files.
