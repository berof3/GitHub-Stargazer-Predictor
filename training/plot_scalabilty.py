import matplotlib.pyplot as plt
import pandas as pd

# 1. Data Setup
data = {
    'Nodes': [1, 2, 3],
    'Runtime': [19.93, 7.97, 7.18]
}
df = pd.DataFrame(data)

# 2. Calculate Scientific Metrics
df['Speedup'] = df['Runtime'][0] / df['Runtime']
df['Efficiency'] = df['Speedup'] / df['Nodes']

# 3. Create the Visualization
plt.rcParams.update({'font.size': 14}) # Increase global font size
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(22, 7))

# --- Graph 1: Horizontal Runtime ---
ax1.plot(df['Nodes'], df['Runtime'], marker='o', color='teal', linewidth=4, markersize=10)
ax1.set_title('Horizontal Runtime', fontweight='bold', fontsize=18)
ax1.set_xlabel('Number of Workers (Nodes)')
ax1.set_ylabel('Execution Time (Seconds)')
ax1.set_xticks([1, 2, 3])
ax1.grid(True, linestyle='--', alpha=0.7)

# --- Graph 2: Horizontal Speedup ---
ax2.plot(df['Nodes'], df['Nodes'], label='Ideal Speedup', linestyle='--', color='red', linewidth=2)
ax2.plot(df['Nodes'], df['Speedup'], marker='s', color='blue', label='Actual Speedup', linewidth=4, markersize=10)
ax2.set_title('Horizontal Speedup', fontweight='bold', fontsize=18)
ax2.set_xlabel('Number of Workers (Nodes)')
ax2.set_ylabel('Speedup Factor')
ax2.set_xticks([1, 2, 3])
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.7)

# --- Graph 3: Horizontal Efficiency ---
ax3.plot(df['Nodes'], [1.0, 1.0, 1.0], label='Ideal Efficiency', linestyle='--', color='red', linewidth=2)
ax3.plot(df['Nodes'], df['Efficiency'], marker='^', color='orange', label='Actual Efficiency', linewidth=4, markersize=10)
ax3.set_title('Horizontal Efficiency', fontweight='bold', fontsize=18)
ax3.set_xlabel('Number of Workers (Nodes)')
ax3.set_ylabel('Efficiency (0.0 - 1.0)')
ax3.set_ylim(0, 1.3) 
ax3.set_xticks([1, 2, 3])
ax3.legend()
ax3.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()

# CRITICAL: Use dpi=300 for high resolution printing
plt.savefig('scalability_report_quality.png', dpi=300)
print("SUCCESS: High-resolution graph saved as 'scalability_report_quality.png'")
