import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Data from analysis
scales = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
none_quality = [4.59, 4.54, 4.14, 3.69, 3.54, 3.96]
none_similarity = [4.90, 5.02, 4.20, 4.17, 3.44, 3.54]
six_quality = [4.56, 4.11, 4.31, 4.03, 3.83, 3.84]
six_similarity = [4.78, 4.89, 5.29, 4.71, 4.57, 4.52]

# Create summary figure
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('TTS Emotion Scaling: Quality vs Intensity Trade-off Analysis\n491 Evaluations from 25 Sessions', fontsize=14, fontweight='bold')

# Quality comparison
ax1 = axes[0]
ax1.plot(scales, none_quality, 'o-', linewidth=3, markersize=8, label='Standard (none)', color='#1f77b4')
ax1.plot(scales, six_quality, 's-', linewidth=3, markersize=8, label='Enhanced (0.6)', color='#ff7f0e') 
ax1.axhline(y=4.0, color='red', linestyle='--', linewidth=2, label='Acceptable threshold')
ax1.fill_between([1.5, 2.0], 3.0, 5.5, alpha=0.2, color='green', label='0.6 advantage zone')
ax1.set_xlabel('Emotion Scale', fontsize=12)
ax1.set_ylabel('Quality Score (1-7)', fontsize=12)
ax1.set_title('Quality Decline vs Scale', fontsize=13, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_ylim(3.0, 5.5)

# Add key annotations
ax1.annotate('0.6 better\nat high scales', xy=(1.8, 4.0), xytext=(2.3, 4.8),
            arrowprops=dict(arrowstyle='->', color='green', lw=2),
            fontsize=11, color='green', fontweight='bold')

# Similarity comparison  
ax2 = axes[1]
ax2.plot(scales, none_similarity, 'o-', linewidth=3, markersize=8, label='Standard (none)', color='#1f77b4')
ax2.plot(scales, six_similarity, 's-', linewidth=3, markersize=8, label='Enhanced (0.6)', color='#ff7f0e')
ax2.axhline(y=4.0, color='red', linestyle='--', linewidth=2, label='Acceptable threshold')
ax2.fill_between([1.5, 2.5], 3.0, 6.0, alpha=0.2, color='green', label='0.6 advantage zone')
ax2.set_xlabel('Emotion Scale', fontsize=12)
ax2.set_ylabel('Similarity Score (1-7)', fontsize=12)
ax2.set_title('Voice Similarity vs Scale', fontsize=13, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_ylim(3.0, 6.0)

# Performance difference
ax3 = axes[2]
quality_diff = [s - n for s, n in zip(six_quality, none_quality)]
similarity_diff = [s - n for s, n in zip(six_similarity, none_similarity)]

bars1 = ax3.bar([s-0.1 for s in scales], quality_diff, 0.2, label='Quality Diff', color='#2ca02c', alpha=0.7)
bars2 = ax3.bar([s+0.1 for s in scales], similarity_diff, 0.2, label='Similarity Diff', color='#d62728', alpha=0.7)

ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax3.axhline(y=0.1, color='green', linestyle='--', alpha=0.7, label='Advantage threshold')
ax3.axhline(y=-0.1, color='red', linestyle='--', alpha=0.7, label='Disadvantage threshold')

ax3.set_xlabel('Emotion Scale', fontsize=12)
ax3.set_ylabel('Score Difference (0.6 - none)', fontsize=12)
ax3.set_title('Expressivity 0.6 Advantage', fontsize=13, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)
ax3.set_xticks(scales)

# Color bars based on advantage
for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
    if quality_diff[i] > 0.1:
        bar1.set_color('#2ca02c')  # Green for advantage
    elif quality_diff[i] < -0.1:
        bar1.set_color('#d62728')  # Red for disadvantage
    else:
        bar1.set_color('#888888')  # Gray for neutral
        
    if similarity_diff[i] > 0.1:
        bar2.set_color('#2ca02c')
    elif similarity_diff[i] < -0.1:
        bar2.set_color('#d62728')
    else:
        bar2.set_color('#888888')

plt.tight_layout()

# Add summary text box
textstr = '''KEY FINDINGS:
• Standard (none): Quality >4.0 up to scale 1.5
• Enhanced (0.6): Quality >4.0 up to scale 2.0  
• 0.6 advantage emerges at scales 1.5+
• Recommended: 0.6 expressivity, scales 1.0-2.0'''

props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
fig.text(0.02, 0.02, textstr, fontsize=11, verticalalignment='bottom', bbox=props)

plt.savefig('/Users/bagsanghui/ssfm30_qa/analysis/tts_tradeoff_summary.png', 
           dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("📊 Summary chart saved: tts_tradeoff_summary.png")