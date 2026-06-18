"""
Push #9 — Final capstone push.

D.1: Focused null on ⅓·w·Y^3·U_e for H₀ (first w-based surprising formula candidate).
D.2: GLM Engine with vocabulary — attempt α parameter derivation.
D.3: Y^12 structural attractor — extract relevant LAW entries from system KB.

Plus: comprehensive capstone summary of all 9 pushes.
"""
from __future__ import annotations
import json, sys, random, math
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, "/home/z/my-project/scripts")
import ubp_unified_v5 as u

F = Fraction
pp = u.PARTICLE_PHYSICS
Y = pp.Y; L = pp.L; L_s = pp.L_s; U_e = pp.U_e; w = pp.wobble
pi = pp.pi; phi = pp.phi; e_const = pp.e_const

print("=" * 80)
print("Push #9 — Capstone: H₀ focused null, GLM Engine, KB LAW extraction")
print("=" * 80)

# ═══════════════════════════════════════════════════════════════════════════════
# D.1: Focused null on ⅓·w·Y^3·U_e for H₀
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("D.1 — Focused null on H₀ = ⅓·w·Y^3·U_e (w-based formula)")
print("=" * 80)

target_h0 = F((6736+7304), 200)  # 70.20 km/s/Mpc (CMB-SNe midpoint)
pred_h0 = F(1, 3) * w * Y**3 * U_e
err_h0 = abs(pred_h0 - target_h0) / target_h0 * 100
print(f"  Target H₀ midpoint = {float(target_h0):.4f} km/s/Mpc")
print(f"  Prediction ⅓·w·Y³·U_e = {float(pred_h0):.4f}")
print(f"  Error: {float(err_h0):.4f}%")

# Focused null: scramble w AND Y (both substrate-dependent)
random.seed(90909)
N_TRIALS = 5000
null_errs_h0 = []
for trial in range(N_TRIALS):
    w_mult = random.uniform(0.1, 10.0)
    Y_mult = random.uniform(0.1, 10.0)
    w_s = float(w) * w_mult
    Y_s = float(Y) * Y_mult
    pred = (1.0/3.0) * w_s * (Y_s**3) * float(U_e)
    err = abs(pred - float(target_h0)) / float(target_h0) * 100
    null_errs_h0.append(err)

null_errs_h0.sort()
hits_h0 = sum(1 for e in null_errs_h0 if e <= float(err_h0))
fp_h0 = hits_h0 / N_TRIALS * 100
print(f"  Null min: {null_errs_h0[0]:.4f}%   p10: {null_errs_h0[N_TRIALS//10]:.4f}%   p50: {null_errs_h0[N_TRIALS//2]:.4f}%")
print(f"  Trials with err ≤ real: {hits_h0}/{N_TRIALS} = {fp_h0:.2f}%")
if fp_h0 < 5:
    verdict_h0 = "SURPRISING — H₀ = ⅓·w·Y³·U_e is the 8th statistically surprising formula (first w-based)"
elif fp_h0 < 20:
    verdict_h0 = "MARGINALLY SURPRISING"
else:
    verdict_h0 = "NOT surprising"
print(f"  VERDICT: {verdict_h0}")

# ═══════════════════════════════════════════════════════════════════════════════
# D.2: GLM Engine with vocabulary
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("D.2 — GLM Engine with vocabulary")
print("=" * 80)

glm_results = {}
try:
    import glm_engine_v31 as glm
    
    # Try GLMDialogueEngine (simpler interface)
    dialogue = glm.GLMDialogueEngine()
    
    queries = [
        "What is the relationship between the Triad and cross-layer friction?",
        "Why does the Octad anchor use alpha one eighth?",
        "What determines the NRCI alpha parameter for CKM mixing?",
        "How does the bit-inversion pairing connect Reality and Potential layers?",
        "What is the structural meaning of Y power twelve self-pairing?",
    ]
    
    for i, q in enumerate(queries):
        print(f"\n  Query {i+1}: {q}")
        try:
            response = dialogue.respond(q, max_depth=2)
            resp_str = str(response)[:500]
            print(f"  Response: {resp_str}")
            glm_results[f"query_{i+1}"] = resp_str
        except Exception as e:
            print(f"  Error: {e}")
            glm_results[f"query_{i+1}"] = f"Error: {e}"
except Exception as e:
    print(f"  GLM Engine failed: {e}")
    glm_results["error"] = str(e)

# ═══════════════════════════════════════════════════════════════════════════════
# D.3: Extract relevant LAW entries from system KB
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("D.3 — System KB LAW extraction (connecting to our 7 surprising formulas)")
print("=" * 80)

with open("/home/z/my-project/scripts/ubp_system_kb.json") as f:
    kb = json.load(f)

entries = kb['entries']
fields = kb['_fields']
idx = {f: i for i, f in enumerate(fields)}

# Extract key physics laws relevant to our findings
relevant_laws = []
for key, val in entries.items():
    if isinstance(val, list) and len(val) >= 3:
        lex = str(val[idx.get('lexicon', 1)])
        tags_str = str(val[idx.get('tags', 2)])
        tags = eval(tags_str) if tags_str.startswith('[') else []
        
        # Filter for laws directly relevant to our findings
        relevant_tags = ['CKM', 'COUPLING', 'ALPHA', 'GRAVITY', 'NRCI', 'OCTAD', 
                        'GOLAY', 'LEECH', 'BARYON', 'PHOTON', 'MASS', 'DARK',
                        'LAYER', 'SHEAR', 'TRIAD', 'BIT', 'SUBSTRATE']
        if any(t in tags for t in relevant_tags) and 'LAW' in lex.upper() and 'LAWRENCIUM' not in lex.upper():
            # Get definition
            defn = ""
            if isinstance(val[idx['lexicon']], list) and len(val[idx['lexicon']]) >= 2:
                defn = str(val[idx['lexicon']][1])
            elif isinstance(val[idx['lexicon']], str):
                defn = val[idx['lexicon']]
            relevant_laws.append({
                "name": lex.replace('[', '').replace(']', '').strip("'\""),
                "definition": defn[:300],
                "tags": tags,
            })

print(f"\n  Found {len(relevant_laws)} relevant physics LAW entries")
print(f"\n  {'Law name':<55} {'Key tags'}")
print(f"  {'-'*55} {'-'*50}")
for law in relevant_laws[:20]:
    name = law['name'][:53]
    key_tags = [t for t in law['tags'] if t in relevant_tags][:5]
    print(f"  {name:<55} {key_tags}")

# ═══════════════════════════════════════════════════════════════════════════════
# Save all results
# ═══════════════════════════════════════════════════════════════════════════════
outp = Path("/home/z/my-project/results/push9_all.json")
with open(outp, "w") as f:
    json.dump({
        "d1_h0_focused_null": {
            "target": float(target_h0),
            "prediction": float(pred_h0),
            "formula": "⅓·w·Y³·U_e",
            "real_err_pct": float(err_h0),
            "n_trials": N_TRIALS,
            "null_min_pct": null_errs_h0[0],
            "null_p50_pct": null_errs_h0[N_TRIALS//2],
            "hits_at_real": hits_h0,
            "fp_rate_pct": fp_h0,
            "verdict": verdict_h0,
        },
        "d2_glm_engine": glm_results,
        "d3_kb_law_extraction": {
            "total_relevant_laws": len(relevant_laws),
            "laws": relevant_laws[:30],
        },
    }, f, indent=2, default=str)
print(f"\n[ok] Results saved to {outp}")
