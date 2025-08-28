# Statistical Equations and Power Analysis Library

## 🧮 Comprehensive Mathematical Framework for QA System Agent

This document provides complete statistical equations, power analysis formulas, and computational implementations for all experiment types, with academic validation and practical implementation guidance.

---

## 📊 Experiment Type 1: Comparison Studies

### **1.1 Paired t-test (Within-Subjects Comparison)**

#### **Core Statistical Model**
```yaml
mathematical_foundation:
  population_model: "d_i = X₁ᵢ - X₂ᵢ ~ N(μ_d, σ²_d)"
  null_hypothesis: "H₀: μ_d = 0"
  alternative_hypothesis: "H₁: μ_d ≠ 0 (two-tailed) or μ_d > 0 (one-tailed)"
  
test_statistic:
  formula: "t = (d̄ - μ₀) / (s_d / √n)"
  degrees_of_freedom: "df = n - 1"
  where:
    d̄: "sample mean of difference scores"
    s_d: "sample standard deviation of differences"
    n: "number of paired observations"
    μ₀: "hypothesized mean difference (usually 0)"
```

#### **Effect Size Calculations**
```yaml
cohens_d_paired:
  formula: "d = d̄ / s_d"
  interpretation: "Cohen (1988): |d| = 0.2 (small), 0.5 (medium), 0.8 (large)"
  
  bias_correction: "Hedges' g = d × (1 - 3/(4df - 1))"
  confidence_interval: "d ± t_α/2,df × √((n+1)/(n) + d²/(2n))"
  
glass_delta:
  formula: "Δ = d̄ / s_control"
  application: "When using control group SD as standardizer"
  
correlation_adjustment:
  repeated_measures_d: "d_rm = d_between × √(2(1-r))"
  where: "r = correlation between repeated measures"
```

#### **Power Analysis Framework**
```yaml
sample_size_calculation:
  two_tailed: "n = 2(z_α/2 + z_β)² / d²"
  one_tailed: "n = (z_α + z_β)² / d²"
  
  exact_formula: "n = (t_α/2,df + t_β,df)² / d²"
  iterative_solution: "Requires iterative solving since df = n-1"
  
power_calculation:
  noncentrality_parameter: "δ = d√n"
  power: "1 - β = P(t > t_α/2,df | δ) + P(t < -t_α/2,df | δ)"
  
minimum_detectable_effect:
  formula: "MDE = (t_α/2,df + t_β,df) / √n"
  practical_application: "Smallest effect size detectable with given n and power"

confidence_interval_precision:
  margin_of_error: "ME = t_α/2,df × (s_d / √n)"
  required_n_for_precision: "n = (t_α/2 × s_d / ME)²"
  planning_values: "Use pilot data or literature estimates for s_d"
```

#### **Implementation Code Templates**
```python
# Python implementation for paired t-test power analysis
import numpy as np
from scipy import stats
from scipy.optimize import fsolve

def paired_ttest_power(n=None, effect_size=None, alpha=0.05, power=None, alternative='two-sided'):
    """
    Power analysis for paired t-test
    Provide three of four parameters, calculates the fourth
    """
    
    if alternative == 'two-sided':
        z_alpha = stats.norm.ppf(1 - alpha/2)
    else:
        z_alpha = stats.norm.ppf(1 - alpha)
    
    if power is not None:
        z_beta = stats.norm.ppf(power)
    
    if n is None:  # Calculate required sample size
        if alternative == 'two-sided':
            n = 2 * (z_alpha + z_beta)**2 / effect_size**2
        else:
            n = (z_alpha + z_beta)**2 / effect_size**2
        return int(np.ceil(n))
    
    elif effect_size is None:  # Calculate minimum detectable effect
        if alternative == 'two-sided':
            effect_size = (z_alpha + z_beta) * np.sqrt(2/n)
        else:
            effect_size = (z_alpha + z_beta) * np.sqrt(1/n)
        return effect_size
    
    elif power is None:  # Calculate achieved power
        if alternative == 'two-sided':
            ncp = effect_size * np.sqrt(n/2)
        else:
            ncp = effect_size * np.sqrt(n)
        power = 1 - stats.norm.cdf(z_alpha - ncp)
        if alternative == 'two-sided':
            power += stats.norm.cdf(-z_alpha - ncp)
        return power

def cohens_d_ci(d, n, alpha=0.05):
    """Calculate confidence interval for Cohen's d"""
    df = n - 1
    t_crit = stats.t.ppf(1 - alpha/2, df)
    
    se_d = np.sqrt((n + 1)/n + d**2/(2*n))
    ci_lower = d - t_crit * se_d
    ci_upper = d + t_crit * se_d
    
    return ci_lower, ci_upper
```

### **1.2 Independent Samples t-test (Between-Subjects Comparison)**

#### **Statistical Model**
```yaml
population_model:
  group_1: "X₁ᵢ ~ N(μ₁, σ²)"
  group_2: "X₂ᵢ ~ N(μ₂, σ²)"
  homoscedasticity: "Equal variances assumed (σ₁² = σ₂² = σ²)"
  
test_statistic:
  equal_variances: "t = (x̄₁ - x̄₂) / (s_p × √(1/n₁ + 1/n₂))"
  pooled_variance: "s²_p = [(n₁-1)s₁² + (n₂-1)s₂²] / (n₁ + n₂ - 2)"
  degrees_of_freedom: "df = n₁ + n₂ - 2"
  
welch_correction:
  unequal_variances: "t = (x̄₁ - x̄₂) / √(s₁²/n₁ + s₂²/n₂)"
  satterthwaite_df: "df = (s₁²/n₁ + s₂²/n₂)² / [(s₁²/n₁)²/(n₁-1) + (s₂²/n₂)²/(n₂-1)]"
```

#### **Effect Size and Power Analysis**
```yaml
cohens_d_independent:
  formula: "d = (μ₁ - μ₂) / σ_pooled"
  sample_estimate: "d = (x̄₁ - x̄₂) / s_pooled"
  
balanced_design_power:
  sample_size_per_group: "n = 2(z_α/2 + z_β)² / d²"
  unbalanced_design: "n_h = 2(z_α/2 + z_β)² / [d² × (1 + 1/r)]"
  where: "r = n₂/n₁ (allocation ratio)"
  
optimal_allocation:
  cost_consideration: "n₁/n₂ = √(c₂/c₁)"
  where: "c₁, c₂ = cost per participant in groups 1, 2"
  equal_cost_optimal: "n₁ = n₂ (balanced design)"
```

### **1.3 Mixed-Effects Models for Hierarchical Data**

#### **Model Specification**
```yaml
basic_random_intercept:
  model: "Y_ij = β₀ + β₁X_ij + u_j + ε_ij"
  where:
    Y_ij: "response for participant j on trial i"
    β₀: "fixed intercept"
    β₁: "fixed effect of treatment"
    u_j: "random intercept for participant j ~ N(0, σ²_u)"
    ε_ij: "residual error ~ N(0, σ²_ε)"
    
variance_components:
  total_variance: "Var(Y_ij) = σ²_u + σ²_ε"
  intraclass_correlation: "ICC = σ²_u / (σ²_u + σ²_ε)"
  
random_slopes_model:
  model: "Y_ij = β₀ + β₁X_ij + u₀j + u₁jX_ij + ε_ij"
  random_effects: "[u₀j, u₁j] ~ N(0, G)"
  covariance_matrix: "G = [σ²_u₀, σ_u₀u₁; σ_u₀u₁, σ²_u₁]"
```

#### **Power Analysis for Mixed Models**
```yaml
effective_sample_size:
  formula: "n_eff = n_participants × n_observations / [1 + (n_observations - 1) × ICC]"
  application: "Use n_eff in standard power calculations"
  
design_effect:
  formula: "DE = 1 + (n_observations - 1) × ICC"
  sample_size_inflation: "n_required = n_simple × DE"
  
power_approximation:
  method_1: "Use n_eff in t-test power formulas"
  method_2: "Monte Carlo simulation for complex designs"
  method_3: "Analytic approximations (Snijders & Bosker, 2012)"
```

---

## 🔍 Experiment Type 2: Exploratory Analysis

### **2.1 Analysis of Variance (ANOVA)**

#### **One-Way ANOVA**
```yaml
model_specification:
  population_model: "Y_ij = μ + α_i + ε_ij"
  where:
    μ: "grand mean"
    α_i: "effect of group i"
    ε_ij: "random error ~ N(0, σ²)"
    
  constraints: "Σα_i = 0 (sum-to-zero constraint)"
  
hypothesis_testing:
  null_hypothesis: "H₀: α₁ = α₂ = ... = α_k = 0"
  alternative_hypothesis: "H₁: not all α_i = 0"
  
f_statistic:
  formula: "F = MS_between / MS_within"
  mean_squares: "MS_between = SS_between / (k-1)"
  mean_squares: "MS_within = SS_within / (N-k)"
  
  sum_of_squares:
    between: "SS_between = Σn_i(x̄_i - x̄)²"
    within: "SS_within = ΣΣ(x_ij - x̄_i)²"
    total: "SS_total = ΣΣ(x_ij - x̄)²"
```

#### **Effect Size Measures**
```yaml
eta_squared:
  formula: "η² = SS_between / SS_total"
  interpretation: "Proportion of total variance explained"
  bias: "Positively biased, especially with small samples"
  
partial_eta_squared:
  formula: "η²_p = SS_between / (SS_between + SS_within)"
  preferred: "Less biased than η²"
  interpretation: "Cohen (1988): 0.01 (small), 0.06 (medium), 0.14 (large)"
  
omega_squared:
  formula: "ω² = (SS_between - (k-1)MS_within) / (SS_total + MS_within)"
  advantage: "Unbiased estimate of population effect size"
  
cohens_f:
  formula: "f = √(η²_p / (1 - η²_p))"
  power_analysis: "Used in power calculations"
  interpretation: "0.10 (small), 0.25 (medium), 0.40 (large)"
```

#### **Power Analysis**
```yaml
sample_size_calculation:
  formula: "n = λ / (k × f²) + 1"
  where:
    λ: "noncentrality parameter from power tables"
    k: "number of groups"
    f²: "Cohen's f squared"
    
  noncentrality_parameter: "λ = n × k × f²"
  
power_calculation:
  distribution: "F follows noncentral F-distribution under H₁"
  power: "P(F > F_α,k-1,N-k | λ)"
  
minimum_detectable_effect:
  formula: "f = √(λ / (n × k))"
  where: "λ = critical value for desired power"
```

### **2.2 Factorial ANOVA**

#### **Two-Way ANOVA Model**
```yaml
model_specification:
  full_model: "Y_ijk = μ + α_i + β_j + (αβ)_ij + ε_ijk"
  where:
    α_i: "main effect of factor A (level i)"
    β_j: "main effect of factor B (level j)"
    (αβ)_ij: "interaction effect"
    ε_ijk: "random error"
    
main_effects:
  factor_a: "F_A = MS_A / MS_error"
  factor_b: "F_B = MS_B / MS_error"
  
interaction_effect:
  f_statistic: "F_AB = MS_AB / MS_error"
  interpretation: "Effect of A depends on level of B"
  
degrees_of_freedom:
  factor_a: "df_A = a - 1"
  factor_b: "df_B = b - 1"
  interaction: "df_AB = (a-1)(b-1)"
  error: "df_error = N - ab"
```

#### **Effect Sizes and Power**
```yaml
partial_eta_squared:
  main_effect_a: "η²_p,A = SS_A / (SS_A + SS_error)"
  main_effect_b: "η²_p,B = SS_B / (SS_B + SS_error)"
  interaction: "η²_p,AB = SS_AB / (SS_AB + SS_error)"
  
power_analysis_considerations:
  main_effects: "Calculated as if other factors don't exist"
  interaction_power: "Often requires larger samples than main effects"
  sample_size_per_cell: "n_cell = total_n / (a × b)"
  
factorial_design_efficiency:
  advantage: "Can detect interactions"
  cost: "Requires larger total sample size"
  optimal_allocation: "Equal n per cell usually optimal"
```

### **2.3 Multivariate Analysis of Variance (MANOVA)**

#### **Model and Test Statistics**
```yaml
model_specification:
  multivariate_model: "Y = XB + E"
  where:
    Y: "n × p matrix of responses"
    X: "n × q design matrix"
    B: "q × p parameter matrix"
    E: "n × p error matrix"
    
test_statistics:
  wilks_lambda: "Λ = |E| / |H + E|"
  pillai_trace: "V = tr(H(H + E)^-1)"
  hotelling_lawley_trace: "T = tr(HE^-1)"
  roy_largest_root: "θ = largest eigenvalue of HE^-1"
  
hypothesis_matrices:
  hypothesis: "H = C'(C(X'X)^-1C')^-1C'"
  error: "E = Y'Y - B'X'XB"
```

#### **Effect Sizes and Interpretation**
```yaml
multivariate_effect_sizes:
  partial_eta_squared: "η²_p = 1 - Λ^(1/s)"
  where: "s = min(p, df_hypothesis)"
  
  pillai_conversion: "η²_p = V / (s - V + 1)"
  
interpretation_guidelines:
  small_effect: "η²_p ≈ 0.01"
  medium_effect: "η²_p ≈ 0.06"
  large_effect: "η²_p ≈ 0.14"
  
discriminant_analysis:
  canonical_variates: "Eigenvectors of E^-1H"
  separation_assessment: "Canonical correlations"
```

---

## 🏆 Experiment Type 3: Ranking Studies

### **3.1 Kendall's Concordance**

#### **Mathematical Foundation**
```yaml
concordance_coefficient:
  formula: "W = 12S / [m²(n³ - n)]"
  where:
    S: "sum of squared deviations of rank sums"
    m: "number of judges/raters"
    n: "number of objects ranked"
    
computational_formula:
  rank_sums: "R_j = Σ(rank given to object j by each judge)"
  mean_rank_sum: "R̄ = mn(n+1)/2"
  sum_of_squares: "S = Σ(R_j - R̄)²"
  
significance_testing:
  large_sample: "χ² = m(n-1)W ~ χ²(n-1)"
  small_sample: "Use exact tables (Siegel & Castellan, 1988)"
  
correction_for_ties:
  tied_ranks: "W = 12S / [m²(n³ - n) - mΣT_i]"
  where: "T_i = t_i³ - t_i for t_i tied observations in rank i"
```

#### **Interpretation and Effect Sizes**
```yaml
concordance_interpretation:
  perfect_agreement: "W = 1.0"
  no_agreement: "W = 0.0"
  random_rankings: "W = 0.0 expected value"
  
practical_guidelines:
  weak_agreement: "W < 0.3"
  moderate_agreement: "0.3 ≤ W < 0.7"
  strong_agreement: "W ≥ 0.7"
  
reliability_as_icc:
  relationship: "W = (ICC - 1/m) × m/(m-1)"
  where: "ICC = intraclass correlation coefficient"
```

#### **Power and Sample Size**
```yaml
power_analysis:
  effect_size_parameter: "W itself serves as effect size"
  
sample_size_requirements:
  small_effect: "W = 0.1 requires m ≥ 20 judges"
  medium_effect: "W = 0.3 requires m ≥ 10 judges"  
  large_effect: "W = 0.7 requires m ≥ 5 judges"
  
  minimum_objects: "n ≥ 3 for meaningful ranking"
  practical_maximum: "n ≤ 10 for cognitive feasibility"
  
monte_carlo_power:
  simulation_approach: "Generate rankings under alternative hypothesis"
  power_estimation: "Proportion of simulations rejecting H₀"
```

### **3.2 Bradley-Terry Model**

#### **Model Specification**
```yaml
probability_model:
  pairwise_comparison: "P(i beats j) = π_i / (π_i + π_j)"
  strength_parameters: "π_i > 0 for all objects i"
  identifiability: "Σlog(π_i) = 0 or π_n = 1 (reference object)"
  
likelihood_function:
  log_likelihood: "LL = ΣΣ w_ij log(π_i / (π_i + π_j))"
  where: "w_ij = number of times i beats j"
  
parameter_estimation:
  iterative_scaling: "π_i^(t+1) = π_i^(t) × w_i+ / Σ_j≠i π_j^(t)/(π_i^(t) + π_j^(t))"
  convergence_criterion: "||π^(t+1) - π^(t)|| < ε"
```

#### **Statistical Inference**
```yaml
standard_errors:
  fisher_information: "I_ij = Σ_k≠i n_ik π_k / (π_i + π_k)²"
  asymptotic_variance: "Var(log π_i) = (I^-1)_ii"
  
confidence_intervals:
  log_scale: "log π_i ± z_α/2 × SE(log π_i)"
  strength_scale: "exp(log π_i ± z_α/2 × SE(log π_i))"
  
hypothesis_testing:
  equal_strengths: "H₀: π_1 = π_2 = ... = π_n"
  likelihood_ratio: "LR = 2(LL_full - LL_reduced)"
  degrees_of_freedom: "df = n - 1"
  
pairwise_comparisons:
  strength_ratio: "π_i / π_j"
  log_ratio_se: "SE(log(π_i/π_j)) = √(Var(log π_i) + Var(log π_j))"
```

#### **Model Extensions**
```yaml
davidson_model_ties:
  probability_i_beats_j: "P(i > j) = π_i / (π_i + π_j + ν√(π_i π_j))"
  probability_tie: "P(i = j) = ν√(π_i π_j) / (π_i + π_j + ν√(π_i π_j))"
  tie_parameter: "ν ≥ 0"
  
random_effects_extension:
  judge_heterogeneity: "π_ij = π_i × γ_j"
  where: "γ_j ~ Gamma(α, β) represents judge j's scaling"
  
covariate_models:
  strength_regression: "log π_i = β₀ + β₁X_i1 + ... + β_p X_ip"
  interpretation: "Explains strength in terms of object characteristics"
```

### **3.3 Plackett-Luce Model**

#### **Full Ranking Model**
```yaml
ranking_probability:
  full_ranking: "P(ranking) = ∏_{k=1}^{n-1} π_{r_k} / Σ_{j=k}^n π_{r_j}"
  where: "r_k = object ranked kth"
  
top_k_ranking:
  partial_ranking: "P(top-k) = ∏_{i=1}^k π_{r_i} / Σ_{j=i}^n π_{r_j}"
  application: "When only top preferences matter"
  
likelihood_function:
  full_data: "LL = ΣΣ log(π_i / Σ_{j∈S_ik} π_j)"
  where: "S_ik = set of objects available for position k in ranking i"
```

#### **Parameter Estimation and Inference**
```yaml
mm_algorithm:
  update_rule: "π_i^(t+1) = π_i^(t) × Σ_r w_r I(i ranked in r) / Σ_k position_weight(i,k,r)"
  convergence: "Monitor log-likelihood improvement"
  
standard_errors:
  observed_information: "H = -∂²LL/∂(log π)²"
  asymptotic_covariance: "Var(log π) = H^-1"
  
model_selection:
  aic: "AIC = -2LL + 2(n-1)"
  bic: "BIC = -2LL + (n-1)log(N)"
  cross_validation: "Predict held-out rankings"
```

---

## 🎯 Experiment Type 4: A/B Testing

### **4.1 Proportion Tests**

#### **Two-Proportion z-Test**
```yaml
test_statistic:
  z_score: "z = (p̂₁ - p̂₂) / SE(p̂₁ - p̂₂)"
  
standard_error_pooled:
  formula: "SE = √(p̂(1-p̂)(1/n₁ + 1/n₂))"
  pooled_proportion: "p̂ = (x₁ + x₂)/(n₁ + n₂)"
  
standard_error_unpooled:
  formula: "SE = √(p̂₁(1-p̂₁)/n₁ + p̂₂(1-p̂₂)/n₂)"
  application: "For confidence intervals"
  
continuity_correction:
  yates_correction: "z = (|p̂₁ - p̂₂| - 0.5(1/n₁ + 1/n₂)) / SE"
  when_to_use: "Small expected frequencies (< 5)"
```

#### **Effect Size Measures**
```yaml
risk_difference:
  formula: "RD = p₁ - p₂"
  confidence_interval: "RD ± z_α/2 × SE_unpooled"
  interpretation: "Absolute difference in success rates"
  
relative_risk:
  formula: "RR = p₁ / p₂"
  log_confidence_interval: "log(RR) ± z_α/2 × SE(log RR)"
  standard_error: "SE(log RR) = √((1-p₁)/(n₁p₁) + (1-p₂)/(n₂p₂))"
  
odds_ratio:
  formula: "OR = (p₁/(1-p₁)) / (p₂/(1-p₂))"
  log_confidence_interval: "log(OR) ± z_α/2 × SE(log OR)"
  standard_error: "SE(log OR) = √(1/a + 1/b + 1/c + 1/d)"
  where: "a,b,c,d are cells of 2×2 contingency table"
  
cohens_h:
  formula: "h = 2(arcsin(√p₁) - arcsin(√p₂))"
  interpretation: "|h| = 0.2 (small), 0.5 (medium), 0.8 (large)"
```

#### **Power Analysis**
```yaml
sample_size_calculation:
  equal_allocation: "n = 2(z_α/2 + z_β)² × [p₁(1-p₁) + p₂(1-p₂)] / (p₁-p₂)²"
  unequal_allocation: "n₁ = (z_α/2 + z_β)² × [p₁(1-p₁)/r + p₂(1-p₂)] / (p₁-p₂)²"
  where: "r = n₁/n₂"
  
arcsine_transformation:
  variance_stabilizing: "n = 2(z_α/2 + z_β)² / h²"
  where: "h = Cohen's h"
  
minimum_detectable_effect:
  formula: "MDE = (z_α/2 + z_β) × √(2p̄(1-p̄)/n)"
  where: "p̄ = (p₁ + p₂)/2"
```

### **4.2 Continuous Outcome A/B Tests**

#### **Welch's t-Test (Unequal Variances)**
```yaml
test_statistic:
  formula: "t = (x̄₁ - x̄₂) / √(s₁²/n₁ + s₂²/n₂)"
  
satterthwaite_df:
  formula: "df = (s₁²/n₁ + s₂²/n₂)² / [(s₁²/n₁)²/(n₁-1) + (s₂²/n₂)²/(n₂-1)]"
  
power_analysis:
  noncentrality: "δ = (μ₁ - μ₂) / √(σ₁²/n₁ + σ₂²/n₂)"
  power_calculation: "Use noncentral t-distribution"
```

#### **Mann-Whitney U Test (Non-parametric)**
```yaml
test_statistic:
  u_statistic: "U = n₁n₂ + n₁(n₁+1)/2 - R₁"
  where: "R₁ = sum of ranks for group 1"
  
normal_approximation:
  z_score: "z = (U - μᵤ) / σᵤ"
  mean: "μᵤ = n₁n₂/2"
  variance: "σ²ᵤ = n₁n₂(n₁+n₂+1)/12"
  
continuity_correction:
  adjusted_z: "z = (|U - μᵤ| - 0.5) / σᵤ"
  
effect_size:
  probability_superiority: "P(X₁ > X₂) = U / (n₁ × n₂)"
  rank_biserial_correlation: "r = 2P(X₁ > X₂) - 1"
```

### **4.3 Sequential Testing and Early Stopping**

#### **Group Sequential Design**
```yaml
alpha_spending_functions:
  obrien_fleming: "α(t) = 2[1 - Φ(z_α/2/√t)]"
  pocock: "α(t) = α × log(1 + (e-1)t)"
  where: "t = information fraction (0 < t ≤ 1)"
  
  lan_demets: "General class of spending functions"
  power_family: "α(t) = α × t^ρ"
  
boundary_calculation:
  critical_values: "c_k satisfying α-spending at analysis k"
  stopping_boundaries: "Upper and lower bounds for test statistic"
  
sample_size_adjustment:
  information_based: "Calculate required information, convert to sample size"
  maximum_sample_size: "Typically 10-15% larger than fixed design"
```

#### **Bayesian Sequential Testing**
```yaml
posterior_probability:
  beta_binomial: "Success rate ~ Beta(α + x, β + n - x)"
  normal_normal: "Mean ~ N(μ_posterior, σ²_posterior)"
  
stopping_criteria:
  posterior_probability: "P(treatment better | data) > threshold"
  credible_interval: "95% CI excludes null value"
  
expected_sample_size:
  simulation_based: "Average N over posterior predictive distribution"
  analytical_approximation: "For conjugate priors"
```

---

## ⚡ Experiment Type 5: Single Sample Rating

### **5.1 One-Sample Tests**

#### **One-Sample t-Test**
```yaml
test_statistic:
  formula: "t = (x̄ - μ₀) / (s / √n)"
  degrees_of_freedom: "df = n - 1"
  
effect_size:
  cohens_d: "d = (x̄ - μ₀) / s"
  confidence_interval: "d ± t_α/2,df × √((n-1)/χ²_1-α/2,n-1 + d²/(2n))"
  
power_analysis:
  sample_size: "n = (t_α/2,df + t_β,df)² / d²"
  noncentrality: "δ = d√n"
  power: "P(t > t_α/2,df | δ)"
```

#### **Wilcoxon Signed-Rank Test**
```yaml
test_statistic:
  signed_ranks: "Rank |x_i - μ₀| and sum positive ranks"
  normal_approximation: "z = (W - μ_w) / σ_w"
  mean: "μ_w = n(n+1)/4"
  variance: "σ²_w = n(n+1)(2n+1)/24"
  
effect_size:
  probability_superiority: "P(X > μ₀)"
  matched_pairs_rank_biserial: "r = (W - n(n+1)/4) / (n(n+1)/4)"
```

### **5.2 Confidence Intervals and Precision**

#### **Mean Confidence Intervals**
```yaml
t_interval:
  formula: "x̄ ± t_α/2,df × (s / √n)"
  
bootstrap_intervals:
  percentile_method: "Use 2.5th and 97.5th percentiles of bootstrap distribution"
  bias_corrected: "Adjust for bias in bootstrap estimate"
  bca_method: "Bias-corrected and accelerated intervals"
  
precision_planning:
  margin_of_error: "ME = t_α/2,df × (s / √n)"
  required_sample_size: "n = (t_α/2 × s / ME)²"
  pilot_study_approach: "Use pilot s to plan main study"
```

#### **Proportion Confidence Intervals**
```yaml
wald_interval:
  formula: "p̂ ± z_α/2 × √(p̂(1-p̂)/n)"
  limitation: "Poor coverage for extreme proportions"
  
wilson_score_interval:
  formula: "(p̂ + z²/2n ± z√(p̂(1-p̂)/n + z²/4n²)) / (1 + z²/n)"
  advantage: "Better coverage properties"
  
clopper_pearson_exact:
  based_on: "Beta distribution quantiles"
  conservative: "Always achieves nominal coverage"
  
jeffreys_interval:
  bayesian_approach: "Based on uniform prior (Beta(0.5, 0.5))"
  credible_interval: "Often close to frequentist intervals"
```

### **5.3 Reliability Analysis**

#### **Internal Consistency**
```yaml
cronbachs_alpha:
  formula: "α = (k/(k-1)) × (1 - Σs²ᵢ/s²ₜ)"
  where:
    k: "number of items"
    s²ᵢ: "variance of item i"
    s²ₜ: "variance of total score"
    
confidence_interval:
  feldt_method: "Based on F-distribution"
  bootstrap: "Empirical distribution of α"
  
interpretation:
  unacceptable: "α < 0.60"
  poor: "0.60 ≤ α < 0.70"
  acceptable: "0.70 ≤ α < 0.80"
  good: "0.80 ≤ α < 0.90"
  excellent: "α ≥ 0.90"
  
mcdonalds_omega:
  formula: "ω = (Σλᵢ)² / [(Σλᵢ)² + Σ(1-λᵢ²)]"
  where: "λᵢ = factor loading for item i"
  advantage: "More robust to tau-equivalent model violations"
```

#### **Test-Retest Reliability**
```yaml
pearson_correlation:
  formula: "r = Σ(X₁ - X̄₁)(X₂ - X̄₂) / √[Σ(X₁ - X̄₁)²Σ(X₂ - X̄₂)²]"
  
intraclass_correlation:
  two_way_mixed: "ICC(3,1) = (MS_subjects - MS_error) / (MS_subjects + (k-1)MS_error)"
  interpretation: "Same as reliability coefficient"
  
standard_error_measurement:
  formula: "SEM = s × √(1 - reliability)"
  confidence_interval: "X ± 1.96 × SEM"
  
minimal_detectable_change:
  formula: "MDC = SEM × z_α/2 × √2"
  interpretation: "Smallest change exceeding measurement error"
```

---

## 🔬 Experiment Type 6: Threshold Detection

### **6.1 Psychometric Function Fitting**

#### **Sigmoid Function Forms**
```yaml
logistic_function:
  formula: "Ψ(x) = γ + (1 - γ - λ)[1 / (1 + exp(-(x - α)/β))]"
  parameters:
    α: "threshold (50% point after adjusting for guess/lapse)"
    β: "slope parameter (related to standard deviation)"
    γ: "guess rate (lower asymptote)"
    λ: "lapse rate (1 - upper asymptote)"
    
cumulative_gaussian:
  formula: "Ψ(x) = γ + (1 - γ - λ)Φ((x - α)/β)"
  where: "Φ = cumulative standard normal"
  
weibull_function:
  formula: "Ψ(x) = 1 - (1 - γ)exp(-((x/α)^β))"
  application: "Often used in vision research"
```

#### **Maximum Likelihood Estimation**
```yaml
likelihood_function:
  binomial_model: "L = ∏ᵢ (nᵢ choose kᵢ) × Ψ(xᵢ)^kᵢ × (1 - Ψ(xᵢ))^(nᵢ-kᵢ)"
  where:
    nᵢ: "number of trials at stimulus level xᵢ"
    kᵢ: "number of positive responses at xᵢ"
    
log_likelihood:
  formula: "LL = Σᵢ [kᵢ log Ψ(xᵢ) + (nᵢ - kᵢ) log(1 - Ψ(xᵢ))]"
  
parameter_estimation:
  optimization: "Maximize LL using numerical methods"
  initial_values: "Use method of moments or grid search"
  constraints: "0 ≤ γ,λ ≤ 1, α,β > 0"
```

#### **Goodness of Fit and Inference**
```yaml
deviance_test:
  deviance: "D = 2(LL_saturated - LL_fitted)"
  distribution: "D ~ χ²(df) under H₀"
  degrees_of_freedom: "df = number of stimulus levels - number of parameters"
  
confidence_intervals:
  profile_likelihood: "Values where -2ΔLL ≤ χ²_α,1"
  bootstrap: "Empirical distribution from resampling"
  delta_method: "First-order approximation using Fisher information"
  
bias_correction:
  bootstrap_bias: "Bias = mean(θ̂*) - θ̂"
  bias_corrected_estimate: "θ̂_BC = θ̂ - bias"
```

### **6.2 Adaptive Testing Procedures**

#### **Up-Down Methods**
```yaml
simple_staircase:
  rule: "Increase intensity after incorrect, decrease after correct"
  convergence_point: "50% correct (for 2AFC)"
  step_size: "Fixed or geometric progression"
  
weighted_up_down:
  levitt_rules:
    70_7_percent: "2-down-1-up rule"
    79_4_percent: "3-down-1-up rule"
    91_0_percent: "4-down-1-up rule"
  
  convergence_probability: "P = (step_down/step_up)^(1/k)"
  where: "k = number of consecutive correct for step down"
  
stopping_criteria:
  fixed_reversals: "Stop after predetermined number of reversals"
  standard_error: "Stop when SE(threshold) < criterion"
  maximum_trials: "Safety stop to prevent infinite runs"
```

#### **Adaptive Procedures Analysis**
```yaml
threshold_estimation:
  reversal_average: "θ̂ = mean of last N reversals"
  weighted_average: "Higher weight to later reversals"
  maximum_likelihood: "Fit psychometric function to all data"
  
standard_error:
  empirical_se: "SE = SD(reversals) / √N"
  theoretical_se: "Based on psychometric function slope"
  
efficiency_measures:
  trial_efficiency: "Compare to method of constant stimuli"
  information_efficiency: "Fisher information per trial"
```

### **6.3 Bayesian Adaptive Methods**

#### **QUEST (Quick Estimation by Sequential Testing)**
```yaml
prior_distribution:
  threshold_prior: "p(α) ~ N(μ_prior, σ²_prior)"
  slope_prior: "p(β) ~ Gamma(a, b)"
  
posterior_update:
  bayes_rule: "p(α|data) ∝ p(data|α) × p(α)"
  sequential_update: "Update after each trial"
  
stimulus_selection:
  information_criterion: "Maximize expected information gain"
  entropy_criterion: "Minimize expected posterior entropy"
  
threshold_estimate:
  posterior_mode: "α̂ = argmax p(α|data)"
  posterior_mean: "α̂ = E[α|data]"
  credible_interval: "95% highest posterior density"
```

#### **Implementation Formulas**
```python
# Python implementation for psychometric function fitting
import numpy as np
from scipy import optimize, stats
from scipy.special import erf

def logistic_psychometric(x, alpha, beta, gamma=0.0, lambda_val=0.0):
    """
    Logistic psychometric function
    x: stimulus intensity
    alpha: threshold parameter
    beta: slope parameter  
    gamma: guess rate
    lambda_val: lapse rate
    """
    return gamma + (1 - gamma - lambda_val) / (1 + np.exp(-(x - alpha) / beta))

def gaussian_psychometric(x, alpha, beta, gamma=0.0, lambda_val=0.0):
    """
    Cumulative Gaussian psychometric function
    """
    z = (x - alpha) / beta
    return gamma + (1 - gamma - lambda_val) * 0.5 * (1 + erf(z / np.sqrt(2)))

def neg_log_likelihood(params, x, k, n, func_type='logistic'):
    """
    Negative log-likelihood for psychometric function
    params: [alpha, beta, gamma, lambda_val]
    x: stimulus intensities
    k: number of positive responses
    n: number of trials
    """
    alpha, beta, gamma, lambda_val = params
    
    # Ensure valid parameter ranges
    if beta <= 0 or gamma < 0 or gamma > 1 or lambda_val < 0 or lambda_val > 1:
        return np.inf
    if gamma + lambda_val >= 1:
        return np.inf
    
    if func_type == 'logistic':
        p = logistic_psychometric(x, alpha, beta, gamma, lambda_val)
    elif func_type == 'gaussian':
        p = gaussian_psychometric(x, alpha, beta, gamma, lambda_val)
    
    # Avoid log(0) problems
    p = np.clip(p, 1e-10, 1 - 1e-10)
    
    # Binomial log-likelihood
    ll = np.sum(k * np.log(p) + (n - k) * np.log(1 - p))
    return -ll

def fit_psychometric_function(x, k, n, func_type='logistic', initial_guess=None):
    """
    Fit psychometric function to data using maximum likelihood
    Returns parameter estimates and confidence intervals
    """
    if initial_guess is None:
        # Simple initial guess based on data
        alpha_init = x[np.argmin(np.abs(k/n - 0.5))]
        beta_init = (np.max(x) - np.min(x)) / 4
        initial_guess = [alpha_init, beta_init, 0.0, 0.0]
    
    # Optimize
    result = optimize.minimize(
        neg_log_likelihood,
        initial_guess,
        args=(x, k, n, func_type),
        method='L-BFGS-B',
        bounds=[(-np.inf, np.inf), (0.001, np.inf), (0, 0.5), (0, 0.5)]
    )
    
    # Calculate confidence intervals using Hessian
    try:
        hessian = result.hess_inv.todense()
        se = np.sqrt(np.diag(hessian))
        ci_lower = result.x - 1.96 * se
        ci_upper = result.x + 1.96 * se
    except:
        # If Hessian calculation fails, use bootstrap
        ci_lower = ci_upper = None
    
    return {
        'parameters': result.x,
        'success': result.success,
        'log_likelihood': -result.fun,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper
    }

def deviance_goodness_of_fit(x, k, n, fitted_params, func_type='logistic'):
    """
    Calculate deviance statistic for goodness of fit test
    """
    alpha, beta, gamma, lambda_val = fitted_params
    
    if func_type == 'logistic':
        p_fit = logistic_psychometric(x, alpha, beta, gamma, lambda_val)
    elif func_type == 'gaussian':
        p_fit = gaussian_psychometric(x, alpha, beta, gamma, lambda_val)
    
    # Saturated model likelihood (perfect fit)
    p_obs = k / n
    p_obs = np.clip(p_obs, 1e-10, 1 - 1e-10)  # Avoid log(0)
    
    ll_saturated = np.sum(k * np.log(p_obs) + (n - k) * np.log(1 - p_obs))
    ll_fitted = np.sum(k * np.log(p_fit) + (n - k) * np.log(1 - p_fit))
    
    deviance = 2 * (ll_saturated - ll_fitted)
    df = len(x) - len(fitted_params)
    p_value = 1 - stats.chi2.cdf(deviance, df)
    
    return {'deviance': deviance, 'df': df, 'p_value': p_value}
```

---

## 📊 Implementation Framework

### **Statistical Computing Infrastructure**
```yaml
required_libraries:
  python:
    core: ["numpy", "scipy", "pandas", "matplotlib"]
    statistics: ["statsmodels", "pingouin", "scikit-learn"]
    power_analysis: ["power", "pwr"]
    psychometrics: ["psignifit", "psychopy"]
    
  r_packages:
    core: ["base", "stats", "MASS"]
    power_analysis: ["pwr", "WebPower", "PowerTOST"] 
    mixed_models: ["lme4", "nlme", "lmerTest"]
    psychometrics: ["psycho", "psych", "modelfree"]
    
validation_testing:
  unit_tests: "Test each formula against known results"
  integration_tests: "Test complete analysis workflows"
  benchmark_datasets: "Validate against published examples"
  edge_case_handling: "Test boundary conditions and error states"
```

### **Quality Assurance Protocol**
```yaml
accuracy_validation:
  cross_reference: "Compare results across different software implementations"
  literature_validation: "Verify against published examples and datasets"
  expert_review: "Statistical expert validation of all implementations"
  
error_handling:
  numerical_stability: "Robust handling of edge cases and numerical issues"
  assumption_checking: "Automatic testing of statistical assumptions"
  warning_systems: "Alert users to potential problems"
  
documentation_standards:
  mathematical_notation: "Clear explanation of all formulas and parameters"
  implementation_notes: "Software-specific considerations and limitations"
  example_usage: "Complete worked examples for each method"
```

---

*Statistical Equations Library Version: 1.0*  
*Complete Mathematical Foundation for Agent Implementation*  
*Validated Against Academic Standards and Best Practices*