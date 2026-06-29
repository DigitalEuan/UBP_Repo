# UBP GLM v3.7 — Unified Standalone Build (Push June #4)
# Instructions for Use

This archive contains the consolidated single-file build of the UBP
Geometric Language Machine, incorporating ALL features from pushes #1-#4
(v3.4 -> v3.5 -> v3.6 -> v3.7) in one editable script with a table of contents.

------------------------------------------------------------------------------
## CONTENTS
------------------------------------------------------------------------------

UBP_GLM_v37_Unified/
+-- README_INSTRUCTIONS.txt      <- this file
+-- UBP_GLM_Push_June4_Report.md <- push #4 report (concise)
+-- glm_v37_unified.py           <- THE standalone script (everything in one file)
+-- v37_test_results.json        <- captured self-test output

------------------------------------------------------------------------------
## PREREQUISITES
------------------------------------------------------------------------------

1. Python 3.12+ (tested on 3.12.13)
2. SymPy 1.14+  (pip install sympy)
3. The original UBP_Repo cloned from github.com/DigitalEuan/UBP_Repo
   You need: UBP_Repo/core_studio_v4.0/core/ on disk, with
   ubp_system_kb.json co-located inside it (copy from
   core_studio_v4.0/system_kb/ubp_system_kb.json).

No other dependencies. The engine is stdlib-only apart from SymPy.

------------------------------------------------------------------------------
## SETUP
------------------------------------------------------------------------------

1. Clone the original repo (if not already present):
     git clone https://github.com/DigitalEuan/UBP_Repo.git

2. Co-locate the system KB:
     cp UBP_Repo/core_studio_v4.0/system_kb/ubp_system_kb.json \
        UBP_Repo/core_studio_v4.0/core/ubp_system_kb.json

3. Edit the UBP_CORE_PATH variable at the top of glm_v37_unified.py
   (line ~48) to point at your UBP_Repo/core_studio_v4.0/core/ directory.
   The default is:
     UBP_CORE_PATH = "/home/z/my-project/ubp_experiment/UBP_Repo/core_studio_v4.0/core"
   Change it to your actual path, e.g.:
     UBP_CORE_PATH = "/home/yourname/UBP_Repo/core_studio_v4.0/core"

------------------------------------------------------------------------------
## QUICK START - run the self-test (12 scenarios)
------------------------------------------------------------------------------

cd UBP_GLM_v37_Unified
python3 glm_v37_unified.py --test

This boots the full v3.7 runtime and runs 12 self-tests:
  A.  Crystallisation (hamiltonian + time -> thesis)
  B.  Calculation tool + lattice grounding (gcd(54,24) -> six)
  C.  Symbolic differentiation (d/dx x^2 -> 2*x)
  D.  Symbolic solve (solve x^2-4 -> [-2, 2])
  E.  Multi-zone routing (2 zones spawned)
  F.  Contradiction detection (boson <-> fermion)
  G.  Autonomous maturation (18 inferred nouns from one seed)
  H.  Warm-start (matches prior crystallised idea)
  I.  Determinism (byte-identical across runs)
  J.  CRG auto-expansion (6 auto-proposed edges)
  K.  Contradiction-driven pivot (spawns competing zone)
  L.  Cross-zone synthesis (unifying meta-thesis)

Expected: 12/12 PASS.

------------------------------------------------------------------------------
## INTERACTIVE USE
------------------------------------------------------------------------------

Single query:
  python3 glm_v37_unified.py --chat "What is gcd(54, 24)?"
  python3 glm_v37_unified.py --chat "differentiate x^3 with respect to x"
  python3 glm_v37_unified.py --chat "Tell me about the hamiltonian and time."

Or in a Python REPL:

    import sys
    sys.path.insert(0, '.')           # or your path to the script
    from glm_v37_unified import GLMRuntimeV37

    rt = GLMRuntimeV37()

    # Basic chat - ideas accumulate, decay, crystallise
    print(rt.chat("Tell me about the hamiltonian and time."))
    print(rt.chat("What about symmetry?"))
    print(rt.chat("What does it generate?"))          # 'it' -> hamiltonian

    # Autonomous maturation (let it think between turns)
    rt.mature(5)                                      # 5 autonomous ticks
    print(rt.idea_state())                            # full multi-zone state

    # Computation - results ground as lattice evidence
    print(rt.chat("What is gcd(54, 24)?"))            # -> six (grounded)
    print(rt.chat("Compute sqrt(144)."))              # -> twelve (grounded)

    # Symbolic math (NEW in v3.7)
    print(rt.chat("differentiate x^2 with respect to x"))   # -> 2*x
    print(rt.chat("integrate 2*x dx"))                       # -> x^2
    print(rt.chat("solve x^2 - 4 for x"))                    # -> [-2, 2]
    print(rt.chat("simplify (x^2 - 1)/(x - 1)"))             # -> x + 1

    # Cross-zone synthesis (NEW in v3.7)
    mt = rt.synthesise()    # unify crystallised zones into a meta-thesis
    if mt: print(mt.thesis)

    # Reset for a new conversation (meta-graph persists for warm-start)
    rt.reset_idea()

------------------------------------------------------------------------------
## API SUMMARY (GLMRuntimeV37)
------------------------------------------------------------------------------

  rt = GLMRuntimeV37()                # boot (engine + CRG + numbers + meta-graph)
  rt.chat(query)                      # one NL turn; returns response string
  rt.mature(n)                        # run n autonomous ticks across all zones
  rt.adversarial()                    # stress-test the active zone's thesis
  rt.synthesise()                     # cross-zone meta-thesis (v3.7)
  rt.idea_state()                     # full structured state (all zones + meta-graph)
  rt.save_idea()                      # persist active crystallised zone to meta-graph
  rt.reset_idea()                     # start fresh (meta-graph retained)
  rt.explain(a, b)                    # direct CRG relation between two concepts
  rt.last_diag()                      # last turn's diagnostics

------------------------------------------------------------------------------
## TABLE OF CONTENTS (inside glm_v37_unified.py)
------------------------------------------------------------------------------

The script is organised by section markers (SSNN) for easy navigation
and editing. Search for the marker to jump to a section:

  SS00  CONFIGURATION & PATHS         - UBP_CORE_PATH, sys.path setup
  SS01  SUBSTRATE IMPORTS             - Golay/Leech engines, BLA, CRG
  SS02  CONSTANTS & TUNABLES          - thresholds, function words, pronouns
  SS03  CRG EXTENDED                  - contradiction edges + auto-expansion
  SS04  NUMBER VOCABULARY             - 55 derived number-word lattice points
  SS05  IDEA EVIDENCE                 - source-tagged evidence dataclass
  SS06  IDEA ZONE v3.7                - decay + ticks + re-crystallisation +
                                        contradiction-aware + adversarial
  SS07  IDEA MANAGER                  - multi-zone routing + cross-zone
                                        synthesis + contradiction-driven pivot
  SS08  IDEA META-GRAPH               - persistence + warm-start
  SS09  TOOLS LAYER                   - SymPy: arithmetic + diff/integral/solve
  SS10  RESPONSE COMPOSER v3.7        - confidence-tagged, multi-zone, synthesis
  SS11  RUNTIME v3.7                  - GLMRuntimeV37 (wires everything)
  SS12  CLI / TEST ENTRY POINT        - --test, --chat, --state

To grow the system further: add a new SSNN section and wire it into SS11.
All sections are self-contained and documented.

------------------------------------------------------------------------------
## CONFIDENCE TAGS (in responses)
------------------------------------------------------------------------------

  [computed]              - SymPy numeric result (highest confidence)
  [computed->grounded]    - result snapped to a lattice number-word
  [symbolic:differentiate] - SymPy symbolic operation (v3.7)
  [symbolic:solve]        - SymPy equation solving (v3.7)
  [CRG:generates]         - hand-curated Concept Relation Graph edge
  [CRG:auto]              - auto-proposed edge (v3.7, lower confidence)
  [KB]                    - looked up from the system knowledge base
  [inferred tick=N]       - autonomous tick discovered this
  [verify]                - ontological health (NRCI, symmetry tax)
  [CONTRADICTION]         - backbone contains a contradicting edge
  [META-THESIS]           - cross-zone unifying statement (v3.7)
  [I get it]              - idea crystallised (coherence >= 0.70)
  [I get it - PROVISIONAL] - counter-query landed, confidence reduced
  [I get it - refined]    - thesis refined after stronger edge arrived
  [warm-start]            - matched a prior crystallised idea
  [gap]                   - no verified vector for these tokens
  [zones: N active=M]     - multi-zone routing summary

------------------------------------------------------------------------------
## CUMULATIVE CAPABILITY STACK (v3.4 -> v3.7)
------------------------------------------------------------------------------

v3.4 (Push #1): IdeaZone + clean composer + defect fixes D1-D3 + anaphora
v3.5 (Push #2): + decay + autonomous ticks + re-crystallisation + calc tool
v3.6 (Push #3): + contradiction edges + adversarial + multi-zone + numbers
                + idea meta-graph (warm-start)
v3.7 (Push #4): + cross-zone synthesis (meta-thesis) + CRG auto-expansion
                + symbolic tools (diff/integral/solve/simplify)
                + contradiction-driven pivot (spawns competing zone)

ALL of the above is in the single glm_v37_unified.py file.

------------------------------------------------------------------------------
## NOTES
------------------------------------------------------------------------------

- Fully deterministic: same input -> byte-identical output (verified by test I).
- Boot: ~3-4 seconds (2,338-word vocab + 127-edge CRG + 6 auto + 55 numbers).
- Per-turn latency: 15-30ms (real-time chat).
- The meta-graph (idea_meta_graph.json) accumulates crystallised ideas across
  sessions. Delete it to start fresh.
- Non-destructive: imports from the original UBP_Repo without modifying it.
- The 24-bit Golay lattice is dense (min Hamming distance 8), so multi-zone
  spawning requires topics that are genuinely >6 bits apart. Physics concepts
  and number-words tend to be distant enough; closely-related physics concepts
  often route to the same zone.

Enjoy experimenting! - Z.ai Code
