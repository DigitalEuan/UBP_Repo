"""
================================================================================
GLM MULTI-TOKEN LEXER v3.3
================================================================================
Fills the second-largest semantic gap: the original engine tokenised every
query at whitespace, destroying multi-word physics concepts.

v3.3 Improvements:
- Adaptive Lexer Weighting: Biases fuzzy matching toward contextual centroid.
- Robust LaTeX scrubbing and stop-word filtering for scientific descriptions.
================================================================================
"""

from __future__ import annotations
import re
import difflib
from typing import List, Set, Tuple, Dict

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

_OP_MAP = {
    r"\\partial": "derivative", r"\\nabla": "gradient", r"\\int": "integral",
    r"\\sum": "sum", r"\\prod": "product", r"\\langle": "expectation",
    r"\\rangle": "expectation", r"\\bar": "conjugate", r"\\dagger": "adjoint",
    r"\\hat": "operator", r"\\tilde": "modified", r"\\overline": "conjugate",
}

def _extract_nested_content(text: str, start_idx: int) -> Tuple[str, int]:
    if start_idx >= len(text) or text[start_idx] != '{': return "", start_idx
    stack, content = 0, []
    for i in range(start_idx, len(text)):
        char = text[i]
        if char == '{':
            stack += 1
            if stack > 1: content.append(char)
        elif char == '}':
            stack -= 1
            if stack == 0: return "".join(content), i + 1
            content.append(char)
        else: content.append(char)
    return "".join(content), len(text)

def scrub_latex(text: str) -> str:
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.DOTALL)
    text = re.sub(r"\$[^$]*\$", " ", text)
    text = re.sub(r"\\begin\{[^}]+\}.*?\\end\{[^}]+\}", " ", text, flags=re.DOTALL)
    for cmd in sorted(_GREEK_MAP, key=len, reverse=True): text = re.sub(cmd + r"(?![a-zA-Z])", " " + _GREEK_MAP[cmd] + " ", text)
    for cmd in sorted(_OP_MAP, key=len, reverse=True): text = re.sub(cmd + r"(?![a-zA-Z])", " " + _OP_MAP[cmd] + " ", text)
    style_commands = [r"\\mathrm", r"\\mathcal", r"\\mathbf", r"\\text", r"\\bm", r"\\dot", r"\\bar", r"\\tilde", r"\\hat", r"\\vec", r"\\acute", r"\\grave", r"\\check", r"\\breve", r"\\underline", r"\\frac", r"\\sqrt"]
    cmd_pattern = "|".join(style_commands)
    def process_recursive(s: str) -> str:
        match = re.search(cmd_pattern, s)
        if not match: return s
        start, end_cmd = match.start(), match.end()
        if s[start:end_cmd] == r"\frac":
            content1, next_idx = _extract_nested_content(s, end_cmd)
            content2, final_idx = _extract_nested_content(s, next_idx)
            return s[:start] + " " + process_recursive(content1) + " " + process_recursive(content2) + " " + process_recursive(s[final_idx:])
        content, final_idx = _extract_nested_content(s, end_cmd)
        if content or final_idx > end_cmd: return s[:start] + " " + process_recursive(content) + " " + process_recursive(s[final_idx:])
        return s[:start] + " " + process_recursive(s[end_cmd:])
    text = process_recursive(text)
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
    text = re.sub(r"[_^]\{([^{}]*)\}", r" \1 ", text)
    text = re.sub(r"[_^]([a-zA-Z0-9])", r" \1 ", text)
    text = re.sub(r"[{}]", " ", text)
    text = re.sub(r"[=+\-*/<>~|]", " ", text)
    return text

STOP_WORDS: Set[str] = {"what", "the", "on", "of", "in", "with", "to", "for", "have", "has", "had", "will", "shall", "should", "would", "may", "might", "must", "can", "could", "about", "does", "why", "how", "a", "an", "this", "that", "those", "these", "it", "be", "are", "is", "was", "were", "been", "being", "we", "you", "i", "they", "by", "as", "if", "so", "do", "at", "from", "into", "when", "where", "which", "then", "there", "here", "their", "its", "any", "each", "such", "more", "most", "much", "very", "well", "also", "only", "even", "thus", "hence", "suppose", "let", "given", "consider", "assume", "find", "show", "describe", "explain", "derive", "calculate", "determine", "both", "between", "all", "your", "answer", "please", "note", "let", "take", "give", "according", "base", "based", "become", "becomes", "called", "can", "carry", "carries", "come", "comes", "consist", "consists", "depend", "depends", "describe", "described", "different", "do", "does", "done", "due", "each", "either", "find", "found", "from", "get", "gets", "give", "given", "gives", "go", "goes", "gone", "have", "has", "had", "how", "however", "if", "in", "instead", "into", "is", "it", "its", "just", "keep", "kept", "known", "large", "larger", "lead", "leads", "let", "like", "make", "makes", "many", "may", "more", "most", "much", "must", "near", "nearly", "need", "needs", "next", "no", "not", "note", "now", "of", "off", "often", "on", "only", "or", "other", "our", "out", "over", "own", "per", "please", "provide", "provides", "rather", "require", "requires", "result", "results", "run", "same", "see", "seen", "set", "shall", "should", "show", "shown", "shows", "since", "small", "smaller", "so", "some", "still", "such", "take", "taken", "takes", "than", "that", "the", "their", "them", "then", "there", "these", "they", "this", "those", "through", "to", "too", "toward", "towards", "under", "until", "up", "upon", "use", "used", "using", "very", "via", "was", "we", "well", "were", "what", "when", "where", "whether", "which", "while", "who", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "zeros"}

_IRREGULAR_LEMMAS: Dict[str, str] = {"led": "lead", "leads": "lead", "leading": "lead", "brought": "bring", "bringing": "bring", "frozen": "freeze", "freezing": "freeze", "shown": "show", "showed": "show", "showing": "show", "gave": "give", "given": "give", "giving": "give", "took": "take", "taken": "take", "taking": "take", "found": "find", "finding": "find", "thought": "think", "thinking": "think", "known": "know", "knew": "know", "knowing": "know", "spent": "spend", "spending": "spend", "built": "build", "building": "build", "seen": "see", "saw": "see", "seeing": "see", "kept": "keep", "keeping": "keep"}

class MultiTokenLexer:
    def __init__(self, vocabulary_words: Set[str], stop_words: Set[str] = None, min_len: int = 2, vocab_vectors: Dict[str, List[int]] = None):
        self.stop_words = set(stop_words or STOP_WORDS)
        self.vocab_vectors = vocab_vectors or {}
        self.min_len, self.multi_word, self.single_word = min_len, [], set()
        for w in vocabulary_words:
            w = w.lower().strip()
            if not w: continue
            parts = re.split(r"[\s\-]+", w)
            if len(parts) > 1: self.multi_word.append(parts)
            else: self.single_word.add(parts[0])
        self.multi_word.sort(key=len, reverse=True)

    def _lemmatize(self, word: str) -> str:
        if word in _IRREGULAR_LEMMAS: return _IRREGULAR_LEMMAS[word]
        if word in self.single_word: return word
        if word.endswith("s") and word[:-1] in self.single_word: return word[:-1]
        if word.endswith("ed") and word[:-2] in self.single_word: return word[:-2]
        if word.endswith("ed") and word[:-1] in self.single_word: return word[:-1]
        if word.endswith("ing") and word[:-3] in self.single_word: return word[:-3]
        if word.endswith("ing") and word[:-3] + "e" in self.single_word: return word[:-3] + "e"
        return word

    def _is_metadata(self, token: str) -> bool:
        if re.match(r"^challenge_?\d+$", token) or token == "challenge": return True
        if re.match(r"^\d+[a-z]?$", token) or token in ("pdf", "json", "py", "txt", "main", "problem", "id", "description"): return True
        return False

    def _fuzzy_match(self, token: str, context_centroid: List[int] = None) -> Optional[str]:
        if len(token) <= 3: return None
        matches = difflib.get_close_matches(token, self.single_word, n=5, cutoff=0.8)
        if not matches: return None
        if not context_centroid or not any(context_centroid): return matches[0]
        from ubp_unified_v5 import BinaryLinearAlgebra as BLA
        best_match, min_dist = matches[0], 99
        for m in matches:
            if m in self.vocab_vectors:
                d = BLA.hamming_distance(self.vocab_vectors[m], context_centroid)
                if d < min_dist: min_dist, best_match = d, m
        return best_match

    def tokenise(self, text: str, context_centroid: List[int] = None) -> List[str]:
        text = scrub_latex(text).lower().replace("_", " ")
        text = re.sub(r"[^a-z0-9\-\s]", " ", text)
        raw = [w for w in re.split(r"\s+", text) if w if not self._is_metadata(w)]
        out, i = [], 0
        while i < len(raw):
            matched = False
            for phrase in self.multi_word:
                k = len(phrase)
                if i + k <= len(raw) and raw[i:i + k] == phrase:
                    out.append(" ".join(phrase)); i += k; matched = True; break
            if matched: continue
            w = raw[i]
            if w in self.single_word: out.append(w)
            elif w not in self.stop_words and len(w) >= self.min_len:
                lemma = self._lemmatize(w)
                if lemma in self.single_word: out.append(lemma)
                else:
                    fuzzy = self._fuzzy_match(lemma, context_centroid)
                    out.append(fuzzy if fuzzy else w)
            i += 1
        return out

def build_lexer_from_vocab(vocab) -> MultiTokenLexer:
    vectors = {l: (w.vector if hasattr(w, "vector") else [0]*24) for l, w in vocab.words.items()}
    return MultiTokenLexer(set(vocab.words.keys()), vocab_vectors=vectors)
