# Methods


## Fluorescent Reporter Calibration

To quantify HQNO and rhamnolipids (RHL)concentrations in microfluidic experiments, we used fluorescent reporters and constructed calibration curves relating fluorescent reporter intensities to compound concentrations. 
Callibration curves were constructed by exposing 

**Reporters**. For HQNO we used a GFP transcriptional reporter for pflB expression, a ... [To be completed by Giulia]. For RHL we followed a previously published protocol that uses uptake of propidium iodine (PI) as proxy for membrane damage ...  . In microfluidics experiments, GFP expression was measured using [microscopy settings], and PI fluorescence using [microscopy settings]. Settigs were held constat betwen expreimnets to allow for qunatitative compasrisons. In flow cytometry, GFP expression was measured using [facs settings], and PI fluorescence using [facs settings].

**Flow cytometry dose response curves**
SA exponential phase cultures were exposed to purified HQNO [brand name] and RHL [specifications and brand name] for X hours. Subsequently, we measured expression levels uing [specification of facs]. GFP expression was measured using [facs settings], and PI fluorescence using [facs settings]. All fluorescent kntenisties were backgriund corrected usig the median cell insitity for the 0 concentrtaion controls, and the median value over all cells was used. Each measuremnet was done in triplicate. 

**Microfluidic callibration measuremnets**
Sa was grown overnight in co-culture with PA dHQNO for HQNO callibration and with PA dRHL for RHL callibration. Subsequently defined concentrations of HQNo or RHL was added to both flow cahnnels. Fluorescent inentsities were measured afteer X hours using [microscopy settings]. Fluorescent ineensisties were backgrund corrected usimg the modal intenisty in the 0 concentration control expreiments. Fr each compoiund and cocn etration we measured X chambers. For each chamber we used median fluorescnt inetsnity from each cell.

The Rgeressions analysys showed that micrlfuidic and mkicrospcpyt uetnsitie ss have linear rleations, with an R2 of 0.86 for HQNO and 0.98 for RHL.  This analysis also revealed that for HQNO cancnetrations below 40 ng/ml the fluorescnet intenisties was below the limit od detection of flow cytometry, but still with n teh rnage for the microsce camera. 


**Cross-platform calibration.** We converted flow cytometry intensities to equivalent microscopy intensities using linear regression between the two measurement modalities at matched inducer concentrations. For HQNO, this callibration was done using concentrations 40, 80,160, 320, and 2500 ng/ml. For RHL, using 0, 25, 50, 75, 100 ug/ml, the measuremnet of 12.5 ug/ml was excluded as it was a clear outlier. Linear regressions were done using Ortogonal Distance Regression to account for measuremnet uncertainty in both flow cytometry and microscopy data, suing the scipy odr function. 

 For HQNO, FACS GFP measurements at low concentrations (0, 10, and 20 ng/ml) were at or near the detection floor and were excluded; we relied on microfluidics measurements for these concentrations. The 4,000 ng/ml point was also excluded due to deviation from Hill-type response, consistent with non-linear effects at high HQNO concentrations. For RHL, the 12.5 μg/ml concentration was identified as an outlier in FACS data and excluded. [^2]

**Dose-response fitting.** Both HQNO and RHL dose-response curves were fitted using a hybrid model combining two approaches. For RHL, we fitted to flow cytometry data only; for HQNO, reporter levels were below the limit of detection for flow cytometry at concentrations below 40 ng/ml, so we pooled flow cytometry and microscopy measurements after conversion to common microscopy units. [^1]

- **Low-concentration region** (HQNO: ≤160 ng/ml; RHL: ≤100 μg/ml): We used a monotonic PCHIP (Piecewise Cubic Hermite Interpolating Polynomial) spline interpolator on log₁₀-transformed concentration values (scipy.interpolate.PchipInterpolator) to accurately capture the highly nonlinear dose-response relationship at low concentrations. [^1]

- **High-concentration region** (above cutoff): We fitted a three-parameter Hill function of the form $y = \frac{y_{max} \cdot x^n}{K^n + x^n}$ to the full concentration range, where $y$ is fluorescent intensity, $x$ is concentration, $y_{max}$ is maximum intensity, $K$ is the half-maximal concentration, and $n$ is the Hill coefficient. For each concentration, we summarized microfluidics measurements by the mean and transformed FACS measurements by the median; when FACS points were excluded, only the microfluidics summary contributed. Zero-concentration controls were excluded from the fit because the three-parameter Hill model assumes a zero lower asymptote. [^1][^2]

- **Hybrid evaluation**: For prediction, the PCHIP spline is used for concentrations ≤ cutoff, and the Hill function is used for concentrations > cutoff, ensuring accurate interpolation across the entire concentration range while maintaining proper asymptotic behavior at high concentrations. [^1]

## Concentration Gradient Inference

We inferred concentration gradients of HQNO and RHL emanating from *P. aeruginosa* producers from fluorescent reporter measurements in microfluidic chambers. [^1]

**Data preprocessing.** Cell-level fluorescent intensity measurements were spatially binned in fixed 1.5 μm bins in both x and y directions as a function of distance from the PA-SA interface. For HQNO, we analyzed only the sides of the chamber because cellular movement in the middle of the chamber distorted the GFP signal; GFP is expressed over time, and when cell movement is faster than the promoter-reporter can adapt to local HQNO concentration, the fluorescent signal reflects a mixture of past positions rather than the immediate environment. Cells at the border move less due to friction and therefore better reflect the immediate environment. For RHL, we analyzed the whole chamber because there was no distortion effect, as the signaling component was added only right before measurement. [^2]

**Background correction for HQNO.** In microfluidic assays, GFP intensities plateaued beyond approximately two-thirds of the chamber length. We interpreted this plateau as the region not reached by HQNO and used it to define the background level for correction. Since GFP intensities in the distal bins varied across replicates, we applied chamber-specific background correction. [^2]

**Concentration estimation.** We converted fluorescent intensities to molecular concentrations using the inverse of the calibrated hybrid dose-response curves. For intensities corresponding to concentrations ≤ cutoff (HQNO: 160 ng/ml; RHL: 100 μg/ml), the inverse PCHIP spline was used; for higher concentrations, the inverse Hill function was applied. This ensures accurate concentration estimation across the full range of observed fluorescent intensities. [^1]

**Diffusion model fitting.** We fitted a one-dimensional steady-state reaction-diffusion model to the inferred concentration profiles to estimate effective diffusion coefficients (D_eff), production rates (S), and uptake rates (k). The model assumes steady-state conditions ($\frac{\partial C}{\partial t} = 0$), diffusion following Fick's second law ($D_{eff} \frac{\partial^2 C}{\partial x^2}$), uniform production in the producer region at rate S, uptake/degradation in the consumer region following first-order kinetics ($-k \cdot C$), a reflective boundary at the interface, and an absorbing boundary at the far end. [^1]

Concentration profiles were fitted to a diffusion-uptake steady-state model expressed in a numerically stable form: $C(x) = c_{max} \cdot \frac{\sinh(\sqrt{A} \cdot (L - x))}{\sinh(\sqrt{A} \cdot L)}$, where $c_{max}$ scales the source concentration, $A$ is an effective uptake/diffusion parameter, and $L$ is a characteristic length beyond the distal end of the chamber. Nonlinear least-squares fitting (SciPy curve_fit) was performed with constraints $c_{max} \geq 0$, $A > 0$, and $L \geq x_{max} + \Delta$ (Δ = 1 bin) to ensure the boundary lay outside the measured domain. A small number of leading bins (typically 2) were excluded prior to fitting. [^2]

**Estimation of effective diffusion coefficients.** To disentangle molecular uptake from diffusion, we estimated diffusion coefficients from both theoretical and experimental sources. We calculated theoretical diffusion parameters using the Stokes-Einstein equation, yielding D_HQNO ≈ 40 μm²/s (assuming a molecular radius of 0.5 nm) and D_RHL ≈ 10-20 μm²/s (radius 1-3 nm). Literature reports a diffusion coefficient of D_RHL ≈ 27 μm²/s in aqueous solution, consistent with our theoretical estimates. [^2]

To account for hindered diffusion in cell-populated microfluidic chambers, we applied a porous-media correction: $D_{eff} = \frac{(1 - \rho)}{(1 + \rho)} \cdot D$, where ρ denotes the cell volume fraction. We estimated cell density from segmented phase-contrast images: the fraction of cell pixels relative to total chamber pixels defined a 2D area fraction (ρ_2D). This was converted to a 3D volume fraction (ρ_3D) using measured cell radius (r_cell = 0.325 μm) and chamber height (h_chamber = 0.8 μm), according to $\rho_{3D} = \frac{4}{3} \cdot \frac{r_{cell}}{h_{chamber}} \cdot \rho_{2D}$. Averaging across ten chamber positions gave ρ_2D = 0.427, corresponding to ρ_3D = 0.463. These values were used to calculate effective diffusion coefficients for HQNO and RHL under experimental conditions. [^2]

## Survival Model

We developed a quantitative model relating *S. aureus* survival to HQNO and RHL concentrations using batch culture survival assays. [^1]

**Experimental setup.** HQNO and RHL were combined at various concentrations in 1 ml of MHB medium within 24-well plates, followed by the addition of *S. aureus* culture. After a 30-minute incubation period, tobramycin was added and the treatment continued for 3 hours. An aliquot was then collected for CFU counting. [^2]

**Model structure.** We fitted a logistic regression model to survival data, with the form:

$$P(survival) = \sigma(m_{RHL} \cdot [RHL] + m_{HQNO} \cdot [HQNO] + b)$$

where $\sigma(z) = \frac{1}{1 + e^{-z}}$ is the logistic function, $m_{RHL}$ and $m_{HQNO}$ are coefficients quantifying the effect of each molecule on survival, and $b$ is the intercept term. [^1]

**Data preprocessing and model fitting.** Survival was calculated as the fraction of colony-forming units (CFU) at 2 h relative to initial CFU at time 0. Growth during early antibiotic treatment could lead to survival >1; all survival values were normalized by dividing by the maximum observed survival to ensure survival ≤ 1. Data points below the limit of detection (LOD) were excluded from fitting, where LOD was calculated per replicate as LOD = 1/CFU_t0. To optimize model performance for microfluidic experiment conditions, models were fitted over three HQNO concentration ranges: 0-40 ng/ml, 0-60 ng/ml, and 0-80 ng/ml. The 60 ng/ml limit was selected as the primary model as it best captured the concentration range observed in microfluidic chambers. We estimated model parameters using least-squares regression on logit-transformed survival values, minimizing squared deviations in logit space. This approach ensures bounded predictions (0-1) and reduces bias toward high-survival values. Goodness of fit was evaluated using R². [^1][^2]

**Model assumption.** The model assumes that the effects of RHL and HQNO on survival are additive on the logit scale, representing independent protective (RHL) and toxic (HQNO) effects. [^1]

## One-Dimensional Reaction-Diffusion Model

To predict survival in linear microfluidic geometries, we implemented a one-dimensional reaction-diffusion model. [^1]

**Governing equations.** The model solves the steady-state reaction-diffusion equations for both HQNO and RHL:

$$D_i \frac{d^2 C_i}{dx^2} + S_i(x) - k_i(x) \cdot C_i = 0$$

where subscript $i$ denotes either HQNO or RHL, $S_i(x)$ is the spatially-dependent production term (non-zero in producer regions), and $k_i(x)$ is the spatially-dependent uptake rate (non-zero in consumer regions). [^1]

**Boundary conditions.** We applied absorbing boundaries at channel ends ($C = 0$) and a reflective boundary at the producer-consumer interface. [^1]

**Parameter estimation.** We estimated production rates by fitting the model to experimental concentration profiles while using independently measured diffusion coefficients and uptake rates. [^1]

**Survival prediction.** We combined predicted concentration profiles with the logistic survival model to estimate spatially-resolved survival probabilities. [^1]

## Two-Dimensional Reaction-Diffusion Model

For complex spatial arrangements, we extended the model to two dimensions to simulate colony growth with open boundaries and mixed chambers with various spatial patterns of producers and consumers. [^1]

**Numerical implementation.** We solved the 2D model numerically using an explicit finite-difference scheme with spatial discretization dx = dy = 1.0 μm on a grid sized according to channel geometry (typically 50 μm producer + 3 μm corridor + 50 μm consumer in x-direction, 50 μm in y-direction). We computed the Laplacian operator using a 5-point stencil and performed time-stepping with an adaptive time step satisfying the CFL stability criterion: $\Delta t \leq \frac{\Delta x^2 \Delta y^2}{2D(\Delta x^2 + \Delta y^2)}$ with a safety factor of 0.9. We set the maximum simulation time to t_max = 10,000 seconds and ran simulations until convergence (maximum concentration change < 10⁻⁶ per time step). Implementation was optimized using Numba JIT compilation. [^1]

**Boundary conditions.** For channel simulations, we applied absorbing boundaries at longitudinal ends, reflective boundaries on sides, and represented internal walls (width 3 μm) as NaN with reflecting boundary conditions to model physical barriers in the experimental setup. For colony simulations, we implemented open boundaries as specified per geometry. [^1]

**Spatial patterns.** For mixed chamber simulations, we tested checkerboard patterns with varying patch sizes, horizontal stripe patterns with varying stripe widths, and random patchy patterns (see Pattern Analysis section). [^1]

## Pattern Analysis and Segregation Quantification

To quantify spatial segregation between producers and consumers, we implemented a multiscale segregation scoring approach adapted from Dogsa & Mandic-Mulec (2023). [^1]

**Segregation score calculation.** For each focal cell of type 1, we calculated:

$$S_i(w) = \frac{\left|\frac{N_{focal,L}}{N_{focal,G}} - \frac{N_{other,L}}{N_{other,G}}\right|}{\frac{N_{focal,L}}{N_{focal,G}} + \frac{N_{other,L}}{N_{other,G}}}$$

where $N_{focal,L}$ and $N_{other,L}$ are counts of focal and other cell types within distance $w$ (window size) from the focal cell, and $N_{focal,G}$ and $N_{other,G}$ are the global counts of each type. The absolute value ensures the score measures segregation magnitude regardless of which type forms the patch. [^1]

**Multiscale Spatial Segregation Level (MSSL).** To capture segregation across spatial scales, we computed segregation scores across multiple window sizes (w = 1 to 25 pixels for synthetic grids with 1-pixel increments; w = 2 to 25 μm for experimental data with 1-μm increments) and calculated MSSL as the area under the segregation-window size curve, normalized by the window size range:

$$MSSL = \frac{\int_{w_{min}}^{w_{max}} S(w) \, dw}{w_{max} - w_{min}}$$

where the integral was computed using the trapezoidal rule (scipy.integrate.trapezoid). [^1]

**Experimental pattern analysis.** For experimental mixed chamber data, we converted cell positions from pixels to micrometers (0.065 μm/pixel), calculated segregation scores for each replicate chamber using a point-based distance method (Euclidean distance) rather than a grid-based approach to account for discrete cell positions, determined survival fraction per chamber as the number of PA cells showing regrowth divided by total PA cells (with per-chamber limit of detection defined as LOD = 1/n_PA), and assessed correlation between MSSL and survival fraction using Spearman rank correlation (ρ), which does not assume linearity and is robust to outliers. [^1]

**Model-experiment integration.** We simulated 2D reaction-diffusion dynamics for the generated synthetic patterns to predict survival as a function of segregation level, allowing comparison with experimental observations. [^1]

## Statistical Analysis

All analyses were performed in Python using standard scientific libraries (NumPy, SciPy, pandas, statsmodels). Model fitting used non-linear least squares (scipy.optimize) and logistic regression (statsmodels). Statistical comparisons employed Spearman rank correlation for non-parametric associations. Uncertainty estimates represent standard deviations across biological replicates or bootstrapped confidence intervals as indicated. [^1]

## Code Availability

All analysis code is available in Jupyter notebooks organized by analysis step, with detailed inline documentation. The computational pipeline is fully reproducible given the provided environment specification (environment.yml) and raw data files. [^1]

---

# To Review

## Colony Printing Experiments

Cells were printed in checkerboard arrays with varying center-to-center distances (500 μm, 250 μm, 150 μm, and < 50 μm) and grown for 6 hours on MHB agar pads containing 3% agarose. Following the growth period, the cells were treated with tobramycin for 15 hours, where the antibiotic was solubilized in 3% agarose and solidified around the agar pads. After the treatment, the agar pads were carefully cut out and the cells were detached by vortexing in 1 ml PBS. Colony forming units (CFU) were subsequently counted for both *S. aureus* and *P. aeruginosa*. The results demonstrated that *S. aureus* exhibited the highest survival rate in checkerboard configurations with 100 μm center-to-center distances. [^2]

[VERIFY: This colony printing methodology is not mentioned in Methods_draft.md. Confirm whether this experimental approach is still part of the current study or has been replaced by other methods.]

## Analytical Solution for Two-Chamber Geometry

An analytical solution was developed for the two-chamber-with-connection geometry. The 2D chamber-gap-chamber geometry was reduced to a 1D coordinate x in [0, 2L+d] with piecewise-constant cross-sectional width: W in the producer [0,L] and consumer [L+d, 2L+d] regions, and W_gap in the diffusive gap [L, L+d]. Species concentrations R(x) satisfy steady-state diffusion with region-specific source/sink terms:

- **Producer [0,L]**: uniform production S, no uptake → D·R''(x) = -S
- **Gap [L,L+d]**: passive diffusion, no sources/sinks → D·R''(x) = 0
- **Consumer [L+d,2L+d]**: first-order uptake/leakage with rate C → D·R''(x) - C·R(x) = 0 (define k = √(C/D))

Boundary conditions are Dirichlet at the outer ends: R(0)=0 and R(2L+d)=0. At each interface (x=L and x=L+d), continuity of concentration and continuity of width-weighted flux were enforced. Solving the ODEs with these six conditions gives a piecewise analytic profile. The closed-form expression relating production rate S to the solute concentration at the consumer-side interface of the gap (R* = R(L+d)) is:

$$S = \frac{2 \cdot D}{L^2} \cdot R^* \cdot \left[ 1 + \frac{k}{\tanh(k \cdot L)} \cdot \left( L + \frac{W}{W_{gap}} \cdot d \right) \right]$$

with k = √(C/D). [^2]

[VERIFY: This analytical solution is not mentioned in Methods_draft.md. Confirm whether this approach was used for parameter estimation or has been superseded by the numerical methods described in the current draft.]

## Alternative Survival Model Fits

Alternative fits were explored for the survival model, including quadratic models in raw survival space and maximum-likelihood fits under Poisson error assumptions. Quadratic fits either overemphasized survival extremes (when including errors) or were highly focused on large survival rates (when fitting to averages without errors). Maximum-likelihood fits under Poisson error assumptions relied on invalid assumptions about plating variability because different dilutions were used for different plating conditions. [^2]

[NOTE: This discussion of alternative approaches is already briefly mentioned in Methods_draft.md but with less detail. The current draft appropriately focuses on the chosen method.]

## Microfluidic Chamber Dimensions

According to code documentation, the geometry was given by:

- L_val = 50.0 μm (Length of producer & consumer regions, each)
- d_val = 3.0 μm (Length of diffusive gap)
- W_val = 40.0 μm (Width of producer/consumer chambers)
- W_gap_val = 0.5/2*W_val μm (Width of the diffusive gap)

However, measurements of chambers in Fiji showed 50 μm chamber width and 50 μm chamber length. [^2]

[CONFLICT: The outdated document mentions W_val = 40.0 μm but also states that Fiji measurements showed 50 μm chamber width. Methods_draft.md states "typically 50 μm producer + 3 μm corridor + 50 μm consumer in x-direction, 50 μm in y-direction" which appears to resolve this discrepancy. Verify final chamber dimensions used in analysis.]

## Cell Size Measurements

*S. aureus* has a size of approximately 0.65 μm. Method: 20 cells were measured using Fiji and the width ranged between 0.5 μm (new daughter cells) and 0.75 μm (mother cells). The mean cell width of 20 cells was 0.65 μm. [^2]

[NOTE: This measurement detail supports the cell radius value (0.325 μm) used in the effective diffusion calculation in the current draft.]

---

# Editor's Notes

## Placeholders

- [PLACEHOLDER: Specific citation for Dogsa & Mandic-Mulec (2023) reference in Pattern Analysis section]
- [PLACEHOLDER: Specific citation for Lebenhaft et al. (1984) reference for porous-media correction]
- [PLACEHOLDER: Specific citation for Arkhipov et al. (2023) reference for RHL diffusion coefficient]
- [PLACEHOLDER: Experimental details about microfluidic chip design and fabrication]
- [PLACEHOLDER: Details about bacterial strains, growth conditions, and reporter constructs]
- [PLACEHOLDER: Microscopy and flow cytometry instrument specifications and settings]
- [PLACEHOLDER: Image analysis and cell segmentation methods]

## Verification Needs

- [VERIFY: Are colony printing experiments still part of the current study? Not mentioned in Methods_draft.md]
- [VERIFY: Was the analytical solution for two-chamber geometry used for parameter estimation, or has it been replaced by numerical methods?]
- [VERIFY: Final microfluidic chamber dimensions - confirm 50 μm width is correct (discrepancy noted in outdated document)]
- [VERIFY: Confirm that the 60 ng/ml HQNO concentration limit for the survival model is the final choice]
- [VERIFY: Are specific model parameter values (c_max, A values) needed in the Methods section, or are these Results content?]

## Conflicts

- [CONFLICT: Chamber width discrepancy - outdated document mentions both 40 μm (in code) and 50 μm (from Fiji measurements). Current draft uses 50 μm, which appears to be the correct value.]

## Style Notes

- The current draft successfully matches the formal, objective academic tone of the main text
- Technical terminology is used consistently with the main manuscript
- Mathematical notation is properly formatted with LaTeX
- The structure follows standard Methods section organization with clear subheadings
- Active voice is used appropriately ("We fitted...", "We calculated...")

[^1]: [Methods_draft](Methods_draft.md) (55%)
[^2]: [outdated_method_details](outdated_method_details.md) (45%)
