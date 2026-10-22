# -*- coding: utf-8 -*-
"""fontes.py -- as FONTES da Bancada Um, lidas do artefato e conferidas por hash (a régua: nada digitado, falha visível).

Cada fonte devolve os dados E a sua proveniência (caminho, sha256, de onde veio o pino). Se o hash não confere com a referência
selada, a carga é RECUSADA (exceção), nunca «ok» falso.
"""
import ast
import hashlib
import json
import io
from pathlib import Path
import os
import re

import numpy as np

IALD = r"C:\IALD"
PONTE = os.path.join(IALD, "Artigo", "Haja_Luz", "A Ponte e o Um")
NOS = os.path.join(PONTE, "Nós")
D1V3 = os.path.join(PONTE, "cache", "d1_camb", "v3")
DESI_DR2_DIR = os.path.join(IALD, "Artigo", "teste_acustico_beta_tgl_v1", "_originais")
DESI_DR2_COPIAS = [os.path.join(IALD, "Artigo", "frente_alpha"),
                   os.path.join(PONTE, "TETELESTAI", "BANCADA_OFICIAL", "data", "cosmology")]
PANTHEON = os.path.join(IALD, "observaveis_tgl", "tgl_data_cache", "pantheon", "Pantheon+SH0ES.dat")


class FonteRecusada(Exception):
    pass


def read_checked(path):
    """Read once: the exact parsed bytes must match the deployment custody pin."""
    from .canonical import verify_source_bytes
    raw = Path(path).read_bytes()
    pin = verify_source_bytes(path, raw)
    return raw, pin["sha256"]


def json_checked(path):
    raw, sha = read_checked(path)
    def reject_constant(value):
        raise FonteRecusada("JSON não finito: " + value)
    return json.loads(raw, parse_constant=reject_constant), sha


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _literal(tree, nome):
    for no in ast.walk(tree):
        if isinstance(no, ast.Assign) and any(isinstance(t, ast.Name) and t.id == nome for t in no.targets):
            return no.value
    raise FonteRecusada("atribuição %s ausente" % nome)


def _avalia(no):
    """Avalia só literais e np.array(literal) -- nunca executa o arquivo."""
    if isinstance(no, ast.Call) and getattr(no.func, "attr", None) == "array":
        return np.array(ast.literal_eval(no.args[0]), float)
    return ast.literal_eval(no)


def alpha_codata_2018():
    """Canonical alpha with version/seal pin; pipeline equality is historical control."""
    from .canonical import read_alpha
    a, prov = read_alpha()
    raw, h = read_checked(os.path.join(D1V3, "d1_v3_pipeline.py"))
    tree = ast.parse(raw.decode("utf-8-sig"))
    a2 = float(_avalia(_literal(tree, "ALPHA_FINE_CODATA_2018")))
    if not np.isfinite(a2) or a != a2:
        raise FonteRecusada("alpha canônico difere do pipeline histórico")
    return a, dict(prov, pipeline_sha256=h, controle_historico_alpha_igual=True)


def d1_v3_primario():
    """Planck 2018 comprimido (R, l_A, ω_b; Zhai+ 2019), DESI DR1 BAO (12 linhas) e SH0ES, LIDOS do pipeline D1 V3 selado por AST
    (sem executar), com o sha256 do pipeline conferido contra MANIFESTO_D1_V3.json."""
    p = os.path.join(D1V3, "d1_v3_pipeline.py")
    man, _ = json_checked(os.path.join(D1V3, "MANIFESTO_D1_V3.json"))
    pino = man["arquivos"]["d1_v3_pipeline.py"]
    raw, h = read_checked(p)
    if h != pino:
        raise FonteRecusada("d1_v3_pipeline.py sha256 %s != manifesto %s" % (h, pino))
    real, _ = json_checked(os.path.join(D1V3, "saida", "D1_CAMB_V3_REAL_RESULT.json"))
    if real.get("scripts", {}).get("pipeline") != h:
        raise FonteRecusada("o resultado real selado não é deste pipeline")
    tree = ast.parse(raw.decode("utf-8-sig"))
    cov = _avalia(_literal(tree, "PLANCK_COV"))
    rows = _avalia(_literal(tree, "DESI_ROWS"))
    sh0es_sigma = float(_avalia(_literal(tree, "SH0ES_SIGMA")))
    fn =next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "_dados_reais")
    ret = next(n for n in ast.walk(fn) if isinstance(n, ast.Return)).value
    kw = {k.arg: k.value for k in ret.keywords}
    planck_mean = _avalia(kw["planck_mean"])
    desi_vals = _avalia(kw["desi_vals"])
    sh0es_mean = float(_avalia(kw["sh0es_mean"]))
    lim = next(n for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "LIMITES" for t in n.targets)).value
    limites = {k.arg: tuple(ast.literal_eval(k.value)) for k in lim.keywords}
    prov = {"arquivo": p, "sha256": h, "pino": "MANIFESTO_D1_V3.json -> arquivos.d1_v3_pipeline.py", "resultado_selado": "D1_CAMB_V3_REAL_RESULT.json"}
    return dict(planck_mean=np.asarray(planck_mean, float), planck_cov=np.asarray(cov, float),
                desi_rows=[tuple(r) for r in rows], desi_vals=np.asarray(desi_vals, float),
                sh0es_mean=sh0es_mean, sh0es_sigma=sh0es_sigma, limites=limites, resultado_selado=real), prov


def desi_dr2():
    """DESI DR2 BAO (13 medidas + covariância 13×13), do _originais do teste acústico; as cópias das outras casas têm de ser idênticas."""
    mean = os.path.join(DESI_DR2_DIR, "desi_gaussian_bao_ALL_GCcomb_mean.txt")
    cov = os.path.join(DESI_DR2_DIR, "desi_gaussian_bao_ALL_GCcomb_cov.txt")
    raw_mean, hm = read_checked(mean)
    raw_cov, hc = read_checked(cov)
    copias = {}
    for d in DESI_DR2_COPIAS:
        for nome, h0 in (("desi_gaussian_bao_ALL_GCcomb_mean.txt", hm), ("desi_gaussian_bao_ALL_GCcomb_cov.txt", hc)):
            q = os.path.join(d, nome)
            if os.path.exists(q):
                copias[q] = (read_checked(q)[1] == h0)
    if not all(copias.values()):
        raise FonteRecusada("uma cópia do DESI DR2 diverge: %s" % copias)
    z, v, q = [], [], []
    for ln in raw_mean.decode("utf-8-sig").splitlines():
        if ln.strip() and not ln.startswith("#"):
            a, b, c = ln.split()
            z.append(float(a)); v.append(float(b)); q.append(c)
    C = np.loadtxt(io.BytesIO(raw_cov))
    if not np.all(np.isfinite(C)) or not np.all(np.isfinite(z + v)) or C.shape != (len(z), len(z)):
        raise FonteRecusada("covariância %s != %d medidas" % (C.shape, len(z)))
    prov = {"media": mean, "media_sha256": hm, "cov": cov, "cov_sha256": hc, "copias_identicas": copias}
    return dict(z=np.array(z), valor=np.array(v), grandeza=q, cov=C), prov


PANTHEON_COV = os.path.join(IALD, "projetos_pyhton", "acom", "tgl_data_cache", "pantheon_covariance.dat")
FONTES_EXTERNAS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fontes_externas")
CHEN_PDF = os.path.join(FONTES_EXTERNAS, "chen_huang_wang_2019_1808.05724.pdf")
MORESCO_JSON = os.path.join(FONTES_EXTERNAS, "moresco_2022_cc.json")   # Fase 4 (30/09): importado do artigo 1 por ferramentas/importar_cronometros_do_artigo.py


def cronometros_moresco2022():
    """Os 32 cronômetros cósmicos H(z) de Moresco+ 2022 (compilação), IMPORTADOS do artigo 1 (tgl_paper_unified.py, dataset embutido) por
    ferramentas/importar_cronometros_do_artigo.py, que grava a proveniência (sha256 do artigo e as linhas). Recusa se ausente ou malformado."""
    if not os.path.exists(MORESCO_JSON):
        raise FonteRecusada("cronômetros ausentes: %s (rode ferramentas/importar_cronometros_do_artigo.py)" % MORESCO_JSON)
    d, source_sha = json_checked(MORESCO_JSON)
    a = np.asarray(d["data"], float)
    if a.shape != (32, 3) or not np.all(np.isfinite(a)) or not np.all(a[:, 2] > 0) or not np.all(a[:, 0] > 0):
        raise FonteRecusada("cronômetros: forma/valores inválidos %s" % (a.shape,))
    prov = dict(d["proveniencia"]); prov["json"] = MORESCO_JSON; prov["json_sha256"] = source_sha
    return dict(z=a[:, 0], H=a[:, 1], sigma=a[:, 2], n=int(a.shape[0])), prov


MORESCO_COV_JSON = os.path.join(FONTES_EXTERNAS, "moresco_2020_cov.json")   # Fase 7 (01/10): ferramentas/importar_covariancia_moresco2020.py


def cronometros_covariancia_moresco2020():
    """Fase 7 (01/10/2026): a covariância completa de Moresco+2020 (ApJ 898, 82; gitlab.com/mmoresco/CCcovariance) montada nos 32 pontos da Bancada, em duas variantes
    ('moresco2020': os 15 pontos de Moresco 2012/2015/2016 com (z, H, σ) DA FONTE e IMF + SPS odd-one-out correlacionados, os 17 outros diagonais; 'moresco2020_todos': a
    sistemática correlacionada em todos — faixa conservadora). Devolve {variante: dict(z, H, cov, sigma_total)} e a proveniência. Recusa se ausente ou não definida positiva."""
    if not os.path.exists(MORESCO_COV_JSON):
        raise FonteRecusada("covariância dos cronômetros ausente: %s (rode ferramentas/importar_covariancia_moresco2020.py)" % MORESCO_COV_JSON)
    d, source_sha = json_checked(MORESCO_COV_JSON)
    z = np.asarray(d["pontos"]["z"], float); H = np.asarray(d["pontos"]["H"], float); sets = {}
    for v, V in d["variantes"].items():
        C = np.asarray(V["cov"], float)
        if C.shape != (32, 32) or not np.all(np.isfinite(C)) or not np.all(np.isfinite(z)) or not np.all(np.isfinite(H)) or not np.allclose(C, C.T):
            raise FonteRecusada("covariância %s: forma/simetria inválida %s" % (v, C.shape))
        np.linalg.cholesky(C)
        sets[v] = dict(z=z, H=H, cov=C, sigma_total=np.sqrt(np.diag(C)), descricao=V["descricao"])
    prov = dict(json=MORESCO_COV_JSON, json_sha256=source_sha, arquivos=d["arquivos"], receita=d["receita"], nota=d["nota"])
    return sets, prov
# DESI 2024 VI (arXiv:2404.03002), Tabela 1: correlação r entre D_M/r_d e D_H/r_d no MESMO z, lida no HTML do arXiv em 28/09/2026 pela gerência
# (auditoria de 28/09, achado D1F-01: o pipeline selado entra só com a diagonal).
DR1_CORRELACOES = {0.510: -0.445, 0.706: -0.420, 0.930: -0.389, 1.317: -0.444, 2.330: -0.477}


def planck_chen2019(planck_mean):
    """Chen, Huang & Wang 2019 (arXiv:1808.05724), Tabela I, ΛCDM, Planck 2018 TT,TE,EE+lowE: σ(R, l_A, ω_b) e a matriz de correlação LIDAS do
    PDF (texto extraído pela auditoria de 28/09; o PDF fica em fontes_externas com sha256). A média é a do pipeline selado, que coincide com a
    tabela. Auditoria de 28/09 (D1F-03): as correlações fora da diagonal do pipeline (0,084/−0,066/−0,119) estavam mal transcritas (tabela:
    0,46/−0,66/−0,33) e a citação «Zhai+ 2019» estava errada."""
    sig = np.array([0.0046, (0.089 + 0.090) / 2.0, 0.00015])
    rho = np.array([[1.0, 0.46, -0.66], [0.46, 1.0, -0.33], [-0.66, -0.33, 1.0]])
    cov = rho * np.outer(sig, sig)
    prov = dict(fonte="Chen, Huang & Wang 2019, arXiv:1808.05724, Tabela I (ΛCDM; TT,TE,EE+lowE)", pdf=CHEN_PDF,
                pdf_sha256=read_checked(CHEN_PDF)[1], media=np.asarray(planck_mean, float).tolist(),
                sigma=sig.tolist(), correlacoes=rho.tolist(), nota="σ de l_A é assimétrico na tabela (+0,089/−0,090); usa-se a média 0,0895")
    return cov, prov


def desi_dr1_covariancia(desi_rows):
    """Covariância do DESI DR1 com as correlações D_M–D_H do mesmo z (DR1_CORRELACOES); fora delas, a diagonal do pipeline selado."""
    n = len(desi_rows)
    sig = np.array([r[2] for r in desi_rows], float)
    C = np.diag(sig ** 2)
    usadas = []
    for i in range(n):
        for j in range(i + 1, n):
            zi, ti, _ = desi_rows[i]; zj, tj, _ = desi_rows[j]
            if abs(zi - zj) < 1e-6 and {int(ti), int(tj)} == {0, 1}:
                r = DR1_CORRELACOES[round(float(zi), 3)]
                C[i, j] = C[j, i] = r * sig[i] * sig[j]
                usadas.append(dict(z=float(zi), r=r))
    assert len(usadas) == 5, usadas
    prov = dict(fonte="DESI 2024 VI, arXiv:2404.03002, Tabela 1 (r entre D_M/r_d e D_H/r_d), lida no HTML do arXiv em 28/09/2026",
                correlacoes=usadas, estatuto_origem="DECLARADO", fonte_primaria_sha256=None,
                admissao_primaria_verificada=False,
                nota="a diagonal é do pipeline pinado; as 5 correlações são transcrição histórica em código. Custódia do código não substitui pino/admissão da fonte primária")
    return C, prov


def pantheon_plus():
    """Pantheon columns; Motor connects the full STAT+SYS covariance and profiles M."""
    raw, h = read_checked(PANTHEON)
    cab = raw.decode("utf-8-sig").splitlines()[0].split()
    arr = np.genfromtxt(io.BytesIO(raw), names=True, dtype=None, encoding="utf-8")
    cols = {n: np.asarray(arr[n]) for n in ("zHD", "zCMB", "zHEL", "m_b_corr", "m_b_corr_err_DIAG", "MU_SH0ES", "MU_SH0ES_ERR_DIAG", "IS_CALIBRATOR", "CEPH_DIST", "USED_IN_SH0ES_HF")}   # 01/10: + calibradores Cefeida
    prov = {"arquivo": PANTHEON, "sha256": h, "n": int(len(arr)), "colunas": len(cab),
            "limitacao": "Covariância STAT+SYS ligada pelo PantheonCov; M profilado; combinações sobrepostas recusadas.",
            "covariancia_em_disco": PANTHEON_COV if os.path.isfile(PANTHEON_COV) else None}
    return cols, prov
