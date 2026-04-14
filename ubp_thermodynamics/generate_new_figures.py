import sys
import math
import matplotlib.pyplot as plt
import numpy as np

# Create the 3D Pantograph Sailing Diagram
plt.figure(figsize=(10, 6))
# A simple representation of the 2D vs 3D drag
angles = np.linspace(0, 90, 100)
drag_2d = np.ones_like(angles) * 100
drag_3d = np.cos(np.radians(angles)) * 100

plt.plot(angles, drag_2d, 'r--', label='2D Plane Drag (100%)')
plt.plot(angles, drag_3d, 'b-', label='3D Pantograph Drag (cos θ)')
plt.axvline(x=73.58, color='g', linestyle=':', label='Sailing Angle (73.58°)')
plt.scatter([73.58], [math.cos(math.radians(73.58))*100], color='g', s=100, zorder=5)

plt.title('Ontological Aerodynamics: Friction Reduction via 3D Skew', fontsize=14)
plt.xlabel('Z-Axis Shear Angle (Degrees)', fontsize=12)
plt.ylabel('Effective Friction (%)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('/home/ubuntu/ubp_thermo_study/figures/fig8_sailing.png', dpi=300, bbox_inches='tight')

# Create the Multi-Lens Bias Diagram
plt.figure(figsize=(10, 6))
labels = ['2D GEAR (Plane)', '3D SAIL (Volume)']
values = [92.01, 8.49]
colors = ['#E31E24', '#0064B4']

plt.bar(labels, values, color=colors)
plt.title('Multi-Lens Geometric Bias (Information Capture %)', fontsize=14)
plt.ylabel('Percentage of Geometric Information', fontsize=12)
for i, v in enumerate(values):
    plt.text(i, v + 2, f"{v}%", ha='center', fontweight='bold')
plt.ylim(0, 110)
plt.grid(axis='y', alpha=0.3)
plt.savefig('/home/ubuntu/ubp_thermo_study/figures/fig9_multilens.png', dpi=300, bbox_inches='tight')

print("Generated new figures: fig8_sailing.png, fig9_multilens.png")
