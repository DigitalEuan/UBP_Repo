import sys
from ubp_phenomenology_v4_2_6 import PhenomenologyEngine, DEF_SEMANTIC_HASH

def run_cheese_mould_study():
    print("--- UBP STUDY: DAIRY MYCOBIOTA GEOMETRY ---")
    engine = PhenomenologyEngine()
    
    # Entities extracted from Kure & Skaar (2019)
    # Group 1: Noble/Ripening Agents (Intentional)
    noble_moulds = [
        "Penicillium roqueforti",
        "Penicillium camemberti",
        "Geotrichum candidum"
    ]
    
    # Group 2: Spoilage Agents (Unintentional/Defects)
    spoilage_moulds = [
        "Penicillium commune",  # Dominant spoiler (42%)
        "Mucor racemosus",      # 'Cat-hair' defect
        "Penicillium solitum",
        "Penicillium crustosum"
    ]
    
    # Group 3: Mycotoxins (Persistent Entropy)
    toxins = [
        "Ochratoxin A",
        "Cyclopiazonic acid",
        "Sterigmatocystin",
        "Roquefortine C"
    ]
    
    results = []
    
    print(f"\n[ANALYSIS] Processing {len(noble_moulds) + len(spoilage_moulds) + len(toxins)} identities...")
    
    # Helper to run batch
    def process_group(group_name, items):
        print(f"\n--- GROUP: {group_name} ---")
        group_scores = []
        for name in items:
            # We use the standard Semantic Hash definition to map the Name -> 24-bit Vector
            data = {"value": name}
            res = engine.process_phenomenon(DEF_SEMANTIC_HASH, data)
            
            # Extract key metrics
            nrci = res['metrics']['nrci']
            tax = res['metrics']['symmetry_tax']
            regime = res['metrics']['coherence']
            
            results.append({
                "name": name,
                "group": group_name,
                "nrci": nrci,
                "tax": tax,
                "regime": regime
            })
            group_scores.append(nrci)
            
        # Calculate Group Average
        if group_scores:
            avg = sum(group_scores) / len(group_scores)
            print(f"  >> GROUP AVERAGE NRCI: {float(avg):.4f}")

    process_group("NOBLE (Ripening)", noble_moulds)
    process_group("SPOILAGE (Defects)", spoilage_moulds)
    process_group("TOXINS (Metabolites)", toxins)
    
    # Find the most coherent entity
    best = max(results, key=lambda x: x['nrci'])
    worst = min(results, key=lambda x: x['nrci'])
    
    print("\n--- STUDY CONCLUSIONS ---")
    print(f"Most Coherent: {best['name']} (NRCI: {float(best['nrci']):.4f} | {best['regime']})")
    print(f"Least Coherent: {worst['name']} (NRCI: {float(worst['nrci']):.4f} | {worst['regime']})")

if __name__ == "__main__":
    run_cheese_mould_study()