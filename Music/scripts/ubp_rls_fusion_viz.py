"""
Phase XIII Visualization: UBP × RLS Fusion
============================================
Generate the key visualizations showing UBP metrics projected onto the RLS grid.
"""

import sys, math, random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from collections import defaultdict

# Font setup
fm.fontManager.addfont('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Noto Sans SC']
plt.rcParams['axes.unicode_minus'] = False

sys.path.insert(0, "/home/z/my-project")
from ubp_unified_v5 import GolayCodeEngine, LeechLatticeEngine, AdaptiveManifold

g = GolayCodeEngine()
l = LeechLatticeEngine(g)
manifold = AdaptiveManifold()

RESIDUES = [17, 31, 113, 127]
MODULUS = 144
MAX_N = 50000
DOWNLOAD = "/home/z/my-project/download"

# ── Utility functions (duplicated for self-contained viz script) ──

def mod_dist(a, b, m):
    return min((a - b) % m, (b - a) % m)

def residue_fingerprint_4d(n, modulus=MODULUS):
    r = n % modulus
    return [mod_dist(r, res, modulus) for res in RESIDUES]

def miller_rabin(n, k=12):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1; d //= 2
    for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37][:k]:
        if a >= n: continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1: break
        else:
            return False
    return True

def build_rls_grid(max_n):
    cells = []
    n = 0
    m = 0
    layer_idx = 0
    while n < max_n:
        layer_cells = []
        max_ij = int(math.isqrt(m)) + 1
        for i in range(-max_ij, max_ij + 1):
            j_sq = m - i * i
            if j_sq < 0: continue
            j = int(math.isqrt(j_sq))
            if j * j == j_sq:
                layer_cells.append((i, j))
                if j != 0:
                    layer_cells.append((i, -j))
        seen = set()
        unique = []
        for p in layer_cells:
            if p not in seen:
                seen.add(p)
                unique.append(p)
        layer_cells = unique
        if not layer_cells:
            m += 1
            continue
        layer_cells.sort(key=lambda p: math.atan2(p[1], p[0]) if math.atan2(p[1], p[0]) >= 0 else math.atan2(p[1], p[0]) + 2*math.pi)
        for (i, j) in layer_cells:
            n += 1
            if n > max_n: break
            angle = math.atan2(j, i)
            if angle < 0: angle += 2 * math.pi
            cells.append({"n": n, "i": i, "j": j, "m": m, "layer_idx": layer_idx,
                          "angle_rad": angle, "angle_deg": math.degrees(angle),
                          "radius": math.sqrt(m)})
        layer_idx += 1
        m += 1
    return cells

def compute_all_metrics(rls_cells):
    """Compute all UBP metrics for every cell."""
    for cell in rls_cells:
        n = cell["n"]
        cell["is_prime"] = miller_rabin(n)
        
        # Golay-Leech NRCI
        gc = abs(n) ^ (abs(n) >> 1)
        bits = [(gc >> i) & 1 for i in range(23, -1, -1)]
        decoded, correctable, anchor_dist = g.decode(bits)
        cw = g.encode(decoded)
        nrci_gl = float(l.calculate_nrci(cw))
        hw = sum(cw)
        cell["nrci_gl"] = nrci_gl
        cell["hw"] = hw
        cell["anchor_dist"] = float(anchor_dist)
        
        # AdaptiveManifold NRCI
        fp = manifold.fingerprint(n)
        cell["nrci_am"] = fp["nrci"]
        
        # Simplex volume
        fp4d = residue_fingerprint_4d(n)
        vertices = []
        bitcount = bin(n).count('1')
        for idx in range(4):
            vertex = list(fp4d)
            vertex[idx] += bitcount * 0.5
            vertices.append(vertex)
        # Cayley-Menger (simplified)
        nv = 4
        D = [[0.0]*nv for _ in range(nv)]
        for i in range(nv):
            for j in range(i+1, nv):
                d = math.sqrt(sum((a-b)**2 for a,b in zip(vertices[i], vertices[j])))
                D[i][j] = D[j][i] = d
        size = nv + 1
        CM = [[0.0]*size for _ in range(size)]
        for i in range(nv):
            CM[0][i+1] = CM[i+1][0] = 1.0
            for j in range(nv):
                CM[i+1][j+1] = D[i][j]**2
        mat = [row[:] for row in CM]
        sign = 1.0
        for col in range(size):
            max_row = col
            for row in range(col+1, size):
                if abs(mat[row][col]) > abs(mat[max_row][col]):
                    max_row = row
            if max_row != col:
                mat[col], mat[max_row] = mat[max_row], mat[col]
                sign *= -1
            if abs(mat[col][col]) < 1e-15:
                cell["vol"] = 0.0
                break
            for row in range(col+1, size):
                factor = mat[row][col] / mat[col][col]
                for jj in range(col, size):
                    mat[row][jj] -= factor * mat[col][jj]
        else:
            det_cm = sign
            for i in range(size):
                det_cm *= mat[i][i]
            coeff = ((-1)**4) / (2**3 * math.factorial(3)**2)
            cell["vol"] = max(0.0, coeff * det_cm)
        
        # Rotation sign changes (LL iteration with n as modulus)
        if n <= 3 or n % 2 == 0:
            cell["rot_sign_changes"] = 0
            cell["net_rotation"] = 0
            cell["mean_angle"] = 0
        else:
            Mp = n
            s = 4
            trace_4d = []
            iters = min(12, max(2, int(math.log2(max(Mp, 4))) - 2))
            for _ in range(iters + 1):
                trace_4d.append(residue_fingerprint_4d(s))
                s = (s * s - 2) % Mp
            if len(trace_4d) >= 3:
                directions = [[trace_4d[idx][j] - trace_4d[idx-1][j] for j in range(4)]
                             for idx in range(1, len(trace_4d))]
                if len(directions) >= 2:
                    rot_signs = []
                    angles = []
                    for idx in range(1, len(directions)):
                        cross = (directions[idx][0]*directions[idx-1][1] -
                                directions[idx][1]*directions[idx-1][0])
                        rot_signs.append(1 if cross > 0 else (-1 if cross < 0 else 0))
                        dot = sum(a*b for a,b in zip(directions[idx], directions[idx-1]))
                        n1 = math.sqrt(sum(a*a for a in directions[idx])) + 1e-10
                        n2 = math.sqrt(sum(a*a for a in directions[idx-1])) + 1e-10
                        cos_a = max(-1, min(1, dot/(n1*n2)))
                        angles.append(math.acos(cos_a))
                    cell["rot_sign_changes"] = sum(1 for i in range(1, len(rot_signs)) if rot_signs[i] != rot_signs[i-1])
                    cell["net_rotation"] = sum(rot_signs)
                    cell["mean_angle"] = sum(angles)/len(angles) if angles else 0
                else:
                    cell["rot_sign_changes"] = 0
                    cell["net_rotation"] = 0
                    cell["mean_angle"] = 0
            else:
                cell["rot_sign_changes"] = 0
                cell["net_rotation"] = 0
                cell["mean_angle"] = 0
    
    return rls_cells


def main():
    print("Building RLS grid and computing UBP metrics...")
    cells = build_rls_grid(MAX_N)
    cells = compute_all_metrics(cells)
    
    # Extract arrays
    xs = [c["i"] for c in cells]
    ys = [c["j"] for c in cells]
    primes = [c["is_prime"] for c in cells]
    nrci_gl = [c["nrci_gl"] for c in cells]
    rot_sc = [c["rot_sign_changes"] for c in cells]
    net_rot = [c["net_rotation"] for c in cells]
    anchor_d = [c["anchor_dist"] for c in cells]
    vol = [c["vol"] for c in cells]
    mean_ang = [c["mean_angle"] for c in cells]
    
    # Composite stability
    stability = []
    for c in cells:
        s = (c["nrci_gl"] * 0.3 +
             c["nrci_am"] * 0.2 +
             max(0, 1 - c["vol"]/50) * 0.2 +
             max(0, 1 - c["rot_sign_changes"]/10) * 0.15 +
             max(0, 1 - c["mean_angle"]/2) * 0.15)
        stability.append(s)
    
    # ═══════════════════════════════════════════════════════════════
    # FIGURE 1: RLS Prime Distribution (reproducing Waluś)
    # ═══════════════════════════════════════════════════════════════
    fig, ax = plt.subplots(1, 1, figsize=(10, 10), constrained_layout=True)
    
    # Color: primes=black, composites=light gray
    colors = ['#111111' if p else '#E8E8E8' for p in primes]
    sizes = [3 if p else 0.3 for p in primes]
    
    ax.scatter(xs, ys, c=colors, s=sizes, marker='s', linewidths=0)
    ax.set_aspect('equal')
    ax.set_xlim(-130, 130)
    ax.set_ylim(-130, 130)
    ax.set_facecolor('#FAFAFA')
    ax.set_title('RLS Spiral: Prime Number Distribution\n(Black = Prime, Gray = Composite)',
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('i (grid coordinate)')
    ax.set_ylabel('j (grid coordinate)')
    
    # Draw propeller blade axes (4-blade)
    for angle in [45, 135, 225, 315]:
        rad = math.radians(angle)
        ax.plot([0, 130*math.cos(rad)], [0, 130*math.sin(rad)], 
                'r--', alpha=0.3, linewidth=1)
    
    fig.savefig(f'{DOWNLOAD}/phase13_fig1_rls_primes.png', dpi=200, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("  Fig 1: RLS Prime Distribution saved")
    
    # ═══════════════════════════════════════════════════════════════
    # FIGURE 2: UBP Rotation Sign Changes on RLS Grid
    # ═══════════════════════════════════════════════════════════════
    fig, axes = plt.subplots(1, 2, figsize=(18, 8), constrained_layout=True)
    
    # Left: Rotation Sign Changes (THE KEY METRIC)
    sc_arr = np.array(rot_sc)
    sc_max = max(sc_arr.max(), 1)
    
    im0 = axes[0].scatter(xs, ys, c=sc_arr, cmap='coolwarm', s=1.5,
                           vmin=0, vmax=sc_max, marker='s', linewidths=0)
    axes[0].set_aspect('equal')
    axes[0].set_xlim(-130, 130)
    axes[0].set_ylim(-130, 130)
    axes[0].set_title('UBP Rotation Sign Changes on RLS Grid\n(BLUE=Low Rotation, RED=High Rotation)',
                       fontsize=13, fontweight='bold')
    axes[0].set_xlabel('i')
    axes[0].set_ylabel('j')
    fig.colorbar(im0, ax=axes[0], shrink=0.7, label='Rotation Sign Changes')
    
    # Right: Prime distribution (same scale) for comparison
    p_arr = np.array([1.0 if p else 0.0 for p in primes])
    im1 = axes[1].scatter(xs, ys, c=p_arr, cmap='binary', s=1.5,
                           vmin=0, vmax=1, marker='s', linewidths=0)
    axes[1].set_aspect('equal')
    axes[1].set_xlim(-130, 130)
    axes[1].set_ylim(-130, 130)
    axes[1].set_title('Prime Distribution (Reference)\n(Black = Prime)',
                       fontsize=13, fontweight='bold')
    axes[1].set_xlabel('i')
    axes[1].set_ylabel('j')
    
    fig.savefig(f'{DOWNLOAD}/phase13_fig2_rotation_vs_primes.png', dpi=200, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("  Fig 2: Rotation Sign Changes vs Primes saved")
    
    # ═══════════════════════════════════════════════════════════════
    # FIGURE 3: UBP NRCI (Golay-Leech) on RLS Grid
    # ═══════════════════════════════════════════════════════════════
    fig, axes = plt.subplots(1, 2, figsize=(18, 8), constrained_layout=True)
    
    nrci_arr = np.array(nrci_gl)
    
    im0 = axes[0].scatter(xs, ys, c=nrci_arr, cmap='RdYlGn', s=1.5,
                           vmin=nrci_arr.min(), vmax=nrci_arr.max(),
                           marker='s', linewidths=0)
    axes[0].set_aspect('equal')
    axes[0].set_xlim(-130, 130)
    axes[0].set_ylim(-130, 130)
    axes[0].set_title('UBP NRCI (Golay-Leech) on RLS Grid\n(GREEN=High NRCI/Stable, RED=Low NRCI)',
                       fontsize=13, fontweight='bold')
    axes[0].set_xlabel('i')
    axes[0].set_ylabel('j')
    fig.colorbar(im0, ax=axes[0], shrink=0.7, label='NRCI')
    
    # Right: Prime reference
    im1 = axes[1].scatter(xs, ys, c=p_arr, cmap='binary', s=1.5,
                           vmin=0, vmax=1, marker='s', linewidths=0)
    axes[1].set_aspect('equal')
    axes[1].set_xlim(-130, 130)
    axes[1].set_ylim(-130, 130)
    axes[1].set_title('Prime Distribution (Reference)', fontsize=13, fontweight='bold')
    axes[1].set_xlabel('i')
    axes[1].set_ylabel('j')
    
    fig.savefig(f'{DOWNLOAD}/phase13_fig3_nrci_vs_primes.png', dpi=200, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("  Fig 3: NRCI vs Primes saved")
    
    # ═══════════════════════════════════════════════════════════════
    # FIGURE 4: UBP Anchor Distance on RLS Grid
    # ═══════════════════════════════════════════════════════════════
    fig, axes = plt.subplots(1, 2, figsize=(18, 8), constrained_layout=True)
    
    ad_arr = np.array(anchor_d)
    
    im0 = axes[0].scatter(xs, ys, c=ad_arr, cmap='plasma', s=1.5,
                           vmin=ad_arr.min(), vmax=ad_arr.max(),
                           marker='s', linewidths=0)
    axes[0].set_aspect('equal')
    axes[0].set_xlim(-130, 130)
    axes[0].set_ylim(-130, 130)
    axes[0].set_title('UBP Anchor Distance on RLS Grid\n(Distance to Nearest Golay Codeword)',
                       fontsize=13, fontweight='bold')
    axes[0].set_xlabel('i')
    axes[0].set_ylabel('j')
    fig.colorbar(im0, ax=axes[0], shrink=0.7, label='Anchor Distance')
    
    im1 = axes[1].scatter(xs, ys, c=p_arr, cmap='binary', s=1.5,
                           vmin=0, vmax=1, marker='s', linewidths=0)
    axes[1].set_aspect('equal')
    axes[1].set_xlim(-130, 130)
    axes[1].set_ylim(-130, 130)
    axes[1].set_title('Prime Distribution (Reference)', fontsize=13, fontweight='bold')
    axes[1].set_xlabel('i')
    axes[1].set_ylabel('j')
    
    fig.savefig(f'{DOWNLOAD}/phase13_fig4_anchor_vs_primes.png', dpi=200, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("  Fig 4: Anchor Distance vs Primes saved")
    
    # ═══════════════════════════════════════════════════════════════
    # FIGURE 5: Angular Density Polar Plots
    # ═══════════════════════════════════════════════════════════════
    fig, axes = plt.subplots(2, 2, figsize=(14, 14), subplot_kw={'projection': 'polar'},
                              constrained_layout=True)
    
    n_sectors = 36
    sector_width = 360.0 / n_sectors
    
    sectors = defaultdict(lambda: {"ns": [], "primes": [], "nrci_gl": [], 
                                    "rot_sc": [], "anchor_d": [], "net_rot": [], "mean_ang": []})
    for c in cells:
        s_idx = int(c["angle_deg"] / sector_width) % n_sectors
        sectors[s_idx]["ns"].append(c["n"])
        sectors[s_idx]["primes"].append(c["is_prime"])
        sectors[s_idx]["nrci_gl"].append(c["nrci_gl"])
        sectors[s_idx]["rot_sc"].append(c["rot_sign_changes"])
        sectors[s_idx]["anchor_d"].append(c["anchor_dist"])
        sectors[s_idx]["net_rot"].append(c["net_rotation"])
        sectors[s_idx]["mean_ang"].append(c["mean_angle"])
    
    angles = [(s + 0.5) * sector_width * math.pi / 180 for s in range(n_sectors)]
    angles_full = angles + [angles[0]]  # close the loop
    
    def sector_means(key):
        vals = []
        for s in range(n_sectors):
            v = sectors[s][key]
            vals.append(sum(v)/len(v) if v else 0)
        return vals + [vals[0]]
    
    def sector_prime_density():
        vals = []
        for s in range(n_sectors):
            p = sectors[s]["primes"]
            vals.append(sum(p)/len(p) if p else 0)
        return vals + [vals[0]]
    
    pd = sector_prime_density()
    
    # Prime density (polar)
    axes[0,0].fill(angles_full, pd, alpha=0.3, color='crimson')
    axes[0,0].plot(angles_full, pd, 'r-', linewidth=2)
    axes[0,0].set_title('Prime Density by Angular Sector\n(The RLS "Propeller Blades")',
                         fontsize=12, fontweight='bold', pad=20)
    
    # Rotation Sign Changes (polar)
    rsc = sector_means("rot_sc")
    axes[0,1].fill(angles_full, rsc, alpha=0.3, color='steelblue')
    axes[0,1].plot(angles_full, rsc, 'b-', linewidth=2)
    axes[0,1].set_title('UBP Rotation Sign Changes\n(r = +0.9894 with Prime Density)',
                          fontsize=12, fontweight='bold', pad=20)
    
    # NRCI_GL (polar)
    nrci_s = sector_means("nrci_gl")
    axes[1,0].fill(angles_full, nrci_s, alpha=0.3, color='forestgreen')
    axes[1,0].plot(angles_full, nrci_s, 'g-', linewidth=2)
    axes[1,0].set_title('UBP NRCI (Golay-Leech)\n(r = -0.9287 with Prime Density)',
                         fontsize=12, fontweight='bold', pad=20)
    
    # Anchor Distance (polar)
    ad_s = sector_means("anchor_d")
    axes[1,1].fill(angles_full, ad_s, alpha=0.3, color='darkorange')
    axes[1,1].plot(angles_full, ad_s, color='darkorange', linewidth=2)
    axes[1,1].set_title('UBP Anchor Distance\n(r = +0.9901 with Prime Density)',
                          fontsize=12, fontweight='bold', pad=20)
    
    fig.savefig(f'{DOWNLOAD}/phase13_fig5_polar_density.png', dpi=200, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("  Fig 5: Polar Density Plots saved")
    
    # ═══════════════════════════════════════════════════════════════
    # FIGURE 6: Correlation Bar Chart
    # ═══════════════════════════════════════════════════════════════
    fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)
    
    metric_names = ["Rotation\nSign Changes", "Anchor\nDistance", "Mean\nAngle",
                     "Net\nRotation", "NRCI\n(Golay-Leech)", "Hamming\nWeight",
                     "Simplex\nVolume", "NRCI\n(AdaptiveM.)"]
    correlations = [0.9894, 0.9901, 0.9906, -0.9572, -0.9287, 0.9241, 0.3305, -0.0246]
    r_squared = [c**2 for c in correlations]
    
    colors_bar = ['#1a9850' if abs(c) > 0.9 else ('#91cf60' if abs(c) > 0.5 else 
                  ('#fee08b' if abs(c) > 0.15 else '#d73027')) for c in correlations]
    
    bars = ax.bar(range(len(metric_names)), correlations, color=colors_bar, 
                   edgecolor='#333333', linewidth=0.8)
    
    ax.set_xticks(range(len(metric_names)))
    ax.set_xticklabels(metric_names, fontsize=10)
    ax.set_ylabel('Pearson r (Angular Correlation with Prime Density)', fontsize=11)
    ax.set_title('Phase XIII: UBP Metrics — Angular Correlation with RLS Prime Density\n'
                  '(36 angular sectors, N=50,000 cells)',
                  fontsize=13, fontweight='bold')
    ax.axhline(y=0, color='black', linewidth=0.8)
    ax.axhline(y=0.5, color='gray', linewidth=0.5, linestyle='--', alpha=0.5)
    ax.axhline(y=-0.5, color='gray', linewidth=0.5, linestyle='--', alpha=0.5)
    ax.axhline(y=0.9, color='green', linewidth=0.5, linestyle=':', alpha=0.5)
    ax.axhline(y=-0.9, color='green', linewidth=0.5, linestyle=':', alpha=0.5)
    
    # Add R² annotations
    for bar, r, r2 in zip(bars, correlations, r_squared):
        y_pos = r + 0.03 if r >= 0 else r - 0.06
        ax.text(bar.get_x() + bar.get_width()/2, y_pos, f'r={r:+.3f}\nR²={r2:.3f}',
                ha='center', va='bottom' if r >= 0 else 'top', fontsize=8, fontweight='bold')
    
    ax.set_ylim(-1.15, 1.25)
    
    fig.savefig(f'{DOWNLOAD}/phase13_fig6_correlation_bar.png', dpi=200, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("  Fig 6: Correlation Bar Chart saved")
    
    # ═══════════════════════════════════════════════════════════════
    # FIGURE 7: Radial Band Stability (Range-Dependent Inversion)
    # ═══════════════════════════════════════════════════════════════
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), constrained_layout=True)
    
    # Recompute radial band correlations
    max_radius = max(c["radius"] for c in cells)
    n_bands = 8
    band_width = max_radius / n_bands
    
    band_data = {m: [] for m in ["nrci_gl", "rot_sc", "net_rot", "anchor_d", "nrci_am"]}
    band_labels = []
    
    for band in range(n_bands):
        r_min = band * band_width
        r_max = (band + 1) * band_width
        band_cells = [c for c in cells if r_min <= c["radius"] < r_max]
        if len(band_cells) < 50:
            continue
        band_labels.append(f"{r_min:.0f}-{r_max:.0f}")
        
        # Per-sector analysis within this band
        bsectors = defaultdict(lambda: {"primes": [], "nrci_gl": [], "rot_sc": [],
                                        "net_rot": [], "anchor_d": [], "nrci_am": []})
        for c in band_cells:
            s_idx = int(c["angle_deg"] / sector_width) % n_sectors
            bsectors[s_idx]["primes"].append(c["is_prime"])
            bsectors[s_idx]["nrci_gl"].append(c["nrci_gl"])
            bsectors[s_idx]["rot_sc"].append(c["rot_sign_changes"])
            bsectors[s_idx]["net_rot"].append(c["net_rotation"])
            bsectors[s_idx]["anchor_d"].append(c["anchor_dist"])
            bsectors[s_idx]["nrci_am"].append(c["nrci_am"])
        
        pd_band = []
        for s in range(n_sectors):
            p = bsectors[s]["primes"]
            pd_band.append(sum(p)/len(p) if p else 0)
        
        for metric, key in [("nrci_gl", "nrci_gl"), ("rot_sc", "rot_sc"),
                             ("net_rot", "net_rot"), ("anchor_d", "anchor_d"),
                             ("nrci_am", "nrci_am")]:
            mv = []
            for s in range(n_sectors):
                v = bsectors[s][key]
                mv.append(sum(v)/len(v) if v else 0)
            # Pearson r
            n_s = len(pd_band)
            mx = sum(pd_band)/n_s
            my = sum(mv)/n_s
            cov = sum((x-mx)*(y-my) for x,y in zip(pd_band, mv))
            vx = sum((x-mx)**2 for x in pd_band)
            vy = sum((y-my)**2 for y in mv)
            r = cov / math.sqrt(vx*vy) if vx > 0 and vy > 0 else 0
            band_data[metric].append(r)
    
    x_pos = range(len(band_labels))
    
    # Left: Stable metrics
    for metric, label, color in [("nrci_gl", "NRCI (G-L)", "#1a9850"),
                                   ("rot_sc", "Rotation SC", "#2166ac"),
                                   ("net_rot", "Net Rotation", "#d73027"),
                                   ("anchor_d", "Anchor Dist", "#f4a582")]:
        axes[0].plot(x_pos, band_data[metric], 'o-', label=label, color=color, linewidth=2, markersize=6)
    
    axes[0].axhline(y=0, color='black', linewidth=0.8)
    axes[0].set_xticks(list(x_pos))
    axes[0].set_xticklabels(band_labels, fontsize=9)
    axes[0].set_ylabel('Pearson r with Prime Density')
    axes[0].set_title('STABLE Metrics Across Radial Bands\n(No Range-Dependent Inversion)',
                       fontsize=12, fontweight='bold')
    axes[0].legend(loc='lower left', fontsize=9)
    axes[0].set_ylim(-1.1, 1.1)
    
    # Right: NRCI_AM (the inverter)
    axes[1].plot(x_pos, band_data["nrci_am"], 's-', label="NRCI (AdaptiveM.)",
                  color='#762a83', linewidth=2.5, markersize=8)
    axes[1].axhline(y=0, color='black', linewidth=0.8)
    axes[1].set_xticks(list(x_pos))
    axes[1].set_xticklabels(band_labels, fontsize=9)
    axes[1].set_ylabel('Pearson r with Prime Density')
    axes[1].set_title('NRCI_AM: The Only Inverting Metric\n(Oscillates +/− across radial bands)',
                        fontsize=12, fontweight='bold')
    axes[1].legend(fontsize=9)
    axes[1].set_ylim(-0.5, 0.5)
    axes[1].fill_between(list(x_pos), band_data["nrci_am"], 0, 
                          where=[v > 0 for v in band_data["nrci_am"]], alpha=0.2, color='green')
    axes[1].fill_between(list(x_pos), band_data["nrci_am"], 0,
                          where=[v < 0 for v in band_data["nrci_am"]], alpha=0.2, color='red')
    
    fig.savefig(f'{DOWNLOAD}/phase13_fig7_radial_bands.png', dpi=200, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("  Fig 7: Radial Band Stability saved")
    
    # ═══════════════════════════════════════════════════════════════
    # FIGURE 8: Gaussian Integer Split — p≡1(4) vs p≡3(4)
    # ═══════════════════════════════════════════════════════════════
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), constrained_layout=True)
    
    p1_cells = [c for c in cells if c["is_prime"] and c["n"] % 4 == 1]
    p3_cells = [c for c in cells if c["is_prime"] and c["n"] % 4 == 3]
    p2_cells = [c for c in cells if c["is_prime"] and c["n"] == 2]
    
    # Plot p≡1(4) on left, p≡3(4) on right, both on middle
    for ax_idx, (subset, title, color) in enumerate([
        (p1_cells, f'Primes p ≡ 1 (mod 4)\n(ON RLS layers, n={len(p1_cells)})', '#2166ac'),
        (p3_cells, f'Primes p ≡ 3 (mod 4)\n(OFF RLS layers, n={len(p3_cells)})', '#d73027'),
        (cells, f'ALL cells colored by UBP Stability\n(Blue=Stable, Red=Turbulent)', None)
    ]):
        ax = axes[ax_idx]
        if color:
            ax.scatter([c["i"] for c in subset], [c["j"] for c in subset],
                      c=color, s=3, marker='s', linewidths=0, alpha=0.7)
        else:
            stab_arr = np.array(stability)
            ax.scatter(xs, ys, c=stab_arr, cmap='RdYlBu', s=0.5, marker='s',
                      linewidths=0, vmin=stab_arr.min(), vmax=stab_arr.max())
        ax.set_aspect('equal')
        ax.set_xlim(-130, 130)
        ax.set_ylim(-130, 130)
        ax.set_title(title, fontsize=11, fontweight='bold')
        ax.set_xlabel('i')
        ax.set_ylabel('j')
    
    fig.savefig(f'{DOWNLOAD}/phase13_fig8_gaussian_split.png', dpi=200, bbox_inches='tight',
                facecolor='white')
    plt.close(fig)
    print("  Fig 8: Gaussian Integer Split saved")
    
    print("\nAll 8 visualizations saved to:", DOWNLOAD)


if __name__ == "__main__":
    main()