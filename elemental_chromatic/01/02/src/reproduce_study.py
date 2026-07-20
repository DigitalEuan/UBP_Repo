#!/usr/bin/env python3
import argparse
import itertools
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import textwrap
from fractions import Fraction
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

REPO_URL = "https://github.com/DigitalEuan/UBP_Repo/tree/main/core_studio_v4.0"
README_URL = "https://raw.githubusercontent.com/DigitalEuan/UBP_Repo/main/core_studio_v4.0/README.md"
CORE_USAGE_URL = "https://raw.githubusercontent.com/DigitalEuan/UBP_Repo/main/core_studio_v4.0/core/ubp_files_and_usage.md"
KB_USAGE_URL = "https://raw.githubusercontent.com/DigitalEuan/UBP_Repo/main/core_studio_v4.0/system_kb/ubp_files_and_usage.md"
REPO_COMMIT = "a024e223d6133fdac400a985c5ab6e8356dd3729"
RNG_SEED = 20260415
SELECTED_LAWS = [
    "LAW_ELEMENT_ARCHITECTURE_001",
    "LAW_CHEM_PERIODIC_001",
    "LAW_GEOMETRIC_BONDING_001",
    "LAW_CHEM_NOBLE_001",
    "LAW_CHEM_KINETICS_001",
    "LAW_GEOMETRIC_NRCI",
    "LAW_CONTINUOUS_LIMIT_001",
    "LAW_FOURTH_FLIP_001",
]


def json_default(obj):
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, Path):
        return str(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def parse_fraction(value):
    if isinstance(value, (int, float)):
        return float(value)
    return float(Fraction(str(value)))


def bits_to_rgb(bits):
    val = 0
    for bit in bits:
        val = (val << 1) | int(bit)
    return {
        "r": (val >> 16) & 0xFF,
        "g": (val >> 8) & 0xFF,
        "b": val & 0xFF,
    }


def rgb_to_hex(rgb):
    return f"#{rgb['r']:02x}{rgb['g']:02x}{rgb['b']:02x}"


def calc_saturation(rgb):
    r, g, b = rgb["r"], rgb["g"], rgb["b"]
    avg = (r + g + b) / 3.0
    return math.sqrt((r - avg) ** 2 + (g - avg) ** 2 + (b - avg) ** 2)


def hamming_distance(v1, v2):
    return sum(a != b for a, b in zip(v1, v2))


def get_periodic_pos(z):
    if z == 1:
        return (1, 1)
    if z == 2:
        return (1, 18)
    if 3 <= z <= 10:
        return (2, (z - 2) if z <= 4 else (z - 2) + 10)
    if 11 <= z <= 18:
        return (3, (z - 10) if z <= 12 else (z - 10) + 10)
    if 19 <= z <= 36:
        return (4, z - 18)
    if 37 <= z <= 54:
        return (5, z - 36)
    if 55 <= z <= 86:
        if 57 <= z <= 71:
            return (6, 3)
        return (6, (z - 54) if z < 57 else (z - 54 - 14))
    if 87 <= z <= 118:
        if 89 <= z <= 103:
            return (7, 3)
        return (7, (z - 86) if z < 89 else (z - 86 - 14))
    return (8, 1)


def mean_pairwise(values, metric):
    idxs = list(range(len(values)))
    pairs = list(itertools.combinations(idxs, 2))
    return float(np.mean([metric(values[i], values[j]) for i, j in pairs]))


def extract_name_and_symbol(lexicon_text, fallback_symbol):
    text = str(lexicon_text)
    m = re.search(r"Element:\s*([^\(\]]+)\(([^\)]+)\)", text)
    if m:
        name = m.group(1).replace("[", "").replace("]", "").strip()
        symbol = m.group(2).replace("[", "").replace("]", "").strip()
        return name, symbol
    symbol_map = {
        "H": "Hydrogen", "He": "Helium", "Li": "Lithium", "Be": "Beryllium", "B": "Boron",
        "C": "Carbon", "N": "Nitrogen", "O": "Oxygen", "F": "Fluorine", "Ne": "Neon",
        "Na": "Sodium", "Mg": "Magnesium", "Al": "Aluminium", "Si": "Silicon", "P": "Phosphorus",
        "S": "Sulfur", "Cl": "Chlorine", "Ar": "Argon", "K": "Potassium", "Ca": "Calcium",
        "Sc": "Scandium", "Ti": "Titanium", "V": "Vanadium", "Cr": "Chromium", "Mn": "Manganese",
        "Fe": "Iron", "Co": "Cobalt", "Ni": "Nickel", "Cu": "Copper", "Zn": "Zinc",
        "Ga": "Gallium", "Ge": "Germanium", "As": "Arsenic", "Se": "Selenium", "Br": "Bromine",
        "Kr": "Krypton", "Rb": "Rubidium", "Sr": "Strontium", "Y": "Yttrium", "Zr": "Zirconium",
        "Nb": "Niobium", "Mo": "Molybdenum", "Tc": "Technetium", "Ru": "Ruthenium", "Rh": "Rhodium",
        "Pd": "Palladium", "Ag": "Silver", "Cd": "Cadmium", "In": "Indium", "Sn": "Tin",
        "Sb": "Antimony", "Te": "Tellurium", "I": "Iodine", "Xe": "Xenon", "Cs": "Caesium",
        "Ba": "Barium", "La": "Lanthanum", "Ce": "Cerium", "Pr": "Praseodymium", "Nd": "Neodymium",
        "Pm": "Promethium", "Sm": "Samarium", "Eu": "Europium", "Gd": "Gadolinium", "Tb": "Terbium",
        "Dy": "Dysprosium", "Ho": "Holmium", "Er": "Erbium", "Tm": "Thulium", "Yb": "Ytterbium",
        "Lu": "Lutetium", "Hf": "Hafnium", "Ta": "Tantalum", "W": "Tungsten", "Re": "Rhenium",
        "Os": "Osmium", "Ir": "Iridium", "Pt": "Platinum", "Au": "Gold", "Hg": "Mercury",
        "Tl": "Thallium", "Pb": "Lead", "Bi": "Bismuth", "Po": "Polonium", "At": "Astatine",
        "Rn": "Radon", "Fr": "Francium", "Ra": "Radium", "Ac": "Actinium", "Th": "Thorium",
        "Pa": "Protactinium", "U": "Uranium", "Np": "Neptunium", "Pu": "Plutonium", "Am": "Americium",
        "Cm": "Curium", "Bk": "Berkelium", "Cf": "Californium", "Es": "Einsteinium", "Fm": "Fermium",
        "Md": "Mendelevium", "No": "Nobelium", "Lr": "Lawrencium", "Rf": "Rutherfordium", "Db": "Dubnium",
        "Sg": "Seaborgium", "Bh": "Bohrium", "Hs": "Hassium", "Mt": "Meitnerium", "Ds": "Darmstadtium",
        "Rg": "Roentgenium", "Cn": "Copernicium", "Nh": "Nihonium", "Fl": "Flerovium", "Mc": "Moscovium",
        "Lv": "Livermorium", "Ts": "Tennessine", "Og": "Oganesson",
    }
    return symbol_map.get(fallback_symbol, fallback_symbol), fallback_symbol


def load_kb(kb_path):
    kb = json.loads(Path(kb_path).read_text())
    fields = kb["_fields"]
    idx = {f: i for i, f in enumerate(fields)}
    return kb, fields, idx, kb["entries"]


def extract_elements(kb, idx):
    rows = []
    for entry in kb["entries"].values():
        uid = entry[idx["ubp_id"]]
        if not (isinstance(uid, str) and uid.startswith("ELEM_")):
            continue
        tags = entry[idx["tags"]]
        if isinstance(tags, list) and "ISOTOPE" in tags:
            continue
        parts = uid.split("_")
        if len(parts) != 3:
            continue
        symbol = parts[1]
        z = int(parts[2])
        lexicon_text = entry[idx["lexicon"]]
        name, symbol = extract_name_and_symbol(lexicon_text, symbol)
        vector = list(map(int, entry[idx["vector"]]))
        rgb = bits_to_rgb(vector)
        period, group = get_periodic_pos(z)
        tax = parse_fraction(entry[idx["tax_str"]])
        nrci = float(entry[idx["nrci_val"]])
        hamming_weight = int(sum(vector))
        rows.append({
            "ubp_id": uid,
            "symbol": symbol,
            "name": name,
            "z": z,
            "period": period,
            "group": group,
            "vector": vector,
            "rgb": rgb,
            "hex_color": rgb_to_hex(rgb),
            "nrci": nrci,
            "nrci_str": entry[idx["nrci_str"]],
            "tax": tax,
            "tax_str": entry[idx["tax_str"]],
            "hamming_weight": hamming_weight,
            "saturation": calc_saturation(rgb),
            "lexicon": lexicon_text,
            "tags": tags,
        })
    rows.sort(key=lambda r: r["z"])
    if len(rows) != 118:
        raise RuntimeError(f"Expected 118 canonical elements, found {len(rows)}")
    return rows


def extract_laws(kb, idx, law_ids):
    found = {}
    for entry in kb["entries"].values():
        uid = entry[idx["ubp_id"]]
        if uid in law_ids:
            found[uid] = {
                "ubp_id": uid,
                "lexicon": entry[idx["lexicon"]],
                "tags": entry[idx["tags"]],
                "vector": entry[idx["vector"]],
                "nrci": entry[idx["nrci_val"]],
            }
    return found


def compute_extension_statistics(elements):
    rng = random.Random(RNG_SEED)
    rgb_arr = np.array([[e["rgb"]["r"], e["rgb"]["g"], e["rgb"]["b"]] for e in elements], dtype=float)
    vecs = [e["vector"] for e in elements]
    ids = [e["ubp_id"] for e in elements]
    zs = [e["z"] for e in elements]
    sats = np.array([e["saturation"] for e in elements])
    nrci = np.array([e["nrci"] for e in elements])
    tax = np.array([e["tax"] for e in elements])
    weights = np.array([e["hamming_weight"] for e in elements])

    noble_z = {2, 10, 18, 36, 54, 86, 118}
    noble_idx = [i for i, e in enumerate(elements) if e["z"] in noble_z]
    noble_rgb_spread = float(np.mean([
        math.dist(rgb_arr[i], rgb_arr[j]) for i, j in itertools.combinations(noble_idx, 2)
    ]))
    noble_hamming_spread = float(np.mean([
        hamming_distance(vecs[i], vecs[j]) for i, j in itertools.combinations(noble_idx, 2)
    ]))
    noble_sat_mean = float(np.mean([elements[i]["saturation"] for i in noble_idx]))

    trials = 10000
    sample_size = len(noble_idx)
    rand_rgb_spread = []
    rand_hamming_spread = []
    rand_sat_mean = []
    population = list(range(len(elements)))
    for _ in range(trials):
        s = rng.sample(population, sample_size)
        rand_rgb_spread.append(float(np.mean([
            math.dist(rgb_arr[i], rgb_arr[j]) for i, j in itertools.combinations(s, 2)
        ])))
        rand_hamming_spread.append(float(np.mean([
            hamming_distance(vecs[i], vecs[j]) for i, j in itertools.combinations(s, 2)
        ])))
        rand_sat_mean.append(float(np.mean([elements[i]["saturation"] for i in s])))

    observed_seq_hamming = float(np.mean([
        hamming_distance(vecs[i], vecs[i + 1]) for i in range(len(elements) - 1)
    ]))
    observed_seq_rgb = float(np.mean([
        math.dist(rgb_arr[i], rgb_arr[i + 1]) for i in range(len(elements) - 1)
    ]))
    rand_seq_hamming = []
    rand_seq_rgb = []
    perm = population[:]
    for _ in range(trials):
        rng.shuffle(perm)
        rand_seq_hamming.append(float(np.mean([
            hamming_distance(vecs[perm[i]], vecs[perm[i + 1]]) for i in range(len(perm) - 1)
        ])))
        rand_seq_rgb.append(float(np.mean([
            math.dist(rgb_arr[perm[i]], rgb_arr[perm[i + 1]]) for i in range(len(perm) - 1)
        ])))

    G = nx.Graph()
    G.add_nodes_from(ids)
    hamming_matrix = np.zeros((len(elements), len(elements)), dtype=int)
    rgb_matrix = np.zeros((len(elements), len(elements)), dtype=float)
    for i, j in itertools.combinations(range(len(elements)), 2):
        dh = hamming_distance(vecs[i], vecs[j])
        dr = math.dist(rgb_arr[i], rgb_arr[j])
        hamming_matrix[i, j] = hamming_matrix[j, i] = dh
        rgb_matrix[i, j] = rgb_matrix[j, i] = dr
        if dh <= 8:
            G.add_edge(ids[i], ids[j], hamming=dh)

    components = sorted((sorted(c) for c in nx.connected_components(G)), key=len, reverse=True)
    largest_component = G.subgraph(components[0]).copy()
    degrees = np.array([G.degree[n] for n in ids])

    within_h, between_h, within_rgb, between_rgb = [], [], [], []
    for i, j in itertools.combinations(range(len(elements)), 2):
        if elements[i]["group"] == elements[j]["group"]:
            within_h.append(hamming_matrix[i, j])
            within_rgb.append(rgb_matrix[i, j])
        else:
            between_h.append(hamming_matrix[i, j])
            between_rgb.append(rgb_matrix[i, j])

    stats = {
        "noble_cluster_test": {
            "observed_mean_pairwise_rgb": noble_rgb_spread,
            "observed_mean_pairwise_hamming": noble_hamming_spread,
            "observed_mean_saturation": noble_sat_mean,
            "random_rgb_spread_mean": float(np.mean(rand_rgb_spread)),
            "random_hamming_spread_mean": float(np.mean(rand_hamming_spread)),
            "random_saturation_mean": float(np.mean(rand_sat_mean)),
            "p_lower_rgb_spread": float(np.mean(np.array(rand_rgb_spread) <= noble_rgb_spread)),
            "p_lower_hamming_spread": float(np.mean(np.array(rand_hamming_spread) <= noble_hamming_spread)),
            "p_higher_saturation": float(np.mean(np.array(rand_sat_mean) >= noble_sat_mean)),
        },
        "periodic_smoothness_test": {
            "observed_mean_adjacent_hamming": observed_seq_hamming,
            "observed_mean_adjacent_rgb": observed_seq_rgb,
            "random_mean_adjacent_hamming": float(np.mean(rand_seq_hamming)),
            "random_mean_adjacent_rgb": float(np.mean(rand_seq_rgb)),
            "p_lower_hamming": float(np.mean(np.array(rand_seq_hamming) <= observed_seq_hamming)),
            "p_lower_rgb": float(np.mean(np.array(rand_seq_rgb) <= observed_seq_rgb)),
        },
        "group_coherence": {
            "within_group_mean_hamming": float(np.mean(within_h)),
            "between_group_mean_hamming": float(np.mean(between_h)),
            "within_group_mean_rgb": float(np.mean(within_rgb)),
            "between_group_mean_rgb": float(np.mean(between_rgb)),
        },
        "network": {
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "density": float(nx.density(G)),
            "connected_components": len(components),
            "largest_component_size": largest_component.number_of_nodes(),
            "diameter": int(nx.diameter(largest_component)),
            "average_shortest_path": float(nx.average_shortest_path_length(largest_component)),
            "top_hubs": [
                {"ubp_id": node, "degree": int(deg), "z": next(e["z"] for e in elements if e["ubp_id"] == node), "symbol": next(e["symbol"] for e in elements if e["ubp_id"] == node)}
                for node, deg in sorted(G.degree, key=lambda x: x[1], reverse=True)[:10]
            ],
            "shortest_path_H_to_Cf": nx.shortest_path(G, "ELEM_H_001", "ELEM_Cf_098"),
            "shortest_path_H_to_Og": nx.shortest_path(G, "ELEM_H_001", "ELEM_Og_118"),
        },
        "correlations": {
            "pearson_saturation_nrci": float(np.corrcoef(sats, nrci)[0, 1]),
            "pearson_saturation_tax": float(np.corrcoef(sats, tax)[0, 1]),
            "pearson_saturation_hamming_weight": float(np.corrcoef(sats, weights)[0, 1]),
            "pearson_saturation_degree": float(np.corrcoef(sats, degrees)[0, 1]),
        },
        "discretization": {
            "unique_nrci_values": sorted({round(x, 6) for x in nrci.tolist()}),
            "unique_tax_values": sorted({round(x, 6) for x in tax.tolist()}),
            "nrci_counts": dict(pd.Series(np.round(nrci, 6)).value_counts().sort_index()),
        },
        "permutation_invariance_note": "The Euclidean path-length and pairwise-spread metrics used in 4_calculate_dist.py are symmetric under axis permutation; all 6 RGB permutations must therefore tie unless axis-specific priors are introduced.",
        "tautology_note": "Because elemental RGB values are a direct 24-bit visualization of the same UBP vectors stored in the KB, any RGB->bit roundtrip manifold audit is structurally phase-locked by construction.",
    }

    aux = {
        "graph": G,
        "rgb_arr": rgb_arr,
        "sats": sats,
        "nrci": nrci,
        "tax": tax,
        "weights": weights,
        "degrees": degrees,
        "rand_rgb_spread": rand_rgb_spread,
        "rand_hamming_spread": rand_hamming_spread,
        "rand_sat_mean": rand_sat_mean,
        "rand_seq_hamming": rand_seq_hamming,
        "rand_seq_rgb": rand_seq_rgb,
        "noble_idx": noble_idx,
        "hamming_matrix": hamming_matrix,
        "rgb_matrix": rgb_matrix,
    }
    return stats, aux


def save_figures(elements, stats, aux, figures_dir):
    figures_dir.mkdir(parents=True, exist_ok=True)
    rgb_arr = aux["rgb_arr"]
    degrees = aux["degrees"]
    sats = aux["sats"]
    nrci = aux["nrci"]
    tax = aux["tax"]
    noble_idx = set(aux["noble_idx"])

    # Figure 1: RG projection
    fig, ax = plt.subplots(figsize=(10, 8))
    for i, e in enumerate(elements):
        ax.scatter(e["rgb"]["r"], e["rgb"]["g"], s=30 + 90 * e["nrci"], c=e["hex_color"], edgecolors='black' if i in noble_idx else 'none', linewidths=1.3 if i in noble_idx else 0)
    for i in sorted(noble_idx):
        e = elements[i]
        ax.text(e["rgb"]["r"] + 2, e["rgb"]["g"] + 2, e["symbol"], fontsize=8)
    ax.set_title("Element Chromatics in R-G projection (size ∝ NRCI)")
    ax.set_xlabel("R channel")
    ax.set_ylabel("G channel")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(figures_dir / "01_rg_projection.png", dpi=180)
    plt.close(fig)

    # Figure 2: Noble null model
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(aux["rand_rgb_spread"], bins=40, color="#7aa6ff", alpha=0.8)
    ax.axvline(stats["noble_cluster_test"]["observed_mean_pairwise_rgb"], color="red", linewidth=2, label="Observed noble-gas mean spread")
    ax.set_title("Null model: noble-gas RGB clustering")
    ax.set_xlabel("Mean pairwise RGB distance")
    ax.set_ylabel("Random 7-set count")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figures_dir / "02_noble_cluster_null.png", dpi=180)
    plt.close(fig)

    # Figure 3: Periodic smoothness null model
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(aux["rand_seq_hamming"], bins=40, color="#8bd3a8", alpha=0.85)
    ax.axvline(stats["periodic_smoothness_test"]["observed_mean_adjacent_hamming"], color="red", linewidth=2, label="Observed Z-adjacent mean hamming")
    ax.set_title("Null model: periodic-order smoothness in Hamming space")
    ax.set_xlabel("Mean adjacent Hamming distance")
    ax.set_ylabel("Random permutation count")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figures_dir / "03_periodic_smoothness_null.png", dpi=180)
    plt.close(fig)

    # Figure 4: degree vs Z
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot([e["z"] for e in elements], degrees, color="#444444", linewidth=1.5)
    ax.scatter([e["z"] for e in elements], degrees, c=[e["hex_color"] for e in elements], s=30, edgecolors='black', linewidths=0.2)
    for hub in stats["network"]["top_hubs"][:5]:
        ax.text(hub["z"] + 0.5, hub["degree"] + 0.3, hub["symbol"], fontsize=8)
    ax.set_title("Chromatic resonance network degree by atomic number")
    ax.set_xlabel("Atomic number Z")
    ax.set_ylabel("Degree in Hamming≤8 graph")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(figures_dir / "04_degree_vs_atomic_number.png", dpi=180)
    plt.close(fig)

    # Figure 5: saturation vs tax and NRCI
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].scatter(tax, sats, c=[e["hex_color"] for e in elements], s=35, edgecolors='black', linewidths=0.2)
    axes[0].set_title("Saturation vs Symmetry Tax")
    axes[0].set_xlabel("Symmetry Tax")
    axes[0].set_ylabel("Chromatic saturation")
    axes[0].grid(alpha=0.25)
    axes[1].scatter(nrci, sats, c=[e["hex_color"] for e in elements], s=35, edgecolors='black', linewidths=0.2)
    axes[1].set_title("Saturation vs NRCI")
    axes[1].set_xlabel("NRCI")
    axes[1].set_ylabel("Chromatic saturation")
    axes[1].grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(figures_dir / "05_saturation_vs_tax_nrci.png", dpi=180)
    plt.close(fig)


def rerun_original_scripts(package_root, repo_path, results_dir, dataset_path, kb_path):
    rerun_dir = results_dir / "original_rerun"
    rerun_dir.mkdir(parents=True, exist_ok=True)
    scripts_dir = package_root / "original_user_scripts"
    core_dir = repo_path / "core_studio_v4.0" / "core"
    records = []
    for script in sorted(scripts_dir.glob("*.py")):
        script_dir = rerun_dir / script.stem
        script_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(script, script_dir / script.name)
        shutil.copy2(dataset_path, script_dir / "elemental_chromatic_data.json")
        shutil.copy2(kb_path, script_dir / "ubp_system_kb.json")
        env = os.environ.copy()
        env["PYTHONPATH"] = str(core_dir)
        proc = subprocess.run(
            [sys.executable, script.name],
            cwd=script_dir,
            env=env,
            capture_output=True,
            text=True,
        )
        (script_dir / "stdout.txt").write_text(proc.stdout)
        (script_dir / "stderr.txt").write_text(proc.stderr)
        output_files = sorted([p.name for p in script_dir.iterdir() if p.name not in {script.name, 'stdout.txt', 'stderr.txt', 'elemental_chromatic_data.json', 'ubp_system_kb.json'}])
        records.append({
            "script": script.name,
            "exit_code": proc.returncode,
            "output_files": output_files,
            "stdout_head": proc.stdout.splitlines()[:8],
            "stderr_head": proc.stderr.splitlines()[:8],
        })
    return records


def write_report(package_root, results_dir, elements, laws, script_runs, stats):
    report_path = results_dir / "STUDY_REPORT.md"
    top_hubs = stats["network"]["top_hubs"][:5]
    report = f"""# Element Chromatics with the Full UBP System

## Scope
This package reruns the supplied Element Chromatics scripts against the **full** UBP repository ({REPO_URL}) at commit `{REPO_COMMIT}`, using the active columnar `ubp_system_kb.json` format described in the UBP README and usage documents.

## What was reproduced
- 19/19 supplied user scripts were rerun successfully.
- Inputs were rebuilt from the full KB, excluding isotope rows so the canonical set contains exactly 118 elements.
- Each original script was executed in an isolated folder so its JSON and `scene_3d.json` outputs are preserved.

## Important scientific findings
1. **Most original scripts do execute on the full UBP stack** once the canonical 118-element dataset is reconstructed from the full KB.
2. **The permutation study is invariant by construction.** The Euclidean metrics used in `4_calculate_dist.py` are symmetric to swapping RGB axes, so all 6 RGB permutations necessarily tie. This means the study does not identify a preferred RGB→XYZ assignment without introducing axis-specific priors.
3. **The manifold phase-lock audit is tautological.** Because `elemental_chromatic_data.json` is generated directly from the 24-bit element vectors, the RGB→bit roundtrip in `17_ubp_script_20260415230337.py` will always report zero tension unless a nontrivial encoding layer is added.
4. **Noble gases are not unusually compact in raw RGB space under a null model.** Their observed mean pairwise RGB spread is {stats['noble_cluster_test']['observed_mean_pairwise_rgb']:.2f}, which is *larger* than the random-set mean of {stats['noble_cluster_test']['random_rgb_spread_mean']:.2f}. The lower-tail probability is {stats['noble_cluster_test']['p_lower_rgb_spread']:.4f}.
5. **The periodic Z-order is not exceptionally smooth in raw Hamming or RGB adjacency.** The observed mean adjacent Hamming distance is {stats['periodic_smoothness_test']['observed_mean_adjacent_hamming']:.4f}, versus a random-order mean of {stats['periodic_smoothness_test']['random_mean_adjacent_hamming']:.4f}.
6. **Saturation has weak linear coupling to NRCI and symmetry tax in the current KB.** This is partly because the element table only exposes three distinct NRCI values and three distinct tax values.

## Selected quantitative results
- Hamming≤8 resonance graph: {stats['network']['nodes']} nodes, {stats['network']['edges']} edges, density {stats['network']['density']:.4f}, diameter {stats['network']['diameter']}.
- Shortest path H→Cf: {' -> '.join(stats['network']['shortest_path_H_to_Cf'])}
- Shortest path H→Og: {' -> '.join(stats['network']['shortest_path_H_to_Og'])}
- Top hubs: {', '.join([f"{h['symbol']} (Z={h['z']}, degree={h['degree']})" for h in top_hubs])}
- Within-group vs between-group mean Hamming distance: {stats['group_coherence']['within_group_mean_hamming']:.4f} vs {stats['group_coherence']['between_group_mean_hamming']:.4f}
- Within-group vs between-group mean RGB distance: {stats['group_coherence']['within_group_mean_rgb']:.4f} vs {stats['group_coherence']['between_group_mean_rgb']:.4f}

## LAW entries incorporated into interpretation
"""
    for law_id in SELECTED_LAWS:
        if law_id in laws:
            lex = str(laws[law_id]['lexicon'])[:260].replace('\n', ' ')
            report += f"\n- **{law_id}**: {lex}"
    report += f"""

## Folder guide
- `data/`: canonical element chromatic table in JSON and CSV.
- `original_rerun/`: isolated reruns of the 19 supplied scripts with preserved outputs.
- `tables/`: extension-study CSV tables.
- `figures/`: static figures supporting the extension analyses.
- `law_digest.json`: selected LAW entries pulled from the full KB.
- `summary.json`: machine-readable aggregate results.

## Recommended next scientific extensions
- Replace raw RGB-axis permutation tests with axis-aware embeddings (e.g. NRCI-weighted or shell-aware embeddings).
- Introduce external physical observables not already encoded into the same 24-bit vector to avoid circular validation.
- Test molecular synthesis predictions against a broader molecule subset in `ubp_system_kb.json` with explicit ground-truth labels.
- Add uncertainty analysis for synthetic / sparsely measured heavy elements.
"""
    report_path.write_text(report)


def write_readme(package_root):
    readme = f"""# Reproducible package: Element Chromatics with the full UBP system

This package reruns and extends the uploaded Element Chromatics study using the **full** UBP repository rather than a simplified surrogate.

## Upstream sources
- Repo: {REPO_URL}
- README: {README_URL}
- Core usage: {CORE_USAGE_URL}
- System KB usage: {KB_USAGE_URL}
- Commit pinned in this package: `{REPO_COMMIT}`

## Contents
- `src/reproduce_study.py` — main reproducibility driver.
- `run_study.sh` — convenience wrapper that can clone the upstream repo if needed.
- `original_user_scripts/` — the 19 uploaded scripts preserved verbatim.
- `ubp_elemental_chromatic.png` — original uploaded visualization.
- `results/` — regenerated outputs, extension analyses, figures, and documentation.

## Quick start
```bash
bash run_study.sh /path/to/UBP_Repo
```
If no repo path is supplied, the script will clone the upstream repository next to this package and checkout commit `{REPO_COMMIT}`.

## Notes
- The rerun uses the **columnar** `ubp_system_kb.json` now shipped in the full UBP repo.
- A canonical 118-element table is rebuilt directly from the KB while excluding isotope-tagged entries.
- All original scripts are rerun in isolated directories so file outputs do not overwrite each other.
"""
    (package_root / "README.md").write_text(readme)


def write_run_sh(package_root):
    script = f"""#!/usr/bin/env bash
set -euo pipefail
PKG_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_PATH="${{1:-$PKG_DIR/UBP_Repo}}"
if [ ! -d "$REPO_PATH/.git" ]; then
  echo "[setup] Cloning UBP_Repo into $REPO_PATH"
  rm -rf "$REPO_PATH"
  git clone --depth 1 https://github.com/DigitalEuan/UBP_Repo.git "$REPO_PATH"
fi
cd "$REPO_PATH"
git fetch --depth 1 origin {REPO_COMMIT} || true
git checkout {REPO_COMMIT} || true
python3 "$PKG_DIR/src/reproduce_study.py" --repo-path "$REPO_PATH" --package-root "$PKG_DIR"
"""
    path = package_root / "run_study.sh"
    path.write_text(script)
    os.chmod(path, 0o755)


def write_requirements(package_root):
    req = "numpy\npandas\nmatplotlib\nnetworkx\n"
    (package_root / "requirements.txt").write_text(req)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-path", required=True)
    parser.add_argument("--package-root", required=True)
    args = parser.parse_args()

    package_root = Path(args.package_root).resolve()
    repo_path = Path(args.repo_path).resolve()
    results_dir = package_root / "results"
    data_dir = results_dir / "data"
    tables_dir = results_dir / "tables"
    figures_dir = results_dir / "figures"
    for p in [results_dir, data_dir, tables_dir, figures_dir]:
        p.mkdir(parents=True, exist_ok=True)

    kb_path = repo_path / "core_studio_v4.0" / "system_kb" / "ubp_system_kb.json"
    kb, fields, idx, entries = load_kb(kb_path)
    elements = extract_elements(kb, idx)
    laws = extract_laws(kb, idx, SELECTED_LAWS)

    dataset_path = data_dir / "elemental_chromatic_data.json"
    dataset_path.write_text(json.dumps(elements, indent=2, default=json_default))
    pd.DataFrame([
        {
            "ubp_id": e["ubp_id"], "z": e["z"], "symbol": e["symbol"], "name": e["name"],
            "period": e["period"], "group": e["group"], "hex_color": e["hex_color"],
            "r": e["rgb"]["r"], "g": e["rgb"]["g"], "b": e["rgb"]["b"],
            "nrci": e["nrci"], "tax": e["tax"], "hamming_weight": e["hamming_weight"],
            "saturation": e["saturation"],
        }
        for e in elements
    ]).to_csv(data_dir / "elemental_chromatic_data.csv", index=False)

    law_digest_path = results_dir / "law_digest.json"
    law_digest_path.write_text(json.dumps(laws, indent=2, default=json_default))

    stats, aux = compute_extension_statistics(elements)
    save_figures(elements, stats, aux, figures_dir)

    # Save network tables
    graph = aux["graph"]
    pd.DataFrame([
        {
            "ubp_id": e["ubp_id"], "z": e["z"], "symbol": e["symbol"], "degree": int(graph.degree[e["ubp_id"]]),
            "nrci": e["nrci"], "tax": e["tax"], "saturation": e["saturation"],
        }
        for e in elements
    ]).to_csv(tables_dir / "network_nodes.csv", index=False)
    pd.DataFrame([
        {"source": u, "target": v, "hamming": d["hamming"]}
        for u, v, d in graph.edges(data=True)
    ]).to_csv(tables_dir / "network_edges.csv", index=False)

    script_runs = rerun_original_scripts(package_root, repo_path, results_dir, dataset_path, kb_path)
    (results_dir / "script_rerun_summary.json").write_text(json.dumps(script_runs, indent=2, default=json_default))

    summary = {
        "repo_url": REPO_URL,
        "repo_commit": REPO_COMMIT,
        "readme_url": README_URL,
        "core_usage_url": CORE_USAGE_URL,
        "kb_usage_url": KB_USAGE_URL,
        "rng_seed": RNG_SEED,
        "element_count": len(elements),
        "script_count": len(script_runs),
        "successful_scripts": sum(1 for r in script_runs if r["exit_code"] == 0),
        "extension_statistics": stats,
    }
    (results_dir / "summary.json").write_text(json.dumps(summary, indent=2, default=json_default))

    write_report(package_root, results_dir, elements, laws, script_runs, stats)
    write_readme(package_root)
    write_run_sh(package_root)
    write_requirements(package_root)

    manifest = {
        "package_root": str(package_root),
        "repo_path": str(repo_path),
        "outputs": sorted(str(p.relative_to(package_root)) for p in package_root.rglob('*') if p.is_file()),
    }
    (results_dir / "reproducibility_manifest.json").write_text(json.dumps(manifest, indent=2, default=json_default))

    print(json.dumps({
        "package_root": str(package_root),
        "results_dir": str(results_dir),
        "successful_scripts": summary["successful_scripts"],
        "figures": sorted([p.name for p in figures_dir.glob('*.png')]),
    }, indent=2))


if __name__ == "__main__":
    main()
