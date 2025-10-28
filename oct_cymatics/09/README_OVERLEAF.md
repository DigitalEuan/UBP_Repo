# UBP Cymatics Study - Phase III: Overleaf Package

## Quick Start Guide

### 1. Upload to Overleaf

**Option A: Zip Upload (Recommended)**
1. Download `ubp_phase_iii_overleaf.zip` from your AI Drive
2. Go to https://www.overleaf.com/project
3. Click "New Project" → "Upload Project"
4. Select the ZIP file
5. Wait for extraction to complete

**Option B: Manual Upload**
1. Create new blank project in Overleaf
2. Upload `ubp_cymatics_phase_iii_paper.tex` as main document
3. Create folders: `figures/`, `data/`, `code/`
4. Upload contents of each folder to corresponding Overleaf folders

### 2. Compile Settings

- **Compiler**: pdfLaTeX
- **Main document**: `ubp_cymatics_phase_iii_paper.tex`
- **Auto-compile**: Recommended (on)

### 3. First Compilation

Click "Recompile" button. The document should compile cleanly with:
- No errors
- Possibly some warnings about font glyphs (subscripts) - these are cosmetic only
- Output: ~15-20 pages PDF

---

## Package Contents

### Main Document
- `ubp_cymatics_phase_iii_paper.tex` - Complete scientific paper (24 KB)

### Figures (3 visualizations)
- `phase_iii_crv_spectrum.png` - CRV frequency spectrum with Y corrections
- `phase_iii_validation_patterns.png` - Predicted cymatic patterns for experimental validation
- `phase_iii_y_analysis.png` - Comprehensive Y constant analysis (6-panel figure)

### Data (JSON format)
- `phase_iii_planck_mass_refined.json` - Best Planck Mass result (5.8% error)
- `phase_iii_cymatics_results.json` - Complete cymatics study data
- `phase_iii_validation_patterns.json` - Experimental validation protocols
- `phase_iii_planck_mass.json` - Initial Planck Mass results (72% error - superseded)

### Code (Python implementations)
- `ubp_phase_iii_advancement.py` - Main Phase III implementation (28 KB)
- `phase_iii_visualizations.py` - Visualization generation and refined derivations (18 KB)

### Documentation
- `PHASE_III_SUMMARY.md` - Executive summary and technical guide (15 KB)
- `README_OVERLEAF.md` - This file

---

## Document Structure

The paper follows standard scientific format:

1. **Abstract** - Summary of Phase III achievements
2. **Introduction** - Context, objectives, key contributions
3. **Theoretical Framework** - UBP concepts, Phase II discovery, Y constant interpretation
4. **Methodology** - Planck Mass derivation, CRV updates, cymatics simulation
5. **Results** - Planck Mass (5.8% error), updated CRVs, validation patterns
6. **Discussion** - Multiple Y constants, exponential relationships, QFT connections
7. **Conclusion** - Summary and future work
8. **Appendices** - Computational details, experimental protocols

**Total Pages**: ~15-20 (depending on figure placement)

**Word Count**: ~6,500 words

---

## Key Results Highlighted in Paper

### Planck Mass Scaling
```
Y_m = π/(5π² + 3) ≈ 0.0600136
m_p = sqrt(ℏc/G) × exp(-Y_m)
Error: 5.8248%
```

### Updated CRV Framework
- 9 fundamental constants with Y corrections
- Information Layer: Y-scaled (π, √2, Y)
- Reality/Activation: Standard scaling (φ, e, √3, τ, X_G, α)

### Experimental Validation
- 4 testable protocols at 3-18 kHz
- Predicted symmetries: Circular, Pentagonal, Square, Mixed
- Y-correction validation method via node spacing ratios

### Gravitational Constant (Phase II validated)
```
G = G_F × (√2/4) × c × Y
Error: 0.066%
```

---

## Editing the Paper

### Adding Figures

Current figures are included but not yet integrated into main text. To add:

```latex
\begin{figure}[H]
\centering
\includegraphics[width=0.9\textwidth]{figures/phase_iii_crv_spectrum.png}
\caption{Phase III CRV Frequency Spectrum showing Y-corrected (red) and standard (cyan) frequencies. Wall of Reality at $10^{12}$ Hz shown as dashed line.}
\label{fig:crv_spectrum}
\end{figure}
```

Place this in **Section 5.2 (Updated Core Resonance Values)** after Table 2.

### Referencing Figures

In text:
```latex
As shown in Figure \ref{fig:crv_spectrum}, Y-corrected CRVs...
```

### Customizing Content

**To shorten**: Remove or condense Appendix sections
**To expand**: Add more detail to Discussion section
**To add data**: Reference JSON files in Data section

---

## Figure Integration Recommendations

### Figure 1: CRV Spectrum (`phase_iii_crv_spectrum.png`)
- **Location**: Section 5.2, after Table 2
- **Purpose**: Visualize frequency distribution and Y-correction pattern
- **Width**: 0.9\textwidth

### Figure 2: Validation Patterns (`phase_iii_validation_patterns.png`)
- **Location**: Section 5.4, after Table 3
- **Purpose**: Show predicted cymatic geometries for experiments
- **Width**: 0.85\textwidth

### Figure 3: Y Analysis (`phase_iii_y_analysis.png`)
- **Location**: Section 4.3 or Section 6 (Discussion)
- **Purpose**: Comprehensive Y constant interpretation
- **Width**: \textwidth (full page width for 6-panel figure)

---

## LaTeX Packages Used

All required packages are already in preamble:

```latex
\usepackage[utf8]{inputenc}      % UTF-8 encoding
\usepackage{amsmath,amssymb}     % Mathematical symbols
\usepackage{graphicx}            % Figure inclusion
\usepackage{hyperref}            % Hyperlinks (references, citations)
\usepackage{geometry}            % Page margins
\usepackage{booktabs}            % Professional tables
\usepackage{float}               % Figure placement [H]
\usepackage{caption}             % Caption customization
```

No additional packages needed. Document should compile on any standard Overleaf instance.

---

## Common Issues and Solutions

### Issue 1: Figures Not Displaying
**Symptom**: Figure placeholders but no images
**Solution**: Check that PNG files are in `figures/` folder, not root directory

### Issue 2: Compilation Timeout
**Symptom**: "Compilation failed: timeout"
**Solution**: This shouldn't happen with current document size. If it does, remove some figures temporarily.

### Issue 3: Font Warnings (Subscript Glyphs)
**Symptom**: Warnings about missing subscript characters
**Solution**: These are cosmetic only. PDF will display correctly. Can ignore or change font to Computer Modern.

### Issue 4: Reference Errors
**Symptom**: "??" instead of figure/table numbers
**Solution**: Compile twice - LaTeX needs two passes to resolve cross-references

---

## Collaboration Settings

### For Solo Editing
- No special settings needed
- Compile on save (auto-compile on)

### For Multi-Author Collaboration
1. Share project via Overleaf "Share" button
2. Use "Track Changes" mode (Editor → Review)
3. Add comments with Ctrl+Shift+A
4. Use Git integration for version control (Project → Sync → GitHub)

---

## Export Options

### PDF Export
- Click "Download PDF" button (top right)
- PDF will include all figures and proper formatting

### Source Export
- Menu → Download → Source
- Downloads ZIP with all `.tex` files and figures

### Overleaf GitHub Sync (Advanced)
- Menu → Sync → GitHub
- Push to repository for version control
- Enables external LaTeX compilation

---

## Advanced Customization

### Change Paper Format
Current: `\documentclass[11pt,a4paper]{article}`

**For US Letter**:
```latex
\documentclass[11pt,letterpaper]{article}
```

**For Two-Column**:
```latex
\documentclass[11pt,twocolumn]{article}
```

**For Preprint Style**:
```latex
\documentclass[11pt,preprint]{revtex4-2}  % Physics journal style
```

### Adjust Margins
Current: `\geometry{margin=1in}`

**For wider margins**:
```latex
\geometry{margin=1.5in}
```

**For custom**:
```latex
\geometry{top=1in, bottom=1in, left=1.25in, right=1.25in}
```

### Add Author Affiliation
Current: Single author

**For multiple authors**:
```latex
\author{
    Euan R A Craig\thanks{Corresponding author: info@digitaleuan.com} \\
    \textit{Digital Euan Research, New Zealand} \\
    \and
    Collaborator Name \\
    \textit{Institution Name}
}
```

---

## Citation and BibTeX (Future Enhancement)

Currently uses `\begin{thebibliography}` (manual citations). To upgrade to BibTeX:

1. Create `references.bib` file:
```bibtex
@article{phase_ii_report,
  author = {Craig, Euan R A},
  title = {UBP Cymatics Study - Phase II Completion Report},
  year = {2025},
  publisher = {Digital Euan Research}
}
```

2. Replace bibliography section with:
```latex
\bibliographystyle{plain}
\bibliography{references}
```

3. Upload `references.bib` to Overleaf project root

---

## Data Access in LaTeX (Optional)

To include data from JSON files in tables:

**Method 1: Manual Copying**
- Open JSON file
- Copy values into LaTeX tables

**Method 2: Python Integration (Advanced)**
- Use Python script to generate LaTeX table code
- Copy-paste generated code into document

**Method 3: External Processing**
- Process JSON with external tool
- Generate CSV
- Use `\usepackage{csvsimple}` to import

---

## Recommended Workflow

### Initial Compilation
1. Upload package to Overleaf
2. Compile to check for errors
3. Review PDF output
4. Check all tables and equations render correctly

### Content Editing
1. Read through paper completely
2. Add/edit sections as needed
3. Insert figures at appropriate locations
4. Update references and citations

### Figure Integration
1. Add Figure 1 (CRV Spectrum) to Section 5.2
2. Add Figure 2 (Validation Patterns) to Section 5.4
3. Add Figure 3 (Y Analysis) to Discussion section
4. Adjust sizes and captions

### Final Review
1. Check all cross-references resolve (no ??)
2. Verify all tables are properly formatted
3. Ensure all equations compile correctly
4. Review figure quality (should be high-res)
5. Check bibliography formatting

### Export
1. Download final PDF
2. Download source ZIP (backup)
3. Share Overleaf link (if collaborating)

---

## Support and Troubleshooting

### Overleaf Documentation
- https://www.overleaf.com/learn

### LaTeX Help
- https://www.overleaf.com/learn/latex/Main_Page

### Contact for Phase III Technical Questions
- **Email**: info@digitaleuan.com
- **GitHub**: https://github.com/DigitalEuan

---

## Version Information

**Phase III Package Version**: 1.0
**Date**: October 2025
**LaTeX Compiler**: pdfLaTeX
**Tested on**: Overleaf (2024/2025 versions)

---

## Next Steps After Compilation

1. **Review Content**: Read through compiled PDF, check for accuracy
2. **Add Figures**: Integrate the 3 PNG visualizations at recommended locations
3. **Expand Discussion**: Add more theoretical interpretation if desired
4. **Prepare Submission**: Format according to target journal requirements
5. **Experimental Validation**: Use protocols in Appendix to design physical experiments
6. **Phase IV Planning**: Use as foundation for extending to Planck Length, Time, etc.

---

## Quick Reference: Key Equations

```latex
% Y Constant
Y = \frac{\pi}{\pi^2 + 2} \approx 0.264675

% X_G Scaling
X_G = c \times Y = 7.9348 \times 10^7

% Gravitational Constant
G = G_F \times \frac{\sqrt{2}}{4} \times c \times Y

% Planck Mass (Phase III)
Y_m = \frac{\pi}{5\pi^2 + 3} \approx 0.0600136
m_p = \sqrt{\frac{\hbar c}{G}} \times e^{-Y_m}

% CRV Formula
\text{CRV} = f_{\text{base}} \times \kappa \times \lambda_{\text{layer}} \times Y_{\text{correction}}
```

---

## License and Attribution

**Content License**: Copyright © 2025 Euan R A Craig, Digital Euan Research

**Usage**: This package is provided for scientific research and publication purposes. When using or citing this work, please reference:

> Craig, E. R. A. (2025). "The Emergence of Physical Constants from Geometric Resonance: Phase III - Universal Applications of the Y Constant". Digital Euan Research, New Zealand.

---

## Acknowledgments in Paper

Current acknowledgments are minimal. To expand:

```latex
\section*{Acknowledgments}
This research builds upon the UBP 3.2+ framework and Phase II discoveries. 
Special thanks to [collaborators/institutions/funding sources]. 
Computational resources provided by [if applicable].
We acknowledge the open-source scientific computing community for tools 
enabling this analysis: NumPy, SciPy, Matplotlib, and LaTeX.
```

---

**End of Overleaf Package README**

For technical support with Phase III science, contact info@digitaleuan.com
For Overleaf/LaTeX help, see: https://www.overleaf.com/learn

Good luck with your paper! 🚀
