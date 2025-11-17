#!/bin/bash
################################################################################
# UBP Mineral Study Phase 2 - Complete Reproduction Script
################################################################################
# This script reproduces all analyses from the Phase 2 study
# Run from the project root directory: bash reproduce.sh
################################################################################

set -e  # Exit on error

echo "================================================================================"
echo "UBP MINERAL STUDY PHASE 2 - COMPLETE REPRODUCTION"
echo "================================================================================"
echo ""
echo "This script will reproduce all analyses and generate all results."
echo "Estimated time: 30-45 minutes"
echo ""
echo "Prerequisites:"
echo "  - Python 3.11"
echo "  - All packages from requirements.txt installed"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

# Create results directory
mkdir -p results

echo ""
echo "================================================================================"
echo "STEP 1: Data Processing (3,112 minerals)"
echo "================================================================================"
python3.11 process_kaggle_minerals.py
echo "✓ Data processing complete"

echo ""
echo "================================================================================"
echo "STEP 2: Phase 2 Coherence Analysis"
echo "================================================================================"
python3.11 phase2_coherence_analysis.py
echo "✓ Coherence analysis complete"

echo ""
echo "================================================================================"
echo "STEP 3: ML Boundary Mapping"
echo "================================================================================"
python3.11 phase2_ml_boundary_mapping.py
echo "✓ ML boundary mapping complete"

echo ""
echo "================================================================================"
echo "STEP 4: Higher-Dimensional Analysis (t-SNE, UMAP, PCA)"
echo "================================================================================"
python3.11 phase2_highdim_analysis.py
echo "✓ Higher-dimensional analysis complete"

echo ""
echo "================================================================================"
echo "STEP 5: Temporal and Defect Dynamics"
echo "================================================================================"
python3.11 phase2_temporal_defect_dynamics.py
echo "✓ Temporal/defect dynamics complete"

echo ""
echo "================================================================================"
echo "STEP 6: Foundational Principles Investigation"
echo "================================================================================"
python3.11 phase2_foundational_principles.py
echo "✓ Foundational principles complete"

echo ""
echo "================================================================================"
echo "STEP 7: VALIDATION - ML Comprehensive"
echo "================================================================================"
python3.11 validation_ml_comprehensive.py
echo "✓ ML validation complete"

echo ""
echo "================================================================================"
echo "STEP 8: VALIDATION - Threshold and Bimodality"
echo "================================================================================"
python3.11 validation_threshold_bimodality.py
echo "✓ Threshold/bimodality validation complete"

echo ""
echo "================================================================================"
echo "STEP 9: VALIDATION - Geometric Uncertainty"
echo "================================================================================"
python3.11 validation_geometric_uncertainty.py
echo "✓ Geometric uncertainty validation complete"

echo ""
echo "================================================================================"
echo "STEP 10: Accuracy Verification"
echo "================================================================================"
python3.11 phase2_accuracy_verification.py
echo "✓ Accuracy verification complete"

echo ""
echo "================================================================================"
echo "REPRODUCTION COMPLETE!"
echo "================================================================================"
echo ""
echo "All results have been generated in the results/ directory:"
echo ""
echo "Key Files:"
echo "  - results/phase2_coherence_analysis_3112.json"
echo "  - results/phase2_ml_summary.json"
echo "  - results/phase2_highdim_summary.json"
echo "  - results/validation_ml_comprehensive.json"
echo "  - results/validation_threshold_bimodality.json"
echo "  - results/validation_geometric_uncertainty.json"
echo ""
echo "Visualizations:"
echo "  - results/phase2_nrci_distribution.png"
echo "  - results/phase2_ml_roc_curves.png"
echo "  - results/phase2_highdim_3d_comparison.png"
echo "  - results/validation_ml_comprehensive.png"
echo "  - results/validation_threshold_bimodality.png"
echo "  - results/validation_geometric_uncertainty.png"
echo ""
echo "To verify results, compare checksums with reproducibility_checksums.txt"
echo ""
