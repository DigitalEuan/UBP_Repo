#!/bin/bash
# Master script to run all analysis modules
# Author: Euan R A Craig
# Date: October 15, 2025

echo "========================================================================"
echo "BLACK HOLES QUANTUM TUNNELING STUDY - COMPLETE ANALYSIS"
echo "Universal Binary Principle (UBP) v3.2"
echo "========================================================================"
echo ""

cd /home/ubuntu/black_holes_quantum_tunnelling

echo "Running Module 1: Classical Hawking Temperature Analysis..."
python3.11 code/module1_classical_hawking.py 2>&1 | grep -v "glyph" | tail -20
echo ""

echo "Running Module 2: UBP Calibration and Mapping..."
python3.11 code/module2_ubp_calibration.py 2>&1 | grep -v "glyph" | tail -20
echo ""

echo "Running Module 3: 6D Bitfield Black Hole Queue Model..."
python3.11 code/module3_bh_queue_model.py 2>&1 | grep -v "glyph" | tail -20
echo ""

echo "Running Module 4: Self-Observing Helix and MQT Boost..."
python3.11 code/module4_helix_mqt.py 2>&1 | grep -v "glyph" | tail -20
echo ""

echo "Running Module 5: Extended Metrics (Kerr and RN)..."
python3.11 code/module5_extended_metrics.py 2>&1 | grep -v "glyph" | tail -20
echo ""

echo "========================================================================"
echo "ALL MODULES COMPLETE"
echo "========================================================================"
echo ""
echo "Generated files:"
ls -lh data/*.csv | wc -l | xargs echo "  Data files:"
ls -lh figures/*.png | wc -l | xargs echo "  Figures:"
echo ""
echo "Study ready for documentation and GitHub packaging."
echo "========================================================================"
