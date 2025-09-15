import matplotlib.pyplot as plt
import numpy as np

# Data from analysis
scales = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
none_emotion = [3.77, 4.56, 4.52, 3.72, 3.41, 4.00]
none_quality = [4.59, 4.54, 4.14, 3.69, 3.54, 3.96]
six_emotion = [3.81, 4.69, 4.40, 4.83, 4.20, 4.36]
six_quality = [4.56, 4.11, 4.31, 4.03, 3.83, 3.84]

# Create figure
fig, axes = plt.subplots(1, 3, figsize=(20, 6))
fig.suptitle('TTS Emotion Expression Analysis: Finding Meaningful Scale Ranges\n491 Evaluations', fontsize=16, fontweight='bold')

# Plot 1: Emotion Expression vs Scale
ax1 = axes[0]
ax1.plot(scales, none_emotion, 'o-', linewidth=3, markersize=10, label='Standard (none)', color='#1f77b4')
ax1.plot(scales, six_emotion, 's-', linewidth=3, markersize=10, label='Enhanced (0.6)', color='#ff7f0e')

# Mark peak points
none_peak_idx = np.argmax(none_emotion)
six_peak_idx = np.argmax(six_emotion)
ax1.scatter(scales[none_peak_idx], none_emotion[none_peak_idx], s=200, color='blue', marker='*', zorder=10)
ax1.scatter(scales[six_peak_idx], six_emotion[six_peak_idx], s=200, color='orange', marker='*', zorder=10)

# Add peak annotations
ax1.annotate(f'Peak: {none_emotion[none_peak_idx]:.2f}\nat scale {scales[none_peak_idx]:.1f}', 
            xy=(scales[none_peak_idx], none_emotion[none_peak_idx]), 
            xytext=(scales[none_peak_idx]-0.3, none_emotion[none_peak_idx]+0.3),
            arrowprops=dict(arrowstyle='->', color='blue', lw=2),
            fontsize=10, color='blue', fontweight='bold')

ax1.annotate(f'Peak: {six_emotion[six_peak_idx]:.2f}\nat scale {scales[six_peak_idx]:.1f}', 
            xy=(scales[six_peak_idx], six_emotion[six_peak_idx]), 
            xytext=(scales[six_peak_idx]+0.2, six_emotion[six_peak_idx]+0.3),
            arrowprops=dict(arrowstyle='->', color='orange', lw=2),
            fontsize=10, color='orange', fontweight='bold')

# Mark meaningful range
ax1.axvspan(1.0, 2.0, alpha=0.2, color='green', label='Meaningful range')
ax1.axhline(y=4.0, color='red', linestyle='--', alpha=0.7, label='Midpoint (4.0)')

ax1.set_xlabel('Emotion Scale', fontsize=12)
ax1.set_ylabel('Emotion Expression Score (1-7)', fontsize=12)
ax1.set_title('Emotion Expression vs Scale', fontsize=13, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_ylim(3.0, 5.5)

# Plot 2: Emotion Improvement Rate
ax2 = axes[1]

# Calculate improvement rates
none_improvements = []
six_improvements = []
scale_midpoints = []

for i in range(1, len(scales)):
    none_rate = (none_emotion[i] - none_emotion[i-1]) / (scales[i] - scales[i-1])
    six_rate = (six_emotion[i] - six_emotion[i-1]) / (scales[i] - scales[i-1])
    none_improvements.append(none_rate)
    six_improvements.append(six_rate)
    scale_midpoints.append((scales[i] + scales[i-1]) / 2)

x_pos = np.arange(len(scale_midpoints))
width = 0.35

bars1 = ax2.bar(x_pos - width/2, none_improvements, width, label='Standard (none)', color='#1f77b4', alpha=0.7)
bars2 = ax2.bar(x_pos + width/2, six_improvements, width, label='Enhanced (0.6)', color='#ff7f0e', alpha=0.7)

# Color bars based on improvement level
for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
    # Green for good improvement (>0.5), red for decline (<-0.5), gray otherwise
    if none_improvements[i] > 0.5:
        bar1.set_color('#2ca02c')
    elif none_improvements[i] < -0.5:
        bar1.set_color('#d62728')
    
    if six_improvements[i] > 0.5:
        bar2.set_color('#2ca02c')
    elif six_improvements[i] < -0.5:
        bar2.set_color('#d62728')

ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax2.axhline(y=0.1, color='green', linestyle='--', alpha=0.7, label='Meaningful threshold')
ax2.axhline(y=-0.5, color='red', linestyle='--', alpha=0.7, label='Decline threshold')

ax2.set_xlabel('Scale Range', fontsize=12)
ax2.set_ylabel('Emotion Change per Scale Unit', fontsize=12)
ax2.set_title('Emotion Improvement Rate\nWhere Scaling Becomes Meaningless', fontsize=13, fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels([f'{scales[i]:.1f}→{scales[i+1]:.1f}' for i in range(len(scale_midpoints))])
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

# Plot 3: Expressivity 0.6 Advantage
ax3 = axes[2]

emotion_diffs = [s - n for s, n in zip(six_emotion, none_emotion)]
quality_diffs = [s - n for s, n in zip(six_quality, none_quality)]

bars1 = ax3.bar([s-0.1 for s in scales], emotion_diffs, 0.2, label='Emotion Advantage', color='purple', alpha=0.7)
bars2 = ax3.bar([s+0.1 for s in scales], quality_diffs, 0.2, label='Quality Advantage', color='green', alpha=0.7)

# Color bars based on advantage level
for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
    if emotion_diffs[i] > 0.2:
        bar1.set_color('#8e44ad')  # Strong purple for emotion advantage
    elif emotion_diffs[i] < -0.2:
        bar1.set_color('#e74c3c')  # Red for disadvantage
    else:
        bar1.set_color('#95a5a6')  # Gray for neutral
        
    if quality_diffs[i] > 0.2:
        bar2.set_color('#27ae60')  # Strong green for quality advantage
    elif quality_diffs[i] < -0.2:
        bar2.set_color('#e74c3c')  # Red for disadvantage
    else:
        bar2.set_color('#95a5a6')  # Gray for neutral

# Highlight the clear advantage zone
ax3.axvspan(1.8, 3.2, alpha=0.15, color='gold', label='0.6 advantage zone')

ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax3.axhline(y=0.2, color='green', linestyle='--', alpha=0.7, label='Significant advantage')
ax3.axhline(y=-0.2, color='red', linestyle='--', alpha=0.7, label='Significant disadvantage')

ax3.set_xlabel('Emotion Scale', fontsize=12)
ax3.set_ylabel('Score Difference (0.6 - none)', fontsize=12)
ax3.set_title('Expressivity 0.6 Advantage Analysis\nWhen 0.6 Becomes Superior', fontsize=13, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)
ax3.set_xticks(scales)

# Add key insights text box
textstr = '''KEY FINDINGS:
• Standard peaks at scale 1.0 (4.56 emotion score)
• Enhanced (0.6) peaks at scale 2.0 (4.83 emotion score)
• 0.6 shows clear advantage at scales 2.0+ 
• Meaningful scaling range: 1.0-2.0
• Beyond 2.0: Quality decline outweighs emotion gain'''

props = dict(boxstyle='round', facecolor='lightblue', alpha=0.8)
fig.text(0.02, 0.02, textstr, fontsize=11, verticalalignment='bottom', bbox=props)

plt.tight_layout()
plt.subplots_adjust(bottom=0.15)  # Make room for text box

plt.savefig('/Users/bagsanghui/ssfm30_qa/analysis/emotion_expressivity_analysis.png', 
           dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("📊 Emotion expressivity analysis saved: emotion_expressivity_analysis.png")
print("\n🎯 ANSWER TO YOUR QUESTION:")
print("="*60)
print("MEANINGFUL SCALE RANGES:")
print("  • Standard (none): Peaks at 1.0, plateaus after 1.0")
print("  • Enhanced (0.6): Peaks at 2.0, meaningful up to 2.0") 
print("  • 0.6 ADVANTAGE: Emerges strongly at scales 2.0+")
print("  • RECOMMENDATION: Use 0.6 with scales 1.0-2.0 for best trade-off")