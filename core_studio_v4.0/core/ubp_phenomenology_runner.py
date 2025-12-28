#!/usr/bin/env python3
"""
================================================================================
UBP PHENOMENOLOGY RUNNER - PRODUCTION v3.9.1
================================================================================
The Execution Layer for the Universal Binary Principle.
"""
import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional, Union
from fractions import Fraction
import ubp_core

class OffBitLayer:
    REALITY = "reality"
    INFORMATION = "information"
    ACTIVATION = "activation"
    UNACTIVATED = "unactivated"

@dataclass(frozen=True)
class PhenomenonDefinition:
    name: str
    domain: str
    bit_mapping: Dict[str, Tuple[int, int]]
    version: int = 1
