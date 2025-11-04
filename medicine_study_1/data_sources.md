# Pharmaceutical Data Sources for UBP Medicine Study

## ChEMBL Database (Release 36)
- **URL**: https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/
- **Release**: ChEMBL 36 (July 2025)
- **Size**: 2.9M compounds, 1.9M assays
- **License**: Creative Commons Attribution-ShareAlike 3.0

### Key Files Available:
1. **chembl_36_chemreps.txt.gz** (274M) - Chemical representations including SMILES, InChI
2. **chembl_36.sdf.gz** (893M) - Full structure data file
3. **chembl_36_sqlite.tar.gz** (5.2G) - Complete SQLite database
4. **chembl_36.h5** (309M) - HDF5 format for Python analysis

### Data Contents:
- FDA-approved drugs with clinical efficacy data
- Bioactivity measurements (IC50, Ki, EC50)
- Target information (proteins, genes)
- Molecular properties (MW, LogP, etc.)
- Therapeutic indications

## Strategy for Pilot Study (~100 compounds):
1. Download chembl_36_chemreps.txt.gz for molecular structures
2. Use ChEMBL web services API to query FDA-approved drugs
3. Filter for compounds with:
   - Known clinical efficacy data
   - Multiple therapeutic classes
   - Molecular weight 150-1000 Da
   - Available bioactivity data

## Strategy for Full Study (~1000 compounds):
1. Download full SQLite database
2. Query for all FDA-approved drugs across therapeutic classes
3. Include clinical candidates with Phase III data
4. Ensure diverse representation across:
   - Cardiovascular (100+)
   - Oncology (150+)
   - CNS/Neurology (100+)
   - Anti-infectives (150+)
   - Metabolic (100+)
   - Immunology (100+)
   - Other classes (300+)
