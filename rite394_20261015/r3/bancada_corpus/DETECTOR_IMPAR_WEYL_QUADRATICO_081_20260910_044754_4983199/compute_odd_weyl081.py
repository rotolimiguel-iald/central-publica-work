"""Finite exact rational/Laurent/exterior controls, using only standard Python."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if ROOT != Path(r"C:\IALD\Central de Patentes\Chatgpt"):
    raise RuntimeError("Wrong output root")
SOURCES = [
    ROOT / "FUNCIONAL_IMPAR_TT_079_20260910/FUNCIONAL_IMPAR_E_ELIMINACAO_DA_CONTRIBUICAO_ANTIFIELD.md",
    ROOT / "LIBERDADE_DE_LEVANTAMENTO_079_20260910/CORRECOES_E4_E5_PROJECAO_SIGMA_E_SISTEMA_LOCAL.md",
    ROOT / "RESIDUO_PONTRYAGIN_S0_078_20260910/CERTIFICADO_NAO_EXATIDAO_A6_E_LIMITE_DO_RAMO.md",
    ROOT / "CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368/CARACTER_EXATO_LAMBDA3_WG_080.json",
    ROOT / "GERACAO_WEYL_H3_E4_080_20260910/GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md",
]

def pin(path):
    data = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def write_new(path, obj):
    data = json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    temp = path.with_name(path.name + ".pending")
    if path.exists() or temp.exists():
        raise FileExistsError(path)
    with temp.open("xb") as output:
        output.write(data)
    if temp.read_bytes() != data:
        raise RuntimeError("Byte mismatch")
    temp.rename(path)

before = [pin(path) for path in SOURCES]
checks = []
def check(name, valid, detail=None):
    checks.append({"name": name, "pass": bool(valid), "detail": detail})
    if not valid:
        raise RuntimeError(name)

# Commutative Laurent polynomials in (k,z,ell,f,p=f',q=f'').
ZERO = (0, 0, 0, 0, 0, 0)
def mono(coefficient=1, **powers):
    indices = {"k": 0, "z": 1, "ell": 2, "f": 3, "p": 4, "q": 5}
    exponent = [0] * 6
    for name, power in powers.items():
        exponent[indices[name]] = power
    return {tuple(exponent): F(coefficient)} if coefficient else {}

def add(*items):
    result = {}
    for item in items:
        for exponent, coefficient in item.items():
            result[exponent] = result.get(exponent, F(0)) + coefficient
    return {e: c for e, c in result.items() if c}

def scale(item, coefficient):
    return {e: c * coefficient for e, c in item.items() if c * coefficient}

def multiply(left, right):
    result = {}
    for e, c in left.items():
        for f, d in right.items():
            exponent = tuple(a + b for a, b in zip(e, f))
            result[exponent] = result.get(exponent, F(0)) + c * d
    return {e: c for e, c in result.items() if c}

def partial(item, axis):
    result = {}
    for exponent, coefficient in item.items():
        if exponent[axis]:
            output = list(exponent)
            output[axis] -= 1
            result[tuple(output)] = coefficient * exponent[axis]
    return result

def total_z(item):
    return add(partial(item, 1), multiply(mono(p=1), partial(item, 3)),
               multiply(mono(q=1), partial(item, 4)))

def point(item):
    # Apply f=0,p=1,q=2/z,ell=z only AFTER differentiating at fixed ell.
    result = {}
    for (k, z, ell, f, p, q), coefficient in item.items():
        if f:
            continue
        exponent = (k, z + ell - q, 0, 0, 0, 0)
        result[exponent] = result.get(exponent, F(0)) + coefficient * 2 ** q
    return {e: c for e, c in result.items() if c}

def encode_poly(item):
    return [{"powers_k_z_ell_f_p_q": list(e), "coefficient": str(c)} for e, c in sorted(item.items())]

# Exterior algebra in four generators, with the above polynomials as even coefficients.
def ext_add(*items):
    result = {}
    for item in items:
        for mask, coefficient in item.items():
            result[mask] = add(result.get(mask, {}), coefficient)
    return {m: c for m, c in result.items() if c}

def ext_scale(item, coefficient):
    return {m: multiply(c, coefficient) for m, c in item.items() if multiply(c, coefficient)}

def wedge(left, right):
    result = {}
    for m, a in left.items():
        for n, b in right.items():
            if m & n:
                continue
            crossings = sum(1 for i in range(4) for j in range(4) if (m >> i & 1) and (n >> j & 1) and i > j)
            term = scale(multiply(a, b), (-1) ** crossings)
            result[m | n] = add(result.get(m | n, {}), term)
    return {m: c for m, c in result.items() if c}

theta = [{1 << i: mono()} for i in range(4)]
def pair(i, j):
    return wedge(theta[i], theta[j])

def epsilon(indices):
    return (-1) ** sum(indices[i] > indices[j] for i in range(4) for j in range(i + 1, 4))

# m^{i3}=-theta^i/z and m^{3i}=+theta^i/z for the four Killing fields of detector079.
m = [[{} for j in range(4)] for i in range(4)]
for i in range(3):
    m[i][3] = ext_scale(theta[i], mono(-1, z=-1))
    m[3][i] = ext_scale(theta[i], mono(z=-1))
beta = {}
for a, b, c, d in permutations(range(4)):
    term = wedge(pair(a, b), m[c][d])
    beta = ext_add(beta, ext_scale(term, mono(F(epsilon((a, b, c, d)), 2))))
check("beta_from_epsilon_contraction", beta == {7: mono(-6, z=-1)})

dtheta = [ext_scale(pair(i, 3), mono(z=-1)) for i in range(3)] + [{}]
def dghost(item):
    result = {}
    for mask, coefficient in item.items():
        indices = [i for i in range(4) if mask >> i & 1]
        for position, index in enumerate(indices):
            term = {0: coefficient}
            for earlier in indices[:position]:
                term = wedge(term, theta[earlier])
            term = wedge(term, dtheta[index])
            for later in indices[position + 1:]:
                term = wedge(term, theta[later])
            result = ext_add(result, ext_scale(term, mono((-1) ** position)))
    return result
dbeta = dghost(beta)
check("s1_beta_from_killing_ghost_bracket", dbeta == {15: mono(-18, z=-2)})
check("ghost_differential_nilpotent_on_generators", all(not dghost(item) for item in dtheta))

# Curvature forms at tau=0 on the linearized Einstein solution; their derivation is written separately.
electric = scale(add(mono(k=2, f=1), mono(-1, z=-1, p=1)), F(1, 2))
magnetic = mono(F(1, 2), k=1, p=1)
forms = {
    (0, 1): ext_add(ext_scale(pair(0, 1), electric), ext_scale(pair(2, 3), magnetic)),
    (0, 2): ext_add(ext_scale(pair(0, 2), scale(electric, -1)), ext_scale(pair(1, 3), magnetic)),
    (1, 3): ext_add(ext_scale(pair(0, 2), magnetic), ext_scale(pair(1, 3), electric)),
    (2, 3): ext_add(ext_scale(pair(0, 1), magnetic), ext_scale(pair(2, 3), scale(electric, -1))),
}
eta = [1, -1, -1, -1]
trace_wedge = {}
for (a, b), form in forms.items():
    trace_wedge = ext_add(trace_wedge, ext_scale(wedge(form, form), mono(-2 * eta[a] * eta[b])))
rho = trace_wedge.get(15, {})
check("trace_weyl_wedge_normalization", trace_wedge == {15: scale(multiply(electric, magnetic), 16)})
j = multiply(rho, mono(z=4, ell=-4))
expected_j = add(mono(4, k=3, z=4, ell=-4, f=1, p=1), mono(-4, k=1, z=3, ell=-4, p=2))
check("pseudoscalar_formula", j == expected_j)
j0 = point(j)
jprime = point(total_z(j))
check("pseudoscalar_at_point", j0 == mono(-4, k=1, z=-1))
check("derivative_at_fixed_ell", jprime == add(mono(4, k=3), mono(-28, k=1, z=-2)))
response = ext_add(wedge(ext_scale(theta[3], jprime), beta), ext_scale(dbeta, j0))
expected_response = add(mono(24, k=3, z=-1), mono(-96, k=1, z=-3))
check("s1_quadratic_candidate", response == {15: expected_response})
reflected = {e: c * ((-1) ** e[0]) for e, c in expected_response.items()}
odd_part = scale(add(expected_response, scale(reflected, -1)), F(1, 2))
check("detector_odd_part", odd_part == expected_response)
at_k_inverse_z = {}
for (k, z, ell, f, p, q), coefficient in odd_part.items():
    key = (0, z - k, 0, 0, 0, 0)
    at_k_inverse_z[key] = at_k_inverse_z.get(key, F(0)) + coefficient
check("nonzero_at_k_inverse_z", at_k_inverse_z == mono(-72, z=-4))

# Exact representation count for the sector with two undifferentiated Weyl tensors.
def irrep(a, b):
    return Counter(product(range(a, -a - 1, -2), range(b, -b - 1, -2)))
weyl_weights = list(irrep(4, 0).elements()) + list(irrep(0, 4).elements())
sym2 = Counter()
for i, jindex in combinations_with_replacement(range(10), 2):
    a, b = weyl_weights[i]
    c, d = weyl_weights[jindex]
    sym2[a + c, b + d] += 1
check("symmetric_square_dimension", sum(sym2.values()) == 55)
remaining = sym2.copy()
decomposition = Counter()
while remaining:
    highest = max(remaining)
    multiplicity = remaining[highest]
    for weight, n in irrep(*highest).items():
        remaining[weight] -= multiplicity * n
    if any(n < 0 for n in remaining.values()):
        raise RuntimeError("Negative character remainder")
    remaining = Counter({w: n for w, n in remaining.items() if n})
    decomposition[highest] += multiplicity
expected_decomposition = Counter({(8, 0): 1, (0, 8): 1, (4, 0): 1, (0, 4): 1, (0, 0): 2, (4, 4): 1})
check("symmetric_square_decomposition", decomposition == expected_decomposition)
ghost_record = json.loads(SOURCES[3].read_bytes())
ghost_multiplicities = {tuple(item["highest_weight"]): item["multiplicity"] for item in ghost_record["decomposition"]}
overlap = [{"highest_weight": list(weight), "weyl_multiplicity": multiplicity,
            "ghost_multiplicity": ghost_multiplicities.get(weight, 0),
            "invariant_count": multiplicity * ghost_multiplicities.get(weight, 0)}
           for weight, multiplicity in sorted(decomposition.items()) if ghost_multiplicities.get(weight, 0)]
check("zero_derivative_invariant_count", sum(item["invariant_count"] for item in overlap) == 10)

after = [pin(path) for path in SOURCES]
check("all_sources_unchanged", before == after)
record = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "REAL exact integer/rational controls; geometric and cohomological contracts in accompanying written note",
    "sources_before": before, "sources_after": after,
    "script": pin(Path(__file__)),
    "runtime": {"python": sys.version, "executable": sys.executable},
    "beta": {"theta_mask": 7, "coefficient": encode_poly(beta[7])},
    "s1_beta": {"theta_mask": 15, "coefficient": encode_poly(dbeta[15])},
    "J": encode_poly(j), "J_at_point": encode_poly(j0), "dJ_dz_at_point": encode_poly(jprime),
    "detector_response_for_J_beta": encode_poly(odd_part),
    "detector_at_k_inverse_z": encode_poly(at_k_inverse_z),
    "engineering_weight_zero_candidate": "Multiply J beta by the inherited gravitational coupling kappa; detector response scales by kappa",
    "symmetric_square_weyl": [{"highest_weight": list(w), "multiplicity": n} for w, n in sorted(decomposition.items())],
    "overlap_with_lambda3_killing_ghosts": overlap,
    "checks": checks, "check_count": len(checks), "all_checks_pass": all(item["pass"] for item in checks),
    "limits": ["No all-jet classification", "No equality between d1 candidate and A6 class", "No solution of full cancellation system", "No execution/import of previous scripts, Lean, SymPy or um.py"],
}
destination = HERE / "CONTROLES_DETECTOR_WEYL_QUADRATICO_081.json"
write_new(destination, record)
print(json.dumps({"receipt": pin(destination), "checks": len(checks), "overlap": overlap, "response": encode_poly(odd_part)}, ensure_ascii=False))
