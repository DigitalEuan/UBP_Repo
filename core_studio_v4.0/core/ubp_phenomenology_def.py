from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple, Any
from fractions import Fraction

"""
================================================================================
1. PHENOMENON DEFINITION CONTRACT
Universal Binary Principle
Version: 3.9.0 Research Edition
Author: Euan R A Craig, New Zealand
Date: 18 December 2025
https://github.com/DigitalEuan/UBP_Repo
================================================================================
"""
@dataclass(frozen=True)
class PhenomenonDefinition:
    """
    Formal definition of a phenomenon for UBP studies.
    """
    name: str
    domain: str
    version: int
    bit_mapping: Dict[str, Tuple[int, int]]
    token_builder: Callable[[Dict[str, Any]], List[str]]
    feature_builder: Callable[[Dict[str, Any]], Dict[str, int | Fraction]]
    coord_mapper: Callable[[Dict[str, Any]], Tuple[int, int, int, int, int, int]]
    tgic_policy: Any
    toggle_rules: List[Any]
    invariants: List[Callable[[Dict[str, Any]], bool]]
