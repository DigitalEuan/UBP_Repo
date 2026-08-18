import GolayTiles.Hexacode
import GolayTiles.Cost
import GolayTiles.Surface
import GolayTiles.Stabiliser
import GolayTiles.Tax
import GolayTiles.Turyn
import GolayTiles.Substrate
import GolayTiles.Code
import GolayTiles.Steiner
import GolayTiles.Enumerator
import GolayTiles.Involution
import GolayTiles.Pyritohedral

/-!
# The Golay tile set

A standalone, machine-checked account of the **Golay tile method**: the
extended binary Golay code `[24, 12, 8]` presented as a `4 × 6` MOG grid, that
grid folded onto the surface of a cube, the cube read as a *tile* whose six
faces carry hexacode digits, and the arithmetic of laying such tiles side by
side — repair, price, symmetry, and the two standard constructions.

Nothing in this library depends on anything outside Mathlib.  Import
`GolayTiles` to get all of it.

## The eleven modules, in dependence order

| module | what it settles |
|---|---|
| `GolayTiles.Hexacode` | `GF(4)`, the `[6,3,4]` hexacode, one tile, and assemblies of tiles |
| `GolayTiles.Cost` | the quanta `Y`, `Q`, and the coherence ladder `1, 1/2, 2/5, 1/3, 1/4` |
| `GolayTiles.Surface` | the cube surface as the MOG grid; `2^24 → 2^18 → 2^12`; face erasure |
| `GolayTiles.Stabiliser` | which of the 48 cube symmetries a given tiling gives away free |
| `GolayTiles.Tax` | syndrome, coset leaders, covering radius 4, the sharp price `4·Q` |
| `GolayTiles.Turyn` | the three-cube (Turyn) construction of the same code |
| `GolayTiles.Substrate` | the code from its generator matrix: `d = 8`, syndrome diagnosis |
| `GolayTiles.Code` | Golay codes abstractly: self-duality and `2^(12-k)` words on `k ≤ 7` cells |
| `GolayTiles.Steiner` | the octads form a Steiner system `S(5, 8, 24)` |
| `GolayTiles.Enumerator` | 759 octads and the weight enumerator `1, 759, 2576, 759, 1` |
| `GolayTiles.Involution` | no tiling of the cube surface is `T_d`- or `O_h`-invariant |
| `GolayTiles.Pyritohedral` | tilings invariant under the rotations `O` and under `T_h`, exactly |

`GolayTiles/README.md` is the prose explanation, with figures and a claim-by-claim
map into these files.
-/
