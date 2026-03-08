# UBP Geometric Virology v3.0 — Project Whiteboard

## Goal
Expand from 12 proteins to 50+ across all major pathogens, build predictive surveillance pipeline, run full therapeutic screening, produce journal-ready paper + upgraded interactive tool.

## Phase Status
- [ ] Phase 1: Data gathering (50+ proteins)
- [ ] Phase 2: KB construction (SOP_002, all proteins)
- [ ] Phase 3: Full simulation suite (collider, TGIC, cytokine)
- [ ] Phase 4: Predictive surveillance pipeline + statistical validation
- [ ] Phase 5: Publication figures
- [ ] Phase 6: Journal paper (LaTeX)
- [ ] Phase 7: Upgraded web tool
- [ ] Phase 8: Package + deliver

## Protein Target List

### SARS-CoV-2 Variants of Concern (Spike proteins)
- [x] WT (B lineage) — from v2
- [x] Delta (B.1.617.2) — from v2
- [x] Omicron BA.1 — from v2
- [ ] Alpha (B.1.1.7)
- [ ] Beta (B.1.351)
- [ ] Gamma (P.1)
- [ ] Omicron BA.2
- [ ] Omicron BA.4/5
- [ ] Omicron XBB.1.5
- [ ] Omicron JN.1

### SARS-CoV-2 Structural Proteins (WT)
- [x] Spike WT — from v2
- [x] Spike RBD — from v2
- [x] Nucleocapsid — from v2
- [x] Membrane — from v2
- [x] Envelope — from v2
- [ ] NSP3 (papain-like protease)
- [ ] NSP5 (3CL main protease — drug target)
- [ ] NSP12 (RNA polymerase — Remdesivir target)

### Influenza
- [x] HA H3N2 — from v2
- [ ] HA H1N1 (seasonal)
- [ ] HA H5N1 (avian, high pathogenicity)
- [ ] NA N1 (neuraminidase — Oseltamivir target)
- [ ] NA N2
- [ ] M2 (ion channel — Amantadine target)

### HIV
- [x] gp120 — from v2
- [ ] gp41 (fusion protein)
- [ ] p24 (capsid)
- [ ] Integrase
- [ ] Protease (drug target)
- [ ] Reverse Transcriptase

### Dengue Virus
- [ ] Envelope protein (serotype 1)
- [ ] Envelope protein (serotype 2)
- [ ] NS5 (RNA polymerase)
- [ ] NS3 (helicase/protease)

### Ebola Virus
- [ ] Glycoprotein (GP)
- [ ] Nucleoprotein (NP)
- [ ] VP40 (matrix protein)

### RSV (Respiratory Syncytial Virus)
- [ ] Fusion protein (F) — Nirsevimab target
- [ ] Attachment protein (G)

### Enterovirus / Poliovirus
- [ ] VP1 capsid protein (EV-D68)
- [ ] 3C protease

### Host Proteins
- [x] ACE2 — from v2
- [ ] TMPRSS2 (SARS-CoV-2 entry co-factor)
- [ ] CD4 (HIV receptor)
- [ ] DC-SIGN (Dengue/Ebola receptor)

### Antibodies / Therapeutics
- [x] CR3022 — from v2
- [x] S309 (Sotrovimab) — from v2
- [ ] LY-CoV555 (Bamlanivimab)
- [ ] REGN10933 (Casirivimab)
- [ ] VRC01 (HIV broadly neutralizing)
- [ ] 2G12 (HIV gp120)
- [ ] mAb114 (Ebola — Ansuvimab)
- [ ] Oseltamivir (small molecule — Influenza NA inhibitor)
- [ ] Remdesivir (small molecule — NSP12 inhibitor)

## Key Metrics to Track
- Leech Tax range across all proteins
- Tilt Angle distribution
- NRCI values
- Correlation: Tax vs R0 (transmissibility)
- Correlation: Gap Score vs IC50 (antibody potency)
- Correlation: Tilt vs transmissibility

## Data Sources
- UniProt (physicochemical properties)
- NCBI Protein database
- PDB (structural data)
- Published literature (Scheller 2020, Mancini 2024, etc.)
- ExPASy ProtParam (pI, MW, GRAVY, secondary structure)

## Notes
- All continuous values must be converted to integer fractions for UBP compliance
- Golay encoding requires 24-bit vectors — use 12 primary + 12 secondary descriptors
- Hamming distances between proteins must be ≥4 bits for meaningful differentiation
