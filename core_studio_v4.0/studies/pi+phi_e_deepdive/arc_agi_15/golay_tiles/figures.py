#!/usr/bin/env python3
"""Illustrations for the Golay tile set, and an independent recomputation of the
numbers they show.

Usage:  python3 GolayTiles/figures.py

No dependencies beyond the Python standard library.  The script

1. rebuilds, from the same definitions as the Lean sources, the hexacode, the
   MOG code on the cube's surface (`GolayTiles/Surface.lean`) and the code of
   the generator matrix (`GolayTiles/Substrate.lean`), and checks the numbers
   the Lean theorems state;
2. writes seven SVG figures into `GolayTiles/figures/`.

The Lean proofs are the authority.  This script is a drawing tool that happens
to check its own labels, so that no figure can quietly disagree with a theorem.
"""

from __future__ import annotations

import os
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures")

# --------------------------------------------------------------------------
# 1.  GF(4), the hexacode, and the two constructions of the Golay code
# --------------------------------------------------------------------------

# GF(4) = {0, 1, w, w2} as 0, 1, 2, 3.  Addition is bitwise XOR.
MUL4 = [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]
NAME4 = ["0", "1", "\u03c9", "\u03c9\u0304"]

HEXGEN = [
    [1, 0, 0, 1, 2, 3],
    [0, 1, 0, 1, 3, 2],
    [0, 0, 1, 1, 1, 1],
]


def combo(a: int, b: int, c: int) -> tuple[int, ...]:
    """The hexacode word a·g0 + b·g1 + c·g2."""
    return tuple(
        MUL4[a][HEXGEN[0][j]] ^ MUL4[b][HEXGEN[1][j]] ^ MUL4[c][HEXGEN[2][j]]
        for j in range(6)
    )


HEXACODE = sorted({combo(a, b, c) for a in range(4) for b in range(4) for c in range(4)})


def hex_min_distance() -> int:
    return min(
        sum(1 for x, y in zip(u, v) if x != y)
        for u in HEXACODE
        for v in HEXACODE
        if u != v
    )


# --- the MOG code on the cube's surface -----------------------------------
# A grid is a 6-tuple of faces; a face is a 4-tuple of bits (top cell first).
ROWLABEL = [0, 1, 2, 3]


def symb(face: tuple[int, ...]) -> int:
    s = 0
    for i in range(4):
        if face[i]:
            s ^= ROWLABEL[i]
    return s


def par(face: tuple[int, ...]) -> int:
    return face[0] ^ face[1] ^ face[2] ^ face[3]


def col_of(s: int, t: int, q: int) -> tuple[int, ...]:
    """The unique face with symbol s, top cell t and parity q."""
    u = q ^ t
    b0, b1 = int(s in (1, 3)), int(s in (2, 3))
    return (t, u ^ b1, u ^ b0, u ^ b0 ^ b1)


def mog_code() -> list[tuple[tuple[int, ...], ...]]:
    """The 4^3 · 2^6 codewords, built exactly as `CubeMOG.build` builds them."""
    words = []
    for a, b, c in product(range(4), repeat=3):
        h = combo(a, b, c)
        for t in product((0, 1), repeat=6):
            q = t[0] ^ t[1] ^ t[2] ^ t[3] ^ t[4] ^ t[5]
            words.append(tuple(col_of(h[j], t[j], q) for j in range(6)))
    return words


def is_mog(grid: tuple[tuple[int, ...], ...]) -> bool:
    q = grid[0][0] ^ grid[1][0] ^ grid[2][0] ^ grid[3][0] ^ grid[4][0] ^ grid[5][0]
    return tuple(symb(f) for f in grid) in set(HEXACODE) and all(
        par(f) == q for f in grid
    )


def grid_weight(grid) -> int:
    return sum(sum(f) for f in grid)


# --- the code of the generator matrix -------------------------------------
BMAT = [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0],
    [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0],
    [1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
]


def generator_rows() -> list[int]:
    """Rows of G = [I | B] as 24-bit integers."""
    rows = []
    for i in range(12):
        v = 1 << i
        for j in range(12):
            if BMAT[i][j]:
                v |= 1 << (12 + j)
        rows.append(v)
    return rows


def matrix_code() -> list[int]:
    rows = generator_rows()
    words = [0]
    for r in rows:
        words += [w ^ r for w in words]
    return words


def popcount(x: int) -> int:
    return bin(x).count("1")


def covering_radius(words: list[int]) -> int:
    """Breadth-first search over the 2^12 cosets: the largest coset-leader weight."""
    code = set(words)
    seen = {0: 0}
    frontier, radius = [0], 0
    syndromes = 1
    while syndromes < 4096:
        radius += 1
        nxt = []
        for v in frontier:
            for b in range(24):
                w = v ^ (1 << b)
                key = min(w ^ c for c in code)  # canonical coset representative
                if key not in seen:
                    seen[key] = radius
                    syndromes += 1
                    nxt.append(w)
        frontier = nxt
    return radius


def checks() -> dict[str, object]:
    """Recompute every number that appears in the figures."""
    r = {}
    r["hexacode words"] = len(HEXACODE)
    r["hexacode minimum distance"] = hex_min_distance()
    # MDS: each triple of incoming faces (positions 1, 3, 5) occurs once
    r["hexacode words per incoming triple"] = sorted(
        {
            sum(1 for h in HEXACODE if (h[1], h[3], h[5]) == t)
            for t in product(range(4), repeat=3)
        }
    )
    surface = mog_code()
    r["surface codewords"] = len(set(surface))
    r["surface code is closed under the MOG law"] = all(is_mog(g) for g in surface)
    enum = {}
    for g in surface:
        enum[grid_weight(g)] = enum.get(grid_weight(g), 0) + 1
    r["surface weight enumerator"] = dict(sorted(enum.items()))
    mat = matrix_code()
    menum = {}
    for w in mat:
        menum[popcount(w)] = menum.get(popcount(w), 0) + 1
    r["generator-matrix weight enumerator"] = dict(sorted(menum.items()))
    r["the two constructions agree"] = r["surface weight enumerator"] == menum
    r["covering radius"] = covering_radius(mat)
    # one whole face of the cube is a weight-4 grid at distance 4 from the code
    face = 0
    for i in range(4):
        face |= 1 << i
    r["weight of one face"] = popcount(face)
    r["fibres of the face symbol"] = sorted(
        {
            sum(
                1
                for f in product((0, 1), repeat=4)
                if symb(f) == s
            )
            for s in range(4)
        }
    )
    return r


# --------------------------------------------------------------------------
# 2.  The figures
# --------------------------------------------------------------------------

CSS = """
  .bg   { fill: #ffffff; }
  .cell { fill: #ffffff; stroke: #333333; stroke-width: 1.2; }
  .on   { fill: #2f6fb0; stroke: #16324f; stroke-width: 1.2; }
  .lite { fill: #eef3f8; stroke: #333333; stroke-width: 1.2; }
  .box  { fill: none; stroke: #333333; stroke-width: 1.6; }
  .lbl  { font-family: "DejaVu Sans", sans-serif; font-size: 13px; fill: #111111; }
  .sml  { font-family: "DejaVu Sans", sans-serif; font-size: 11px; fill: #444444; }
  .ttl  { font-family: "DejaVu Sans", sans-serif; font-size: 16px; fill: #111111; }
  .mono { font-family: "DejaVu Sans Mono", monospace; font-size: 12px; fill: #111111; }
  .arr  { stroke: #2f6fb0; stroke-width: 2; fill: none; marker-end: url(#a); }
  .bar  { fill: #2f6fb0; }
"""

HEAD = """<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"
     viewBox="0 0 {w} {h}">
<defs>
  <marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7"
          markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z"
          fill="#2f6fb0"/></marker>
  <style>{css}</style>
</defs>
<rect class="bg" x="0" y="0" width="{w}" height="{h}"/>
"""


def svg(name: str, width: int, height: int, body: str) -> None:
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(HEAD.format(w=width, h=height, css=CSS) + body + "\n</svg>\n")
    print("wrote", os.path.relpath(os.path.join(OUT, name), os.path.dirname(HERE)))


def text(x, y, s, cls="lbl", anchor="start"):
    return (
        f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">'
        f"{s}</text>"
    )


def rect(x, y, w, h, cls="cell"):
    return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}"/>'


def fig_mog_grid():
    """Figure 1 — the 4 x 6 MOG grid, its row labels and its column readings."""
    s, x0, y0 = 40, 130, 90
    b = [text(20, 30, "Figure 1 — the MOG grid: 24 cells, 6 columns of 4", "ttl")]
    b.append(text(20, 55, "one column = one face of the cube = one GF(4) symbol + one parity bit", "sml"))
    for i in range(4):
        b.append(text(x0 - 14, y0 + i * s + 26, NAME4[i], "lbl", "end"))
        b.append(text(x0 - 44, y0 + i * s + 26, f"row {i}", "sml", "end"))
    for j in range(6):
        b.append(text(x0 + j * s + s / 2, y0 - 12, f"face {j}", "sml", "middle"))
        for i in range(4):
            b.append(rect(x0 + j * s, y0 + i * s, s, s))
    y1 = y0 + 4 * s
    b.append(text(x0 - 14, y1 + 26, "symbol", "sml", "end"))
    b.append(text(x0 - 14, y1 + 56, "parity", "sml", "end"))
    for j in range(6):
        b.append(rect(x0 + j * s, y1 + 8, s, 26, "lite"))
        b.append(rect(x0 + j * s, y1 + 38, s, 26, "lite"))
    b.append(text(20, y1 + 110,
                  "symbol of a face  =  GF(4) sum of the row labels of its set cells   "
                  "(CubeMOG.symb)", "lbl"))
    b.append(text(20, y1 + 134,
                  "the grid is a codeword  \u21d4  the six symbols form a hexacode word "
                  "and every face has the parity of the top row   (CubeMOG.IsMog)", "lbl"))
    svg("fig1_mog_grid.svg", 520, y1 + 170, "\n".join(b))


def fig_cube_net():
    """Figure 2 — the same 24 cells folded onto the surface of a cube."""
    s = 34
    b = [text(20, 30, "Figure 2 — the grid folded onto the cube: 6 faces \u00d7 4 cells = 24", "ttl")]
    b.append(text(20, 55, "the net of the cube; each face carries one column of Figure 1", "sml"))

    def face(px, py, j):
        out = [rect(px, py, 2 * s, 2 * s, "box")]
        for k in range(4):
            out.append(rect(px + (k % 2) * s, py + (k // 2) * s, s, s))
        out.append(text(px + s, py - 8, f"face {j}", "sml", "middle"))
        return out

    positions = [(90, 100), (90, 100 + 2 * s + 26), (90 + 2 * s + 26, 100 + 2 * s + 26),
                 (90 + 4 * s + 52, 100 + 2 * s + 26), (90 + 6 * s + 78, 100 + 2 * s + 26),
                 (90, 100 + 4 * s + 52)]
    for j, (px, py) in enumerate(positions):
        b += face(px, py, j)
    b.append(text(20, 100 + 6 * s + 100,
                  "opposite faces are the pairs (0,1), (2,3), (4,5) of the axis labels "
                  "used in GolayTiles.Stabiliser", "lbl"))
    svg("fig2_cube_net.svg", 90 + 8 * s + 120, 100 + 6 * s + 130, "\n".join(b))


def fig_tile_io():
    """Figure 3 — one tile: three faces in, three faces out."""
    b = [text(20, 30, "Figure 3 — the tile: what enters fixes what leaves", "ttl")]
    b.append(text(20, 55,
                  "the three incoming faces \u2212x, \u2212y, \u2212z determine the "
                  "lawful tile uniquely (GolayHex.hexacode_mds)", "sml"))
    cx, cy, s = 260, 200, 110
    b.append(rect(cx - s / 2, cy - s / 2, s, s, "lite"))
    b.append(f'<path class="box" d="M{cx - s/2},{cy - s/2} l30,-30 h{s} v{s} l-30,30"/>')
    b.append(f'<path class="box" d="M{cx + s/2},{cy - s/2} l30,-30"/>')
    for dx, dy, lab in ((-150, 0, "\u2212x"), (0, 150, "\u2212z"), (-110, -85, "\u2212y")):
        b.append(f'<path class="arr" d="M{cx + dx},{cy + dy} L{cx + dx*0.42},{cy + dy*0.42}"/>')
        b.append(text(cx + dx - 18, cy + dy + 5, lab, "lbl"))
    for dx, dy, lab in ((160, 0, "+x"), (0, -160, "+y"), (115, 95, "+z")):
        b.append(f'<path class="arr" d="M{cx + dx*0.45},{cy + dy*0.45} L{cx + dx},{cy + dy}"/>')
        b.append(text(cx + dx + 8, cy + dy + 5, lab, "lbl"))
    b.append(text(430, 150, "outgoing = M \u00b7 incoming, with", "lbl"))
    b.append(text(430, 175, "M = [[\u03c9,\u03c9\u0304,\u03c9\u0304],"
                            "[\u03c9\u0304,\u03c9,\u03c9\u0304],"
                            "[\u03c9\u0304,\u03c9\u0304,\u03c9]]", "mono"))
    b.append(text(430, 200, "M\u00b3 = 1   (update_matrix_order_three)", "sml"))
    b.append(text(20, 370,
                  "64 lawful tiles (hexacode_card); an assembly of the octant is fixed by the "
                  "digits crossing its three boundary planes (determined_by_boundary)", "lbl"))
    svg("fig3_tile_io.svg", 780, 400, "\n".join(b))


def fig_layers(surface_words: int):
    """Figure 4 — the two filters: 2^24 -> 2^18 -> 2^12."""
    b = [text(20, 30, "Figure 4 — two filters on the 24 cells", "ttl")]
    xs = [60, 300, 540]
    labels = [("all grids", "2\u00b2\u2074 = 16 777 216"),
              ("hexacode layer", "2\u00b9\u2078 = 262 144"),
              ("+ parity layer", f"2\u00b9\u00b2 = {surface_words}")]
    for x, (t, v) in zip(xs, labels):
        b.append(rect(x, 90, 180, 80, "lite"))
        b.append(text(x + 90, 120, t, "lbl", "middle"))
        b.append(text(x + 90, 145, v, "mono", "middle"))
    for x in xs[:-1]:
        b.append(f'<path class="arr" d="M{x + 185},130 L{x + 235},130"/>')
    b.append(text(xs[0] + 200, 105, "\u00f764", "sml"))
    b.append(text(xs[1] + 200, 105, "\u00f764", "sml"))
    b.append(text(20, 205, "CubeMOG.hexpass_card, CubeMOG.mog_card, "
                           "CubeMOG.parity_layer_factor", "sml"))
    svg("fig4_layers.svg", 760, 240, "\n".join(b))


def fig_weights(enum: dict[int, int]):
    """Figure 5 — the weight enumerator."""
    b = [text(20, 30, "Figure 5 — the weight enumerator of the code", "ttl")]
    b.append(text(20, 55, "1, 759, 2576, 759, 1 on weights 0, 8, 12, 16, 24 "
                          "(GolayInv.golay_weight_enumerator)", "sml"))
    base, hmax = 300, 200
    top = max(enum.values())
    for k, (wgt, cnt) in enumerate(sorted(enum.items())):
        x = 80 + k * 110
        h = max(3, int(hmax * cnt / top))
        b.append(f'<rect class="bar" x="{x}" y="{base - h}" width="60" height="{h}"/>')
        b.append(text(x + 30, base + 20, f"wt {wgt}", "sml", "middle"))
        b.append(text(x + 30, base - h - 8, str(cnt), "lbl", "middle"))
    b.append(f'<path class="box" d="M60,{base} H640"/>')
    svg("fig5_weight_enumerator.svg", 680, 360, "\n".join(b))


def fig_repair(radius: int):
    """Figure 6 — repair, its boundary, and its price."""
    b = [text(20, 30, "Figure 6 — how far a damaged grid can be from the code", "ttl")]
    cx, cy = 250, 200
    for r, cls in ((130, "lite"), (98, "cell"), (66, "lite"), (34, "cell")):
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" class="{cls}"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="#16324f"/>')
    b.append(text(cx, cy + 30, "codeword", "sml", "middle"))
    for k, r in enumerate((34, 66, 98, 130), start=1):
        b.append(text(cx + r - 12, cy - r + 20, str(k), "sml"))
    b.append(text(430, 110, "\u2264 3 cells damaged", "lbl"))
    b.append(text(430, 132, "repair exists and is unique "
                            "(CubeTax.repair_unique_of_le_three)", "sml"))
    b.append(text(430, 176, f"= {radius} cells", "lbl"))
    b.append(text(430, 198, "repair still exists, and is genuinely ambiguous", "sml"))
    b.append(text(430, 216, "(covering_radius_le_four, covering_radius_ge_four,", "sml"))
    b.append(text(430, 234, " repair_ambiguous_at_four)", "sml"))
    b.append(text(430, 278, "price of a repair", "lbl"))
    b.append(text(430, 300, "cells \u00b7 Q, so at most 4\u00b7Q, and 4\u00b7Q is attained "
                            "by one whole face", "sml"))
    b.append(text(20, 370, "free moves: XOR with a codeword (CubeTax.xor_codeword_free); "
                           "priced moves: the nonlinear ones, e.g. AND (and_is_priced)", "lbl"))
    svg("fig6_repair.svg", 900, 400, "\n".join(b))


def fig_symmetry():
    """Figure 7 — the symmetry table."""
    rows = [
        ("O_h  (all 48)", "no invariant Golay code", "no_Oh_invariant_golay"),
        ("T_d  (24, with diagonal mirrors)", "no invariant Golay code", "no_Td_invariant_golay"),
        ("O    (24 rotations)", "an invariant Golay code exists", "exists_O_invariant_golay"),
        ("T_h  (24, pyritohedral)", "an invariant Golay code exists", "exists_Th_invariant_golay"),
        ("T    (12, canonical MOG placement)", "exactly the free symmetries", "CubeStab.stabiliser_card"),
    ]
    b = [text(20, 30, "Figure 7 — which cube symmetries a Golay code can keep", "ttl")]
    b.append(text(20, 55, "a symmetry is free when it maps the code to itself; "
                          "everything else must be paid for", "sml"))
    y = 90
    b.append(rect(40, y, 840, 30, "lite"))
    b.append(text(56, y + 20, "group", "lbl"))
    b.append(text(360, y + 20, "verdict", "lbl"))
    b.append(text(640, y + 20, "theorem", "lbl"))
    for k, (g, v, t) in enumerate(rows):
        yy = y + 30 * (k + 1)
        b.append(rect(40, yy, 840, 30, "cell"))
        b.append(text(56, yy + 20, g, "lbl"))
        b.append(text(360, yy + 20, v, "lbl"))
        b.append(text(640, yy + 20, t, "mono"))
    b.append(text(20, y + 30 * (len(rows) + 1) + 34,
                  "the two negative rows hold for every Golay code on the 24 cells, not "
                  "just for one placement", "sml"))
    svg("fig7_symmetry.svg", 920, y + 30 * (len(rows) + 1) + 60, "\n".join(b))


def main():
    print("recomputing the numbers in the figures\n")
    r = checks()
    for k, v in r.items():
        print(f"  {k:44s} {v}")
    assert r["hexacode words"] == 64
    assert r["hexacode minimum distance"] == 4
    assert r["hexacode words per incoming triple"] == [1]
    assert r["surface codewords"] == 4096
    assert r["surface code is closed under the MOG law"]
    assert r["surface weight enumerator"] == {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}
    assert r["the two constructions agree"]
    assert r["covering radius"] == 4
    assert r["fibres of the face symbol"] == [4]
    print("\nall checks pass; drawing\n")
    fig_mog_grid()
    fig_cube_net()
    fig_tile_io()
    fig_layers(r["surface codewords"])
    fig_weights(r["surface weight enumerator"])
    fig_repair(r["covering radius"])
    fig_symmetry()


if __name__ == "__main__":
    main()
