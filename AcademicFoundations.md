# Academic Foundations for Experiment Types

## 🎓 Comprehensive Academic Framework for QA System Agent

This document provides detailed academic foundations for each experiment type, complete with peer-reviewed methodological backing, statistical requirements, and validation frameworks.

---

## 📊 Experiment Type 1: Comparison Studies

### **Academic Foundation**

#### **Methodological Basis**
```yaml
primary_framework: "Comparative Judgment Theory (Thurstone, 1927)"
statistical_foundation: "Paired Comparison Analysis (David, 1988)"
validation_studies:
  - "Bradley-Terry Models for Paired Comparisons (Bradley & Terry, 1952)"
  - "Analysis of Preferences (Luce, 1959)" 
  - "Modern Psychophysics (Gescheider, 1997)"

quality_assessment_standards:
  - "ITU-T P.800: Methods for subjective determination of transmission quality"
  - "ITU-T P.830: Subjective performance assessment of telephone-band speech"
  - "ISO 20462-3: Photography — Psychophysical experimental methods"
```

#### **Design Principles (Montgomery, 2017)**
```yaml
fundamental_requirements:
  randomization:
    purpose: "Control for systematic bias"
    implementation: "Latin square or balanced incomplete block designs"
    validation: "Residual analysis for systematic patterns"
    
  replication:
    purpose: "Estimate experimental error"
    requirement: "Minimum 3 replications per condition pair"
    power_consideration: "n ≥ 6 for detecting d=0.8 with 80% power"
    
  blocking:
    purpose: "Control for nuisance variables"
    application: "Participant characteristics, session order, stimulus properties"
    analysis: "Mixed-effects models with random participant effects"
```

#### **Statistical Methods with Academic Backing**
```yaml
paired_t_test:
  when_appropriate: "Two conditions, continuous outcome, normal differences"
  assumptions:
    normality: "Shapiro-Wilk test on difference scores (p > 0.05)"
    independence: "No systematic order effects (requires randomization)"
  
  effect_size_calculation:
    cohens_d: "d = (M₁ - M₂) / SD_diff"
    interpretation: "Cohen (1988): 0.2=small, 0.5=medium, 0.8=large"
    confidence_intervals: "Hedges & Olkin (1985) bias correction for small n"
    
  power_analysis:
    formula: "n = 2(z_α/2 + z_β)² / d²"
    minimum_detectable_effect: "MDES = 2.8 × σ / √n for α=0.05, β=0.20"
    sample_size_justification: "G*Power 3.1.9.7 calculations required"

mixed_effects_model:
  when_appropriate: "Multiple stimuli per participant, hierarchical data"
  model_specification: "lme4::lmer(rating ~ condition + (1|participant) + (1|stimulus))"
  
  variance_components:
    participant_variance: "σ²_participant: between-subject differences"
    stimulus_variance: "σ²_stimulus: systematic stimulus effects"
    residual_variance: "σ²_residual: measurement error"
    
  power_considerations:
    effective_sample_size: "n_eff = n_participants × n_stimuli / (1 + (n_stimuli-1)×ICC)"
    ICC_estimation: "Requires pilot data or literature estimates"
    
  reporting_requirements:
    random_effects: "Report variance components with confidence intervals"
    fixed_effects: "β coefficients with SE and t-statistics"
    model_fit: "AIC, BIC, log-likelihood, R² marginal/conditional"
```

#### **Academic Validation Checklist**
```yaml
experimental_control:
  counterbalancing:
    requirement: "Williams Square design for order effects"
    reference: "Williams (1949), Experimental designs balanced for pairs"
    validation: "Chi-square test for order independence"
    
  stimulus_control:
    matching: "Stimuli matched on relevant dimensions (pitch, duration, etc.)"
    reference: "Keppel & Wickens (2004), Design and Analysis Ch. 8"
    validation: "ANOVA on stimulus characteristics before evaluation"
    
  environmental_control:
    standardization: "Identical presentation conditions"
    reference: "ITU-T P.800 listening test requirements"
    validation: "Equipment calibration records"

statistical_validity:
  assumption_testing:
    normality: "Required for t-tests, QQ-plots + Shapiro-Wilk"
    homoscedasticity: "Levene's test for equal variances"
    independence: "Durbin-Watson test for serial correlation"
    
  multiple_comparisons:
    family_wise_error: "Bonferroni, Holm, or Benjamini-Hochberg correction"
    reference: "Hochberg & Tamhane (1987), Multiple Comparison Procedures"
    implementation: "p.adjust() function in R"
    
  effect_size_reporting:
    requirement: "Cohen's d with 95% CI for all comparisons"
    reference: "APA Publication Manual 7th Edition"
    interpretation: "Domain-specific benchmarks when available"
```

---

## 🔍 Experiment Type 2: Exploratory Analysis

### **Academic Foundation**

#### **Methodological Framework**
```yaml
theoretical_basis: "Exploratory Data Analysis (Tukey, 1977)"
factorial_design_theory: "Box, Hunter & Hunter (2005), Statistics for Experimenters"
quality_assessment_framework: "Comprehensive Quality Evaluation (Jekosch, 2005)"

established_approaches:
  - "Full Factorial Designs (2^k and 3^k designs)"
  - "Response Surface Methodology (Montgomery, 2017)"
  - "Taguchi Methods for Robust Design (Phadke, 1989)"
  - "Multivariate Analysis of Variance (Johnson & Wichern, 2007)"
```

#### **Design Principles**
```yaml
factorial_design_requirements:
  complete_crossing:
    purpose: "Estimate all main effects and interactions"
    implementation: "All combinations of factor levels tested"
    power_consideration: "n per cell ≥ 5 for reliable interaction detection"
    
  factor_selection:
    criterion: "Theoretical importance and practical relevance"
    limitation: "2^k rule: k ≤ 5 for manageable design"
    screening: "Fractional factorial designs for initial exploration"
    
  response_variable_selection:
    requirement: "Multiple dependent variables for comprehensive assessment"
    correlation_structure: "Principal component analysis for dimension reduction"
    measurement_scales: "Interval or ratio scales preferred for ANOVA"
```

#### **Statistical Methods with Academic Foundation**
```yaml
multivariate_anova:
  when_appropriate: "Multiple correlated dependent variables"
  test_statistics:
    willks_lambda: "Λ = |E| / |H + E|"
    pillai_trace: "V = tr(H(H + E)^-1)"
    hotelling_t2: "T² = tr(H × E^-1)"
    
  assumptions:
    multivariate_normality: "Mardia's test or Henze-Zirkler test"
    homogeneity_covariance: "Box's M test"
    independence: "Residual analysis"
    
  effect_size_measures:
    partial_eta_squared: "η²_p = λ / (1 + λ) for each factor"
    interpretation: "Cohen (1988): 0.01=small, 0.06=medium, 0.14=large"
    
  post_hoc_analysis:
    discriminant_analysis: "Identify which variables differentiate groups"
    univariate_follow_up: "Protected F-tests with α adjustment"

response_surface_analysis:
  when_appropriate: "Continuous factors, optimization goals"
  model_specification: "Y = β₀ + Σβᵢxᵢ + Σβᵢᵢxᵢ² + ΣΣβᵢⱼxᵢxⱼ + ε"
  
  design_requirements:
    central_composite: "2^k factorial + axial + center points"
    box_behnken: "Alternative for 3-level designs"
    space_filling: "Latin hypercube for computer experiments"
    
  analysis_methods:
    ridge_analysis: "Find optimal factor combinations"
    canonical_analysis: "Characterize response surface shape"
    confidence_regions: "Bootstrap or delta method"

cluster_analysis:
  when_appropriate: "Exploratory pattern identification"
  distance_measures:
    euclidean: "For continuous variables"
    manhattan: "Robust to outliers"
    correlation: "For profile similarity"
    
  clustering_methods:
    hierarchical: "Ward's method with dendrograms"
    k_means: "When number of clusters known"
    model_based: "Gaussian mixture models"
    
  validation:
    silhouette_analysis: "Average silhouette width > 0.5"
    gap_statistic: "Tibshirani et al. (2001) method"
    cross_validation: "Stability across random subsamples"
```

#### **Sample Size Requirements**
```yaml
factorial_anova:
  general_rule: "n ≥ 20 per cell for stable estimates"
  interaction_detection: "n ≥ 25 per cell for medium interactions (f² = 0.25)"
  power_analysis: "G*Power with specific f² values"
  
multivariate_analysis:
  minimum_ratio: "n ≥ 5 × number of variables (Tabachnick & Fidell, 2019)"
  recommended_ratio: "n ≥ 10 × number of variables for stable results"
  special_cases: "n ≥ 100 for factor analysis, n ≥ 200 for SEM"

effect_size_estimation:
  small_effects: "n ≥ 100 total for detecting f² = 0.02"
  medium_effects: "n ≥ 50 total for detecting f² = 0.15"
  large_effects: "n ≥ 25 total for detecting f² = 0.35"
```

---

## 🏆 Experiment Type 3: Ranking Studies

### **Academic Foundation**

#### **Theoretical Framework**
```yaml
ranking_theory: "Theory of Choice Behavior (Luce, 1959)"
paired_comparison_models: "Bradley-Terry-Luce Models (Agresti, 2002)"
consensus_measurement: "Kendall's Concordance Theory (Kendall, 1948)"

established_methodologies:
  - "Thurstone Case V Scaling (Thurstone, 1927)"
  - "Bradley-Terry Models (Bradley & Terry, 1952)"
  - "Plackett-Luce Models (Plackett, 1975)"
  - "Random Utility Models (McFadden, 1974)"
  
validation_literature:
  - "Handbook of Choice Modelling (Hess & Daly, 2014)"
  - "Analyzing Sensory Data with R (Lê & Worch, 2015)"
  - "Preference Learning (Fürnkranz & Hüllermeier, 2010)"
```

#### **Design Considerations**
```yaml
ranking_vs_rating:
  ranking_advantages:
    - "Eliminates scale usage bias"
    - "Forces discrimination between options"
    - "More realistic decision-making context"
    
  ranking_limitations:
    - "Information loss compared to interval scales"
    - "Computational complexity for many items"
    - "Cognitive burden for large choice sets"
    
  design_decision_criteria:
    ranking_preferred: "When relative preferences are primary interest"
    rating_preferred: "When absolute quality levels matter"
    hybrid_approaches: "Best-worst scaling combines benefits"

complete_vs_partial_rankings:
  complete_ranking:
    application: "≤ 7 items (Miller's magical number)"
    analysis: "Full ranking information available"
    cognitive_load: "Manageable for trained evaluators"
    
  partial_ranking:
    application: "> 7 items, focus on top preferences"
    design: "Top-k rankings or paired comparisons"
    analysis: "Requires specialized models (Plackett-Luce)"
    
  paired_comparison:
    application: "Large item sets, systematic sampling"
    design: "Balanced incomplete block designs"
    analysis: "Bradley-Terry or Thurstone models"
```

#### **Statistical Methods with Academic Validation**
```yaml
kendalls_concordance:
  purpose: "Measure agreement between multiple rankers"
  formula: "W = 12S / [m²(n³ - n)]"
  where:
    S: "Sum of squared deviations of rank sums from mean"
    m: "Number of judges/evaluators"
    n: "Number of items ranked"
    
  interpretation:
    W_values: "0 = no agreement, 1 = perfect agreement"
    guidelines: "W > 0.1 weak, W > 0.3 moderate, W > 0.7 strong"
    
  significance_testing:
    chi_square: "χ² = m(n-1)W, df = n-1"
    exact_test: "Available for small samples (m ≤ 7, n ≤ 10)"
    
  assumptions:
    independence: "Rankers evaluate independently"
    identical_distributions: "Same ranking task for all judges"
    
bradley_terry_model:
  purpose: "Estimate item strengths from pairwise preferences"
  probability_model: "P(i beats j) = πᵢ / (πᵢ + πⱼ)"
  
  parameter_estimation:
    maximum_likelihood: "Iterative proportional fitting algorithm"
    standard_errors: "Based on Fisher information matrix"
    confidence_intervals: "Profile likelihood or Wald intervals"
    
  model_diagnostics:
    goodness_of_fit: "χ² test comparing observed vs predicted"
    overdispersion: "Quasi-likelihood adjustment"
    transitivity: "Check for A>B>C>A violations"
    
  extensions:
    random_effects: "Account for judge heterogeneity"
    covariates: "Include item or judge characteristics"
    ties: "Davidson (1970) extension for tied preferences"

plackett_luce_model:
  purpose: "Model full rankings or top-k selections"
  probability_model: "P(ranking) = ∏ πᵢ / Σ remaining πⱼ"
  
  estimation_methods:
    mm_algorithm: "Minorization-maximization (Hunter, 2004)"
    em_algorithm: "Expectation-maximization for missing data"
    bayesian: "MCMC for uncertainty quantification"
    
  model_selection:
    aic_bic: "Compare models with different complexity"
    cross_validation: "Predict hold-out rankings"
    goodness_of_fit: "Pearson residuals analysis"

thurstone_scaling:
  purpose: "Convert rankings to interval-scale measurements"
  model_assumption: "Underlying normal distributions for utilities"
  
  case_v_assumptions:
    equal_variances: "All items have same error variance"
    zero_correlations: "Independent utility judgments"
    
  scaling_procedure:
    z_score_conversion: "Convert proportion preferences to z-scores"
    least_squares_solution: "Solve for scale values"
    
  validation:
    circular_triads: "Check for intransitive preferences"
    goodness_of_fit: "Chi-square test of model predictions"
```

#### **Sample Size and Power Analysis**
```yaml
kendalls_concordance:
  minimum_sample: "m ≥ 3 judges, n ≥ 3 items"
  power_considerations:
    small_effect: "W = 0.1 requires m ≥ 20 for 80% power"
    medium_effect: "W = 0.3 requires m ≥ 10 for 80% power"
    large_effect: "W = 0.7 requires m ≥ 5 for 80% power"
    
  reliability_requirements:
    acceptable: "m ≥ 6 judges for W > 0.3"
    good: "m ≥ 10 judges for W > 0.5"
    excellent: "m ≥ 15 judges for W > 0.7"

bradley_terry_analysis:
  minimum_comparisons: "Each pair compared ≥ 3 times"
  balanced_design: "Equal number of comparisons per pair"
  power_analysis: "Depends on true strength differences"
  
  detectability:
    small_difference: "π₁/π₂ = 1.5 requires n ≥ 100 comparisons"
    medium_difference: "π₁/π₂ = 2.0 requires n ≥ 50 comparisons"
    large_difference: "π₁/π₂ = 3.0 requires n ≥ 25 comparisons"

ranking_studies:
  complete_rankings:
    minimum: "n ≥ 20 rankers for stable estimates"
    recommended: "n ≥ 30 rankers for hypothesis testing"
    
  partial_rankings:
    top_k_studies: "n ≥ 50 for reliable preference estimation"
    paired_comparison: "n ≥ 10 × number_of_items for full connectivity"
```

---

## 🎯 Experiment Type 4: A/B Testing

### **Academic Foundation**

#### **Statistical Framework**
```yaml
hypothesis_testing_theory: "Neyman-Pearson Framework (Neyman & Pearson, 1933)"
experimental_design: "Randomized Controlled Trials (Fisher, 1935)"
online_experimentation: "A/B Testing Methodology (Kohavi et al., 2009)"

established_literature:
  - "Trustworthy Online Controlled Experiments (Kohavi et al., 2020)"
  - "Experimental and Quasi-Experimental Designs (Campbell & Stanley, 1963)"
  - "Statistical Power Analysis (Cohen, 1988)"
  - "Multiple Comparisons in A/B Testing (Deng et al., 2016)"

industry_standards:
  - "Netflix Experimentation Platform (Xu et al., 2015)"
  - "Facebook's Planout Framework (Bakshy et al., 2014)"
  - "Microsoft's ExP Platform (Deng et al., 2013)"
```

#### **Design Principles**
```yaml
randomization_requirements:
  individual_randomization:
    method: "Simple random assignment"
    implementation: "Cryptographic hash functions for consistent assignment"
    validation: "Balance checks on observable characteristics"
    
  stratified_randomization:
    purpose: "Ensure balance on important covariates"
    implementation: "Block randomization within strata"
    analysis: "Stratified analysis for improved precision"
    
  cluster_randomization:
    when_needed: "Network effects or spillover concerns"
    analysis_adjustment: "Intracluster correlation correction"
    sample_size_inflation: "Design effect = 1 + (m-1)×ICC"

power_analysis_framework:
  effect_size_specification:
    minimum_practical_difference: "Business-relevant threshold"
    standardized_effect: "Cohen's d or odds ratio"
    confidence_level: "Typically α = 0.05"
    power_requirement: "Usually 1-β = 0.80"
    
  sample_size_calculation:
    two_sample_t_test: "n = 2(z_α/2 + z_β)² × σ² / Δ²"
    proportion_test: "n = (z_α/2 + z_β)² × [p₁(1-p₁) + p₂(1-p₂)] / (p₁-p₂)²"
    survival_analysis: "Schoenfeld (1981) formula for hazard ratios"
    
  sequential_testing:
    purpose: "Early stopping for futility or efficacy"
    methods: "Group sequential (O'Brien-Fleming, Pocock boundaries)"
    alpha_spending: "Lan-DeMets alpha spending functions"
```

#### **Statistical Methods with Validation**
```yaml
primary_analysis:
  two_sample_t_test:
    assumptions:
      normality: "Central limit theorem for large n (≥30 per group)"
      equal_variances: "Welch's correction if Levene test p < 0.05"
      independence: "Proper randomization procedure"
      
    effect_size_reporting:
      cohens_d: "d = (x̄₁ - x̄₂) / s_pooled"
      confidence_interval: "Hedges & Olkin (1985) bias correction"
      practical_significance: "Compare to minimum meaningful difference"
  
  chi_square_test:
    application: "Categorical outcomes (conversion rates, etc.)"
    assumptions:
      expected_frequency: "≥5 in each cell"
      independence: "Proper randomization"
      
    effect_size_measures:
      odds_ratio: "OR = (a×d)/(b×c) for 2×2 tables"
      phi_coefficient: "φ = √(χ²/n) for 2×2 tables"
      cramers_v: "V = √(χ²/[n×min(r-1,c-1)]) for larger tables"

regression_analysis:
  when_appropriate: "Control for baseline covariates"
  model_specification: "Y = β₀ + β₁×treatment + β₂×covariate + ε"
  
  advantages:
    precision_improvement: "Reduced residual variance"
    bias_reduction: "Control for chance imbalances"
    subgroup_analysis: "Interaction terms for heterogeneity"
    
  reporting_requirements:
    adjusted_treatment_effect: "β₁ with 95% CI"
    covariate_effects: "Report all β coefficients"
    model_diagnostics: "Residual plots, R², leverage analysis"

bayesian_analysis:
  when_appropriate: "Prior information available, decision-theoretic framework"
  prior_specification:
    non_informative: "Jeffreys or reference priors"
    informative: "Based on historical data or expert opinion"
    sensitivity_analysis: "Multiple priors to test robustness"
    
  inference_methods:
    credible_intervals: "95% highest posterior density intervals"
    posterior_probability: "P(treatment effect > threshold | data)"
    bayes_factors: "Evidence for/against null hypothesis"
```

#### **Multiple Testing Corrections**
```yaml
family_wise_error_rate:
  bonferroni_correction:
    formula: "α_adjusted = α / k"
    application: "Conservative, suitable for small k"
    reference: "Dunn (1961), Multiple comparisons procedures"
    
  holm_bonferroni:
    procedure: "Step-down method starting with smallest p-value"
    advantage: "More powerful than Bonferroni"
    implementation: "p.adjust(method='holm') in R"
    
false_discovery_rate:
  benjamini_hochberg:
    formula: "Critical value = (i/k) × α"
    application: "Large number of tests, exploratory research"
    reference: "Benjamini & Hochberg (1995)"
    
  q_value_method:
    advantage: "Estimates proportion of false discoveries"
    implementation: "qvalue package in R"
    interpretation: "q < 0.05 means ≤5% FDR"
```

---

## ⚡ Experiment Type 5: Single Sample Rating

### **Academic Foundation**

#### **Psychometric Theory**
```yaml
measurement_theory: "Classical Test Theory (Gulliksen, 1950)"
scale_development: "DeVellis Scale Development (DeVellis, 2017)"
response_bias_theory: "Social Desirability and Response Sets (Paulhus, 1991)"

established_frameworks:
  - "Mean Opinion Score Methodology (ITU-T P.800)"
  - "Likert Scale Construction (Likert, 1932)"
  - "Semantic Differential Technique (Osgood et al., 1957)"
  - "Visual Analog Scales in Research (Wewers & Lowe, 1990)"
  
validation_literature:
  - "Scale Reliability and Validity (Nunnally & Bernstein, 1994)"
  - "Response Scale Selection in Research (Krosnick & Fabrigar, 1997)"
  - "Cross-cultural Scale Validation (Byrne, 2010)"
```

#### **Scale Design Principles**
```yaml
scale_type_selection:
  likert_scales:
    optimal_points: "5-7 points for reliability-validity balance"
    labeling: "All points labeled vs. endpoints only"
    neutral_option: "Include middle category vs. force choice"
    
  visual_analog_scales:
    advantages: "Continuous measurement, no response clustering"
    disadvantages: "Difficult on mobile devices, cultural differences"
    implementation: "0-100mm line with end anchors"
    
  semantic_differential:
    application: "Attitude measurement, concept evaluation"
    format: "Bipolar adjective pairs with 7-point scales"
    analysis: "Factor analysis for dimension identification"

response_bias_control:
  acquiescence_bias:
    definition: "Tendency to agree regardless of content"
    control: "Reverse-coded items, balanced keying"
    detection: "Factor analysis of positively/negatively worded items"
    
  extreme_response_bias:
    definition: "Overuse of scale endpoints"
    control: "Forced ranking, ipsative scaling"
    detection: "Standard deviation of responses within person"
    
  social_desirability:
    definition: "Responding in socially acceptable manner"
    control: "Anonymous responding, indirect questioning"
    measurement: "Marlowe-Crowne Social Desirability Scale"
```

#### **Statistical Analysis Methods**
```yaml
descriptive_statistics:
  central_tendency:
    mean: "Appropriate for interval/ratio scales"
    median: "Robust to outliers, ordinal scales"
    mode: "Most frequent response, all scales"
    
  variability_measures:
    standard_deviation: "For interval/ratio scales"
    interquartile_range: "For ordinal scales"
    frequency_distributions: "Response pattern analysis"
    
  normality_assessment:
    graphical: "Histograms, Q-Q plots, box plots"
    statistical: "Shapiro-Wilk, Kolmogorov-Smirnov tests"
    transformation: "Log, square root, Box-Cox if needed"

reliability_analysis:
  internal_consistency:
    cronbachs_alpha: "α ≥ 0.70 for research, ≥ 0.90 for clinical decisions"
    mcdonalds_omega: "More robust to tau-equivalence violations"
    split_half_reliability: "Spearman-Brown prophecy formula"
    
  test_retest_reliability:
    correlation_coefficient: "r ≥ 0.70 for acceptable stability"
    time_interval: "2-4 weeks optimal for most constructs"
    systematic_change: "Paired t-test for mean differences"
    
  inter_rater_reliability:
    intraclass_correlation: "ICC(2,1) for consistency, ICC(2,k) for averages"
    kappa_coefficient: "For categorical ratings"
    limits_of_agreement: "Bland-Altman plots for continuous measures"

validity_assessment:
  content_validity:
    expert_review: "Subject matter experts evaluate relevance"
    content_validity_ratio: "CVR = (Ne - N/2) / (N/2)"
    cognitive_interviews: "Think-aloud protocols during responding"
    
  construct_validity:
    factor_analysis: "Exploratory (EFA) then confirmatory (CFA)"
    convergent_validity: "Correlations with related measures (r > 0.50)"
    discriminant_validity: "Low correlations with unrelated measures (r < 0.30)"
    
  criterion_validity:
    concurrent_validity: "Correlation with established gold standard"
    predictive_validity: "Ability to predict future outcomes"
    incremental_validity: "Additional prediction beyond existing measures"
```

#### **Sample Size Requirements**
```yaml
reliability_estimation:
  cronbachs_alpha:
    minimum: "n ≥ 100 for stable estimates"
    recommended: "n ≥ 200 for precise confidence intervals"
    rule_of_thumb: "n ≥ 10 × number of items"
    
  test_retest_reliability:
    correlation_estimation: "n ≥ 84 for r = 0.70 with 80% power"
    confidence_intervals: "n ≥ 100 for reasonably narrow CIs"

factor_analysis:
  exploratory_fa:
    minimum_ratio: "5:1 participants to items"
    preferred_ratio: "10:1 or 20:1 for stable solutions"
    absolute_minimum: "n ≥ 100 regardless of item number"
    
  confirmatory_fa:
    simple_models: "n ≥ 100 for models with few factors"
    complex_models: "n ≥ 200-400 for adequate fit assessment"
    bootstrap_requirements: "n ≥ 500 for bootstrap confidence intervals"

mean_comparisons:
  one_sample_t_test:
    small_effect: "n ≥ 84 for d = 0.3 with 80% power"
    medium_effect: "n ≥ 34 for d = 0.5 with 80% power"
    large_effect: "n ≥ 15 for d = 0.8 with 80% power"
    
  confidence_intervals:
    narrow_ci: "n ≥ 100 for CI width ≤ 0.4×SD"
    precision_requirement: "Calculate based on desired CI width"
```

---

## 🔬 Experiment Type 6: Threshold Detection

### **Academic Foundation**

#### **Psychophysical Theory**
```yaml
classical_psychophysics: "Fechner's Elements of Psychophysics (Fechner, 1860)"
signal_detection_theory: "Green & Swets Signal Detection Theory (1966)"
adaptive_methods: "Levitt Transformed Up-Down Methods (Levitt, 1971)"

modern_frameworks:
  - "Psychometric Function Fitting (Wichmann & Hill, 2001)"
  - "Adaptive Psychophysical Procedures (Leek, 2001)"
  - "Bayesian Adaptive Estimation (Kontsevich & Tyler, 1999)"
  - "Maximum Likelihood Difference Scaling (Maloney & Yang, 2003)"
  
validation_studies:
  - "Comparison of Threshold Estimation Methods (García-Pérez, 1998)"
  - "Reliability of Psychophysical Measurements (Klein, 2001)"
  - "Just Noticeable Difference Methodology (Gescheider, 1997)"
```

#### **Threshold Measurement Methods**
```yaml
method_of_limits:
  procedure: "Present stimuli in ascending/descending series"
  threshold_estimation: "Average of reversal points"
  
  advantages:
    - "Simple to implement and understand"
    - "Quick measurements for screening"
    - "Good for preliminary threshold estimates"
    
  limitations:
    - "Subject to habituation and expectation errors"
    - "Response bias affects measurements"
    - "Less precise than adaptive methods"
    
  analysis:
    threshold_calculation: "50% point from psychometric function"
    reliability: "Test-retest correlation across sessions"
    bias_correction: "Counterbalance ascending/descending orders"

method_of_constant_stimuli:
  procedure: "Present fixed set of stimuli in random order"
  threshold_estimation: "Fit psychometric function, find 50% point"
  
  advantages:
    - "Most accurate and reliable method"
    - "Complete psychometric function obtained"
    - "Unbiased by sequential dependencies"
    
  stimulus_selection:
    range: "Cover 10-90% detection probability"
    spacing: "Log spacing for most sensory dimensions"
    repetitions: "≥20 trials per stimulus level"
    
  psychometric_function_fitting:
    function_form: "Cumulative Gaussian or logistic"
    parameters: "Threshold (μ) and slope (σ)"
    goodness_of_fit: "Chi-square test, deviance analysis"
    confidence_intervals: "Bootstrap or likelihood-based methods"

adaptive_methods:
  simple_up_down:
    rule: "Increase after incorrect, decrease after correct"
    convergence: "Converges to 50% correct point"
    step_size: "Fixed or decreasing geometric progression"
    
  weighted_up_down:
    rule: "Different step sizes for up vs down movements"
    target_percentage: "Can converge to any specified percentage"
    levitt_rules: "2-down-1-up for 70.7%, 3-down-1-up for 79.4%"
    
  staircase_analysis:
    threshold_estimation: "Average of reversal points (skip first few)"
    standard_error: "Standard deviation of reversals / √n"
    stopping_criteria: "Fixed number of reversals or trials"
```

#### **Statistical Analysis Framework**
```yaml
psychometric_function_analysis:
  model_fitting:
    maximum_likelihood: "Fit psychometric function to proportion data"
    least_squares: "Alternative when assumptions met"
    robust_methods: "When outliers present"
    
  function_forms:
    logistic: "F(x) = 1 / (1 + exp(-(x-μ)/σ))"
    cumulative_gaussian: "F(x) = Φ((x-μ)/σ)"
    weibull: "F(x) = 1 - exp(-((x/α)^β))"
    
  parameter_interpretation:
    threshold: "50% detection point (μ parameter)"
    slope: "Steepness of psychometric function (1/σ)"
    lapse_rate: "Upper asymptote < 1.0 for inattention"
    guess_rate: "Lower asymptote > 0.0 for forced choice"
    
  goodness_of_fit:
    deviance_test: "Compare fitted model to saturated model"
    chi_square_test: "Binomial probability model test"
    residual_analysis: "Standardized residuals vs. stimulus level"

threshold_reliability:
  test_retest_reliability:
    correlation: "Pearson r between threshold estimates"
    coefficient_of_repeatability: "1.96 × SD of differences"
    bland_altman_analysis: "Plot differences vs. means"
    
  internal_consistency:
    split_half_reliability: "Odd vs. even trials correlation"
    spearman_brown_correction: "Adjust for reduced trial number"
    
  measurement_error:
    standard_error_measurement: "SEM = SD × √(1-reliability)"
    confidence_intervals: "Threshold ± 1.96 × SEM"
    minimal_detectable_change: "MDC = SEM × 1.96 × √2"

change_detection_analysis:
  difference_thresholds:
    just_noticeable_difference: "Smallest detectable change"
    weber_fraction: "ΔI/I for intensity discrimination"
    difference_limen: "75% correct point in 2AFC tasks"
    
  statistical_comparison:
    paired_t_test: "Compare thresholds before/after manipulation"
    effect_size: "Cohen's d for magnitude of threshold change"
    power_analysis: "Sample size for detecting threshold shifts"
    
  clinical_significance:
    minimal_important_difference: "Smallest change that matters"
    reliable_change_index: "RCI = (X₂ - X₁) / SEM_diff"
    normative_comparisons: "Compare to healthy population norms"
```

#### **Sample Size and Power Considerations**
```yaml
threshold_estimation_precision:
  method_of_constant_stimuli:
    minimum_trials: "20 trials per stimulus level"
    typical_levels: "5-7 stimulus levels"
    total_trials: "100-140 trials per threshold estimate"
    
  adaptive_methods:
    minimum_reversals: "6-8 reversals for stable threshold"
    typical_trials: "50-80 trials per threshold estimate"
    multiple_tracks: "2-3 interleaved tracks for reliability"

reliability_studies:
  test_retest_design:
    minimum_participants: "n ≥ 20 for correlation estimates"
    preferred_sample: "n ≥ 50 for stable reliability coefficients"
    session_separation: "1-7 days optimal interval"
    
  internal_consistency:
    split_half_analysis: "Minimum 40 trials for stable estimates"
    odd_even_reliability: "≥60 trials recommended"

group_comparisons:
  between_subjects:
    small_effect: "n ≥ 64 per group for d = 0.5"
    medium_effect: "n ≥ 26 per group for d = 0.8"
    large_effect: "n ≥ 15 per group for d = 1.2"
    
  within_subjects:
    small_effect: "n ≥ 34 for d = 0.5"
    medium_effect: "n ≥ 15 for d = 0.8"
    large_effect: "n ≥ 9 for d = 1.2"
    
  power_analysis_considerations:
    threshold_variability: "Use pilot data or literature estimates"
    measurement_error: "Account for threshold estimation error"
    correlation_structure: "For repeated measures designs"
```

---

## 📋 Academic Validation Summary

### **Peer Review Requirements**
```yaml
methodology_review:
  required_expertise:
    - "Experimental psychology (PhD level)"
    - "Statistics/psychometrics (PhD level)"  
    - "Domain-specific knowledge (TTS, UI, audio, etc.)"
    
  validation_tasks:
    - "Review statistical power calculations"
    - "Validate experimental design choices"
    - "Approve effect size interpretations"
    - "Confirm assumption testing procedures"

literature_foundation:
  primary_sources: "Peer-reviewed methodology papers"
  textbook_references: "Established statistical textbooks"
  standards_compliance: "ITU, ISO, APA guidelines"
  recent_developments: "Last 10 years of methodological advances"

expert_consultation:
  advisory_board: "3-5 experts per domain area"
  regular_review: "Annual methodology updates"
  conflict_resolution: "Multiple expert opinion synthesis"
  quality_assurance: "Systematic validation protocols"
```

### **Implementation Safeguards**
```yaml
agent_limitations:
  acknowledge_uncertainty: "Clear boundaries of automated advice"
  expert_escalation: "When to require human consultation"
  methodology_updates: "Continuous learning from new research"
  error_detection: "Systematic validation of recommendations"

quality_control:
  peer_review_integration: "All recommendations pre-validated"
  usage_monitoring: "Track accuracy of agent suggestions"
  feedback_incorporation: "Learn from user corrections"
  periodic_audits: "Regular methodology reviews"
```

---

*Academic Foundations Document Version: 1.0*  
*Requires Expert Validation Before Agent Implementation*  
*Complete Peer Review Process Essential*