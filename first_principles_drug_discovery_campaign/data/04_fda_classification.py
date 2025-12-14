#!/usr/bin/env python3
"""
Step 4: FDA Classification Layer

Simulates regulatory classification of drug candidates based on "First Principles"
(UBP - Universal Binary Proteomics) profiles using FDA-style categories.

Classification Criteria:
- Class I (Breakthrough Therapy): Docking Distance ≤ 2 AND Syndrome Weight ≤ 3
- Class II (Priority Review): Docking Distance ≤ 3 AND Syndrome Weight ≤ 4
- Class III (Standard Review): All other non-toxic candidates

Author: K-Dense System
Date: 2025-12-11
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Session paths
SESSION_DIR = Path("/app/sandbox/session_20251211_141515_ba86f641fd8f")
WORKFLOW_DIR = SESSION_DIR / "workflow"
RESULTS_DIR = SESSION_DIR / "results"

# Input/Output files
INPUT_FILE = WORKFLOW_DIR / "analysis_results.json"
OUTPUT_JSON = WORKFLOW_DIR / "fda_classification_results.json"
OUTPUT_SUMMARY = WORKFLOW_DIR / "fda_submission_summary.txt"

# Classification thresholds
CLASS_I_THRESHOLDS = {
    "docking_distance": 2,
    "syndrome_weight": 3,
    "name": "Class I - Breakthrough Therapy Designation",
    "description": "High complementarity and high structural stability"
}

CLASS_II_THRESHOLDS = {
    "docking_distance": 3,
    "syndrome_weight": 4,
    "name": "Class II - Priority Review",
    "description": "Good complementarity and structural stability"
}

CLASS_III = {
    "name": "Class III - Standard Review",
    "description": "Standard candidates meeting basic safety criteria"
}


def load_analysis_results() -> Dict[str, Any]:
    """Load analysis results from previous step."""
    print(f"Loading analysis results from: {INPUT_FILE}")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Analysis results not found: {INPUT_FILE}")

    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    ranked_candidates = data.get('ranked_non_toxic', [])
    metadata = data.get('metadata', {})

    print(f"✓ Loaded {len(ranked_candidates)} non-toxic candidates")
    print(f"  Target: {metadata.get('target_chembl_id', 'N/A')}")
    print(f"  Toxicity mask: {metadata.get('toxicity_mask', 'N/A')}")

    return data


def classify_candidate(candidate: Dict[str, Any]) -> str:
    """
    Classify a candidate based on UBP metrics.

    Returns:
        Classification label: 'Class I', 'Class II', or 'Class III'
    """
    docking_distance = candidate.get('docking_distance', float('inf'))
    syndrome_weight = candidate.get('syndrome_weight', float('inf'))

    # Class I: Breakthrough Therapy
    if (docking_distance <= CLASS_I_THRESHOLDS['docking_distance'] and
        syndrome_weight <= CLASS_I_THRESHOLDS['syndrome_weight']):
        return 'Class I'

    # Class II: Priority Review
    elif (docking_distance <= CLASS_II_THRESHOLDS['docking_distance'] and
          syndrome_weight <= CLASS_II_THRESHOLDS['syndrome_weight']):
        return 'Class II'

    # Class III: Standard Review
    else:
        return 'Class III'


def classify_top_candidates(ranked_candidates: List[Dict], n_candidates: int = 50) -> Dict[str, Any]:
    """
    Classify the top N candidates.

    Args:
        ranked_candidates: List of candidates (already ranked)
        n_candidates: Number of top candidates to classify

    Returns:
        Dictionary with classification results
    """
    print(f"\n=== Classifying Top {n_candidates} Candidates ===")

    # Take top N candidates
    top_n = ranked_candidates[:n_candidates]

    # Initialize classification buckets
    classifications = {
        'Class I': [],
        'Class II': [],
        'Class III': []
    }

    # Classify each candidate
    for i, candidate in enumerate(top_n, 1):
        classification = classify_candidate(candidate)

        # Add classification info to candidate
        candidate_classified = candidate.copy()
        candidate_classified['fda_classification'] = classification
        candidate_classified['rank'] = i

        classifications[classification].append(candidate_classified)

        if i <= 10 or i % 10 == 0:
            print(f"  [{i}/{n_candidates}] {candidate['chembl_id']}: {classification} "
                  f"(DD={candidate['docking_distance']}, SW={candidate['syndrome_weight']})")

    # Summary statistics
    print(f"\n=== Classification Summary ===")
    print(f"  Class I (Breakthrough):  {len(classifications['Class I'])} candidates")
    print(f"  Class II (Priority):     {len(classifications['Class II'])} candidates")
    print(f"  Class III (Standard):    {len(classifications['Class III'])} candidates")
    print(f"  Total Classified:        {sum(len(v) for v in classifications.values())} candidates")

    return classifications


def generate_submission_package(candidate: Dict[str, Any], rank: int) -> Dict[str, Any]:
    """
    Generate a detailed Digital Submission Package for a candidate.

    Args:
        candidate: Candidate data dictionary
        rank: Overall rank of the candidate

    Returns:
        Submission package dictionary
    """
    package = {
        "submission_id": f"UBP-{candidate['chembl_id']}-{datetime.now().strftime('%Y%m%d')}",
        "rank": rank,
        "candidate_identification": {
            "chembl_id": candidate['chembl_id'],
            "hex_seed": candidate['seed_hex'],
            "decimal_seed": candidate['seed'],
            "smiles": candidate['smiles']
        },
        "mechanism_of_action": {
            "primary_mechanism": "Informational Complementarity via Hamming Resonance",
            "theoretical_basis": "Universal Binary Proteomics (UBP) First Principles",
            "description": "Candidate demonstrates complementary information-theoretic patterns with target protein structure, suggesting potential for selective molecular recognition."
        },
        "efficacy_profile": {
            "docking_distance": candidate['docking_distance'],
            "docking_interpretation": "Hamming distance from target (lower = better complementarity)",
            "syndrome_weight": candidate['syndrome_weight'],
            "syndrome_interpretation": "Error-correction weight (lower = higher structural stability)",
            "syndrome_correctable": candidate.get('syndrome_correctable', False)
        },
        "safety_profile": {
            "toxicity_status": "PASS - Non-toxic",
            "screening_method": "Bit-Mask Toxicity Screen",
            "toxicity_mask": "0x800001",
            "toxicity_details": "Candidate passed informational toxicity filters based on structural bit patterns"
        },
        "chemical_structure": {
            "smiles": candidate['smiles'],
            "molecular_signature": candidate.get('signature', {})
        },
        "regulatory_classification": {
            "fda_class": candidate['fda_classification'],
            "classification_basis": f"Docking Distance ≤ {candidate['docking_distance']}, Syndrome Weight ≤ {candidate['syndrome_weight']}"
        },
        "metadata": {
            "analysis_date": datetime.now().isoformat(),
            "methodology": "UBP First Principles Analysis",
            "data_source": "ChEMBL Database",
            "analysis_version": "1.0"
        }
    }

    return package


def generate_submission_packages(classifications: Dict[str, List], n_top: int = 5) -> List[Dict]:
    """
    Generate submission packages for the top N candidates across all classes.

    Args:
        classifications: Classification results dictionary
        n_top: Number of top candidates to generate packages for

    Returns:
        List of submission packages
    """
    print(f"\n=== Generating Submission Packages for Top {n_top} Candidates ===")

    # Combine all classified candidates and sort by rank
    all_classified = []
    for class_name, candidates in classifications.items():
        all_classified.extend(candidates)

    all_classified.sort(key=lambda x: x['rank'])

    # Generate packages for top N
    packages = []
    for candidate in all_classified[:n_top]:
        package = generate_submission_package(candidate, candidate['rank'])
        packages.append(package)

        print(f"  ✓ Package generated: {package['submission_id']} "
              f"(Rank {candidate['rank']}, {candidate['fda_classification']})")

    return packages


def save_results(classifications: Dict, packages: List[Dict], metadata: Dict):
    """Save classification results to JSON and summary to text file."""

    # Prepare JSON output
    output_data = {
        "metadata": {
            "analysis_date": datetime.now().isoformat(),
            "total_candidates_classified": sum(len(v) for v in classifications.values()),
            "classification_criteria": {
                "class_i": CLASS_I_THRESHOLDS,
                "class_ii": CLASS_II_THRESHOLDS,
                "class_iii": CLASS_III
            },
            "source_analysis": str(INPUT_FILE),
            "target_info": {
                "target_chembl_id": metadata.get('target_chembl_id'),
                "toxicity_mask": metadata.get('toxicity_mask')
            }
        },
        "classifications": classifications,
        "top_5_submission_packages": packages
    }

    # Save JSON
    print(f"\nSaving classification results to: {OUTPUT_JSON}")
    with open(OUTPUT_JSON, 'w') as f:
        json.dump(output_data, f, indent=2)
    print(f"✓ Saved {OUTPUT_JSON.name} ({OUTPUT_JSON.stat().st_size / 1024:.1f} KB)")

    # Generate human-readable summary
    generate_summary_report(classifications, packages, metadata)


def generate_summary_report(classifications: Dict, packages: List[Dict], metadata: Dict):
    """Generate human-readable summary report."""

    print(f"\nGenerating summary report: {OUTPUT_SUMMARY}")

    lines = []
    lines.append("=" * 80)
    lines.append("FDA CLASSIFICATION SUMMARY REPORT")
    lines.append("UBP First Principles Drug Discovery Pipeline")
    lines.append("=" * 80)
    lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    lines.append(f"Analysis Date: {metadata.get('analysis_date', 'N/A')}")
    lines.append(f"Target: {metadata.get('target_chembl_id', 'N/A')}")
    lines.append(f"Toxicity Screen Mask: {metadata.get('toxicity_mask', 'N/A')}")

    lines.append("\n" + "-" * 80)
    lines.append("CLASSIFICATION OVERVIEW")
    lines.append("-" * 80)

    total = sum(len(v) for v in classifications.values())
    for class_name in ['Class I', 'Class II', 'Class III']:
        count = len(classifications[class_name])
        percentage = (count / total * 100) if total > 0 else 0

        if class_name == 'Class I':
            desc = CLASS_I_THRESHOLDS['name']
            criteria = f"DD ≤ {CLASS_I_THRESHOLDS['docking_distance']}, SW ≤ {CLASS_I_THRESHOLDS['syndrome_weight']}"
        elif class_name == 'Class II':
            desc = CLASS_II_THRESHOLDS['name']
            criteria = f"DD ≤ {CLASS_II_THRESHOLDS['docking_distance']}, SW ≤ {CLASS_II_THRESHOLDS['syndrome_weight']}"
        else:
            desc = CLASS_III['name']
            criteria = "All other non-toxic candidates"

        lines.append(f"\n{class_name}: {desc}")
        lines.append(f"  Criteria: {criteria}")
        lines.append(f"  Candidates: {count} ({percentage:.1f}%)")

    lines.append("\n" + "=" * 80)
    lines.append("TOP 5 CANDIDATE SUBMISSION PACKAGES")
    lines.append("=" * 80)

    for i, package in enumerate(packages, 1):
        cand_id = package['candidate_identification']
        efficacy = package['efficacy_profile']
        regulatory = package['regulatory_classification']

        lines.append(f"\n{'─' * 80}")
        lines.append(f"RANK {i}: {cand_id['chembl_id']}")
        lines.append(f"{'─' * 80}")
        lines.append(f"Submission ID: {package['submission_id']}")
        lines.append(f"FDA Classification: {regulatory['fda_class']}")
        lines.append(f"\nCandidate Identification:")
        lines.append(f"  ChEMBL ID: {cand_id['chembl_id']}")
        lines.append(f"  Hex Seed: {cand_id['hex_seed']}")
        lines.append(f"  Decimal Seed: {cand_id['decimal_seed']}")
        lines.append(f"\nMechanism of Action:")
        lines.append(f"  {package['mechanism_of_action']['primary_mechanism']}")
        lines.append(f"  Basis: {package['mechanism_of_action']['theoretical_basis']}")
        lines.append(f"\nEfficacy Profile:")
        lines.append(f"  Docking Distance: {efficacy['docking_distance']} (Hamming distance from target)")
        lines.append(f"  Syndrome Weight: {efficacy['syndrome_weight']} (Error-correction weight)")
        lines.append(f"  Correctable: {'Yes' if efficacy['syndrome_correctable'] else 'No'}")
        lines.append(f"\nSafety Profile:")
        lines.append(f"  Status: {package['safety_profile']['toxicity_status']}")
        lines.append(f"  Method: {package['safety_profile']['screening_method']}")
        lines.append(f"  Mask: {package['safety_profile']['toxicity_mask']}")
        lines.append(f"\nChemical Structure (SMILES):")
        lines.append(f"  {cand_id['smiles']}")

    lines.append("\n" + "=" * 80)
    lines.append("METHODOLOGY NOTES")
    lines.append("=" * 80)
    lines.append("""
This classification represents a novel "First Principles" approach to drug discovery
using Universal Binary Proteomics (UBP) and information-theoretic metrics:

1. Informational Docking: Candidates are evaluated based on Hamming distance
   (bit-wise complementarity) rather than traditional molecular docking.

2. Syndrome Analysis: Error-correction theory (Golay codes) is applied to assess
   structural stability and resilience.

3. Bit-Mask Toxicity Screening: Toxicity is predicted using structural bit patterns
   and information filters.

This represents a computational framework for molecular screening that prioritizes
information-theoretic compatibility over traditional structure-activity relationships.

DISCLAIMER: This is a simulated regulatory classification based on computational
metrics. Actual FDA submissions require extensive preclinical and clinical validation.
""")

    lines.append("=" * 80)
    lines.append("END OF REPORT")
    lines.append("=" * 80)

    # Write to file
    report_text = "\n".join(lines)
    with open(OUTPUT_SUMMARY, 'w') as f:
        f.write(report_text)

    print(f"✓ Saved {OUTPUT_SUMMARY.name} ({OUTPUT_SUMMARY.stat().st_size / 1024:.1f} KB)")


def main():
    """Main execution function."""
    print("=" * 80)
    print("FDA CLASSIFICATION LAYER - Step 4")
    print("UBP First Principles Drug Discovery Pipeline")
    print("=" * 80)

    try:
        # Load analysis results
        data = load_analysis_results()
        ranked_candidates = data['ranked_non_toxic']
        metadata = data['metadata']

        # Classify top 50 candidates
        classifications = classify_top_candidates(ranked_candidates, n_candidates=50)

        # Generate submission packages for top 5
        submission_packages = generate_submission_packages(classifications, n_top=5)

        # Save results
        save_results(classifications, submission_packages, metadata)

        print("\n" + "=" * 80)
        print("✓ FDA Classification Layer Complete")
        print("=" * 80)
        print(f"\nOutputs:")
        print(f"  - {OUTPUT_JSON}")
        print(f"  - {OUTPUT_SUMMARY}")
        print("\nClassification Summary:")
        print(f"  Class I (Breakthrough):  {len(classifications['Class I'])} candidates")
        print(f"  Class II (Priority):     {len(classifications['Class II'])} candidates")
        print(f"  Class III (Standard):    {len(classifications['Class III'])} candidates")
        print(f"  Top 5 Packages:          {len(submission_packages)} generated")

        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
