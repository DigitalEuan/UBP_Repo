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


def _extract_nested_content(text: str, start_idx: int) -> Tuple[str, int]:
    """Helper to extract content between matching braces starting at start_idx."""
    if start_idx >= len(text) or text[start_idx] != '{':
        return "", start_idx

    stack = 0
    content = []
    for i in range(start_idx, len(text)):
        char = text[i]
        if char == '{':
            stack += 1
            if stack > 1:
                content.append(char)
        elif char == '}':
            stack -= 1
            if stack == 0:
                return "".join(content), i + 1
            content.append(char)
        else:
            content.append(char)
    return "".join(content), len(text)

def scrub_latex(text: str) -> str:
    """Strip LaTeX dollar-math, expand Greek/operator commands, drop the rest.
    Uses recursive-style processing for nested macros. Pure deterministic."""
    # 1. Replace block math and environments
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.DOTALL)
    text = re.sub(r"\$[^$]*\$", " ", text)
    text = re.sub(r"\\begin\{[^}]+\}.*?\\end\{[^}]+\}", " ", text, flags=re.DOTALL)

    # 2. Expand Greek letters and operators
    for cmd in sorted(_GREEK_MAP, key=len, reverse=True):
        text = re.sub(cmd + r"(?![a-zA-Z])", " " + _GREEK_MAP[cmd] + " ", text)
    for cmd in sorted(_OP_MAP, key=len, reverse=True):
        text = re.sub(cmd + r"(?![a-zA-Z])", " " + _OP_MAP[cmd] + " ", text)

    # 3. Handle nested font-style commands recursively
    style_commands = [
        r"\\mathrm", r"\\mathcal", r"\\mathbf", r"\\text", r"\\bm", r"\\dot",
        r"\\bar", r"\\tilde", r"\\hat", r"\\vec", r"\\acute", r"\\grave",
        r"\\check", r"\\breve", r"\\underline", r"\\frac", r"\\sqrt"
    ]

    # Compile a single pattern for all style commands to find the leftmost one
    cmd_pattern = "|".join(style_commands)

    def process_recursive(s: str) -> str:
        match = re.search(cmd_pattern, s)
        if not match:
            return s

        start = match.start()
        end_cmd = match.end()

        # Special case for \frac which has two braced arguments
        if s[start:end_cmd] == r"\frac":
            content1, next_idx = _extract_nested_content(s, end_cmd)
            content2, final_idx = _extract_nested_content(s, next_idx)
            # Process contents recursively and join
            return s[:start] + " " + process_recursive(content1) + " " + process_recursive(content2) + " " + process_recursive(s[final_idx:])

        # Standard single-argument macro
        content, final_idx = _extract_nested_content(s, end_cmd)
        if content or final_idx > end_cmd:
            return s[:start] + " " + process_recursive(content) + " " + process_recursive(s[final_idx:])
        else:
            # Command without braces, just skip it
            return s[:start] + " " + process_recursive(s[end_cmd:])

    text = process_recursive(text)

    # 4. Clean up remaining LaTeX syntax
    # Drop any remaining \command tokens (non-braced)
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
    # Drop subscript / superscript markers and braces
    text = re.sub(r"[_^]\{([^{}]*)\}", r" \1 ", text)
    text = re.sub(r"[_^]([a-zA-Z0-9])", r" \1 ", text)
    # Final pass on stray braces and symbols
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

    def _lemmatize(self, word: str) -> str:
        """Lightweight lemmatizer: strip common suffixes if the base exists."""
        if word in self.single_word:
            return word
        # Handle plurals
        if word.endswith("s") and word[:-1] in self.single_word:
            return word[:-1]
        # Handle past tense
        if word.endswith("ed") and word[:-2] in self.single_word:
            return word[:-2]
        if word.endswith("ed") and word[:-1] in self.single_word: # e.g. 'dated' -> 'date'
            return word[:-1]
        # Handle gerund
        if word.endswith("ing") and word[:-3] in self.single_word:
            return word[:-3]
        if word.endswith("ing") and word[:-3] + "e" in self.single_word: # e.g. 'coding' -> 'code'
            return word[:-3] + "e"
        return word

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
                # Try lemmatization
                lemma = self._lemmatize(w)
                if lemma in self.single_word:
                    out.append(lemma)
                else:
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