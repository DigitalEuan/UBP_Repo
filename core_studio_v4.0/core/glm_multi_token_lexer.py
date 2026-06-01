"""
================================================================================
GLM MULTI-TOKEN LEXER v1.0
================================================================================
Fills the second-largest semantic gap: the original engine tokenised every
query at whitespace, destroying multi-word physics concepts such as
'Weyl anomaly', 'Hatsugai-Kohmoto model', or 'spin squeezing parameter'.

This module performs three jobs, in order:
  1. LaTeX scrub          –  strips $...$ blocks and LaTeX-command tokens, then
                              converts a small dictionary of Greek-letter
                              commands to their plain-text names so they
                              can still match the vocabulary.
  2. Multi-word detect    –  greedy longest-match against a curated list
                              of physics phrases (loaded from the pack).
  3. Standard tokenise    –  whitespace + stop-word filter for the remainder.

The lexer is PURE (no I/O, no random state) and stdlib only.
================================================================================
"""

from __future__ import annotations
import re
from typing import List, Set, Tuple


# ───────────────────────────────────────────────────────────────────────────────
# LATEX SCRUB
# ───────────────────────────────────────────────────────────────────────────────

_GREEK_MAP = {
    r"\\alpha": "alpha", r"\\beta": "beta", r"\\gamma": "gamma",
    r"\\delta": "delta", r"\\epsilon": "epsilon", r"\\zeta": "zeta",
    r"\\eta": "eta", r"\\theta": "theta", r"\\iota": "iota",
    r"\\kappa": "kappa", r"\\lambda": "lambda", r"\\mu": "mu",
    r"\\nu": "nu", r"\\xi": "xi", r"\\pi": "pi",
    r"\\rho": "rho", r"\\sigma": "sigma", r"\\tau": "tau",
    r"\\upsilon": "upsilon", r"\\phi": "phi", r"\\chi": "chi",
    r"\\psi": "psi", r"\\omega": "omega",
    r"\\Gamma": "gamma", r"\\Delta": "delta", r"\\Theta": "theta",
    r"\\Lambda": "lambda", r"\\Xi": "xi", r"\\Pi": "pi",
    r"\\Sigma": "sigma", r"\\Phi": "phi", r"\\Psi": "psi",
    r"\\Omega": "omega",
}

# Common operator macros that map to semantic words
_OP_MAP = {
    r"\\partial": "derivative",
    r"\\nabla": "gradient",
    r"\\int": "integral",
    r"\\sum": "sum",
    r"\\prod": "product",
    r"\\langle": "expectation",
    r"\\rangle": "expectation",
    r"\\bar": "conjugate",
    r"\\dagger": "adjoint",
    r"\\hat": "operator",
    r"\\tilde": "modified",
    r"\\overline": "conjugate",
}


def scrub_latex(text: str) -> str:
    """Strip LaTeX dollar-math, expand Greek/operator commands, drop the rest.
    Pure deterministic."""
    # Replace inline and display math blocks with a single space (we keep the
    # surrounding prose).
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.DOTALL)
    text = re.sub(r"\$[^$]*\$", " ", text)
    text = re.sub(r"\\begin\{[^}]+\}.*?\\end\{[^}]+\}", " ", text, flags=re.DOTALL)
    # Expand Greek letters (longer names first to avoid partial overlap)
    for cmd in sorted(_GREEK_MAP, key=len, reverse=True):
        text = re.sub(cmd + r"(?![a-zA-Z])", " " + _GREEK_MAP[cmd] + " ", text)
    for cmd in sorted(_OP_MAP, key=len, reverse=True):
        text = re.sub(cmd + r"(?![a-zA-Z])", " " + _OP_MAP[cmd] + " ", text)
    # Drop any remaining \command tokens
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
    # Drop subscript / superscript braces, leaving the content
    text = re.sub(r"[_^]\{([^{}]*)\}", r" \1 ", text)
    text = re.sub(r"[_^]([a-zA-Z0-9])", r" \1 ", text)
    # Drop stray braces and math symbols
    text = re.sub(r"[{}]", " ", text)
    text = re.sub(r"[=+\-*/<>~|]", " ", text)
    return text


# ───────────────────────────────────────────────────────────────────────────────
# DEFAULT STOP-WORDS
# ───────────────────────────────────────────────────────────────────────────────

STOP_WORDS: Set[str] = {
    "what", "is", "the", "of", "to", "in", "and", "for", "with", "on",
    "about", "does", "why", "how", "can", "a", "an", "this", "that",
    "it", "be", "are", "was", "we", "you", "i", "they", "by", "as",
    "or", "if", "not", "so", "do", "at", "from", "into", "when",
    "then", "there", "here", "their", "its", "any", "each", "such",
    "more", "most", "much", "very", "well", "also", "only", "even",
    "thus", "hence", "given", "consider", "suppose", "assume", "let",
    "find", "show", "use", "using", "explain", "describe", "derive",
}


# ───────────────────────────────────────────────────────────────────────────────
# LEXER
# ───────────────────────────────────────────────────────────────────────────────

class MultiTokenLexer:
    """Multi-word-aware tokenizer for physics queries."""

    def __init__(self, vocabulary_words: Set[str],
                 stop_words: Set[str] = None,
                 min_len: int = 2):
        """
        vocabulary_words: any keys (single or hyphen-joined-with-space) the
                          lexer should recognise as atomic.
        """
        self.stop_words = set(stop_words or STOP_WORDS)
        self.min_len = min_len
        # Split words containing spaces -> multi-word phrases
        self.multi_word: List[List[str]] = []
        self.single_word: Set[str] = set()
        for w in vocabulary_words:
            w = w.lower().strip()
            if not w:
                continue
            # Treat hyphens like spaces (e.g. 'rayleigh-benard')
            parts = re.split(r"[\s\-]+", w)
            if len(parts) > 1:
                self.multi_word.append(parts)
            else:
                self.single_word.add(parts[0])
        # Sort multi-word phrases by length descending for greedy match
        self.multi_word.sort(key=len, reverse=True)

    def tokenise(self, text: str) -> List[str]:
        """Return a deterministic list of meaning-bearing tokens / phrases."""
        text = scrub_latex(text)
        text = text.lower()
        # keep alphanumerics, spaces, hyphens
        text = re.sub(r"[^a-z0-9\-\s]", " ", text)
        # split into raw word list
        raw = [w for w in re.split(r"\s+", text) if w]

        out: List[str] = []
        i = 0
        while i < len(raw):
            matched = False
            # try longest multi-word phrase first
            for phrase in self.multi_word:
                k = len(phrase)
                if i + k > len(raw):
                    continue
                if raw[i:i + k] == phrase:
                    out.append(" ".join(phrase))
                    i += k
                    matched = True
                    break
            if matched:
                continue
            w = raw[i]
            # also accept hyphenated single-tokens like 'rayleigh-benard'
            if w in self.single_word:
                out.append(w)
            elif w not in self.stop_words and len(w) >= self.min_len:
                out.append(w)
            i += 1
        return out


# ───────────────────────────────────────────────────────────────────────────────
# CONVENIENCE
# ───────────────────────────────────────────────────────────────────────────────

def build_lexer_from_vocab(vocab) -> MultiTokenLexer:
    """Create a lexer whose phrase table matches the live vocabulary keys."""
    return MultiTokenLexer(set(vocab.words.keys()))


if __name__ == "__main__":
    # Smoke test
    vocab_words = {
        "weyl anomaly", "beta function", "rayleigh number",
        "spin squeezing", "hatsugai-kohmoto", "majorana",
        "parton", "quantum", "metric",
    }
    lx = MultiTokenLexer(vocab_words)
    q = r"What is the $\beta$-function for a Hatsugai-Kohmoto Majorana with spin squeezing?"
    print(lx.tokenise(q))