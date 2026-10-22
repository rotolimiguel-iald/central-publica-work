# -*- coding: utf-8 -*-
# CONFERENCIA DO REDATOR — F1.FREQUENCIA (trilha POSTO), gerencia c1, 12/10/2026.
# So LEITURA fora de 4_RELATORIO; grava SO 4_RELATORIO\CONFERENCIA_REDATOR.json.
# Nao executa o um.py (le os bytes por linha). beta NUNCA literal: alpha lido da linha unica
# 'ALPHA_FINE_CODATA_2018 = ...' dos bytes do um.py; beta = alpha*sqrt(e) em runtime; a string de conferencia
# e lida do PREREGISTRO congelado (beta_runtime.beta_float64), nunca digitada aqui.
# Sondas suplementares (fora do pre-registro, marcadas assim): R5 (superposicao pura), iteracao do ponto final
# sob C = D o Ad(S) o D, os dois polos da nao-defasagem, A8 (Q_theta x 1 - F_theta(1)), a identidade de projetor
# por tras do 'verificado ao vivo'. Nenhum dado observado, nenhum provedor, nenhuma ferramenta da Bancada.
import os, re, json, math, hashlib, time, sys
import numpy as np

BASE = r"C:\IALD\Central de Patentes\work\frequencia_defasa_12out"
REL = os.path.join(BASE, "4_RELATORIO")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um" + "\\N\u00f3s"
UMPY = os.path.join(NOS, "um.py")
CORE = os.path.join(NOS, "um_absoluto.json")
SELO = os.path.join(NOS, "um_absoluto_selo.json")
V = {
    "V1": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_10out_posto_rank_texto_verbatim.txt",
    "V2": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
    "V3": r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_posto_rank_verbatim.txt",
    "V4": r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt",
}
AUD = (r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes"
       r"\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\pt12")
PEDRA = os.path.join(BASE, "3_KERNEL", "sandbox", "TGLExt", "TheUnitIsTheRank.lean")
OLEAN = os.path.join(BASE, "3_KERNEL", "olean", "TheUnitIsTheRank.olean")
AUDIT_LEAN = os.path.join(BASE, "3_KERNEL", "sandbox", "AuditTheUnitIsTheRank.lean")

falhas = []


def rb(p):
    with open(p, "rb") as fh:
        return fh.read()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def fsha(p):
    b = rb(p)
    return len(b), sha(b)


def falha(msg):
    falhas.append(msg)


out = {"documento": "CONFERENCIA_REDATOR — F1.FREQUENCIA (trilha POSTO)", "gerencia": "c1",
       "autor": "redator da unidade (subagente)", "inicio_local": time.strftime("%Y-%m-%d %H:%M:%S"),
       "escopo": "so leitura fora de 4_RELATORIO; um.py lido por bytes/linha, nao executado; sem dado observado, "
                 "provedor, chamada paga ou Bancada"}

# ---------------------------------------------------------------- 1. beta de runtime (bytes do um.py)
um = rb(UMPY)
um_sha = sha(um)
linhas = um.split(b"\n")
alvo = [i for i, l in enumerate(linhas, 1)
        if re.match(rb"^ALPHA_FINE_CODATA_2018\s*=\s*[0-9.eE+-]+\s*$", l.strip())]
if len(alvo) != 1:
    falha("linha de ALPHA_FINE_CODATA_2018 nao unica: %r" % alvo)
alpha_txt = linhas[alvo[0] - 1].split(b"=", 1)[1].strip().decode("ascii")
sealed = [(i, re.match(rb"^SEALED_CODATA_ALPHA\s*=\s*([0-9.eE+-]+)", l.strip()).group(1).decode("ascii"))
          for i, l in enumerate(linhas, 1)
          if re.match(rb"^SEALED_CODATA_ALPHA\s*=\s*[0-9.eE+-]+\s*(#.*)?$", l.strip())]
# (tentativa 1 deste script usava '...\s*$' e nao achava a linha 95, que tem comentario ao fim; corrigido so o leitor)
beta = float(alpha_txt) * math.sqrt(math.e)
pre = json.loads(rb(os.path.join(BASE, "1_PREREGISTRO", "PREREGISTRO.json")).decode("utf-8"))
conf_txt = pre["beta_runtime"]["beta_float64"]          # string de conferencia lida do pre-registro congelado
beta_confere = (repr(beta) == conf_txt)
if not beta_confere:
    falha("beta de runtime nao confere com o pre-registro")
thM = math.asin(math.sqrt(beta))
v4 = rb(V["V4"]).decode("utf-8")
m_op = re.search(r"\\approx\s*([0-9]+\.[0-9]+)", v4)
num_op = m_op.group(1) if m_op else None
out["beta_runtime"] = {
    "um_py_sha256": um_sha, "um_py_bytes": len(um), "alpha_linha": alvo[0], "alpha_texto": alpha_txt,
    "SEALED_CODATA_ALPHA": sealed, "sealed_igual": bool(sealed) and all(s[1] == alpha_txt for s in sealed),
    "receita": "float(alpha_texto) * math.sqrt(math.e)", "beta_repr": repr(beta),
    "conferencia_lida_do_PREREGISTRO": conf_txt, "beta_confere": beta_confere, "theta_M_repr": repr(thM),
    "numero_do_operador_V4_l16_lido_dos_bytes": num_op,
    "abs_beta_menos_numero_do_operador": (abs(beta - float(num_op)) if num_op else None),
}

# ---------------------------------------------------------------- 2. pinos (verbatins, um.py, core, selo)
pin = {}
for k, p in V.items():
    n, h = fsha(p)
    esperado = pre["a_verbatins"][k]["sha256"]
    pin[k] = {"arquivo": p, "bytes": n, "sha256": h, "confere_com_PREREGISTRO": h == esperado}
    if h != esperado:
        falha("verbatim %s nao confere" % k)
v2b = rb(V["V2"])
v2_l1_33 = b"\n".join(v2b.split(b"\n")[:33])
pin["V2_trilha_l1_33"] = {"bytes": len(v2_l1_33), "sha256": sha(v2_l1_33),
                          "confere_com_PREREGISTRO": sha(v2_l1_33) == pre["a_verbatins"]["V2"]["trilha"]["sha256"]}
for p, n_esp, h_esp in pre["pinos"][:3]:
    n, h = fsha(p)
    pin[os.path.basename(p)] = {"bytes": n, "sha256": h, "confere_com_PREREGISTRO": (n == n_esp and h == h_esp)}
    if h != h_esp:
        falha("pino %s nao confere" % p)
out["pinos"] = pin

# ---------------------------------------------------------------- 3. FREEZE e as pastas da unidade
fz = json.loads(rb(os.path.join(BASE, "1_PREREGISTRO", "FREEZE.json")).decode("utf-8"))
freeze_ok = True
for nome in ("PREREGISTRO.json", "PREREGISTRO.md"):
    n, h = fsha(os.path.join(BASE, "1_PREREGISTRO", nome))
    if (n, h) != (fz[nome]["bytes"], fz[nome]["sha256"]):
        freeze_ok = False
        falha("FREEZE: %s mudou" % nome)
for rel, (n_esp, h_esp) in fz["demais_arquivos_da_pasta"].items():
    n, h = fsha(os.path.join(BASE, "1_PREREGISTRO", rel.replace("/", "\\")))
    if (n, h) != (n_esp, h_esp):
        freeze_ok = False
        falha("FREEZE: %s mudou" % rel)
presentes = set()
for dp, dns, fns in os.walk(os.path.join(BASE, "1_PREREGISTRO")):
    for fn in fns:
        presentes.add(os.path.relpath(os.path.join(dp, fn), os.path.join(BASE, "1_PREREGISTRO")).replace("\\", "/"))
esperados = {"FREEZE.json", "PREREGISTRO.json", "PREREGISTRO.md"} | set(fz["demais_arquivos_da_pasta"])
novos = sorted(presentes - esperados)
if novos:
    freeze_ok = False
    falha("FREEZE: arquivos novos em 1_PREREGISTRO: %r" % novos)
n_fz, h_fz = fsha(os.path.join(BASE, "1_PREREGISTRO", "FREEZE.json"))
out["freeze"] = {"FREEZE.json": {"bytes": n_fz, "sha256": h_fz}, "congelado_utc": fz["congelado_utc"],
                 "PREREGISTRO.json": fz["PREREGISTRO.json"], "PREREGISTRO.md": fz["PREREGISTRO.md"],
                 "demais_conferidos": len(fz["demais_arquivos_da_pasta"]), "arquivos_novos": novos,
                 "veredito": "FREEZE_CONFERE" if freeze_ok else "FREEZE_NAO_CONFERE"}

rk = json.loads(rb(os.path.join(BASE, "3_KERNEL", "RESULTADO_KERNEL.json")).decode("utf-8"))
man_ok, man_div = True, []
for rel, (n_esp, h_esp) in rk["manifesto_3_KERNEL"].items():
    p = os.path.join(BASE, "3_KERNEL", rel.replace("/", "\\"))
    if not os.path.isfile(p):
        man_ok = False
        man_div.append(rel + " (ausente)")
        continue
    n, h = fsha(p)
    if (n, h) != (n_esp, h_esp):
        man_ok = False
        man_div.append(rel)
n_p, h_p = fsha(PEDRA)
n_o, h_o = fsha(OLEAN)
n_a, h_a = fsha(AUDIT_LEAN)
out["kernel_da_unidade"] = {
    "manifesto_3_KERNEL_confere": man_ok, "divergencias": man_div,
    "pedra": {"arquivo": PEDRA, "bytes": n_p, "sha256": h_p, "confere": h_p == rk["pedra"]["sha256"]},
    "olean": {"arquivo": OLEAN, "bytes": n_o, "sha256": h_o, "confere": h_o == rk["compilacao"]["olean"]["sha256"]},
    "auditoria_lean": {"arquivo": AUDIT_LEAN, "bytes": n_a, "sha256": h_a},
    "RESULTADO_KERNEL.json": dict(zip(("bytes", "sha256"), fsha(os.path.join(BASE, "3_KERNEL", "RESULTADO_KERNEL.json")))),
    "resumo_K": rk["resumo"],
}
if not (man_ok and h_p == rk["pedra"]["sha256"] and h_o == rk["compilacao"]["olean"]["sha256"]):
    falha("3_KERNEL nao confere com o proprio manifesto")

ro = json.loads(rb(os.path.join(BASE, "2_OPTICO", "RESULTADO_OPTICO.json")).decode("utf-8"))
out["optico_da_unidade"] = {
    "RESULTADO_OPTICO.json": dict(zip(("bytes", "sha256"), fsha(os.path.join(BASE, "2_OPTICO", "RESULTADO_OPTICO.json")))),
    "run_optico.py": dict(zip(("bytes", "sha256"), fsha(os.path.join(BASE, "2_OPTICO", "run_optico.py")))),
    "controles_ok": ro["controles_ok"], "nao_conformes_ao_esperado": ro["nao_conformes_ao_esperado"],
    "alertas": ro["alertas"], "resumo_por_parte": ro["resumo_por_parte"],
}

# ---------------------------------------------------------------- 4. citacoes do cabecalho da pedra (bytes)
def norm(s):
    return re.sub(r"\s+", " ", s).strip()


Vtxt = {k: rb(p).decode("utf-8") for k, p in V.items()}
Vtxt["V2"] = v2_l1_33.decode("utf-8")
ped = rb(PEDRA).decode("utf-8").split("\n")
cab = "\n".join(ped[22:33])                 # l.23..33: '## Os textos do operador' ate o fim do item V4
cit = []
for bloco in re.split(r"\n\* ", "\n" + cab):
    mv = re.match(r"(V[1-4]) ", bloco)
    if not mv:
        continue
    vk = mv.group(1)
    for c in re.findall(r"«(.*?)»", bloco, flags=re.S):
        frags = [norm(f) for f in c.split("\u2026") if norm(f)]
        alvo_t = norm(Vtxt[vk])
        pos, ok = 0, True
        for f in frags:
            j = alvo_t.find(f, pos)
            if j < 0:
                ok = False
                break
            pos = j + len(f)
        estado = ("VERBATIM" if ok and len(frags) == 1 else "VERBATIM_COM_RETICENCIAS" if ok else "NAO_LITERAL")
        cit.append({"atribuida_a": vk, "citacao": norm(c), "fragmentos": len(frags), "estado": estado})
v1t, v2t = Vtxt["V1"], Vtxt["V2"]
formula_ordem = "\u03c1 = |\u03c8\u27e9\u27e8\u03c8|, com Tr(\u03c1) = 1 e Tr(\u03c1\u00b2) = 1"
out["citacoes"] = {
    "pedra_cabecalho_l23_33": cit,
    "contagem": {e: sum(1 for x in cit if x["estado"] == e) for e in ("VERBATIM", "VERBATIM_COM_RETICENCIAS", "NAO_LITERAL")},
    "ordem_formula_atribuida_a_V1_esta_em_V1": formula_ordem in v1t,
    "V1_l6_termina_em": v1t.split("\n")[5][-9:],
    "V2_formula_so_em_LaTeX_l16": v2t.split("\n")[15],
    "V2_l1_33_quando_eu_derivei": v2t.count("Quando eu derivei"),
    "V2_l1_33_voce_impos": v2t.count("você impôs"),
    "V2_l1_33_ocorrencias_de_voce": len(re.findall(r"\bvocê\b", v2t)),
}

# ---------------------------------------------------------------- 5. sondas suplementares [REAL medido aqui]
def rank(A, tol=1e-12):
    s = np.linalg.svd(A, compute_uv=False)
    return int(np.sum(s > tol)), float(min(s))


c, s = math.cos(thM), math.sin(thM)
S = np.array([[c, s], [-s, c]], dtype=complex)            # Smat do kernel em theta_M
rho_star = np.array([[1, 0], [0, 0]], dtype=complex)
Q0 = np.eye(2) - rho_star
D = lambda x: np.diag(np.diag(x))                         # D_inf = diagExpect
Ad = lambda U, x: U @ x @ U.conj().T

# 5a. R5: a superposicao PURA ja tem posto 1 (nulidade n-1); so a mistura I/d tem nucleo vazio
r5 = []
for n in (2, 3, 4):
    psi = np.ones(n, dtype=complex) / math.sqrt(n)
    pur = np.outer(psi, psi.conj())
    mix = np.eye(n) / n
    P = np.zeros((n, n), dtype=complex); P[0, 0] = 1
    lido_pur = P @ pur @ P / np.trace(P @ pur)
    lido_mix = P @ mix @ P / np.trace(P @ mix)
    r5.append({"n": n,
               "superposicao_pura_posto_nulidade": [rank(pur)[0], n - rank(pur)[0]],
               "mistura_I_n_posto_nulidade": [rank(mix)[0], n - rank(mix)[0]],
               "leitura_de_posto_1_sobre_a_pura_peso_de_Born": float(np.trace(P @ pur).real),
               "leitura_de_posto_1_sobre_a_mistura_peso_de_Born": float(np.trace(P @ mix).real),
               "saida_das_duas_leituras_e_P": bool(np.allclose(lido_pur, P, atol=1e-12) and np.allclose(lido_mix, P, atol=1e-12))})
out["sonda_R5_superposicao_pura"] = {
    "estatuto": "[REAL medido aqui; sonda suplementar, fora do pre-registro; o mesmo fato e termo de kernel: rankOne_density (P1.d) e half_identity_rank_nullity (P2.a)]",
    "casos": r5,
    "leitura": "a letra de V1 l.7 ('deixa de ter um nucleo vazio (nullity) ... e ganha posto definido') so vale lendo 'superposicao' como a mistura de posto cheio I/d (nulidade 0); a superposicao PURA ja tem posto 1 e nulidade n-1 antes de qualquer leitura"}

# 5b. o ponto final de UMA passagem sob o canal iterado C = D o Ad(S) o D (F1.ATRATOR)
tudo = D(Ad(S, rho_star))
C = lambda x: D(Ad(S, D(x)))
x = tudo.copy(); traj = []
for k in range(0, 4097):
    if k in (0, 1, 2, 10, 100, 1000, 4096):
        traj.append({"n": k, "p1": float(x[1, 1].real), "posto": rank(x)[0],
                     "dist_I2_frobenius": float(np.linalg.norm(x - np.eye(2) / 2))})
    x = C(x)
lam = 1 - 2 * beta
out["sonda_iteracao_do_ponto_final"] = {
    "estatuto": "[REAL medido aqui; refaz por conta propria a SONDA_ITERACAO do auditor de estatuto; fora do pre-registro]",
    "tudo_uma_passagem_diag": [float(tudo[0, 0].real), float(tudo[1, 1].real)],
    "tudo_p1_menos_beta": float(tudo[1, 1].real) - beta,
    "C_de_tudo_p1": float(C(tudo)[1, 1].real), "forma_fechada_2b_1_menos_b": 2 * beta * (1 - beta),
    "C_de_tudo_igual_tudo": bool(np.allclose(C(tudo), tudo, atol=1e-15)),
    "lambda_1_menos_2beta": lam, "cota_dist_n1000": math.sqrt(2) * abs(beta - 0.5) * lam ** 1000,
    "trajetoria": traj,
    "leitura": "o Tudo tipado (diag(1-beta, beta), posto 2) e ponto de UMA passagem; sob C iterado nao e estacionario e C^n -> I/2; beta fixa a taxa lambda = 1 - 2beta, nao o ponto fixo (coerente com a F1.ATRATOR)"}

# 5c. os dois polos da nao-defasagem
polos = []
for nome, th in (("theta=0 (transmissao total, |t|^2=1)", 0.0), ("theta=pi/2 (reflexao total, |r|^2=1)", math.pi / 2),
                 ("theta=theta_M", thM)):
    Sx = np.array([[math.cos(th), math.sin(th)], [-math.sin(th), math.cos(th)]], dtype=complex)
    F1 = Ad(Sx, rho_star)
    polos.append({"caso": nome, "D_inf_F_igual_F": bool(np.allclose(D(F1), F1, atol=1e-12)),
                  "posto_F": rank(F1)[0], "posto_D_inf_F": rank(D(F1))[0],
                  "abs_t2": float(math.cos(th) ** 2), "abs_r2": float(math.sin(th) ** 2)})
out["sonda_dois_polos"] = {"estatuto": "[REAL medido aqui; o mesmo fato e termo de kernel: dephasing_trivial_iff, B8.b]",
                           "casos": polos,
                           "leitura": "a nao-defasagem tem DOIS polos (theta=0 e theta=pi/2, i.e. beta=0 e beta=1), ambos de posto 1; na tipagem da matriz-S, 'o que nao transmite' (V4 l.9) aponta theta=pi/2, e o nothing_branch (theta=0) e transmissao total"}

# 5d. A8: o Q_theta do um.py (S^H Q0 S = R Q0 R^T) x 1 - F_theta(1) (= Q_{-theta})
R = np.array([[c, -s], [s, c]], dtype=complex)            # a matriz R do um.py l.6518
Qth = R @ Q0 @ R.T
um_menos_F = np.eye(2) - Ad(S, rho_star)
out["sonda_A8_qual_Q"] = {
    "estatuto": "[REAL medido aqui; reproduz o anexo A8 do otico]",
    "Qtheta_umpy_igual_SH_Q0_S": bool(np.allclose(Qth, S.conj().T @ Q0 @ S, atol=1e-15)),
    "Qtheta_umpy_igual_1_menos_F": bool(np.allclose(Qth, um_menos_F, atol=1e-12)),
    "frobenius_da_diferenca": float(np.linalg.norm(Qth - um_menos_F)), "forma_fechada_2sqrt2_sc": 2 * math.sqrt(2) * s * c,
    "vazamento_nos_dois": [float(np.trace(rho_star @ Qth).real), float(np.trace(rho_star @ um_menos_F).real)],
    "leitura": "os dois 'Q' diferem fora da diagonal e dao o mesmo vazamento s^2; o texto da v392 precisa dizer qual Q e o Q-chapeu de V4"}

# 5e. a identidade de projetor por tras de '||{Q_0, rho*}|| = 0' (verificado ao vivo, um.py l.6515 e artigo l.168102)
rng = np.random.default_rng(20261012)
maxdev = 0.0
for n in (2, 3, 4):
    for _ in range(200):
        A = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        Qm, _r = np.linalg.qr(A)
        d = int(rng.integers(1, n))
        P = Qm[:, :d] @ Qm[:, :d].conj().T
        maxdev = max(maxdev, float(np.linalg.norm(P @ (np.eye(n) - P) + (np.eye(n) - P) @ P)))
out["sonda_identidade_de_projetor"] = {
    "estatuto": "[REAL medido aqui; a identidade e trivial e vale para TODO projetor]",
    "norma_anticomutador_Q0_rhostar": float(np.linalg.norm(Q0 @ rho_star + rho_star @ Q0)),
    "max_P_1menosP_mais_1menosP_P_em_600_projetores": maxdev,
    "leitura": "o 'verificado ao vivo' de ||{Q_0, rho*}|| = 0 e a identidade P(1-P) + (1-P)P = 0 de qualquer projetor; nao carrega beta; o enunciado com theta generico e B2.a (anticomm_zero_iff)"}

# 5f. onde o beta entra na funcao do um.py (leitura das linhas, sem executar)
func = [l.decode("utf-8", "replace") for l in linhas[6487:6533]]
out["leitura_codigo_fractal_dephasing"] = {
    "estatuto": "[REAL — leitura por numero de linha dos bytes do um.py v391]",
    "linhas_6509_6519": {str(6509 + i): func[21 + i].strip() for i in range(0, 11)},
    "ha_passo_de_defasagem_no_codigo": any(("diag" in l and "np.diag" in l) or "dephase" in l for l in func[21:32]),
    "leitura": "no codigo, beta entra so por theta_M (a rotacao R, regime angular); a funcao nao aplica D: o 'D_beta' do rotulo nao e implementado ali; no kernel (GlobalLiftLadder) a matriz-S gera a distincao e o dephasing a inscreve como peso"}

# ---------------------------------------------------------------- 6. contagens dos vereditos
pp = {p["id"]: p for p in rk["por_parte"]}
out["contagens"] = {k: len(v) for k, v in rk["resumo"].items() if isinstance(v, list)}
out["falhas"] = falhas
out["veredito"] = "CONFERENCIA_DO_REDATOR_PASSOU" if not falhas else "CONFERENCIA_DO_REDATOR_COM_FALHAS"
out["fim_local"] = time.strftime("%Y-%m-%d %H:%M:%S")
dest = os.path.join(REL, "CONFERENCIA_REDATOR.json")
if os.path.exists(dest):
    print("FALHA VISIVEL: destino ja existe (nao sobrescrevo): " + dest, file=sys.stderr)
    sys.exit(2)
txt = json.dumps(out, ensure_ascii=False, indent=1)
with open(dest, "w", encoding="utf-8") as fh:
    fh.write(txt)
print(txt)
sys.exit(0 if not falhas else 1)
