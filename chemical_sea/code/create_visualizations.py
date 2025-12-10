#!/usr/bin/env python3

import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load data
with open("../results/voyage_5_comprehensive.json", "r") as f:
    data = json.load(f)

# --- Prepare DataFrame ---
df = pd.DataFrame(data["patterns"])

# Convert necessary columns to numeric, coercing errors
df['atomic_number'] = pd.to_numeric(df['atomic_number'], errors='coerce')
df['period'] = pd.to_numeric(df['period'], errors='coerce')
df['group'] = pd.to_numeric(df['group'], errors='coerce')
df['alpha'] = pd.to_numeric(df['optimal_alpha'], errors='coerce')
df['value'] = pd.to_numeric(df['measured_value'], errors='coerce')

# Rename for clarity
df = df.rename(columns={
    "atomic_number": "Z",
    "element": "Symbol",
    "period": "Period",
    "group": "Group",
    "property_name": "property"
})

# --- Figure 3: Periodic Table Heatmap (Ionization Energy alpha) ---

# Filter and pivot data, ensuring we have something to plot
ion_df = df[df["property"] == "first_ionization"].dropna(subset=['Period', 'Group', 'alpha'])
if not ion_df.empty:
    heatmap_data = ion_df.pivot_table(
        index="Period", columns="Group", values="alpha"
    )
    if not heatmap_data.empty:
        plt.figure(figsize=(16, 8))
        sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="viridis")
        plt.title("Periodic Table Heatmap of α for First Ionization Energy")
        plt.xlabel("Group")
        plt.ylabel("Period")
        plt.savefig("../results/figure_3_heatmap.png")
        plt.close()
        print("Generated: figure_3_heatmap.png")
    else:
        print("Skipped Heatmap: No data to plot after pivoting.")
else:
    print("Skipped Heatmap: No ionization energy data found.")


# --- Figure 4: Correlation Matrix of alpha values ---

# Pivot the table to have properties as columns
alpha_df = df.pivot_table(index="Symbol", columns="property", values="alpha")

# Calculate correlation matrix
correlation_matrix = alpha_df.corr()

plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Correlation Matrix of α Values Across Chemical Properties")
plt.savefig("../results/figure_4_correlation_matrix.png")
plt.close()

print("Generated: figure_4_correlation_matrix.png")

# --- Figure 1: 3D Chemical Sea ---
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

plot_df = df[df["property"] == "first_ionization"].dropna(subset=['Z', 'Period', 'alpha', 'Group'])

sc = ax.scatter(plot_df["Z"], plot_df["Period"], plot_df["alpha"], c=plot_df["Group"], cmap="viridis", s=50)

ax.set_xlabel("Atomic Number (Z)")
ax.set_ylabel("Period")
ax.set_zlabel("α (Ionization Energy)")
ax.set_title("The Chemical Sea: α for Ionization Energy")
plt.colorbar(sc, label="Group")
plt.savefig("../results/figure_1_3d_chemical_sea.png")
plt.close()

print("Generated: figure_1_3d_chemical_sea.png")

# --- Figure 2: Master Plot ---
Y_CONSTANT = 0.264675430404527

properties = df["property"].unique()
num_properties = len(properties)
fig, axes = plt.subplots(nrows=(num_properties + 1) // 2, ncols=2, figsize=(15, 5 * ((num_properties + 1) // 2)))
axes = axes.flatten()

for i, prop in enumerate(properties):
    prop_df = df[df["property"] == prop].dropna(subset=['alpha', 'value'])
    if not prop_df.empty:
        p_ref_series = prop_df[prop_df["Symbol"] == "H"]["value"]
        if not p_ref_series.empty:
            p_ref = p_ref_series.iloc[0]
            if p_ref > 0:
                # Use .loc to avoid SettingWithCopyWarning
                prop_df.loc[:, "log_ratio"] = np.log(prop_df["value"] / p_ref)
                
                axes[i].scatter(prop_df["alpha"], prop_df["log_ratio"], label=prop)
                
                # Plot theoretical line
                x_vals = np.linspace(prop_df["alpha"].min(), prop_df["alpha"].max(), 100)
                y_vals = -x_vals * np.log(Y_CONSTANT)
                axes[i].plot(x_vals, y_vals, color='r', linestyle='--', label=f"Slope = -ln(Y)")
                
                axes[i].set_title(f"Master Plot for {prop.replace('_', ' ').title()}")
                axes[i].set_xlabel("α")
                axes[i].set_ylabel("ln(P / P_ref)")
                axes[i].legend()
                axes[i].grid(True)

# Hide unused subplots
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.savefig("../results/figure_2_master_plot.png")
plt.close()

print("Generated: figure_2_master_plot.png")
