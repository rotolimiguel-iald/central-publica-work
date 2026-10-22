"""Exact integer characters for exterior degree three of (1,1)+(2,0)+(0,2).

Only Python standard library. No source files are imported or executed.
All outputs are new files adjacent to this script under Chatgpt.
"""
from collections import Counter
from datetime import datetime, timezone
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib
import json
import platform
import sys

HERE = Path(__file__).resolve().parent
if HERE.parent != Path(r"C:\IALD\Central de Patentes\Chatgpt"):
    raise RuntimeError("Unexpected output directory")

def pin(path):
    content = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}

def atomic_new(path, value):
    content = json.dumps(value, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    temporary = path.with_name(path.name + ".pending")
    if path.exists() or temporary.exists():
        raise FileExistsError(path)
    with temporary.open("xb") as output:
        output.write(content)
    if temporary.read_bytes() != content:
        raise RuntimeError("Output byte mismatch")
    temporary.rename(path)

def irrep_character(a, b):
    if a < 0 or b < 0:
        raise ValueError("Negative highest weight")
    return Counter(product(range(a, -a - 1, -2), range(b, -b - 1, -2)))

def convolve(left, right):
    result = Counter()
    for (a, b), ma in left.items():
        for (c, d), mb in right.items():
            result[a + c, b + d] += ma * mb
    return result

def encode_character(character):
    return [{"weight": [a, b], "multiplicity": n} for (a, b), n in sorted(character.items()) if n]

script_before = pin(Path(__file__))
checks = []
def check(name, valid, detail=None):
    checks.append({"name": name, "pass": bool(valid), "detail": detail})
    if not valid:
        raise RuntimeError(name)

# Build the basis weights from the three input highest weights, not a table for wedge^3.
input_irreps = [(1, 1), (2, 0), (0, 2)]
basis_weights = []
for a, b in input_irreps:
    basis_weights.extend(irrep_character(a, b).elements())
check("one_particle_dimension", len(basis_weights) == 10)

# Distinct basis indices, including distinct zero-weight vectors, label exterior monomials.
exterior = Counter()
exterior_basis_count = 0
for indices in combinations(range(len(basis_weights)), 3):
    exterior_basis_count += 1
    weight = tuple(sum(basis_weights[index][axis] for index in indices) for axis in (0, 1))
    exterior[weight] += 1
check("exterior_basis_count", exterior_basis_count == comb(10, 3) == 120)
check("exterior_character_dimension", sum(exterior.values()) == 120)

# Independent Newton character identity: 6 wedge^3 chi = chi^3 - 3 chi psi_2(chi) + 2 psi_3(chi).
chi = Counter(basis_weights)
chi_cubed = convolve(convolve(chi, chi), chi)
psi2 = Counter({(2 * a, 2 * b): n for (a, b), n in chi.items()})
psi3 = Counter({(3 * a, 3 * b): n for (a, b), n in chi.items()})
mixed = convolve(chi, psi2)
support = set(chi_cubed) | set(mixed) | set(psi3)
numerator = {weight: chi_cubed[weight] - 3 * mixed[weight] + 2 * psi3[weight] for weight in support}
check("newton_coefficients_divisible_by_six", all(n % 6 == 0 for n in numerator.values()))
newton = Counter({weight: n // 6 for weight, n in numerator.items() if n})
check("newton_matches_exterior_enumeration", newton == exterior)

# Highest weights are recovered from the computed character by lexicographic elimination.
remaining = exterior.copy()
decomposition = Counter()
steps = []
while remaining:
    highest = max(remaining)
    a, b = highest
    multiplicity = remaining[highest]
    if a < 0 or b < 0 or multiplicity <= 0:
        raise RuntimeError("Invalid dominant highest weight")
    representation = irrep_character(a, b)
    for weight, n in representation.items():
        remaining[weight] -= multiplicity * n
    if any(n < 0 for n in remaining.values()):
        raise RuntimeError("Negative remainder during character elimination")
    remaining = Counter({weight: n for weight, n in remaining.items() if n})
    decomposition[highest] += multiplicity
    steps.append({"highest_weight": [a, b], "multiplicity": multiplicity, "remaining_dimension": sum(remaining.values())})
check("highest_weight_elimination_terminates_nonnegative", not remaining)

reconstructed = Counter()
for (a, b), multiplicity in decomposition.items():
    for weight, n in irrep_character(a, b).items():
        reconstructed[weight] += multiplicity * n
check("irreducible_character_reconstruction", reconstructed == exterior)
dimension = sum(n * (a + 1) * (b + 1) for (a, b), n in decomposition.items())
check("irreducible_dimension", dimension == 120, dimension)
check("first_weyl_reflection", Counter({(-a, b): n for (a, b), n in exterior.items()}) == exterior)
check("second_weyl_reflection", Counter({(a, -b): n for (a, b), n in exterior.items()}) == exterior)
check("chirality_exchange", Counter({(b, a): n for (a, b), n in exterior.items()}) == exterior)

# The supplied manual proposal is used only as a comparison after the decomposition was computed.
manual_proposal = Counter({(4, 0): 1, (0, 4): 1, (2, 0): 1, (0, 2): 1,
                           (0, 0): 4, (2, 2): 4, (3, 3): 1,
                           (3, 1): 2, (1, 3): 2, (1, 1): 4})
check("manual_proposal_matches_computation", decomposition == manual_proposal)

max_first = max(a for a, b in exterior)
max_second = max(b for a, b in exterior)
check("coordinate_weight_bound", (max_first, max_second) == (4, 4))
overlap = []
for chirality in ("left", "right"):
    coordinate_bound = max_first if chirality == "left" else max_second
    largest_possible_r = coordinate_bound - 4
    for r in range(max(-1, largest_possible_r) + 1):
        highest = (4 + r, r) if chirality == "left" else (r, 4 + r)
        multiplicity = decomposition[highest]
        if multiplicity:
            overlap.append({"chirality": chirality, "r": r, "highest_weight": list(highest), "multiplicity": multiplicity})
check("weyl_tower_overlap", overlap == [
    {"chirality": "left", "r": 0, "highest_weight": [4, 0], "multiplicity": 1},
    {"chirality": "right", "r": 0, "highest_weight": [0, 4], "multiplicity": 1},
])
script_after = pin(Path(__file__))
check("computation_script_unchanged", script_before == script_after)

result = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "REAL exact integer arithmetic; finite-dimensional character identity only",
    "weight_convention": "Highest weights are nonnegative integers 2j for sl2(C) x sl2(C)",
    "input_irreps": [list(x) for x in input_irreps],
    "one_particle_basis_weights": [list(weight) for weight in basis_weights],
    "exterior_degree": 3,
    "exterior_character": encode_character(exterior),
    "decomposition": [{"highest_weight": [a, b], "multiplicity": n, "irrep_dimension": (a + 1) * (b + 1)} for (a, b), n in sorted(decomposition.items())],
    "elimination_steps": steps,
    "total_dimension": dimension,
    "weyl_jet_tower_comparison": {
        "proposed_towers": "(4+r,r) and (r,4+r), r a nonnegative integer",
        "coordinate_bounds": [max_first, max_second],
        "all_r_exclusion": "For r >= 1 one coordinate is at least 5, above the character bound 4",
        "overlap": overlap,
        "jet_complex_identification_proved_here": False,
    },
    "checks": checks,
    "check_count": len(checks),
    "all_checks_pass": all(item["pass"] for item in checks),
    "script_before": script_before,
    "script_after": script_after,
    "runtime": {"python": sys.version, "implementation": platform.python_implementation(), "executable": sys.executable},
    "scope_exclusions": ["No classification of H3(s0) E4", "No Calabi or natural jet comparison", "No cohomology base change", "No claim about delta(K), QME, or UV"],
    "no_sympy_lean_um_or_source_import": True,
}
destination = HERE / "CARACTER_EXATO_LAMBDA3_WG_080.json"
atomic_new(destination, result)
print(json.dumps({"result": pin(destination), "decomposition": result["decomposition"], "checks": len(checks), "weyl_overlap": overlap}, ensure_ascii=False))
