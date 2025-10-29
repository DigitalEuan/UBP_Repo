# NIST Bell Test Data Sources

## Primary Data Repository

**NIST Bell Test Research Software and Data**
- URL: https://www.nist.gov/pml/applied-physics-division/bell-test-research-software-and-data/repository-bell-test-research-1
- Storage: Amazon S3 cloud
- Data from: Shalm et al. 2015 loophole-free Bell test

## Recommended Dataset for UBP Study

**21_15 Run with 200ns Additional Delay (Light Cone Shift)**

This is one of the main experimental runs used in the published paper.

### Alice Data
- File: `21_15_CH_pockel_100kHz.run.200nsadditiondelay_lightconeshift.alice.dat.compressed.zip`
- Size: 1.2 GB compressed
- URL: https://s3.amazonaws.com/bell-test-data/21_15_CH_pockel_100kHz.run.200nsadditiondelay_lightconeshift.alice.dat.compressed.zip

### Bob Data
- File: `21_15_CH_pockel_100kHz.run.200nsadditiondelay_lightconeshift.bob.dat.compressed.zip`
- Size: 1.3 GB compressed
- URL: https://s3.amazonaws.com/bell-test-data/21_15_CH_pockel_100kHz.run.200nsadditiondelay_lightconeshift.bob.dat.compressed.zip

## Alternative: Smaller Training Dataset

**03_31 Training Run**

Smaller dataset for initial testing and validation.

### Alice Data
- File: `03_31_CH_pockel_100kHz.run4.afterTimingfix2_training.alice.dat.compressed.zip`
- Size: 205.9 MB compressed
- URL: https://s3.amazonaws.com/bell-test-data/03_31_CH_pockel_100kHz.run4.afterTimingfix2_training.alice.dat.compressed.zip

### Bob Data
- File: `03_31_CH_pockel_100kHz.run4.afterTimingfix2_training.bob.dat.compressed.zip`
- Size: 216.4 MB compressed
- URL: https://s3.amazonaws.com/bell-test-data/03_31_CH_pockel_100kHz.run4.afterTimingfix2_training.bob.dat.compressed.zip

## Data Format (from quantum_grok_1.txt)

Based on the instructions in quantum_grok_1.txt:

- Format: Space-separated text files (.dat)
- Columns: ~256 columns per file
  - Col 0: Timestamp
  - Cols 1-2: Alice/Bob early +/− detector counts
  - Cols 3-4: Alice/Bob late +/− detector counts
  - Additional columns for time bins

- Binary extraction:
  - 1 if + detector click (count > 0)
  - 0 if − detector click (count > 0)
  - -1 for no-click (invalid trial)

- Valid pairs: Only use trials where both Alice and Bob have valid clicks

## Expected Data Characteristics

- Total trials: ~10^7 to 10^8 per run
- CHSH violation: S ≈ 2.4 (quantum prediction ≈ 2.828)
- Detection efficiency: ~75% (loophole-free threshold)
- Correlation: Strong anti-correlation for entangled pairs

## Download Strategy

1. Start with training dataset (03_31) for code validation
2. Download main dataset (21_15) for full analysis
3. Extract and process using code from quantum_grok_1.txt
4. Validate against published CHSH values from paper

