"""
UBP VIROLOGY KB BUILDER v2.0
==============================
Builds SOP_002-compliant KB entries with RICH multi-dimensional
molecular descriptors to ensure distinct vectors for each protein.

The math_dna string encodes:
- Molecular weight (Da)
- Isoelectric point (x100)
- GRAVY hydrophobicity (x1000)
- Secondary structure: alpha-helix %, beta-sheet %, loop %
- Amino acid count
- Functional class (numeric code)
- Binding affinity (where applicable)
- Mutation count (for variants)

This ensures each protein gets a genuinely unique 24-bit Golay vector.

Sources:
- Scheller et al. 2020 (PMC7283733) - MW, pI, GRAVY
- Mancini et al. 2024 (PMC11497030) - Secondary structure %
- Lan et al. 2020 (Nature) - RBD structure
- UniProt/ExPASy ProtParam
"""

import json
import sys
import hashlib
sys.path.append('/home/ubuntu/UBP_Repo/core_studio_v4.0/core')
from ubp_kb_architect import KBArchitect

def main():
    arch = KBArchitect()
    new_entries = {}

    # ============================================================
    # PROTEIN DEFINITIONS WITH FULL MOLECULAR DESCRIPTORS
    # Format: M=MW_Da|pI=pI*100|GRAVY=GRAVY*1000|Helix=pct|Sheet=pct|Loop=pct|AA=count|Class=N|...
    # All values are integers or fractions (no floats) per UBP SOP_002
    # ============================================================
    
    proteins = [
        {
            "ubp_id": "PROTEIN_VIRAL_SARS2_SPIKE_WT_001",
            "name": "[Protein: SARS-CoV-2 Spike Glycoprotein WT (S)]",
            "definition": "[Homotrimeric class I fusion protein. S1 binds ACE2 via RBD; S2 mediates membrane fusion. Furin cleavage site unique to SARS-CoV-2. pI=6.24 places it near neutral at physiological pH.]",
            # MW=141178 Da, pI=624/100, GRAVY=-79/1000, Helix=36%, Sheet=28%, Loop=36%, AA=1273, Class=1 (viral fusion)
            "math": "M=141178|pI=624/100|GRAVY=-79/1000|Helix=36|Sheet=28|Loop=36|AA=1273|Class=1|Furin=1",
            "hierarchy": "1xGLYCOPROTEIN_TRIMER",
            "tags": ["BIOLOGY", "PROTEIN", "VIRUS", "SARS_COV2", "SPIKE", "FUSION_PROTEIN", "IMMUNOLOGY"]
        },
        {
            "ubp_id": "PROTEIN_VIRAL_SARS2_SPIKE_RBD_001",
            "name": "[Protein: SARS-CoV-2 Spike RBD (S1 Receptor Binding Domain)]",
            "definition": "[Twisted five-stranded antiparallel beta-sheet core. Directly contacts ACE2 Lys31 and Lys353. pI=8.91 (basic); 26 kDa. 15 key contact residues with ACE2.]",
            # MW=26034 Da, pI=891/100, GRAVY=-120/1000, Helix=12%, Sheet=48%, Loop=40%, AA=223, Class=1
            "math": "M=26034|pI=891/100|GRAVY=-120/1000|Helix=12|Sheet=48|Loop=40|AA=223|Class=1|ACE2_contacts=15",
            "hierarchy": "1xDOMAIN_BETA_SHEET",
            "tags": ["BIOLOGY", "PROTEIN", "VIRUS", "SARS_COV2", "RBD", "IMMUNOLOGY", "EPITOPE"]
        },
        {
            "ubp_id": "PROTEIN_VIRAL_SARS2_NUCLEOCAPSID_001",
            "name": "[Protein: SARS-CoV-2 Nucleocapsid Protein (N)]",
            "definition": "[RNA-binding phosphoprotein. Highly basic pI=10.07. Primary diagnostic antigen. Forms dimers and higher-order oligomers. Not a vaccine target due to intracellular location.]",
            # MW=45626 Da, pI=1007/100, GRAVY=-971/1000, Helix=22%, Sheet=18%, Loop=60%, AA=419, Class=2 (RNA binding)
            "math": "M=45626|pI=1007/100|GRAVY=-971/1000|Helix=22|Sheet=18|Loop=60|AA=419|Class=2|Diag=1",
            "hierarchy": "1xPHOSPHOPROTEIN",
            "tags": ["BIOLOGY", "PROTEIN", "VIRUS", "SARS_COV2", "NUCLEOCAPSID", "DIAGNOSTIC"]
        },
        {
            "ubp_id": "PROTEIN_VIRAL_SARS2_MEMBRANE_001",
            "name": "[Protein: SARS-CoV-2 Membrane Protein (M)]",
            "definition": "[Most abundant structural protein. Three transmembrane domains. Hydrophobic GRAVY=0.446. Drives viral assembly and budding. pI=9.51 (basic).]",
            # MW=25147 Da, pI=951/100, GRAVY=446/1000, Helix=55%, Sheet=10%, Loop=35%, AA=222, Class=3 (membrane)
            "math": "M=25147|pI=951/100|GRAVY=446/1000|Helix=55|Sheet=10|Loop=35|AA=222|Class=3|TM_domains=3",
            "hierarchy": "1xTRANSMEMBRANE_PROTEIN",
            "tags": ["BIOLOGY", "PROTEIN", "VIRUS", "SARS_COV2", "MEMBRANE", "ASSEMBLY"]
        },
        {
            "ubp_id": "PROTEIN_VIRAL_SARS2_ENVELOPE_001",
            "name": "[Protein: SARS-CoV-2 Envelope Protein (E)]",
            "definition": "[Smallest structural protein. Viroporin (ion channel). Extremely hydrophobic GRAVY=1.128. Single transmembrane domain. pI=8.57. Critical for viral pathogenesis.]",
            # MW=8365 Da, pI=857/100, GRAVY=1128/1000, Helix=70%, Sheet=5%, Loop=25%, AA=75, Class=4 (viroporin)
            "math": "M=8365|pI=857/100|GRAVY=1128/1000|Helix=70|Sheet=5|Loop=25|AA=75|Class=4|Ion_channel=1",
            "hierarchy": "1xVIROPORIN",
            "tags": ["BIOLOGY", "PROTEIN", "VIRUS", "SARS_COV2", "ENVELOPE", "ION_CHANNEL"]
        },
        {
            "ubp_id": "PROTEIN_VIRAL_INFLUENZA_HA_H3N2_001",
            "name": "[Protein: Influenza A Hemagglutinin H3N2 (HA)]",
            "definition": "[Class I fusion protein. Binds sialic acid alpha-2,6 linkages. pH 5.0-5.5 triggers irreversible conformational change to post-fusion state. Metastable prefusion trimer. pI=5.8.]",
            # MW=63800 Da, pI=580/100, GRAVY=-120/1000, Helix=38%, Sheet=22%, Loop=40%, AA=566, Class=1
            "math": "M=63800|pI=580/100|GRAVY=-120/1000|Helix=38|Sheet=22|Loop=40|AA=566|Class=1|pH_trigger=550",
            "hierarchy": "1xGLYCOPROTEIN_TRIMER",
            "tags": ["BIOLOGY", "PROTEIN", "VIRUS", "INFLUENZA", "HEMAGGLUTININ", "FUSION_PROTEIN"]
        },
        {
            "ubp_id": "PROTEIN_VIRAL_HIV_GP120_001",
            "name": "[Protein: HIV-1 Envelope Glycoprotein gp120]",
            "definition": "[Heavily glycosylated; 50% mass is N-linked carbohydrate. Binds CD4 then CCR5/CXCR4. Conformational masking shields conserved epitopes. pI=8.3. 5 variable loops (V1-V5).]",
            # MW=120000 Da, pI=830/100, GRAVY=-450/1000, Helix=15%, Sheet=35%, Loop=50%, AA=856, Class=1
            "math": "M=120000|pI=830/100|GRAVY=-450/1000|Helix=15|Sheet=35|Loop=50|AA=856|Class=1|Glycan_shield=1|V_loops=5",
            "hierarchy": "1xGLYCOPROTEIN",
            "tags": ["BIOLOGY", "PROTEIN", "VIRUS", "HIV", "ENVELOPE", "FUSION_PROTEIN", "GLYCAN_SHIELD"]
        },
        {
            "ubp_id": "PROTEIN_HOST_ACE2_001",
            "name": "[Protein: Human ACE2 Receptor (hACE2)]",
            "definition": "[Zinc metalloprotease. SARS-CoV-2 entry receptor. Expressed in lung type II pneumocytes, heart, kidney, gut. pI=5.35 (acidic). Cleaves angiotensin II. 805 amino acids.]",
            # MW=92500 Da, pI=535/100, GRAVY=-210/1000, Helix=42%, Sheet=18%, Loop=40%, AA=805, Class=5 (receptor)
            "math": "M=92500|pI=535/100|GRAVY=-210/1000|Helix=42|Sheet=18|Loop=40|AA=805|Class=5|Zn_metalloprotease=1",
            "hierarchy": "1xRECEPTOR_METALLOPROTEASE",
            "tags": ["BIOLOGY", "PROTEIN", "HOST", "RECEPTOR", "ACE2", "SARS_COV2"]
        },
        {
            "ubp_id": "PROTEIN_ANTIBODY_CR3022_001",
            "name": "[Protein: Neutralizing Antibody CR3022 (anti-SARS RBD)]",
            "definition": "[IgG1 antibody isolated from SARS-CoV-1 convalescent patient. Cross-reactive with SARS-CoV-2 RBD cryptic epitope. Kd=6.3 nM. PDB:6W41. Partial neutralization only.]",
            # MW=148000 Da, pI=720/100, GRAVY=-380/1000, Helix=12%, Sheet=55%, Loop=33%, AA=1330, Class=6 (antibody)
            "math": "M=148000|pI=720/100|GRAVY=-380/1000|Helix=12|Sheet=55|Loop=33|AA=1330|Class=6|Kd=63/10|PDB=6W41",
            "hierarchy": "1xIGG1_ANTIBODY",
            "tags": ["BIOLOGY", "PROTEIN", "ANTIBODY", "IMMUNOLOGY", "SARS_COV2", "NEUTRALIZING"]
        },
        {
            "ubp_id": "PROTEIN_ANTIBODY_S309_001",
            "name": "[Protein: Neutralizing Antibody S309 (Sotrovimab precursor)]",
            "definition": "[Broadly neutralizing IgG1. Binds SARS-CoV-2 RBD at conserved N-glycan site. Kd=0.6 nM. Basis for Sotrovimab therapeutic. Retains partial activity vs Omicron (IC50=8.2 nM).]",
            # MW=148000 Da, pI=780/100, GRAVY=-350/1000, Helix=12%, Sheet=55%, Loop=33%, AA=1330, Class=6
            "math": "M=148000|pI=780/100|GRAVY=-350/1000|Helix=12|Sheet=55|Loop=33|AA=1330|Class=6|Kd=6/10|PDB=6WPS|Broad=1",
            "hierarchy": "1xIGG1_ANTIBODY",
            "tags": ["BIOLOGY", "PROTEIN", "ANTIBODY", "IMMUNOLOGY", "SARS_COV2", "NEUTRALIZING", "THERAPEUTIC"]
        },
        {
            "ubp_id": "PROTEIN_VIRAL_SARS2_OMICRON_SPIKE_001",
            "name": "[Protein: SARS-CoV-2 Omicron BA.1 Spike (Variant of Concern)]",
            "definition": "[32 spike mutations vs WT; 15 in RBD. Enhanced ACE2 affinity. Significant immune escape from prior immunity. Altered charge distribution: pI=6.31 vs WT 6.24. Lower hydrophobicity.]",
            # MW=141500 Da, pI=631/100, GRAVY=-82/1000, Helix=36%, Sheet=27%, Loop=37%, AA=1273, Mut=32
            "math": "M=141500|pI=631/100|GRAVY=-82/1000|Helix=36|Sheet=27|Loop=37|AA=1273|Class=1|Furin=1|Mut=32|RBD_mut=15",
            "hierarchy": "1xGLYCOPROTEIN_TRIMER",
            "tags": ["BIOLOGY", "PROTEIN", "VIRUS", "SARS_COV2", "SPIKE", "OMICRON", "VARIANT", "IMMUNE_ESCAPE"]
        },
        {
            "ubp_id": "PROTEIN_VIRAL_SARS2_DELTA_SPIKE_001",
            "name": "[Protein: SARS-CoV-2 Delta B.1.617.2 Spike (Variant of Concern)]",
            "definition": "[9 spike mutations vs WT; 2 in RBD (L452R, T478K). P681R at furin cleavage site enhances processing. Enhanced ACE2 affinity. pI=6.27. Increased transmissibility and severity.]",
            # MW=141300 Da, pI=627/100, GRAVY=-80/1000, Helix=36%, Sheet=28%, Loop=36%, AA=1273, Mut=9
            "math": "M=141300|pI=627/100|GRAVY=-80/1000|Helix=36|Sheet=28|Loop=36|AA=1273|Class=1|Furin=1|Mut=9|RBD_mut=2|P681R=1",
            "hierarchy": "1xGLYCOPROTEIN_TRIMER",
            "tags": ["BIOLOGY", "PROTEIN", "VIRUS", "SARS_COV2", "SPIKE", "DELTA", "VARIANT"]
        }
    ]

    print(f"Building {len(proteins)} SOP_002-compliant viral protein KB entries...")
    print("=" * 60)

    for p in proteins:
        fp, entry = arch.create_entry(
            ubp_id=p['ubp_id'],
            lexicon_name=p['name'],
            definition=p['definition'],
            math_dna=p['math'],
            hierarchy=p['hierarchy'],
            tags=p['tags']
        )
        new_entries[fp] = entry
        print(f"  {p['ubp_id']}")
        print(f"    Vector: {entry['atlas']['vector']}")
        print(f"    NRCI:   {entry['atlas']['nrci_score']}")
        print(f"    Tax:    {entry['atlas']['tax'][:40]}...")
        print(f"    Tilt:   {entry['atlas']['tilt']}°")
        print()

    with open('/home/ubuntu/virology_kb_entries_v2.json', 'w') as f:
        json.dump(new_entries, f, indent=2)

    print(f"Saved {len(new_entries)} entries to virology_kb_entries_v2.json")
    
    # Verify uniqueness
    vectors = [tuple(e['atlas']['vector']) for e in new_entries.values()]
    unique_vectors = set(vectors)
    print(f"\nVector uniqueness: {len(unique_vectors)}/{len(vectors)} unique vectors")
    
    # Show pairwise Hamming distances
    print("\nPairwise Hamming distances (first 6 proteins):")
    entries_list = list(new_entries.values())[:6]
    from ubp_core_v5_3_merged import BinaryLinearAlgebra
    for i in range(len(entries_list)):
        for j in range(i+1, len(entries_list)):
            d = BinaryLinearAlgebra.hamming_distance(
                entries_list[i]['atlas']['vector'],
                entries_list[j]['atlas']['vector']
            )
            print(f"  {entries_list[i]['ubp_id'][-15:]} vs {entries_list[j]['ubp_id'][-15:]}: d={d}")

if __name__ == "__main__":
    main()
