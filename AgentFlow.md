# Agent Flow for QA System Construction

## 🧠 Core Patterns from TTS QA Case Study

Based on the successful TTS emotion scale evaluation system, this document outlines the systematic approach an AI agent should follow when constructing new QA experiments.

---

## 📋 Pattern 1: Reference-Target Comparison Logic

### **Critical Questions to Ask**
```yaml
reference_analysis:
  primary_questions:
    - "What should serve as the neutral baseline for comparison?"
    - "How do we match each target to its appropriate reference?"
    - "Are multiple references needed per target?"
    - "What logic determines reference selection?"
  
  shared_vs_different:
    - "What information is identical between reference and target?"
    - "What variables change between reference and target?"
    - "How should shared information be displayed to avoid redundancy?"
```

### **TTS QA Case Example**
```typescript
// Reference Logic Pattern
reference_matching: {
  shared_variables: ["voice_id", "text_type", "emotion_value"],
  different_variables: ["emotion_scale", "processing_method"],
  matching_formula: "${voice_id}_${text_type}_reference_${emotion_value}.wav",
  
  display_strategy: {
    shared_content: "Text displayed once above both players",
    reference_specific: "Neutral baseline (style_label='normal-1')",
    target_specific: "Emotional version (scale: ${scale})"
  }
}
```

### **Agent Prompts for Reference Analysis**

**Prompt 1: Reference Identification**
```
You are helping a researcher design a comparison experiment. 

TASK: Identify the appropriate reference baseline.

Questions to explore:
1. "In your experiment, what represents the 'neutral' or 'baseline' condition?"
2. "Should every test sample have its own unique reference, or can references be shared?"
3. "What variables should remain constant between reference and target?"
4. "What specific variable(s) are you testing by changing from reference to target?"

Example: If testing TTS emotion scales, the reference might be "same voice, same text, but no emotion applied"

Please describe your baseline condition:
```

**Prompt 2: Matching Logic**
```
Now let's define how to match targets with their references.

TASK: Create the reference matching logic.

Based on your variables:
- Shared variables: [voice, text, emotion_type]
- Test variable: [emotion_scale] 
- Reference condition: [no_emotion_applied]

Questions:
1. "Does each target need a unique reference file/sample?"
2. "What naming or identification system will link targets to references?"
3. "Are there any combinations where a reference doesn't exist?"

Provide your matching formula:
Pattern: ${shared_var1}_${shared_var2}_reference_${identifier}
```

---

## 📊 Pattern 2: Variable Matrix Analysis

### **Systematic Variable Assessment**

**Agent Prompts for Variable Analysis**

**Prompt 1: Variable Discovery**
```
Let's map out all the variables in your experiment systematically.

TASK: Complete variable inventory

1. INDEPENDENT VARIABLES (what you're testing):
   - Primary variable: [e.g., emotion_scale: 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
   - Secondary variables: [e.g., emotion_type: label vs vector]

2. CONTROL VARIABLES (kept constant):
   - [e.g., voice_id: v001, v002]
   - [e.g., text_type: match, neutral, opposite]

3. CONTEXTUAL VARIABLES (experimental conditions):
   - [e.g., processing_type: standard vs enhanced]

Please list all your variables and their possible values:
```

**Prompt 2: Combination Mathematics**
```
Now let's calculate your experimental scope.

CURRENT VARIABLES:
${list_of_variables_with_counts}

CALCULATION:
Total combinations = ${var1_count} × ${var2_count} × ${var3_count} × ...
Reference samples needed = ${calculation_for_references}
Target samples needed = ${calculation_for_targets}

REALITY CHECK:
1. Total samples: ${total_number}
2. Is this realistic for your timeline/budget?
3. Can humans realistically evaluate this many samples?
4. Do you need all combinations or can we use strategic sampling?

Should we reduce scope or use sampling strategies?
```

### **TTS QA Case Pattern**
```yaml
variable_matrix:
  independent_variables:
    emotion_scale: [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]  # 6 options
    emotion_type: ["label", "vector"]                # 2 options
  
  control_variables:
    voice_id: ["v001", "v002"]                      # 2 options
    text_type: ["match", "neutral", "opposite"]     # 3 options
    emotions: ["angry", "sad", "happy", ...]        # 12 options
  
  contextual_variables:
    expressivity: ["none", "0.6"]                   # 2 options
  
  total_combinations: 2×12×3×6×2×2 = 1,728 possible
  actual_generated: 1,008 files (strategic reduction)
  per_session_sample: 25 (cognitive load consideration)
```

---

## 🎯 Pattern 3: Credibility and Sampling Strategy

### **Research Purpose Classification**

**Agent Prompts for Research Purpose**

**Prompt 1: Purpose and Credibility Requirements**
```
Let's understand your research goals and credibility needs.

TASK: Define research purpose and standards

1. RESEARCH PURPOSE:
   □ Academic publication (high statistical rigor)
   □ Product decision support (practical insights) 
   □ Internal validation (quick feedback)
   □ User experience research (behavioral patterns)

2. DECISION IMPACT:
   - "What decisions will be made based on these results?"
   - "What level of confidence do you need?"
   - "Is this exploratory or confirmatory research?"

3. CREDIBILITY TOLERANCE:
   - "Can you accept directional insights over statistical significance?"
   - "Would 70% confidence be sufficient for your decisions?"
   - "Do you need to defend these results to external stakeholders?"

Your purpose: ___________
Credibility needs: ___________
```

**Prompt 2: Sampling Strategy**
```
Based on your purpose, let's design the sampling strategy.

PURPOSE: ${research_purpose}
TOTAL COMBINATIONS: ${total_combinations}
REALISTIC CONSTRAINTS: ${budget_time_participants}

SAMPLING OPTIONS:

1. RANDOM SAMPLING (current TTS QA approach):
   - Sample size: ${suggested_sample_size}
   - Per participant: ${per_session_samples} 
   - Statistical confidence: ~${confidence_percentage}%
   - Pros: Unbiased, statistically valid
   - Cons: Might miss edge cases

2. STRATIFIED SAMPLING:
   - Ensure coverage of all key variable combinations
   - Pros: Comprehensive coverage
   - Cons: Larger sample needed

3. FOCUSED SAMPLING:
   - Target specific combinations of interest
   - Pros: Efficient, targeted insights
   - Cons: Limited generalizability

Which approach fits your needs?
```

### **TTS QA Case Example**
```yaml
research_purpose: "Product decision support for emotion scale ranges"
specific_goal: "Identify at what scale values emotional expression fails"
credibility_approach: "Accept practical insights over perfect statistical rigor"

sampling_strategy:
  method: "random_sampling"
  total_combinations: 1008
  per_session_samples: 25
  cognitive_justification: "Prevent evaluator fatigue and maintain quality"
  coverage_strategy: "Random ensures unbiased representation across all variable combinations"
  
decision_criteria:
  success_metric: "Identify specific scale thresholds where quality degrades"
  failure_detection: "Find actor_id + emotion combinations where even low scales fail"
  actionable_outcome: "Set appropriate scale ranges for production UI"
```

---

## 🔄 Complete Agent Flow

### **Phase 1: Research Purpose Discovery**

**Initial Conversation Prompt**
```
Hello! I'm here to help you design a quality assessment experiment.

Let's start with the big picture:

1. WHAT are you evaluating? 
   (e.g., "TTS voice quality", "UI designs", "audio compression")

2. WHY are you doing this evaluation?
   (e.g., "decide which TTS system to use", "optimize emotion expression parameters")

3. WHO will use these results?
   (e.g., "product team", "academic publication", "internal validation")

4. WHEN do you need results?
   (this affects our sampling strategy)

Please describe your evaluation goals:
```

### **Phase 2: Variable Structure Analysis**

**Reference-Target Analysis Prompt**
```
Based on your description, I see you need to compare different conditions.

Let's structure this properly:

1. REFERENCE (baseline): What represents your "neutral" or "control" condition?

2. TARGETS (test conditions): What variations are you testing against the baseline?

3. SHARED ELEMENTS: What stays the same between reference and target?
   (This helps us avoid redundant information in the UI)

For example, in TTS evaluation:
- Reference: Same voice, same text, no emotion
- Target: Same voice, same text, WITH emotion at different scales  
- Shared: Text content (show once), voice identity
- Different: Emotion processing (show separately)

Describe your reference-target structure:
```

**Variable Matrix Prompt**
```
Now let's map all your variables systematically:

TEMPLATE TO FILL:
```yaml
variables:
  primary_test_variable:
    name: "what you're primarily testing"
    values: ["option1", "option2", "option3"]
    
  secondary_variables:
    - name: "additional factor 1"
      values: ["a", "b"] 
    - name: "additional factor 2"
      values: ["x", "y", "z"]
      
  control_variables:
    - name: "kept constant"
      values: ["fixed_value"]
```

CALCULATION CHECK:
- Total combinations: ${auto_calculated}
- Realistic for evaluation? ${yes_no_analysis}
- Recommended approach: ${sampling_strategy}

Fill in your variables:
```

### **Phase 3: Sampling and Credibility Design**

**Sampling Strategy Prompt**
```
Based on your ${total_combinations} possible combinations:

EVALUATION CONSTRAINTS:
1. How many people can participate? ____
2. How long can each session be? ____ minutes
3. When do you need results? ____
4. Budget/resource constraints? ____

CREDIBILITY REQUIREMENTS:
□ Need statistical significance for publication
□ Need directional insights for product decisions  
□ Need quick validation for internal use
□ Need comprehensive coverage of edge cases

RECOMMENDED APPROACH:
Based on your inputs: ${recommended_sampling_method}
- Sample size: ${recommended_sample_size}
- Per person: ${recommended_per_session}
- Expected confidence: ${confidence_level}
- Timeline: ${estimated_timeline}

Does this approach work for your needs?
```

### **Phase 4: UI and Experience Design**

**Interface Design Prompt**
```
Let's design the evaluation experience:

DISPLAY STRATEGY:
Based on your reference-target setup:

1. SHARED INFORMATION:
   - What: ${shared_elements}
   - Display: Single section above comparison
   - Style: ${suggested_styling}

2. REFERENCE SECTION:
   - Title: "${reference_title}"
   - Color theme: Blue (neutral/baseline)
   - Content: ${reference_specific_info}

3. TARGET SECTION:  
   - Title: "${target_title_template}"
   - Color theme: Orange (test condition)
   - Content: ${target_specific_info}

4. EVALUATION FORM:
   - Dimensions: ${evaluation_dimensions}
   - Scale: ${scale_type_and_range}
   - Required fields: ${required_vs_optional}

Does this layout work for your experiment?
```

### **Phase 5: Implementation and Validation**

**System Generation Prompt**
```
Perfect! I'll now generate your custom QA system with:

CONFIGURATION SUMMARY:
- Purpose: ${research_purpose}
- Method: ${reference_target_or_other}
- Variables: ${variable_summary}
- Sampling: ${sampling_approach}
- UI Theme: ${color_scheme_and_layout}
- Sample size: ${total_samples}
- Per session: ${per_session_samples}

GENERATED COMPONENTS:
□ Custom AudioPlayer/MediaPlayer with your color scheme
□ Dynamic evaluation form with your dimensions
□ Sample management system with your matching logic
□ Database schema optimized for your variables
□ Analytics dashboard for your specific metrics

NEXT STEPS:
1. Review generated code
2. Test with pilot data
3. Adjust based on feedback  
4. Deploy for full study

Shall I proceed with generation?
```

---

## 🎭 Example Conversation Flow

### **TTS Emotion Scale Case Reconstruction**

**Agent**: Hello! What are you evaluating?

**Researcher**: "I want to test TTS emotion expression at different scale levels to decide what scale ranges to offer users."

**Agent**: I see you're testing TTS emotion scales for product decisions. Let's structure this:

1. **Reference**: What's your baseline? 
**Researcher**: "Same voice and text, but no emotion applied - just neutral speech."

2. **Targets**: What variations are you testing?
**Researcher**: "Same voice and text, but with emotions at different intensity scales like 0.5, 1.0, 1.5, up to 3.0."

**Agent**: Perfect! So your shared element is the text content - we can display that once above both audio players. Now, let's map your variables:

**Variables Identified:**
```yaml
primary_test_variable: 
  emotion_scale: [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
  
secondary_variables:
  emotion_type: [label_based, vector_based]
  emotion_value: [angry, sad, happy, whisper, toneup, tonedown, excited, furious, terrified, fear, surprise, excitement]
  
control_variables:
  voice_id: [v001, v002]
  text_type: [match, neutral, opposite]
  
contextual_variables:
  expressivity: [none, enhanced_0.6]
```

**Total combinations**: 2×12×3×6×2×2 = 1,728

**Agent**: That's a lot! For product decisions, do you need to test every combination, or can we use random sampling?

**Researcher**: "Random sampling is fine. I need to catch any specific combinations where scaling fails, even at low levels."

**Agent**: Excellent approach! I recommend:
- **Total sample pool**: 1,008 strategically selected combinations
- **Per session**: 25 samples (prevents cognitive overload)
- **Expected insight**: Identify problematic scale thresholds across all variable combinations

**UI Design**: 
- Shared text at top
- Blue reference player (neutral baseline)  
- Orange target player (with emotion scale)
- 3-dimension evaluation form

**Agent**: Shall I generate this system for you?

**Researcher**: "Yes, and make sure the reference matching works properly!"

**Agent**: *Generates complete TTS QA system with proper reference logic*

---

## 🎯 Key Agent Principles

### **1. Purpose-First Approach**
- Always start with research goals, not technical details
- Adapt credibility requirements to actual decision needs
- Embrace practical insights over perfect statistical rigor when appropriate

### **2. Systematic Variable Analysis**
- Map all variables before designing samples
- Calculate realistic scope constraints
- Offer sampling strategies based on purpose

### **3. Cognitive Load Awareness**
- Consider human evaluation limits
- Design sessions for sustained attention
- Balance comprehensiveness with quality

### **4. Reference Logic Priority**
- Establish matching logic early
- Ensure shared vs. different information is clear
- Validate reference availability across all conditions

### **5. Flexible Implementation**
- Generate code that matches research purpose
- Allow iteration based on pilot testing
- Support both rigorous and pragmatic approaches

---

*Agent Flow Version: 1.0*  
*Based on: Successful TTS QA System Pattern*  
*Focus: Product Decision Support Research*