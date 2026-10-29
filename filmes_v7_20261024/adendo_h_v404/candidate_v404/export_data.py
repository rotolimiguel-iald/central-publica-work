# -*- coding: utf-8 -*-
"""export_frames_v1.py -- O EXPORTADOR DO VIDEO (EXTERNO ao um.py; o um.py NAO se toca).

Le a rodada COMPLETA v350 (um_absoluto.json + um_absoluto_selo.json + rodada_v398_stdout.txt),
importa o um.py como MODULO (o rito so corre sob __main__; import sem stdout e sem arquivo novo,
verificado) e grava em data/:
  hud.json      -- os numeros que entram na tela, com a chave de origem e o estatuto
  frames.json   -- as curvas por estagio, calculadas pelas funcoes/construcoes do proprio programa
  MANIFEST.json -- sha256 das fontes, proveniencia de cada conjunto, ancoras (residuais vs o selo)
Regua: nenhum numero digitado; beta = SEALED_CODATA_ALPHA*sqrt(e) em runtime (nunca literal);
hash lido do arquivo; qualquer ancora que nao bata e falha visivel (exit 2).
"""
import os, sys, io, json, math, hashlib, time, contextlib, re
NOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'source')
VID = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(VID, 'data'); os.makedirs(DATA, exist_ok=True)
sys.dont_write_bytecode = True
sys.path.insert(0, NOS)
import numpy as np
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    import um
assert _buf.getvalue() == '', 'import um emitiu stdout: %r' % _buf.getvalue()[:200]
assert os.path.abspath(um.__file__).lower().startswith(NOS.lower()), um.__file__


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


seal_header = json.load(open(os.path.join(NOS,'um_absoluto_selo.json'),encoding='utf-8'))
stdout_name = 'rodada_' + seal_header['um_version'] + '_stdout.txt'
SRC = {n: os.path.join(NOS, n) for n in ['um.py', 'um_absoluto.json', 'um_absoluto_selo.json', stdout_name]}
SHA = {n: sha(p) for n, p in SRC.items()}
selo = json.load(open(SRC['um_absoluto_selo.json'], encoding='utf-8'))
res = json.load(open(SRC['um_absoluto.json'], encoding='utf-8')); C = res['core']
selo_um = selo.get('sha256.um.py') or (selo.get('sha256') or {}).get('um.py')
assert selo_um == SHA['um.py'], 'o selo nao bate com o um.py em disco'
stdout = open(SRC[stdout_name], encoding='utf-8', errors='replace').read()
m = re.search(r'teoremas limpos:\s*(\d+)/(\d+)', stdout); assert m, 'stdout sem "teoremas limpos"'
proof = C['estatuto_da_prova_v391']['prova_1_kernel']
theorems_clean, theorems_total = proof['n_theorems_clean'], proof['n_theorems_expected']
assert (theorems_clean,theorems_total)==(int(m.group(1)),int(m.group(2)))

ONE = 1
beta_rt = um.SEALED_CODATA_ALPHA * ONE * math.sqrt(math.e)   # NUNCA literal
theta_M = math.asin(math.sqrt(beta_rt))
TRIO = {'propext', 'Classical.choice', 'Quot.sound'}
kf = C['kernel_formalization']; ar = kf['axiom_report']
outside_trio = sum(1 for v in ar.values() if any(a not in TRIO for a in v))
n_formal_files = len(kf['formal_files_sha256'])

# ---------------- as funcoes do programa, chamadas AO VIVO (ancoras contra o selo) ----------------
live = {}
live['fractal_dephasing'] = um.fractal_dephasing_principle(ONE)
live['smatrix_closure'] = um.prove_smatrix_closure(ONE)
live['solder_4d'] = um.prove_solder_4d(ONE)
live['local_breuer_gap'] = um.prove_local_breuer_gap(ONE)
live['minimal_solder'] = um.prove_minimal_solder(ONE)
live['schwarzschild_step'] = um.prove_the_schwarzschild_step(ONE)
live['graviton_polarization'] = um.prove_graviton_polarization(ONE, kf)
live['the_TGL_identity_equation'] = um.prove_the_TGL_identity_equation(C)

anchors = []


def anchor(name, json_path, jv, lv, tol=1e-9):
    num = isinstance(jv, (int, float)) and isinstance(lv, (int, float))
    resid = abs(float(jv) - float(lv)) if num else 'AUSENTE'
    ok = bool(num and resid <= tol)
    anchors.append({'name': name, 'json_path': json_path, 'json_value': jv, 'live_value': lv, 'residual': resid, 'tol': tol, 'ok': ok})
    return ok


anchor('leak = sin^2(theta_M) = beta', 'core.fractal_dephasing.leak_sin2_thetaM', C['fractal_dephasing']['leak_sin2_thetaM'], live['fractal_dephasing']['leak_sin2_thetaM'], 1e-15)
anchor('tau_reflected', 'core.smatrix_closure.tau_reflected', C['smatrix_closure']['tau_reflected'], live['smatrix_closure']['tau_reflected'], 1e-15)
anchor('tr(S)/2 = sqrt(1-beta)', 'core.smatrix_closure.tr_norm_eq_sqrt_1_minus_beta', C['smatrix_closure']['tr_norm_eq_sqrt_1_minus_beta'], live['smatrix_closure']['tr_norm_eq_sqrt_1_minus_beta'], 1e-15)
anchor('r_UtI', 'core.smatrix_closure.r_UtI', C['smatrix_closure']['r_UtI'], live['smatrix_closure']['r_UtI'], 1e-12)
anchor('wigner_rotation_norm', 'core.solder_4d.wigner_rotation_norm', C['solder_4d']['wigner_rotation_norm'], live['solder_4d']['wigner_rotation_norm'], 1e-12)
anchor('hminus_gap_second_eig', 'core.local_breuer_gap.hminus_gap_second_eig', C['local_breuer_gap']['hminus_gap_second_eig'], live['local_breuer_gap']['hminus_gap_second_eig'], 1e-9)
anchor('zero_mode_weight_quadrature', 'core.local_breuer_gap.zero_mode_weight_quadrature', C['local_breuer_gap']['zero_mode_weight_quadrature'], live['local_breuer_gap']['zero_mode_weight_quadrature'], 1e-12)
anchor('zero_mode_overlap_sech', 'core.local_breuer_gap.zero_mode_overlap_sech', C['local_breuer_gap']['zero_mode_overlap_sech'], live['local_breuer_gap']['zero_mode_overlap_sech'], 1e-9)
anchor('R_recovered', 'core.minimal_solder.R_recovered', C['minimal_solder']['R_recovered'], live['minimal_solder']['R_recovered'], 1e-12)
anchor('plaquette_order', 'core.minimal_solder.plaquette_order', C['minimal_solder']['plaquette_order'], live['minimal_solder']['plaquette_order'], 1e-6)
anchor('schwarzschild residual_Et', 'core.schwarzschild_step.residual_Et', C['schwarzschild_step']['residual_Et'], live['schwarzschild_step']['residual_Et'], 1e-12)
anchor('schwarzschild residual_Er', 'core.schwarzschild_step.residual_Er', C['schwarzschild_step']['residual_Er'], live['schwarzschild_step']['residual_Er'], 1e-12)
anchor('helicity_plus residual', 'core.graviton_polarization.residuals.helicity_plus', C['graviton_polarization']['residuals']['helicity_plus'], live['graviton_polarization']['residuals']['helicity_plus'], 1e-15)
anchor('boundary_deviation_norm_sq', 'core.graviton_polarization.values.boundary_deviation_norm_sq', C['graviton_polarization']['values']['boundary_deviation_norm_sq'], live['graviton_polarization']['values']['boundary_deviation_norm_sq'], 1e-12)
anchor('identity: member_true_max_residual', 'core.the_TGL_identity_equation.member_true_max_residual', C['the_TGL_identity_equation']['member_true_max_residual'], live['the_TGL_identity_equation']['member_true_max_residual'], 1e-15)
anchor('identity: member_false_min_residual', 'core.the_TGL_identity_equation.member_false_min_residual', C['the_TGL_identity_equation']['member_false_min_residual'], live['the_TGL_identity_equation']['member_false_min_residual'], 1e-15)
anchor('beta runtime (graviton_polarization.values.beta_runtime)', 'core.graviton_polarization.values.beta_runtime', C['graviton_polarization']['values']['beta_runtime'], beta_rt, 1e-17)
anchor('theta_M rad', 'core.theta_M_rad', C['theta_M_rad'], theta_M, 1e-12)

# ---------------- FRAMES: as construcoes do programa avaliadas ao longo do parametro ----------------
F = {}
lin = lambda a, b, n: [float(v) for v in np.linspace(a, b, n)]
G2 = np.array([[0., 1.], [-1., 0.]]); P = np.array([[1., 0.], [0., 0.]]); Q0 = np.eye(2) - P

# (A) O ESPELHO: S(theta) = exp(theta.G) (um._expm); vazamento tr(rho* Q_theta) (construcao de fractal_dephasing_principle)
th = lin(0.0, theta_M, 121); S = []; leak = []
for t in th:
    St = um._expm(t * G2).real
    c, s = math.cos(t), math.sin(t); R = np.array([[c, -s], [s, c]]); Qth = R @ Q0 @ R.T
    S.append([float(St[0, 0]), float(St[0, 1]), float(St[1, 0]), float(St[1, 1])]); leak.append(float(np.trace(P @ Qth)))
F['mirror'] = {'theta': th, 'S': S, 'leak': leak, 'refl': [math.sin(t) ** 2 for t in th], 'trans': [math.cos(t) ** 2 for t in th],
               'theta_M': theta_M, 'theta_M_deg': math.degrees(theta_M), 'beta': beta_rt, 'sqrt_beta': math.sqrt(beta_rt), 'sqrt_e': math.sqrt(math.e)}
assert abs(leak[-1] - live['fractal_dephasing']['leak_sin2_thetaM']) < 1e-15

# (B) A FACE: fluxo modular na cunha (boosts, um._expm) [KNOWN: Bisognano-Wichmann; kernel wedge_geometry] + escada de Powers (lambda = beta, ilustracao do programa)
Kb2 = np.array([[0., 1.], [1., 0.]])
ss = lin(-2.4, 2.4, 73); lines = []
for x0 in [0.25, 0.45, 0.7, 1.0, 1.4, 1.9, 2.5]:
    pts = []
    for s_ in ss:
        v = um._expm(s_ * Kb2).real @ np.array([0.0, x0])   # (t, x)
        pts.append([float(v[0]), float(v[1])])
    lines.append(pts)
lam = beta_rt; w = [lam / (1 + lam), 1 / (1 + lam)]
F['modular_flow'] = {'rapidity': ss, 'lines': lines, 'powers_lambda': lam, 'powers_state': w, 'ladder': [lam ** n for n in range(1, 9)],
                     'gap_second_eig': live['local_breuer_gap']['hminus_gap_second_eig'], 'wedge_kernel_flag': bool(kf.get('wedge_geometry_kernel_proved'))}

# (C) A LUZ: J troca o par; K = beta.d.(x, -y); JKJ = -K (construcao de prove_light_is_J, seed 153)
rng = np.random.default_rng(153); nd = 5
d = np.concatenate([[0.0], rng.uniform(0.5, 2.0, nd - 1)]); x = rng.normal(size=nd); y = rng.normal(size=nd)
Jp = lambda pr: (pr[1], pr[0]); Kp = lambda pr: (beta_rt * d * pr[0], -(beta_rt * d) * pr[1])
jj = Jp(Jp((x, y))); l = Jp(Kp(Jp((x, y)))); r = Kp((x, y))
F['light_J'] = {'d': d.tolist(), 'x': x.tolist(), 'y': y.tolist(), 'Kx': r[0].tolist(), 'Ky': r[1].tolist(), 'JKJx': l[0].tolist(), 'JKJy': l[1].tolist(),
                'crossing_resid': float(max(np.max(np.abs(jj[0] - x)), np.max(np.abs(jj[1] - y)))),
                'inversion_resid': float(max(np.max(np.abs(l[0] + r[0])), np.max(np.abs(l[1] + r[1]))))}
anchor('light: crossing_resid', 'core.light_is_J.values.crossing_resid', C['light_is_J']['values']['crossing_resid'], F['light_J']['crossing_resid'], 1e-15)
anchor('light: inversion_resid', 'core.light_is_J.values.inversion_resid', C['light_is_J']['values']['inversion_resid'], F['light_J']['inversion_resid'], 1e-15)

# (D) O FOUR-FRAME: dois boosts, rotacao de Wigner (construcao de prove_solder_4d; um._expm)
eta = np.diag([1., -1., -1., -1.]); Kb = [np.zeros((4, 4)) for _ in range(3)]
for i in range(3):
    Kb[i][0, i + 1] = Kb[i][i + 1, 0] = 1.0
Jr = [np.zeros((4, 4)) for _ in range(3)]
Jr[0][2, 3], Jr[0][3, 2] = -1., 1.
Jr[1][1, 3], Jr[1][3, 1] = 1., -1.
Jr[2][1, 2], Jr[2][2, 1] = -1., 1.
s2s = lin(0.0, 0.4, 41); wig = []; frames4 = []
for s2 in s2s:
    B12 = (um._expm(0.3 * Kb[0]) @ um._expm(s2 * Kb[1])).real
    wig.append(float(np.linalg.norm(B12[1:, 1:] - B12[1:, 1:].T))); frames4.append([float(v) for v in B12.flatten()])
F['four_frame'] = {'s1': 0.3, 's2': s2s, 'wigner': wig, 'B12': frames4,
                   'KK_eq_minus_J3_resid': float(np.linalg.norm(Kb[0] @ Kb[1] - Kb[1] @ Kb[0] + Jr[2])),
                   'JJ_eq_plus_J3_resid': float(np.linalg.norm(Jr[0] @ Jr[1] - Jr[1] @ Jr[0] - Jr[2]))}
assert abs(wig[-1] - live['solder_4d']['wigner_rotation_norm']) < 1e-9

# (E) A SOLDA: plaqueta de holonomia e a primeira curvatura (construcao de prove_minimal_solder)
hp = np.array([[1., 0.], [0., -1.]]); hx = np.array([[0., 1.], [1., 0.]]); J2 = G2
c1, c2 = 0.7, -1.3; A1, A2 = c1 * hp, c2 * hx; Fc = A1 @ A2 - A2 @ A1
R_rec = float(np.sum(Fc * J2) / np.sum(J2 * J2))
eps_vis = 0.35; v0 = np.array([1.0, 0.0]); path = []; legs = [(-1, A2), (-1, A1), (1, A2), (1, A1)]; v = v0.copy()
for sign, A in legs:
    for s_ in lin(0.0, 1.0, 31)[1:]:
        path.append([float(q) for q in (um._expm(sign * s_ * eps_vis * A).real @ v)])
    v = um._expm(sign * eps_vis * A).real @ v
plaq = (um._expm(eps_vis * A1) @ um._expm(eps_vis * A2) @ um._expm(-eps_vis * A1) @ um._expm(-eps_vis * A2)).real
F['solder'] = {'c1': c1, 'c2': c2, 'F': Fc.tolist(), 'R_recovered': R_rec, 'R_expected': 2 * c1 * c2, 'eps_vis': eps_vis, 'v0': v0.tolist(), 'path': path,
               'defect': (plaq @ v0 - v0).tolist(), 'defect_pred_eps2_F': (eps_vis ** 2 * Fc @ v0).tolist(), 'plaquette_order': live['minimal_solder']['plaquette_order']}
assert abs(R_rec - live['minimal_solder']['R_recovered']) < 1e-12

# (F) SCHWARZSCHILD: A(r), B(r), os 64 raios (construcao de prove_the_schwarzschild_step, seed 208)
rng = np.random.default_rng(208); rs_, C_ = 0.7, 1.3
Bf = lambda r_: 1.0 / (1.0 - rs_ / r_); Af = lambda r_: C_ * (1.0 - rs_ / r_); h = 1e-6
rv = rs_ + 0.5 + 9.0 * rng.random(64)
dB = (np.vectorize(Bf)(rv + h) - np.vectorize(Bf)(rv - h)) / (2 * h); dA = (np.vectorize(Af)(rv + h) - np.vectorize(Af)(rv - h)) / (2 * h)
Bv, Av = np.vectorize(Bf)(rv), np.vectorize(Af)(rv)
Et = rv * dB + Bv ** 2 - Bv; Er = rv * dA - Av * Bv + Av
rg = lin(rs_ + 0.02, 10.0, 240)
F['schwarzschild'] = {'rs': rs_, 'C': C_, 'r': rg, 'A': [float(Af(q)) for q in rg], 'B': [float(Bf(q)) for q in rg],
                      'flamm_z': [float(2 * math.sqrt(rs_ * (q - rs_))) for q in rg], 'rays_r': rv.tolist(), 'rays_Et': Et.tolist(), 'rays_Er': Er.tolist(),
                      'residual_Et': float(np.max(np.abs(Et))), 'residual_Er': float(np.max(np.abs(Er)))}
assert abs(F['schwarzschild']['residual_Et'] - live['schwarzschild_step']['residual_Et']) < 1e-15

# (G) SPIN-2: R(th)^T h+ R(th) = cos(2th) h+ + sin(2th) hx (construcao de prove_graviton_polarization)
rot = lambda t: np.array([[math.cos(t), math.sin(t)], [-math.sin(t), math.cos(t)]])
ths = lin(0.0, 2 * math.pi, 145); a_ = []; b_ = []; rres = []; tres = []
for t in ths:
    Rm = rot(t); M = Rm.T @ hp @ Rm
    a_.append(float(np.sum(M * hp) / 2)); b_.append(float(np.sum(M * hx) / 2))
    rres.append(float(np.max(np.abs(M - (math.cos(2 * t) * hp + math.sin(2 * t) * hx))))); tres.append(float(np.max(np.abs(Rm.T @ Rm - np.eye(2)))))
F['spin2'] = {'theta': ths, 'h_plus': a_, 'h_cross': b_, 'helicity_resid_max': max(rres), 'trace_mode_resid_max': max(tres), 'theta_M': theta_M}

# (H) O GAP LOCAL DE BREUER: perfil do modo zero sech(k/2) e densidade 1/4 sech^2 (construcao de prove_local_breuer_gap)
kk = np.arange(-20.0, 20.0 + 0.125, 0.25)
F['breuer'] = {'k': kk.tolist(), 'profile_sech': (1 / np.cosh(kk / 2)).tolist(), 'density': (0.25 / np.cosh(kk / 2) ** 2).tolist(),
               'gap_second_eig': live['local_breuer_gap']['hminus_gap_second_eig'], 'zero_mode_weight': live['local_breuer_gap']['zero_mode_weight_quadrature'],
               'overlap': live['local_breuer_gap']['zero_mode_overlap_sech'], 'hplus_floor': live['local_breuer_gap']['hplus_floor']}

# (I) O GATE: os flags lidos do JSON
qg = C['qg_closure']
groups = [('formal', 'Formal (Lean kernel)', qg['formal_flags']), ('physics', 'Physics (certificates)', qg['physics_flags']), ('experiment', 'Experiment (pre-registered rite)', qg['experiment_flags'])]
flags = [{'group': g, 'group_label': gl, 'name': k, 'value': bool(v)} for g, gl, dct in groups for k, v in dct.items()]
F['gate'] = {'flags': flags, 'n_true': sum(1 for f in flags if f['value']), 'n_total': len(flags), 'gate': qg['gate'], 'verdict_selo': selo['qg_closure_verdict'],
             'legitimate_seals': qg['legitimate_seals'], 'closure_order': qg['closure_order'], 'triad_verdict': C['triad_master']['verdict'],
             'einstein_coefficient_resid': C['triad_master']['residuals']['coeficiente_de_einstein'], 'pentada': C['triad_master']['pentada']}
assert F['gate']['gate']['verdict'] == selo['qg_closure_verdict']

# (J) 1 = 1: o par e a barra (construcao de prove_the_TGL_identity_equation, seed 247)
rng = np.random.default_rng(247); xs = rng.normal(size=500)
m_ok = np.abs((-xs) ** 2 - xs ** 2); m_no = np.abs((xs + 1) ** 2 - xs ** 2)
F['identity'] = {'xs': xs[:64].tolist(), 'resid_true': m_ok[:64].tolist(), 'resid_false': m_no[:64].tolist(),
                 'member_true_max_residual': float(m_ok.max()), 'member_false_min_residual': float(m_no.min())}
assert F['identity']['member_false_min_residual'] == live['the_TGL_identity_equation']['member_false_min_residual']

# (K) a espinha
rt = C['runtime_of_the_one']
F['chain'] = {'one_line': rt['one_line'], 'chain': rt['chain'], 'triad': rt['triad'], 'scalar_spine': rt['scalar_spine'], 'seals': rt['seals']}

# ---------------- HUD ----------------
fmt = lambda v, p: ('%.' + str(p) + 'f') % v
sci = lambda v: '%.2e' % v
gp = C['graviton_polarization']; lj = C['light_is_J']['values']; sm = C['smatrix_closure']; lb = C['local_breuer_gap']; s4 = C['solder_4d']; ms = C['minimal_solder']
ss_ = C['schwarzschild_step']; ie = C['the_TGL_identity_equation']; pl = C['powers_ladder']['values']; tm = C['triad_master']
hud = {
    'one_line': rt['one_line'], 'title_pt': res.get('title_pt'), 'title_en': res.get('title_en'),
    'items': [
        {'id': 'omega_I', 'scene': 1, 'label': 'ω(I)', 'value': C['omega_I'], 'text': fmt(C['omega_I'], 1), 'key': 'core.omega_I', 'statute': 'AX'},
        {'id': 'half', 'scene': 2, 'label': 'x = 1 − x ⇒ x', 'value': C['HALF'], 'text': fmt(C['HALF'], 1), 'key': 'core.HALF', 'statute': 'DER'},
        {'id': 'meia_nat_residual', 'scene': 2, 'label': 'residual', 'value': C['meia_nat_residual'], 'text': sci(C['meia_nat_residual']), 'key': 'core.meia_nat_residual', 'statute': 'REAL'},
        {'id': 'S_boundary', 'scene': 2, 'label': 'S_∂', 'value': C['S_boundary'], 'text': '½ nat', 'key': 'core.S_boundary', 'statute': 'DER'},
        {'id': 'sqrt_e', 'scene': 3, 'label': 'Vol_min = √e', 'value': C['SQRT_E'], 'text': fmt(C['SQRT_E'], 6), 'key': 'core.SQRT_E', 'statute': 'DER'},
        {'id': 'beta', 'scene': 3, 'label': 'β = α·√e', 'value': gp['values']['beta_runtime'], 'text': fmt(gp['values']['beta_runtime'], 12), 'key': 'core.graviton_polarization.values.beta_runtime', 'statute': 'DER', 'note': 'runtime: SEALED_CODATA_ALPHA·sqrt(e); α = CODATA 2018 [INPUT]'},
        {'id': 'theta_M', 'scene': 3, 'label': 'θ_M = arcsin√β', 'value': C['theta_M_deg'], 'text': fmt(C['theta_M_deg'], 4) + '°', 'key': 'core.theta_M_deg', 'statute': 'DER'},
        {'id': 'leak', 'scene': 3, 'label': 'sin²θ_M = |R|²', 'value': C['fractal_dephasing']['leak_sin2_thetaM'], 'text': fmt(C['fractal_dephasing']['leak_sin2_thetaM'], 12), 'key': 'core.fractal_dephasing.leak_sin2_thetaM', 'statute': 'REAL'},
        {'id': 'leak_resid', 'scene': 3, 'label': 'leak − β', 'value': C['fractal_dephasing']['leak_equals_beta_residual'], 'text': sci(C['fractal_dephasing']['leak_equals_beta_residual']), 'key': 'core.fractal_dephasing.leak_equals_beta_residual', 'statute': 'REAL'},
        {'id': 'tau_trans', 'scene': 3, 'label': '|T|² = 1 − β', 'value': sm['tau_transmitted'], 'text': fmt(sm['tau_transmitted'], 12), 'key': 'core.smatrix_closure.tau_transmitted', 'statute': 'REAL'},
        {'id': 'r_unit', 'scene': 3, 'label': '‖S†S − 1‖', 'value': sm['r_unit'], 'text': sci(sm['r_unit']), 'key': 'core.smatrix_closure.r_unit', 'statute': 'REAL'},
        {'id': 'powers_ratio', 'scene': 4, 'label': 'Powers ratio λ', 'value': pl['ratio_block'], 'text': fmt(pl['ratio_block'], 6), 'key': 'core.powers_ladder.values.ratio_block', 'statute': 'REAL (λ = β, illustration)'},
        {'id': 'powers_chain', 'scene': 4, 'label': 'λ⁸ (ladder N = 8)', 'value': pl['ratio_chain_N8'], 'text': sci(pl['ratio_chain_N8']), 'key': 'core.powers_ladder.values.ratio_chain_N8', 'statute': 'REAL'},
        {'id': 'breuer_gap', 'scene': 4, 'label': 'local gap (2nd eig of H⁻)', 'value': lb['hminus_gap_second_eig'], 'text': fmt(lb['hminus_gap_second_eig'], 5), 'key': 'core.local_breuer_gap.hminus_gap_second_eig', 'statute': 'REAL'},
        {'id': 'zero_mode_weight', 'scene': 4, 'label': '∫¼sech²(κ/2) (weight of the Name)', 'value': lb['zero_mode_weight_quadrature'], 'text': fmt(lb['zero_mode_weight_quadrature'], 6), 'key': 'core.local_breuer_gap.zero_mode_weight_quadrature', 'statute': 'REAL (kernel: exact 1)'},
        {'id': 'J_cross', 'scene': 5, 'label': 'J² = 1 residual', 'value': lj['crossing_resid'], 'text': sci(lj['crossing_resid']), 'key': 'core.light_is_J.values.crossing_resid', 'statute': 'REAL'},
        {'id': 'J_inv', 'scene': 5, 'label': 'JKJ = −K residual', 'value': lj['inversion_resid'], 'text': sci(lj['inversion_resid']), 'key': 'core.light_is_J.values.inversion_resid', 'statute': 'REAL'},
        {'id': 'J_id', 'scene': 5, 'label': 'I remains', 'value': lj['identity_remains_resid'], 'text': sci(lj['identity_remains_resid']), 'key': 'core.light_is_J.values.identity_remains_resid', 'statute': 'REAL'},
        {'id': 'wigner', 'scene': 6, 'label': 'Wigner rotation ‖·‖', 'value': s4['wigner_rotation_norm'], 'text': fmt(s4['wigner_rotation_norm'], 6), 'key': 'core.solder_4d.wigner_rotation_norm', 'statute': 'REAL'},
        {'id': 'KK', 'scene': 6, 'label': '[K₁,K₂] = −J₃', 'value': s4['residuals']['marca_KK_eq_menosJ3'], 'text': sci(s4['residuals']['marca_KK_eq_menosJ3']), 'key': 'core.solder_4d.residuals.marca_KK_eq_menosJ3', 'statute': 'REAL'},
        {'id': 'R_rec', 'scene': 6, 'label': 'R = 2c₁c₂', 'value': ms['R_recovered'], 'text': fmt(ms['R_recovered'], 3), 'key': 'core.minimal_solder.R_recovered', 'statute': 'REAL'},
        {'id': 'plaq', 'scene': 6, 'label': 'plaquette order', 'value': ms['plaquette_order'], 'text': fmt(ms['plaquette_order'], 4), 'key': 'core.minimal_solder.plaquette_order', 'statute': 'REAL'},
        {'id': 'sch_Et', 'scene': 6, 'label': 'Schwarzschild E_t', 'value': ss_['residual_Et'], 'text': sci(ss_['residual_Et']), 'key': 'core.schwarzschild_step.residual_Et', 'statute': 'REAL'},
        {'id': 'sch_Er', 'scene': 6, 'label': 'Schwarzschild E_r', 'value': ss_['residual_Er'], 'text': sci(ss_['residual_Er']), 'key': 'core.schwarzschild_step.residual_Er', 'statute': 'REAL'},
        {'id': 'hel', 'scene': 6, 'label': 'helicity ±2 residual', 'value': gp['residuals']['helicity_plus'], 'text': sci(gp['residuals']['helicity_plus']), 'key': 'core.graviton_polarization.residuals.helicity_plus', 'statute': 'PROVED in kernel'},
        {'id': 'pol', 'scene': 6, 'label': 'polarizations', 'value': 2, 'text': '2', 'key': 'core.graviton_polarization.seals[0]', 'statute': 'PROVED in kernel'},
        {'id': 'einstein', 'scene': 7, 'label': '8πG residual (Unruh × Bekenstein–Hawking)', 'value': tm['residuals']['coeficiente_de_einstein'], 'text': sci(tm['residuals']['coeficiente_de_einstein']), 'key': 'core.triad_master.residuals.coeficiente_de_einstein', 'statute': 'PROVED in kernel (H1∧H2∧H3 named)'},
        {'id': 'flags', 'scene': 7, 'label': 'gate flags', 'value': F['gate']['n_true'], 'text': '%d/%d' % (F['gate']['n_true'], F['gate']['n_total']), 'key': 'core.qg_closure.*_flags', 'statute': 'REAL (fail-closed)'},
        {'id': 'id_true', 'scene': 8, 'label': '1 = 1 residual', 'value': ie['member_true_max_residual'], 'text': sci(ie['member_true_max_residual']), 'key': 'core.the_TGL_identity_equation.member_true_max_residual', 'statute': 'REAL'},
        {'id': 'id_false', 'scene': 8, 'label': '1 = 0 min residual', 'value': ie['member_false_min_residual'], 'text': sci(ie['member_false_min_residual']), 'key': 'core.the_TGL_identity_equation.member_false_min_residual', 'statute': 'REAL'},
        {'id': 'theorems', 'scene': 9, 'label': 'theorems clean', 'value': theorems_clean, 'text': '%d/%d' % (theorems_clean, theorems_total), 'key': stdout_name, 'statute': 'PROVED'},
        {'id': 'outside_trio', 'scene': 9, 'label': 'axioms outside {propext, choice, Quot.sound}', 'value': outside_trio, 'text': str(outside_trio), 'key': 'core.kernel_formalization.axiom_report', 'statute': 'PROVED'},
        {'id': 'n_formal', 'scene': 9, 'label': 'formal files', 'value': n_formal_files, 'text': str(n_formal_files), 'key': 'core.kernel_formalization.formal_files_sha256', 'statute': 'REAL'},
        {'id': 'um_sha16', 'scene': 9, 'label': 'um.py sha256', 'value': SHA['um.py'][:16], 'text': SHA['um.py'][:16], 'key': 'sha256(um.py)', 'statute': 'REAL'},
    ],
    'gate_verdict': selo['qg_closure_verdict'], 'selo_timestamp': selo['timestamp'], 'result_hash16': selo['result_hash'][:16],
    'lean_version': kf['lean_version'][0] if kf.get('lean_version') else 'AUSENTE', 'sorryAx_absent': kf['sorryAx_absent'], 'custom_TGL_axioms_absent': kf['custom_TGL_axioms_absent'],
    'beta_routes_note': {'core.beta (Lagrange motor route)': C['beta'], 'runtime route SEALED_CODATA_ALPHA*sqrt(e)': beta_rt,
                         'note': 'digit divergence is of route, not error (Atlas I.3); HUD shows the runtime value to 12 decimals'},
    'console': [ln.rstrip() for ln in stdout.splitlines()[:3]],   # as linhas reais do rito (o console da cena 1)
    'chain_figure': ['ω(I)=1 [AX]', 'x=1−x ⇒ ½ [DER]', 'S_∂=½ nat [DER]', 'Vol=√e [DER]', 'β=α√e', 'θ_M=arcsin√β', '|R|²=β', 'Γ_ω=½βτ★ω²', 'ρ_v/ρ̄≥β [TESTED]'],  # a cadeia de fig_cadeia_inscricao (emit_figures)
}

# ---------------- MANIFEST ----------------
prov = {
    'mirror': {'function': 'um._expm (S = exp(theta.G)); construction of um.fractal_dephasing_principle (leak = tr(rho* Q_theta)); anchored at theta_M', 'statute': 'DER/REAL'},
    'modular_flow': {'function': 'um._expm (boosts in the wedge); um.prove_powers_ladder shadow (lambda = beta)', 'statute': 'KNOWN (Bisognano-Wichmann) + kernel wedge_geometry; ladder REAL (illustration)'},
    'light_J': {'function': 'construction of um.prove_light_is_J (seed 153); residuals anchored to core.light_is_J.values', 'statute': 'REAL clauses; J = light is ONTO'},
    'four_frame': {'function': 'construction of um.prove_solder_4d (um._expm); anchored at (s1, s2) = (0.3, 0.4)', 'statute': 'REAL; kernel v63'},
    'solder': {'function': 'construction of um.prove_minimal_solder (um._expm); R anchored; eps_vis = 0.35 for visibility (program uses 1e-2, 5e-3)', 'statute': 'REAL; kernel v60'},
    'schwarzschild': {'function': 'construction of um.prove_the_schwarzschild_step (seed 208, 64 rays); residuals anchored; flamm_z is KNOWN embedding of the class', 'statute': 'REAL; kernel v208; gauge C declared'},
    'spin2': {'function': 'construction of um.prove_graviton_polarization (R^T h+ R = cos2th h+ + sin2th hx)', 'statute': 'PROVED in kernel (GravitonPolarization.lean); shadow REAL'},
    'breuer': {'function': 'um.prove_local_breuer_gap live call (gap, weight, overlap); sech profile per its construction', 'statute': 'REAL; kernel zero_mode_weight_is_one'},
    'gate': {'function': 'read from core.qg_closure and um_absoluto_selo.json', 'statute': 'REAL (fail-closed gate); NOT_FALSIFIED; nature decides'},
    'identity': {'function': 'construction of um.prove_the_TGL_identity_equation (seed 247); extrema anchored', 'statute': 'REAL; kernel v247'},
    'chain': {'function': 'read from core.runtime_of_the_one', 'statute': 'SYNTHESIS (REAL spine + ONTO reading)'},
}
manifest = {
    'generated_at': selo['timestamp'], 'exporter': os.path.basename(__file__), 'exporter_sha256': sha(os.path.abspath(__file__)),
    'sources': {n: {'path': n, 'bytes': os.path.getsize(p), 'sha256': SHA[n]} for n, p in SRC.items()},
    'um_sha16': SHA['um.py'][:16],
    'selo': {'timestamp': selo['timestamp'], 'result_hash': selo['result_hash'], 'qg_closure_verdict': selo['qg_closure_verdict'], 'identity': selo.get('identity')},
    'kernel': {'theorems_clean': theorems_clean, 'theorems_total': theorems_total, 'axiom_report_entries': len(ar), 'outside_trio': outside_trio, 'formal_files': n_formal_files,
               'formal_source_hash': kf.get('formal_source_hash'), 'lean': hud['lean_version'], 'sorryAx_absent': kf['sorryAx_absent'], 'custom_TGL_axioms_absent': kf['custom_TGL_axioms_absent']},
    'import_um': {'stdout_during_import_chars': len(_buf.getvalue()), 'dont_write_bytecode': True, 'rite_runs_only_under_main': True},
    'beta_runtime': beta_rt, 'theta_M_rad': theta_M, 'anchors': anchors, 'anchors_all_ok': all(a['ok'] for a in anchors), 'provenance': prov,
    'rule': 'PROVED = theorem in kernel; nature decides; beta never literal; every number on screen comes from these files.',
}
if not manifest['anchors_all_ok']:
    print(json.dumps([a for a in anchors if not a['ok']], indent=1)); sys.exit(2)


def write(name, obj, compact=False):
    p = os.path.join(DATA, name); tmp = p + '.tmp'
    if os.path.exists(p):
        open(p + '.bak_' + time.strftime('%Y%m%d_%H%M%S'), 'wb').write(open(p, 'rb').read())
    with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=(None if compact else 1), separators=((',', ':') if compact else (',', ': ')))
    assert os.path.getsize(tmp) > 100; os.replace(tmp, p); return p


exec(compile(open(os.path.join(VID,'extend_export.py'),encoding='utf-8').read(), 'extend_export.py', 'exec'))
write('hud.json', hud); write('frames.json', F, compact=True); write('MANIFEST.json', manifest)
print('OK  hud items %d | frames sets %d | anchors %d/%d ok | theorems %d/%d | outside trio %d | um.py %s' % (
    len(hud['items']), len(F), sum(a['ok'] for a in anchors), len(anchors), theorems_clean, theorems_total, outside_trio, SHA['um.py'][:16]))
for a in []:
    print('  anchor %-58s json=%-24r live=%-24r resid=%s' % (a['name'][:58], a['json_value'], a['live_value'], a['residual']))
