# UBP Skill: Geometric Rational Reasoning

**Version:** 1.0
**Author:** E. R. A. Craig / Manus AI

## Overview

This skill provides a complete and faithful implementation of the **Universal Binary Principle (UBP)** system for geometric rational reasoning. It allows users and AI agents to perform topological navigation within the 24-dimensional Leech Lattice, leveraging the error-correcting properties of the Golay code to achieve deterministic, float-free, and logically sound conclusions.

The skill encapsulates the entire UBP reasoning pipeline, from concept vectorization and memory retrieval to self-aware coherence checking and knowledge base archival. It is designed for researchers, developers, and AI agents who require a rigorous, precise, and non-probabilistic reasoning framework.

## System Requirements

- Python 3.10+
- All core UBP scripts (included in the `scripts/` directory)

## Initialization

To use the skill, first import the main interface and get the reasoning engine instance:

```python
from scripts.ubp_geometric_reasoning_main import get_reasoning_engine

# Initialize the engine (loads the default knowledge base)
ubp = get_reasoning_engine()
```

## Key Capabilities

This skill exposes eight primary capabilities:

### 1. `vectorize_concept(concept: str)`

Performs the complete UBP vectorization protocol on a concept string.

-   **Arguments:**
    -   `concept` (str): The concept to vectorize.
-   **Returns:** (dict) A dictionary containing the `vector`, `fingerprint`, `domain`, `nrci`, and `hamming_weight`.

**Example:**
```python
result = ubp.vectorize_concept("Energy")
print(result)
# {
#   'concept': 'Energy',
#   'vector': [0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0],
#   'fingerprint': '...', 
#   'domain': 'SUBSTANCE', 
#   'nrci': 2.0, 
#   'hamming_weight': 12,
#   'errors_corrected': 1
# }
```

### 2. `reason_about(query: str)`

Executes the full, multi-layered reasoning pipeline on a natural language query.

-   **Arguments:**
    -   `query` (str): The natural language query.
-   **Returns:** (dict) A dictionary containing the `status`, `vector`, `resonance`, `coherence`, and `energy_cost`.

**Example:**
```python
result = ubp.reason_about("What is the nature of time?")
print(result)
# {
#   'status': 'ACCEPTED',
#   'concept': 'WHAT IS THE NATURE OF TIME?',
#   'vector_hex': '...', 
#   'resonance': {'anchor': 'TIME', 'distance': 0, 'type': 'PERFECT'},
#   'observer_metrics': {'action': 'MAINTAIN', 'coherence': 1.0, ...}
# }
```

### 3. `find_counterpart(concept: str, target_domain: str)`

Finds the geometric equivalent of a concept in a different Octad domain.

-   **Arguments:**
    -   `concept` (str): The source concept.
    -   `target_domain` (str): The target domain (e.g., "MECHANISM", "QUANTITY").
-   **Returns:** (dict) A dictionary containing the counterpart concept's information.

**Example:**
```python
result = ubp.find_counterpart("Hydrogen", "ALGORITHM")
print(result)
# {
#   'source_concept': 'Hydrogen',
#   'target_domain': 'ALGORITHM',
#   'counterpart': 'If-Then Logic',
#   'hamming_distance': 5,
#   'status': 'FOUND'
# }
```

### 4. `calculate_coherence(vector: List[int])`

Performs a deep coherence analysis on a 24-bit vector, including NRCI and tetradic health.

-   **Arguments:**
    -   `vector` (List[int]): The 24-bit vector.
-   **Returns:** (dict) A dictionary containing `nrci`, `health`, `regime`, `stability`, and `symmetry_tax`.

**Example:**
```python
vector = [1] * 24
result = ubp.calculate_coherence(vector)
print(result)
# {
#   'nrci': 0.0, 
#   'health': {'reality': 0.0, ...}, 
#   'regime': 'low', 
#   'stability': 0.0, 
#   'symmetry_tax': 12.0
# }
```

### 5. `snap_to_lattice(noisy_vector: List[int])`

Applies the reflexive error-correction logic (`Repair(v) = Encode(Decode(v))`) to a noisy vector.

-   **Arguments:**
    -   `noisy_vector` (List[int]): A 24-bit vector that may contain errors.
-   **Returns:** (dict) A dictionary containing the `corrected_vector`, `errors_fixed`, and `status`.

**Example:**
```python
noisy_vector = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
result = ubp.snap_to_lattice(noisy_vector)
print(result)
# {
#   'original_vector': [1, 0, ...],
#   'corrected_vector': [0, 0, ...],
#   'errors_fixed': 1,
#   'status': 'CORRECTED'
# }
```

### 6. `query_memory(search_term: str, max_results: int = 12)`

Retrieves a cluster of relevant memories from the knowledge base, sorted by geometric proximity.

-   **Arguments:**
    -   `search_term` (str): The keyword or concept to search for.
    -   `max_results` (int): The maximum number of results to return.
-   **Returns:** (List[dict]) A list of memory entries with their Hamming distances.

**Example:**
```python
results = ubp.query_memory("gravity", max_results=3)
for r in results:
    print(f"- {r['name']} (Distance: {r['hamming_distance']})")
# - Force: Gravity (Distance: 0)
# - Spacetime Curvature (Distance: 4)
# - General Relativity (Distance: 6)
```

### 7. `validate_concept(concept_data: dict)`

Runs a new concept through the rigorous 5-phase UBP Research Protocol.

-   **Arguments:**
    -   `concept_data` (dict): A dictionary containing the concept's `name`, `math`, `language`, `script`, and `tags`.
-   **Returns:** (dict) A dictionary containing the validation results for each phase and promotion eligibility.

**Example:**
```python
concept = {
    "name": "Test Particle",
    "math": "m=1.0",
    "language": "A test particle for validation",
    "script": "particle = {'mass': 1.0}",
    "tags": ["test", "particle"]
}
result = ubp.validate_concept(concept)
print(result)
# {
#   'phase_1_initiation': 'PASS',
#   'phase_2_development': 'PASS',
#   'phase_3_distillation': 'PASS (Coherent)',
#   'phase_4_promotion': 'PASS',
#   'phase_5_archival': 'READY',
#   'promotion_eligible': True
# }
```

### 8. `archive_to_kb(concept_data: dict)`

Formats a validated concept into a JSON string ready for archival in the UBP knowledge base.

-   **Arguments:**
    -   `concept_data` (dict): The concept data to format.
-   **Returns:** (str) A formatted JSON string for the knowledge base entry.

**Example:**
```python
concept = {
    "ubp_id": "TEST_001",
    "name": "Test Concept",
    "math": "x=1",
    "language": "A test concept",
    "script": "x = 1",
    "tags": ["test"]
}
json_entry = ubp.archive_to_kb(concept)
print(json_entry)
# {
#   "<fingerprint>": {
#     "ubp_id": "TEST_001",
#     "name": "Test Concept",
#     ...
#   }
# }
```

## Bundled Reference Documents

This skill includes the following reference documents in the `references/` directory to provide context for the AI and users:

-   `ubp_laws.md`: A complete guide to the core laws of the UBP system.
-   `octad_guide.md`: A description of the eight geometric domains of existence.
-   `research_protocol.md`: A detailed breakdown of the 5-phase research and validation protocol.
