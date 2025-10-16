"""
UBP Virtual Machine Package

This package contains the runtime execution environment for UBP scripts.
It orchestrates the pure semantic functions and manages state transitions.
"""

from .runtime import Runtime
from .dsl import parse_ubp_script, eval_program

__version__ = "1.0.0"
__all__ = ["Runtime", "parse_ubp_script", "eval_program"]

