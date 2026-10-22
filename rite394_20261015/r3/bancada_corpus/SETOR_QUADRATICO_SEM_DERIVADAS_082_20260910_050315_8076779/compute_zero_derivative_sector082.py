"""New exact exterior calculation082; copied pure functions, no old source execution."""
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if ROOT != Path(r"C:\IALD\Central de Patentes\Chatgpt"):
    raise RuntimeError("Unexpected output root")
checks = []
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

def check(name, valid, detail=None):
    checks.append({"name": name, "pass": bool(valid), "detail": detail})
    if not valid:
        raise RuntimeError(name)

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

def pair(i, j):
    return wedge(theta[i], theta[j])

def epsilon(indices):
    return (-1) ** sum(indices[i] > indices[j] for i in range(4) for j in range(i + 1, 4))

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

SOURCES = [
    ROOT / "DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md",
    ROOT / "DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTROLES_DETECTOR_WEYL_QUADRATICO_081.json",
    ROOT / "FUNCIONAL_IMPAR_TT_079_20260910/FUNCIONAL_IMPAR_E_ELIMINACAO_DA_CONTRIBUICAO_ANTIFIELD.md",
    ROOT / "CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368/CARACTER_EXATO_LAMBDA3_WG_080.json",
]
before = [pin(path) for path in SOURCES]
eta = [1, -1, -1, -1]
theta = [{1 << i: mono()} for i in range(4)]
dtheta = [ext_scale(pair(i, 3), mono(z=-1)) for i in range(3)] + [{}]
mupper = [[{} for b in range(4)] for a in range(4)]
for i in range(3):
    mupper[i][3] = ext_scale(theta[i], mono(-1, z=-1))
    mupper[3][i] = ext_scale(theta[i], mono(z=-1))
mlower = [[ext_scale(mupper[a][b], mono(eta[a] * eta[b])) for b in range(4)] for a in range(4)]
mixed_m = [[ext_scale(mupper[a][b], mono(eta[b])) for b in range(4)] for a in range(4)]

def matmul(left, right):
    return [[ext_add(*(wedge(left[a][c], right[c][b]) for c in range(4))) for b in range(4)] for a in range(4)]

def trace(matrix):
    return ext_add(*(matrix[a][a] for a in range(4)))

def dual_mixed(matrix):
    result = [[{} for b in range(4)] for a in range(4)]
    for a, b, c, d in permutations(range(4)):
        # *M^a_b = eta_a/2 epsilon_abcd M^{cd}; M^{cd}=M^c_d eta_d.
        coefficient = F(eta[a] * eta[d] * epsilon((a, b, c, d)), 2)
        result[a][b] = ext_add(result[a][b], ext_scale(matrix[c][d], mono(coefficient)))
    return result

star_m = dual_mixed(mixed_m)
double_star = dual_mixed(star_m)
check("hodge_square_minus_identity", double_star == [[ext_scale(item, mono(-1)) for item in row] for row in mixed_m])

beta_even = ext_add(*(wedge(mlower[a][b], pair(a, b)) for a in range(4) for b in range(4)))
beta_odd = ext_add(*(ext_scale(wedge(pair(a, b), mupper[c][d]), mono(F(epsilon((a, b, c, d)), 2))) for a, b, c, d in permutations(range(4))))
gamma_even = trace(matmul(matmul(mixed_m, mixed_m), mixed_m))
gamma_odd = trace(matmul(star_m, matmul(mixed_m, mixed_m)))
ghost_cubics = {"beta_even": beta_even, "beta_odd": beta_odd, "gamma_even": gamma_even, "gamma_odd": gamma_odd}
check("beta_even_zero", not beta_even)
check("beta_odd_value", beta_odd == {7: mono(-6, z=-1)})
check("gamma_even_zero", not gamma_even)
check("gamma_odd_value", gamma_odd == {7: mono(6, z=-3)})
check("odd_cubics_proportional", gamma_odd == ext_scale(beta_odd, mono(-1, z=-2)))
ghost_d = {name: dghost(value) for name, value in ghost_cubics.items()}
check("beta_odd_differential", ghost_d["beta_odd"] == {15: mono(-18, z=-2)})
check("gamma_odd_differential", ghost_d["gamma_odd"] == {15: mono(18, z=-4)})
check("even_cubics_differentials_zero", not ghost_d["beta_even"] and not ghost_d["gamma_even"])

electric = scale(add(mono(k=2, f=1), mono(-1, z=-1, p=1)), F(1, 2))
magnetic = mono(F(1, 2), k=1, p=1)
scalar_I = multiply(scale(add(multiply(electric, electric), scale(multiply(magnetic, magnetic), -1)), 16), mono(z=4, ell=-4))
scalar_J = multiply(scale(multiply(electric, magnetic), 16), mono(z=4, ell=-4))
def odd_part(value):
    reflected = {e: c * ((-1) ** e[0]) for e, c in value.items()}
    return scale(add(value, scale(reflected, -1)), F(1, 2))
def at_k_times_inverse_z(value, factor):
    result = {}
    for (k, z, ell, f, p, q), coefficient in value.items():
        exponent = (0, z - k, 0, 0, 0, 0)
        result[exponent] = result.get(exponent, F(0)) + coefficient * factor ** k
    return {e: c for e, c in result.items() if c}

responses = {}
for scalar_name, scalar in [("I", scalar_I), ("J", scalar_J)]:
    value = point(scalar)
    derivative = point(total_z(scalar))
    for name, cubic in ghost_cubics.items():
        response = ext_add(wedge(ext_scale(theta[3], derivative), cubic), ext_scale(ghost_d[name], value))
        responses[scalar_name + "_" + name] = odd_part(response.get(15, {}))
check("I_sector_invisible", all(not value for name, value in responses.items() if name.startswith("I_")))
check("J_even_cubics_invisible", not responses["J_beta_even"] and not responses["J_gamma_even"])
profile = add(mono(24, k=3, z=-1), mono(-96, k=1, z=-3))
check("J_beta_profile", responses["J_beta_odd"] == profile)
check("J_gamma_profile", responses["J_gamma_odd"] == multiply(profile, mono(-1, z=-2)))
check("all_scalar_product_responses_zero_at_k_2_over_z", all(not at_k_times_inverse_z(value, 2) for value in responses.values()))

# A ten-element Weyl basis from symmetric trace-free electric and magnetic 3x3 matrices.
def epsilon3(i, j, k):
    if len({i, j, k}) != 3:
        return 0
    order = (i, j, k)
    return (-1) ** sum(order[a] > order[b] for a in range(3) for b in range(a + 1, 3))

matrices = [
    [[1, 0, 0], [0, -1, 0], [0, 0, 0]],
    [[1, 0, 0], [0, 1, 0], [0, 0, -2]],
]
for a, b in [(0, 1), (0, 2), (1, 2)]:
    value = [[0] * 3 for _ in range(3)]
    value[a][b] = value[b][a] = 1
    matrices.append(value)

def weyl_tensor(E, B):
    out = {}
    def put(a, b, c, d, value):
        for aa, bb, ss in [(a, b, 1), (b, a, -1)]:
            for cc, dd, tt in [(c, d, 1), (d, c, -1)]:
                for indices in [(aa, bb, cc, dd), (cc, dd, aa, bb)]:
                    if indices in out and out[indices] != ss * tt * value:
                        raise RuntimeError("Inconsistent curvature assignment")
                    out[indices] = ss * tt * value
    for i, j in product(range(1, 4), repeat=2):
        put(0, i, 0, j, E[i - 1][j - 1])
    for i in range(1, 4):
        for j in range(1, 4):
            for k in range(j + 1, 4):
                put(0, i, j, k, sum(epsilon3(j, k, l) * B[i - 1][l - 1] for l in range(1, 4)))
    for i in range(1, 4):
        for j in range(i + 1, 4):
            for k in range(1, 4):
                for l in range(k + 1, 4):
                    put(i, j, k, l, -sum(epsilon3(i, j, m) * epsilon3(k, l, n) * E[m - 1][n - 1] for m in range(1, 4) for n in range(1, 4)))
    return {indices: out.get(indices, 0) for indices in product(range(4), repeat=4)}

zero = [[0] * 3 for _ in range(3)]
weyl_basis = [weyl_tensor(M, zero) for M in matrices] + [weyl_tensor(zero, M) for M in matrices]
all_bianchi = all(T[a, b, c, d] + T[b, c, a, d] + T[c, a, b, d] == 0 for T in weyl_basis for a, b, c, d in product(range(4), repeat=4))
all_traceless = all(sum(eta[a] * T[a, b, a, d] for a in range(4)) == 0 for T in weyl_basis for b, d in product(range(4), repeat=2))
check("ten_weyl_tensors_bianchi", all_bianchi)
check("ten_weyl_tensors_traceless", all_traceless)
evaluated = []
for T in weyl_basis:
    contraction = ext_add(*(ext_scale(wedge(pair(a, b), mupper[c][d]), mono(T[a, b, c, d])) for a, b, c, d in product(range(4), repeat=4) if T[a, b, c, d]))
    evaluated.append(contraction)
check("weyl_C_C_m_zero_on_entire_ten_dimensional_fiber", all(not item for item in evaluated))
check("ghost_d_of_zero_weyl_contractions", all(not dghost(item) for item in evaluated))

after = [pin(path) for path in SOURCES]
check("sources_unchanged", before == after)
record = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "REAL exact finite algebra; global interpretation only in written note",
    "sources_before": before, "sources_after": after,
    "script": pin(Path(__file__)),
    "runtime": {"python": sys.version, "executable": sys.executable},
    "ghost_cubic_values": {name: [{"theta_mask": mask, "coefficient": encode_poly(coeff)} for mask, coeff in value.items()] for name, value in ghost_cubics.items()},
    "ghost_cubic_differentials": {name: [{"theta_mask": mask, "coefficient": encode_poly(coeff)} for mask, coeff in value.items()] for name, value in ghost_d.items()},
    "scalar_product_detector_profiles_unweighted": {name: encode_poly(value) for name, value in responses.items()},
    "engineering_prefactors": {"beta_cubics": "kappa", "gamma_cubics": "kappa squared"},
    "weyl_type_contractions": {"basis_size": 10, "all_zero": True, "scope": "Algebraic fiber; derivative with respect to arbitrary Weyl components is zero by the same linear identity"},
    "checks": checks, "check_count": len(checks), "all_checks_pass": all(item["pass"] for item in checks),
    "scope": "Ten invariant contractions with two undifferentiated Weyl tensors; no all-jet/no full delta(K) exclusion",
}
destination = HERE / "CONTROLES_SETOR_SEM_DERIVADAS_082.json"
write_new(destination, record)
print(json.dumps({"receipt": pin(destination), "checks": len(checks), "profiles": record["scalar_product_detector_profiles_unweighted"]}, ensure_ascii=False))
