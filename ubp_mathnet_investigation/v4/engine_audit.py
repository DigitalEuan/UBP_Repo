"""
Pure UBP Engine Audit — no external LLMs, no numpy
Tests every available engine and documents what each can genuinely do.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
from fractions import Fraction

results = {}

# 1. Core Golay + Leech
try:
    from core import GOLAY_ENGINE, LEECH_ENGINE
    test_vec = [1,0,1,1,0,0,1,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
    snapped, info = GOLAY_ENGINE.snap_to_codeword(test_vec)
    tax = LEECH_ENGINE.calculate_symmetry_tax(test_vec)
    nrci = float(Fraction(10,1) / (Fraction(10,1) + Fraction(float(tax)).limit_denominator(1000)))
    results['core_golay_leech'] = f'OK: snap_weight={sum(snapped)}, nrci={nrci:.4f}, syndrome={info.get("syndrome_weight",0)}'
except Exception as e:
    results['core_golay_leech'] = f'FAIL: {e}'

# 2. EML ALU (pure math operations — no EmlTreeNode, no snap_eml_to_lattice)
try:
    from ubp_eml_alu_sovereign import GrandUnifiedEmlALU
    alu = GrandUnifiedEmlALU()
    r1 = alu.eml(complex(3), complex(7))
    r2 = alu.sin(complex(1.0))
    r3 = alu.factorial(5)
    r4 = alu.ln(complex(2.718281828))
    results['alu_math'] = f'OK: eml(3,7)={r1.real:.4f}, sin(1)={r2.real:.4f}, 5!={r3}, ln(e)={r4.real:.4f}'
except Exception as e:
    results['alu_math'] = f'FAIL: {e}'

# 3. Observer Dynamics
try:
    from ubp_observer_dynamics import ObserverDynamicsEngine
    obs = ObserverDynamicsEngine()
    vec = [1,0,1,1,0,0,1,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
    soc = obs.calculate_soc_energy(vec, Fraction(7,10))
    read = obs.conscious_read(vec, Fraction(7,10))
    results['observer'] = f'OK: soc={float(soc):.2f}, status={read.get("status","?")}, charge={read.get("charge","?")}'
except Exception as e:
    results['observer'] = f'FAIL: {e}'

# 4. Semantic Engine
try:
    from ubp_semantic_engine import UBPSemanticEngine
    sem = UBPSemanticEngine()
    sem.load('core/ubp_system_kb.json', 'core/ubp_lang_kb_combined_v4.json')
    r = sem.query('prime divisibility', top_k=3)
    results['semantic'] = f'OK: top3={[x.ubp_id for x in r]}'
except Exception as e:
    results['semantic'] = f'FAIL: {e}'

# 5. MoE Cortex (N-gram, no LLM)
try:
    from ubp_moe_cortex_v2 import UBPMoECortexV2
    moe = UBPMoECortexV2()
    resp = moe.research('prime number', max_words=6)
    results['moe_cortex'] = f'OK: "{resp}"'
except Exception as e:
    results['moe_cortex'] = f'FAIL: {e}'

# 6. MathObjectV4
try:
    from math_atlas import MathObjectV4
    obj = MathObjectV4('TEST_7', 'seven', 'NT', 'math.nt')
    path = obj.add_path([('D', 7)], 'test')
    nrci7 = float(Fraction(10,1) / (Fraction(10,1) + path.tax))
    vec7 = obj.get_vector()
    results['math_atlas'] = f'OK: nrci={nrci7:.4f}, vec_weight={sum(vec7)}, vec[:4]={vec7[:4]}'
except Exception as e:
    results['math_atlas'] = f'FAIL: {e}'

# 7. TGIC Engine
try:
    from ubp_tgic_engine import TGICExactEngine, OffBit
    tgic = TGICExactEngine()
    vec = [1,0,1,1,0,0,1,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0]
    ob = OffBit(tuple(vec), 0)
    S = {'A': ob}
    energy = tgic.get_total_energy(S)
    results['tgic'] = f'OK: energy={float(energy):.4f}'
except Exception as e:
    results['tgic'] = f'FAIL: {e}'

# 8. UBPPyVM
try:
    from ubp_py_runtime import UBPPyVM, MOGOntology
    vm = UBPPyVM(kb_path='core/ubp_system_kb.json', lattice_path='/tmp/test_vm.json')
    vm.let('X', '7/1')
    vm.let('Y', '3/1')
    vm.synth('Z', '1xX + 1xY', u_score=0.9)
    results['pyvm'] = f'OK: X.dqi={vm.env["X"].dqi:.4f}, Z.dqi={vm.env["Z"].dqi:.4f}'
except Exception as e:
    results['pyvm'] = f'FAIL: {e}'

# 9. Phenomenology
try:
    from ubp_phenomenology import PhenomenologyEngine, NoumenalProjector
    phenom = PhenomenologyEngine()
    proj = NoumenalProjector()
    r = phenom.process_phenomenon('prime', 7)
    p = proj.project(r.nrci)
    results['phenomenology'] = f'OK: nrci={r.nrci:.4f}, state={p}'
except Exception as e:
    results['phenomenology'] = f'FAIL: {e}'

# 10. FOM System
try:
    from ubp_fom_system import FOMSystem
    fom = FOMSystem()
    frame = fom.select_frame('Number Theory')
    results['fom'] = f'OK: frame={frame}'
except Exception as e:
    results['fom'] = f'FAIL: {e}'

# 11. Integrated Engine (Penta-audit)
try:
    from ubp_integrated_engine_v1 import UBPIntegratedEngineV1
    eng = UBPIntegratedEngineV1()
    audit = eng.run_penta_audit('prime number theory', [1,0,1,1,0,0,1,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0])
    results['integrated'] = f'OK: keys={list(audit.keys())[:4]}'
except Exception as e:
    results['integrated'] = f'FAIL: {e}'

# 12. MoE Cortex research method
try:
    from ubp_moe_cortex_v2 import UBPMoECortexV2
    moe2 = UBPMoECortexV2()
    # Test the research method with a math-domain query
    resp2 = moe2.research('divisibility modular arithmetic', max_words=8)
    results['moe_math_query'] = f'OK: "{resp2}"'
except Exception as e:
    results['moe_math_query'] = f'FAIL: {e}'

# Print results
print("\n" + "="*60)
print("PURE UBP ENGINE AUDIT — NO EXTERNAL DEPENDENCIES")
print("="*60)
ok_count = 0
for name, status in results.items():
    icon = 'OK ' if status.startswith('OK') else 'ERR'
    print(f"  [{icon}] {name:25s}: {status[:80]}")
    if status.startswith('OK'):
        ok_count += 1
print("="*60)
print(f"  {ok_count}/{len(results)} engines operational")
print("="*60)
