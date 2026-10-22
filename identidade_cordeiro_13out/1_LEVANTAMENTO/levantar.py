# -*- coding: utf-8 -*-
"""LEVANTAMENTO da F1.IDENTIDADE (13/10/2026), so leitura.
(1) mapa de rotas: consultas (rotas.py consultar), saida integral gravada aqui;
(2) inventario da bancada: busca por palavras-chave;
(3) kernel do Nos: declaracoes procuradas (texto), com arquivo, linha e sha16 do arquivo;
(4) candidatas da v392: sha16 dos bytes conferido;
(5) um.py v391: a linha 5557 lida nos bytes (sem executar).
Grava LEVANTAMENTO_DADOS.json nesta pasta."""
import os, sys, json, hashlib, subprocess, re, datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
NOS = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N" + chr(0xF3) + "s"
K = NOS + "/tgl_kernel"
W = "C:/IALD/Central de Patentes/work"
ROTAS = "C:/IALD/MAPA_DE_ROTAS/rotas.py"
INV = "C:/IALD/Central de Patentes/memory/INVENTARIO_BANCADA_CHATGPT.json"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


out = {"quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}

# (1) mapa de rotas
temas = ["identidade", "agape", "Lagrange", "Torre", "torre", "cordeiro", "Nome posto", "eu sou", "Palavra",
         "motor", "Fundacao", "TheUnitIsTheRank", "posto", "tempo"]
cons = {}
for t in temas:
    r = subprocess.run([sys.executable, "-X", "utf8", ROTAS, "consultar", t], capture_output=True)
    txt = r.stdout.decode("utf-8", errors="replace")
    fn = "rotas_consultar_" + re.sub(r"[^A-Za-z0-9]+", "_", t) + ".json"
    open(os.path.join(AQUI, fn), "wb").write(r.stdout)
    try:
        d = json.loads(txt)
        cons[t] = {"arquivo": fn, "sha256": hashlib.sha256(r.stdout).hexdigest(), "n": d.get("n"),
                   "cabeca": d.get("cabeca"),
                   "rotas": [[x.get("rota_id"), x.get("status"), (x.get("veredito") or "")[:120]] for x in d.get("rotas", [])]}
    except Exception as e:
        cons[t] = {"arquivo": fn, "erro": repr(e)}
out["mapa_de_rotas"] = cons

# (2) inventario da bancada
s = open(INV, encoding="utf-8").read()
kws = ["NamedIdentity", "Cordeiro", "cordeiro", "Christ", "Cristo", "IAmThat", "eu_sou", "the_name_reads_one",
       "alpha_face", "Lagrange", "IdentityHasAName", "sacrific"]
out["inventario_bancada"] = {"arquivo": INV, "sha256": sha(INV),
                             "contagens": {k: len(re.findall(k, s)) for k in kws},
                             "nota": "Christ = 1 ocorrencia: lowerChristoffelJet/lower_christoffel_metric_identity (Christoffel), "
                                     "nao relacionada; nenhuma pedra de identidade nomeada na bancada"}

# (3) kernel do Nos
procurar = {
    "omega_of_one": "TheAlphaAndTheOmega.lean", "the_alpha_face": "TheAlphaAndTheOmega.lean",
    "the_form_admits_every_alpha": "TheAlphaAndTheOmega.lean", "agape": "Fundacao.lean", "abismo": "Fundacao.lean",
    "the_floor_fixes_the_cut": "Fundacao.lean", "agape_is_inhabited": "Fundacao.lean",
    "observing_adds_nothing": "TheObserverReadsTheAngle.lean", "post": "TheVerbSelectsTheAction.lean",
    "post_apply": "TheVerbSelectsTheAction.lean", "post_isIdempotent": "TheVerbSelectsTheAction.lean",
    "post_fixes_the_action": "TheVerbSelectsTheAction.lean", "reading": "TheVerbSelectsTheAction.lean",
    "reading_post_is_born": "TheVerbSelectsTheAction.lean", "dephase": "Ergodicity.lean",
    "diag_invariant": "Ergodicity.lean", "dephase_tendsto_expectation": "Ergodicity.lean",
    "diagExpect": "CondExpect.lean", "trace_diagExpect": "CondExpect.lean", "SiteProfile": "TowerDefinite.lean",
    "TowerPre": "TowerDefinite.lean", "TowerHilbert": "TowerHilbert.lean", "hOmega_norm": "TowerHilbert.lean",
    "omegaState": "TheFactorObject.lean", "theFactorObject": "TheFactorObject.lean",
    "towerFlow": "TowerModular.lean", "tower_kms": "TowerModular.lean", "modularFlow": "ModularFlowHilbert.lean",
    "modularFlow_fixes_omega": "ModularPower.lean", "modularConjugation_preserves_state": "ModularPower.lean",
    "sitePauliX": "SitePauliObservables.lean", "site_pauli_x_state": "SitePauliObservables.lean",
    "pauli_x_gns_norm": "LocalHorizontalPauli.lean", "the_power_has_two_fixed_points": "TheAxiomAndTheFalseWitness.lean",
    "the_two_indices_agree_only_at_the_atom": "TheWeightIsNotTheRank.lean",
    "half_is_the_fixed_point_of_the_swap": "TheFiveHalves.lean", "identity_weighs_as_the_name": "TheElementaryReason.lean",
}
kd = {}
for nome, arq in procurar.items():
    p = K + "/TGLExt/" + arq
    linhas = open(p, "rb").read().decode("utf-8").split("\n")
    hit = [i + 1 for i, l in enumerate(linhas)
           if re.match(r"^\s*(noncomputable )?(theorem|lemma|def|abbrev|structure) " + re.escape(nome) + r"\b", l)]
    olean = K + "/.lake/build/lib/lean/TGLExt/" + arq[:-5] + ".olean"
    kd[nome] = {"arquivo": "TGLExt/" + arq, "linhas": hit, "fonte_sha16": sha(p)[:16],
                "olean_existe": os.path.exists(olean)}
out["kernel_nos"] = kd
# leituras teologicas ja no kernel (texto, [ONTO]) e ausencia de pedra nomeada
gr = []
for raiz, _, fs in os.walk(K + "/TGLExt"):
    for f in fs:
        if f.endswith(".lean"):
            p = os.path.join(raiz, f)
            for i, l in enumerate(open(p, "rb").read().decode("utf-8", errors="replace").split("\n")):
                if re.search(r"Cristo|CRISTO|cordeiro|Cordeiro|NamedIdentity", l):
                    gr.append([os.path.relpath(p, K).replace("\\", "/"), i + 1, l.strip()[:220]])
out["kernel_nos_grep_Cristo_cordeiro_NamedIdentity"] = gr

# (4) candidatas da v392
cand = {
    "TheUnitIsTheRank_r3": W + "/frequencia_defasa_12out/5_R3/sandbox/TGLExt/TheUnitIsTheRank.lean",
    "TheTimeIsNotAPost": W + "/tempo_santo_12out/5_R2/1_PEDRA/sandbox/TheTimeIsNotAPost.lean",
    "IALD_motor_r3": W + "/organismo_iald_12out/7_R3_DOCSTRINGS/fonte/TGLExt/IALD.lean",
    "Palavra": W + "/leitura_cria_o_objeto_07out/Palavra.lean",
}
esperado = {"TheUnitIsTheRank_r3": "e95775d61db38633", "TheTimeIsNotAPost": "4d8a82591badd010",
            "IALD_motor_r3": "d7c1f1d3b03e6095", "Palavra": "33184b49a8bba7e7"}
cd = {}
for k, p in cand.items():
    h = sha(p)
    txt = open(p, "rb").read().decode("utf-8")
    imps = [l.strip() for l in txt.split("\n") if l.startswith("import ")]
    cd[k] = {"caminho": p, "sha16": h[:16], "confere": h[:16] == esperado[k], "imports": imps}
out["candidatas_v392"] = cd

# (5) um.py v391, linha 5557, nos bytes
U = NOS + "/um.py"
b = open(U, "rb").read()
L = b.split(b"\n")
out["um_py"] = {"sha16": hashlib.sha256(b).hexdigest()[:16], "l5557": L[5556].decode("utf-8").rstrip("\r"),
                "l5559": L[5558].decode("utf-8").rstrip("\r"), "executado": False}

json.dump(out, open(os.path.join(AQUI, "LEVANTAMENTO_DADOS.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"rotas": {t: v.get("n") for t, v in cons.items()}, "inv": out["inventario_bancada"]["contagens"],
                  "kernel_faltando": [n for n, v in kd.items() if not v["linhas"]],
                  "grep": len(gr), "cand": {k: v["confere"] for k, v in cd.items()}, "um": out["um_py"]},
                 ensure_ascii=False, indent=0))
