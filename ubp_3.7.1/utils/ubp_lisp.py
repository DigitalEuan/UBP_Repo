"""
Universal Binary Principle (UBP) Framework v3.7.1 - UBP-Lisp: Native Computational Ontology and BitBase for UBP
Author: Euan Craig, New Zealand
Date: 01 December 2025

Implements the complete UBP-Lisp language and BitBase system that serves
as the native computational ontology for the UBP framework. Provides
domain-specific language constructs for UBP operations, BitBase storage,
and JIT compilation capabilities.

Mathematical Foundation:
- S-expression based syntax for UBP operations
- BitBase: Content-addressable storage for UBP computations (now leveraging HexDictionary)
- Native UBP primitives: toggle, resonance, entanglement, etc.
- JIT compilation for performance optimization
- Ontological type system for UBP entities
"""

import numpy as np
import math
import ast
import hashlib
import json
import time
from typing import Dict, List, Tuple, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import re

# Import HexDictionary for persistent storage
from utils.hex_dictionary import HexDictionary
# Import UBPConfig for constants
from utils.ubp_config import get_config, UBPConfig
from core.state import OffBit, UBPState # Needed for some UBP operations

_config: UBPConfig = get_config() # Initialize configuration

class UBPType(Enum):
    """UBP-Lisp data types"""
    OFFBIT = "offbit"           # 24-bit OffBit
    BITFIELD = "bitfield"       # 6D Bitfield
    REALM = "realm"             # UBP realm
    FREQUENCY = "frequency"     # Resonance frequency
    COHERENCE = "coherence"     # Coherence value
    TENSOR = "tensor"           # Purpose tensor
    GLYPH = "glyph"             # Rune Protocol glyph
    FUNCTION = "function"       # UBP-Lisp function
    SYMBOL = "symbol"           # Lisp symbol
    NUMBER = "number"           # Numeric value
    LIST = "list"               # Lisp list
    STRING = "string"           # String literal
    BOOLEAN = "boolean"         # Boolean value
    NIL = "nil"                 # Nil value

# --- UBP-Lisp Core Data Structures ---

@dataclass(frozen=True)
class UBPAtom:
    """Base class for all UBP-Lisp atoms (symbols, numbers, strings, etc.)"""
    value: Any
    type: UBPType

@dataclass(frozen=True)
class UBPSymbol(UBPAtom):
    """A UBP-Lisp symbol (e.g., 'toggle', 'resonance')"""
    type: UBPType = UBPType.SYMBOL

@dataclass(frozen=True)
class UBPFunction(UBPAtom):
    """A native UBP-Lisp function"""
    type: UBPType = UBPType.FUNCTION
    
    def __call__(self, *args):
        return self.value(*args)

@dataclass(frozen=True)
class UBPList(UBPAtom):
    """A UBP-Lisp list (S-expression)"""
    type: UBPType = UBPType.LIST
    
    def __iter__(self):
        return iter(self.value)
    
    def __getitem__(self, key):
        return self.value[key]
    
    def __len__(self) -> int:
        return len(self.value)

# --- UBP-Lisp Environment and Primitives ---

def _ubp_toggle(offbit: OffBit) -> OffBit:
    """Native UBP primitive: toggle an OffBit."""
    if not isinstance(offbit, OffBit):
        raise TypeError(f"toggle expects OffBit, got {type(offbit)}")
    return offbit.toggle()

def _ubp_resonance(state: UBPState) -> float:
    """Native UBP primitive: compute resonance frequency (placeholder)."""
    # Placeholder for actual resonance computation using FFT/GeometricCodex
    return state.coherence * 100.0 # Use state.coherence for 3.7.1 compatibility

def _ubp_entangle(offbit1: OffBit, offbit2: OffBit) -> Tuple[OffBit, OffBit]:
    """Native UBP primitive: entangle two OffBits (placeholder)."""
    # Placeholder for actual entanglement logic
    return offbit1.toggle_bit(0), offbit2.toggle_bit(1)

def _ubp_to_python(obj: Any) -> Any:
    """Recursively convert UBP-Lisp objects to standard Python types for serialization."""
    if isinstance(obj, UBPList):
        # Convert list of pairs ((k v) (k v)) to a dictionary
        py_dict = {}
        for item in obj.value:
            if isinstance(item, UBPList) and len(item.value) == 2:
                key = _ubp_to_python(item.value[0])
                value = _ubp_to_python(item.value[1])
                py_dict[key] = value
            else:
                # If not a pair, just convert to a list
                return [_ubp_to_python(item) for item in obj.value]
        return py_dict
    elif isinstance(obj, UBPAtom):
        return obj.value
    elif isinstance(obj, OffBit):
        return obj.value # Store OffBit as its integer value
    elif isinstance(obj, UBPState):
        return obj.copy() # Store a copy of the state object
    elif isinstance(obj, list):
        return [_ubp_to_python(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: _ubp_to_python(v) for k, v in obj.items()}
    return obj

def _ubp_hex_store(data: Any, data_type: str, metadata: Optional[Dict] = None) -> str:
    """Native UBP primitive: store data in HexDictionary."""
    hd = HexDictionary()
    
    # Convert UBP-Lisp metadata structure to Python dictionary for serialization
    py_metadata = _ubp_to_python(metadata) if metadata else None
    
    # data_type is passed as a string literal from Lisp, so it's already a Python string
    return hd.store(_ubp_to_python(data), data_type, py_metadata)

def _ubp_hex_retrieve(key: str) -> Any:
    """Native UBP primitive: retrieve data from HexDictionary."""
    hd = HexDictionary()
    data, _ = hd.retrieve(key)
    return data

def _ubp_add(*args):
    """Lisp primitive: addition."""
    return sum(args)

def _ubp_sub(a, b):
    """Lisp primitive: subtraction."""
    return a - b

def _ubp_mul(*args):
    """Lisp primitive: multiplication."""
    result = 1
    for x in args:
        result *= x
    return result

def _ubp_div(a, b):
    """Lisp primitive: division."""
    return a / b

def _ubp_gt(a, b):
    """Lisp primitive: greater than."""
    return a > b

def _ubp_lt(a, b):
    """Lisp primitive: less than."""
    return a < b

def _ubp_eq(a, b):
    """Lisp primitive: equality."""
    return a == b

def _ubp_list(*args):
    """Lisp primitive: create a list."""
    return UBPList(value=list(args))

def _ubp_car(l: UBPList):
    """Lisp primitive: get the first element of a list."""
    if not isinstance(l, UBPList) or not l.value:
        raise ValueError("car expects a non-empty list")
    return l.value[0]

def _ubp_cdr(l: UBPList):
    """Lisp primitive: get the rest of a list."""
    if not isinstance(l, UBPList) or not l.value:
        raise ValueError("cdr expects a non-empty list")
    return UBPList(value=l.value[1:])

def _ubp_cons(x, y: UBPList):
    """Lisp primitive: construct a new list."""
    if not isinstance(y, UBPList):
        raise TypeError("cons expects a list as the second argument")
    return UBPList(value=[x] + y.value)

def _ubp_is_nil(x):
    """Lisp primitive: check for nil."""
    return x is None

def _ubp_is_list(x):
    """Lisp primitive: check for list."""
    return isinstance(x, UBPList)

def _ubp_is_symbol(x):
    """Lisp primitive: check for symbol."""
    return isinstance(x, UBPSymbol)

def _ubp_is_offbit(x):
    """Lisp primitive: check for OffBit."""
    return isinstance(x, OffBit)

def _ubp_if(condition, true_branch, false_branch):
    """Lisp primitive: conditional execution."""
    return true_branch if condition else false_branch

def _ubp_define(env, symbol: UBPSymbol, value):
    """Lisp primitive: define a variable in the environment."""
    if not isinstance(symbol, UBPSymbol):
        raise TypeError("define expects a symbol as the first argument")
    env[symbol.value] = value
    return None # Returns nil

def _ubp_lambda(env, params: UBPList, body):
    """Lisp primitive: create a lambda function."""
    def _lambda_func(*args):
        if len(args) != len(params):
            raise ValueError(f"Lambda expects {len(params)} arguments, got {len(args)}")
        
        # Create a new environment for the function call
        new_env = env.copy()
        for param, arg in zip(params.value, args):
            if not isinstance(param, UBPSymbol):
                raise TypeError("Lambda parameters must be symbols")
            new_env[param.value] = arg
        
        # Evaluate the body in the new environment
        return evaluate(body, new_env)
    
    return UBPFunction(value=_lambda_func)

def _ubp_begin(*args):
    """Lisp primitive: execute a sequence of expressions and return the last result."""
    return args[-1] if args else None

def _ubp_quote(x):
    """Lisp primitive: return the expression without evaluating it."""
    return x

def create_ubp_lisp_environment(state: Optional[UBPState] = None) -> Dict[str, Any]:
    """
    Create the initial UBP-Lisp environment with native primitives.
    """
    env = {
        # UBP Primitives
        'toggle': UBPFunction(value=_ubp_toggle),
        'resonance': UBPFunction(value=_ubp_resonance),
        'entangle': UBPFunction(value=_ubp_entangle),
        'hex-store': UBPFunction(value=_ubp_hex_store),
        'hex-retrieve': UBPFunction(value=_ubp_hex_retrieve),
        
        # Standard Lisp Primitives
        '+': UBPFunction(value=_ubp_add),
        '-': UBPFunction(value=_ubp_sub),
        '*': UBPFunction(value=_ubp_mul),
        '/': UBPFunction(value=_ubp_div),
        '>': UBPFunction(value=_ubp_gt),
        '<': UBPFunction(value=_ubp_lt),
        '=': UBPFunction(value=_ubp_eq),
        'list': UBPFunction(value=_ubp_list),
        'car': UBPFunction(value=_ubp_car),
        'cdr': UBPFunction(value=_ubp_cdr),
        'cons': UBPFunction(value=_ubp_cons),
        'nil?': UBPFunction(value=_ubp_is_nil),
        'list?': UBPFunction(value=_ubp_is_list),
        'symbol?': UBPFunction(value=_ubp_is_symbol),
        'offbit?': UBPFunction(value=_ubp_is_offbit),
        'if': UBPFunction(value=_ubp_if),
        'define': UBPFunction(value=_ubp_define),
        'lambda': UBPFunction(value=_ubp_lambda),
        'begin': UBPFunction(value=_ubp_begin),
        'quote': UBPFunction(value=_ubp_quote),
        
        # Constants
        'T': True,
        'F': False,
        'NIL': None,
    }
    
    if state:
        env['STATE'] = state
        
    return env

# --- UBP-Lisp Parser ---

def tokenize(chars: str) -> List[str]:
    """Convert a string of characters into a list of tokens."""
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def read_from_tokens(tokens: List[str]) -> UBPList:
    """Read an expression from a sequence of tokens."""
    if not tokens:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop ')'
        return UBPList(value=L)
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token: str) -> UBPAtom:
    """Numbers become numbers; every other token is a symbol."""
    try:
        return UBPAtom(type=UBPType.NUMBER, value=int(token))
    except ValueError:
        try:
            return UBPAtom(type=UBPType.NUMBER, value=float(token))
        except ValueError:
            if token.lower() == 'true':
                return UBPAtom(type=UBPType.BOOLEAN, value=True)
            elif token.lower() == 'false':
                return UBPAtom(type=UBPType.BOOLEAN, value=False)
            elif token.lower() == 'nil':
                return UBPAtom(type=UBPType.NIL, value=None)
            elif token.startswith('"') and token.endswith('"'):
                return UBPAtom(type=UBPType.STRING, value=token[1:-1])
            else:
                return UBPSymbol(value=token)

def parse(program: str) -> UBPList:
    """Read a UBP-Lisp expression from a string."""
    return read_from_tokens(tokenize(program))

# --- UBP-Lisp Evaluator ---

def evaluate(x: Any, env: Dict[str, Any]) -> Any:
    """Evaluate an expression in an environment."""
    
    # 1. Atom (Symbol, Number, String, Boolean, Nil)
    if not isinstance(x, UBPList):
        if isinstance(x, UBPSymbol):
            # Look up symbol in environment
            if x.value in env:
                return env[x.value]
            else:
                raise NameError(f"Symbol not found: {x.value}")
        elif isinstance(x, UBPAtom):
            # Return literal value for Number, String, Boolean, Nil
            return x.value
        else:
            # Return raw value (e.g., OffBit, UBPState)
            return x
    
    # 2. List (S-expression)
    
    # Special forms (handled by primitives)
    if len(x) > 0 and isinstance(x[0], UBPSymbol):
        op = x[0].value
        
        if op == 'quote':
            return x[1]
        elif op == 'if':
            (_, test, conseq, alt) = x.value
            exp = conseq if evaluate(test, env) else alt
            return evaluate(exp, env)
        elif op == 'define':
            (_, symbol, exp) = x.value
            env[symbol.value] = evaluate(exp, env)
            return None # Returns nil
        elif op == 'lambda':
            (_, params, body) = x.value
            return _ubp_lambda(env, params, body)
        elif op == 'begin':
            val = None
            for exp in x.value[1:]:
                val = evaluate(exp, env)
            return val
    
    # Function call
    proc = evaluate(x[0], env)
    args = [evaluate(exp, env) for exp in x.value[1:]]
    
    if isinstance(proc, UBPFunction):
        return proc(*args)
    else:
        raise TypeError(f"First element of list must be a function, got {type(proc)}")

# --- Main Execution ---

def ubp_lisp_run(program: str, state: Optional[UBPState] = None, env: Optional[Dict[str, Any]] = None) -> Any:
    """
    Parse, evaluate, and run a UBP-Lisp program.
    """
    if env is None:
        env = create_ubp_lisp_environment(state)
    parsed_program = parse(program)
    return evaluate(parsed_program, env)

# Clean up imports for the final file
# No need to delete UBPState as it is imported from core.state
