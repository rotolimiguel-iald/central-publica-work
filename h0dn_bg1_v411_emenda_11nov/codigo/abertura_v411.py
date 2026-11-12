# -*- coding: utf-8 -*-
"""v411 -- rotina de ABERTURA do teste H0DN x BG1 como FUNCAO PURA: `abrir(y255, ...)` recebe o vetor como argumento.
Este modulo nao le arquivo de vetor. Os carregadores (carregar_*) so' leem arquivos de DESENHO (rede, estimador congelado,
estimador S0, BG1) e o README da colaboracao (alvos do portao 1b, pinado por sha256 OBRIGATORIO); aceitam caminho ou bytes.

Ordem em `abrir`: conferir_integridade (fiacao NOSSA; falha = ValueError("integridade: ...")) -> vetor (float64 (255,) finito;
senao ValueError("vetor: ...")) -> portao 1 = 1b.reproduz E 1d (se 1b reproduz, as conferencias internas pesos/1c viram
integridade: falha = ValueError) -> se o portao falhar, ramo (1) e NADA mais e' calculado (t, z, coerencia, estresse = None)
-> estatistica primaria S0 -> veredito (modelo publicado) + linha ao lado (Cefeidas livres) -> coerencia (so' relatada)
-> estresses (i) tau por linha, (ii) ancora unica, (iii) vies por hospedeira.
"""
import hashlib
import io
import itertools
import json
import re
import sys
from pathlib import Path

import numpy as np
import scipy.linalg
from scipy.stats import norm

sys.path.insert(0, str(Path(__file__).resolve().parent))
from estimator_v411 import evaluate          # noqa: E402
from veredito_v411 import veredito_h0dn_v411  # noqa: E402

TOL_H0, TOL_SIG, TOL_CHI2 = 0.5e-4, 0.5e-4, 0.5e-4   # tolerancias do portao 1b (spec)
TOL_FP = 1e-9                                         # impressao digital (portao 1d)
TOL_W = 1e-10                                         # pesos congelados vs colaboracao (1b interno) e centragem (1c)
TOL_INT = 1e-9                                        # alinhamento desenho/pesos/nulo na integridade
TOL_SD_REL = 1e-12                                    # sd recalculados e D na integridade
TAUS_B = (0.02, 0.05)                                 # estresse (iii): vies maximo por hospedeiro, em mag
MODELOS = ["published_baseline", "free_cepheid_host_differential_bias"]
N_LINHAS, N_S0, N_FORA = 255, 242, 13
N_NULO, POSTO_C, POSTO_C0, N_TOCADAS, N_HOSP = 72, 183, 170, 111, 37
ANCORAS = ("N4258", "LMC", "MW")
_RE_TOC = re.compile(r"^Host equation for (\S+) with MAS: ceph_hst&(N4258|LMC|MW)&R22$")
_RE_HOST = re.compile(r"^Host equation for (\S+)")
FORMULA_III = "delta = B * soma_g | soma_{i em g} w_i c_i |"
MODELO_ESTRESSE_I = ("ruido adicional independente e homoscedastico nas 111 linhas brutas (R_extra = tau^2 I_111); pesos mantidos; "
                     "tau_hat = RMS em torno de zero da projecao nula (norma / raiz de 72); "
                     "estimado depois de observar o vetor: pos-observacao, nao cego")
CHAVES_VEREDITOS = ("inconclusivo", "lei_falsificada", "subpotente", "tensao", "nao_discriminado", "faixas", "sufixo", "leitura_partes")


# ------------------------------------------------------------------ carregadores (so' desenho; caminho ou bytes)
def _fonte(p):
    return io.BytesIO(bytes(p)) if isinstance(p, (bytes, bytearray)) else p


def carregar_rede(path):
    with np.load(_fonte(path), allow_pickle=False) as d:
        return {"A": d["A"].copy(), "C": d["C"].copy(), "c": d["c_cepheid"].copy(), "h_index": int(d["h_index"]),
                "row_names": [str(x) for x in d["row_names"]], "param_names": [str(x) for x in d["param_names"]]}


def carregar_congelado(path):
    with np.load(_fonte(path), allow_pickle=False) as d:
        return {"weights": d["weights"].copy(), "null_basis": d["null_basis"].copy(), "gradient_h": d["gradient_h"].copy(),
                "gradient_k": d["gradient_k"].copy(), "sd_null": d["sd_null"].copy(), "sd_tgl": d["sd_tgl"].copy(),
                "logK": float(d["logK"]), "H0": float(d["H0"]), "model_names": [str(x) for x in d["model_names"]]}


def carregar_s0(path):
    out = {}
    with np.load(_fonte(path), allow_pickle=False) as d:
        for k in d.files:
            v = d[k]
            if v.ndim == 0:
                out[k] = v.item()
            elif v.dtype.kind == "U":
                out[k] = [str(x) for x in v]
            else:
                out[k] = v.copy()
    return out


def carregar_bg(path):
    if isinstance(path, (bytes, bytearray)):
        return json.loads(bytes(path).decode("utf-8"))
    return json.loads(Path(path).read_text(encoding="utf-8"))


_RE_BASE = re.compile(r"H0=([0-9]+(?:\.[0-9]+)?)\+/-([0-9]+(?:\.[0-9]+)?) km/s/Mpc \| Chi-squared=([0-9]+(?:\.[0-9]+)?) \| ndof=([0-9]+)")


def ler_alvos_readme(path, sha256_esperado):
    """Le a linha de base documentada pela colaboracao no README (H0, sigma, chi2, ndof) e confere o sha256 do arquivo.
    `sha256_esperado` e' OBRIGATORIO (None ou vazio -> ValueError). O alvo de impressao digital (fp) NAO sai daqui."""
    if not isinstance(sha256_esperado, str) or not re.fullmatch(r"[0-9a-f]{64}", sha256_esperado):
        raise ValueError("sha256_esperado obrigatorio (64 hex minusculos)")
    raw = bytes(path) if isinstance(path, (bytes, bytearray)) else Path(path).read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != sha256_esperado:
        raise ValueError("README da colaboracao nao bate com o pino sha256: " + sha)
    ms = list(_RE_BASE.finditer(raw.decode("utf-8")))
    if len(ms) != 1:
        raise ValueError("esperada exatamente 1 linha de base no README, achei %d" % len(ms))
    m = ms[0]
    return {"H0": float(m.group(1)), "sig": float(m.group(2)), "chi2": float(m.group(3)), "ndof": int(m.group(4)),
            "linha": m.group(0), "sha256": sha, "bytes": len(raw)}


# ------------------------------------------------------------------ formulas da colaboracao (solver.py, linhas 85-113)
def numeros_colaboracao(y, A, C, h_index):
    Cp, rank = scipy.linalg.pinv(C, atol=1e-10, rtol=0.0, return_rank=True)
    solmat = A.T @ Cp @ A
    invsolmat = np.linalg.inv(solmat)
    solval = A.T @ Cp @ y
    params = invsolmat @ solval
    res = y - A @ params
    logh = float(params[h_index])
    H0 = 10 ** logh
    sig = 10 ** (logh + np.sqrt(invsolmat[h_index, h_index])) - H0
    chi2 = float(res.T @ Cp @ res)
    return {"logh": logh, "H0": float(H0), "sig": float(sig), "chi2": chi2, "rank": int(rank),
            "ndof": int(rank - A.shape[1]), "params": params}


def impressao_digital(y, null_basis_255):
    return float(np.max(np.abs(y @ null_basis_255))) if null_basis_255.shape[1] else 0.0


def _alvos_completos(alvos):
    falta = [k for k in ("H0", "sig", "chi2", "ndof", "fp") if k not in alvos]
    if falta:
        raise ValueError("alvos incompletos (faltam %s)" % falta)


def _pack_estimator(s0, sufixo=""):
    return {"weights": s0["weights" + sufixo], "null_basis": s0["null_basis" + sufixo], "gradient_h": s0["gradient_h"],
            "gradient_k": s0["gradient_k"], "sd_null": s0["sd_null" + sufixo], "sd_tgl": s0["sd_tgl" + sufixo],
            "logK": s0["logK"], "H0": s0["H0"]}


def _ramo_vazio(D0, ramos):
    # z nan so' atravessa o float(); o ramo (1) retorna antes de usar z
    return veredito_h0dn_v411(float("nan"), float("nan"), float(D0), False, ramos)


# ------------------------------------------------------------------ integridade (fiacao NOSSA: recusa dura, nao e' veredito)
def _falha(msg):
    raise ValueError("integridade: " + msg)


def _maxabs(x):
    x = np.asarray(x)
    return float(np.max(np.abs(x))) if x.size else 0.0


def _eh(n, i):
    e = np.zeros(n)
    e[i] = 1.0
    return e


def conferir_integridade(rede, congelado, s0, bg, ramos):
    """Confere, SEM tocar o vetor, que desenho/pesos/nulo/escalas/ramos estao alinhados. ValueError("integridade: <motivo>")
    na primeira falha; devolve os valores medidos."""
    try:
        return _conferir_integridade(rede, congelado, s0, bg, ramos)
    except ValueError:
        raise
    except Exception as e:  # fiacao quebrada que o numpy denuncia por outro tipo de erro
        raise ValueError("integridade: erro de fiacao (%s: %s)" % (type(e).__name__, e))


def _checar_base_nula(Nb, rotulo):
    """A1a: exatamente 72 colunas e ortonormal (max|N'N - I| < 1e-9)."""
    Nb = np.asarray(Nb, float)
    if Nb.ndim != 2 or Nb.shape[1] != N_NULO:
        _falha("base nula %s deve ter exatamente %d colunas (forma %s)" % (rotulo, N_NULO, Nb.shape))
    d = _maxabs(Nb.T @ Nb - np.eye(N_NULO))
    if not d < TOL_INT:
        _falha("base nula %s nao e' ortonormal (max|N'N-I| = %.3e)" % (rotulo, d))
    return d


def _posto(M):
    return int(np.sum(np.linalg.eigvalsh((M + M.T) / 2) > 1e-10))


def _conferir_integridade(rede, congelado, s0, bg, ramos):
    A, C, c, h = rede["A"], rede["C"], rede["c"], int(rede["h_index"])
    n = A.shape[0]
    out = {}
    # ---- a. ordem dos modelos
    if list(s0["model_names"]) != MODELOS or list(congelado["model_names"]) != MODELOS:
        _falha("ordem dos modelos (S0 %s | congelado %s)" % (list(s0["model_names"]), list(congelado["model_names"])))
    out["model_names"] = list(MODELOS)
    # ---- b. identidade do S0
    if n != N_LINHAS or C.shape != (n, n) or c.shape != (n,) or len(rede["row_names"]) != n:
        _falha("dimensoes da rede")
    keep = np.asarray(s0["keep"])
    if keep.ndim != 1 or keep.shape[0] != N_S0 or keep.dtype.kind not in "iu":
        _falha("keep: %d indices inteiros exigidos" % N_S0)
    if keep.min() < 0 or keep.max() >= n:
        _falha("keep fora de range(%d)" % n)
    if not np.all(np.diff(keep) > 0):
        _falha("keep nao e' unico e crescente")
    sn = [i for i, r in enumerate(rede["row_names"]) if r.startswith("SNe Ia equation")]
    if len(sn) != 55:
        _falha("a rede deveria ter 55 linhas 'SNe Ia equation' (tem %d)" % len(sn))
    compl = sorted(set(range(n)) - set(int(i) for i in keep))
    if compl != sn[-N_FORA:]:
        _falha("o complemento de keep nao e' o das ultimas %d linhas 'SNe Ia equation'" % N_FORA)
    out["keep_n"] = int(keep.shape[0])
    out["complemento_de_keep"] = compl
    colmask = np.asarray(s0["colmask"], bool)
    hs0 = int(s0["h_index_s0"])
    if colmask.shape != (A.shape[1],) or not colmask[h] or hs0 != int(np.sum(colmask[:h])):
        _falha("colmask/h_index_s0 incoerentes")
    # ---- c. alinhamento pesos/desenho/nulo
    A0, c0 = A[keep][:, colmask], c[keep]
    W, N0 = np.asarray(s0["weights"], float), np.asarray(s0["null_basis"], float)
    if W.shape != (2, N_S0) or N0.ndim != 2 or N0.shape[0] != N_S0:
        _falha("formas de weights/null_basis do S0")
    out["base_nula_S0_ortonormal_dif"] = _checar_base_nula(N0, "S0")
    ext0 = np.column_stack([A0, c0])
    d1 = _maxabs(W[0] @ A0 - _eh(A0.shape[1], hs0))
    d2 = _maxabs(W[1] @ ext0 - _eh(ext0.shape[1], hs0))
    dn = _maxabs(W @ N0)
    Csub = C[np.ix_(keep, keep)]
    dcn = _maxabs(Csub @ N0)
    for nome, v in (("weights[0] @ A0 - e_h", d1), ("weights[1] @ [A0,c0] - e_h", d2), ("weights @ null_basis", dn), ("C_S0 @ null_basis", dcn)):
        if not v < TOL_INT:
            _falha("S0 %s = %.3e (limite %.0e)" % (nome, v, TOL_INT))
    out["S0"] = {"peso_desenho_publicado": d1, "peso_desenho_cefeidas_livres": d2, "peso_nulo": dn, "C_nulo": dcn}
    # ---- A1b: postos
    p0, pc = _posto(Csub), _posto(C)
    if p0 != POSTO_C0 or pc != POSTO_C:
        _falha("posto de C[keep][:,keep] = %d (esperado %d) e de C = %d (esperado %d)" % (p0, POSTO_C0, pc, POSTO_C))
    out["postos"] = {"C_S0": p0, "C_255": pc}
    # ---- A1c: touched = linhas do S0 com norma de null_basis > 1e-9 = 37 hospedeiras x 3 ancoras
    touched = np.asarray(s0["touched"])
    if touched.ndim != 1 or touched.dtype.kind not in "iu" or touched.shape[0] != N_TOCADAS:
        _falha("touched: %d indices inteiros exigidos" % N_TOCADAS)
    nrm = np.linalg.norm(N0, axis=1)
    if set(np.where(nrm > 1e-9)[0].tolist()) != set(int(i) for i in touched):
        _falha("touched nao e' o conjunto das linhas do S0 com norma de null_basis > 1e-9")
    names0 = [rede["row_names"][int(i)] for i in keep]
    pares_ha = []
    for i in touched:
        m = _RE_TOC.match(names0[int(i)])
        if not m:
            _falha("linha tocada com nome inesperado: " + names0[int(i)])
        pares_ha.append((m.group(1), m.group(2)))
    hosts_t = sorted(set(hh for hh, _ in pares_ha))
    if len(hosts_t) != N_HOSP or len(set(pares_ha)) != N_TOCADAS or any(set(aa for hh, aa in pares_ha if hh == g) != set(ANCORAS) for g in hosts_t):
        _falha("as linhas tocadas nao sao %d hospedeiras x 3 ancoras" % N_HOSP)
    out["touched"] = {"n": int(touched.shape[0]), "hospedeiras": len(hosts_t)}
    # ---- A1d: sum_w2_touched
    s2 = np.array([float(np.sum(W[i][touched] ** 2)) for i in range(2)])
    s2_st = np.asarray(s0["sum_w2_touched"], float)
    rel_s2 = np.abs(s2 - s2_st) / s2
    if not np.all(rel_s2 <= 1e-12):
        _falha("sum_w2_touched nao bate com o recalculo (rel %.3e)" % rel_s2.max())
    out["sum_w2_touched_rel"] = rel_s2.tolist()
    # ---- A1e: s_host (soma COM SINAL dos pesos nas linhas do S0 com c != 0 de cada hospedeira) e sum_abs_s_host
    host_names = list(s0["host_names"])
    hosp = {}
    for j, nm in enumerate(names0):
        if c0[j] != 0:
            m = _RE_HOST.match(nm)
            if not m:
                _falha("linha com c != 0 que nao e' 'Host equation for': " + nm)
            hosp.setdefault(m.group(1), []).append(j)
    if len(host_names) != len(set(host_names)) or set(host_names) != set(hosp):
        _falha("host_names nao e' o conjunto das hospedeiras com linhas c != 0")
    sh = np.array([[float(sum(W[i][j] for j in hosp[hn])) for hn in host_names] for i in range(2)])
    sh_st = np.asarray(s0["s_host"], float)
    if sh_st.shape != sh.shape or not _maxabs(sh_st - sh) <= 1e-15:
        _falha("s_host nao bate com o recalculo (max |dif| = %.3e)" % (_maxabs(sh_st - sh) if sh_st.shape == sh.shape else float("nan")))
    sa_st = np.asarray(s0["sum_abs_s_host"], float)
    if not _maxabs(sa_st - np.abs(sh).sum(axis=1)) <= 1e-15:
        _falha("sum_abs_s_host nao e' a soma dos modulos de s_host")
    out["s_host_dif"] = _maxabs(sh_st - sh)
    # (extra) o estimador congelado de 255 linhas usado nos portoes 1b/1d
    W255, N255 = np.asarray(congelado["weights"], float), np.asarray(congelado["null_basis"], float)
    if W255.shape != (2, n) or N255.ndim != 2 or N255.shape[0] != n:
        _falha("formas de weights/null_basis do congelado")
    out["base_nula_congelado_ortonormal_dif"] = _checar_base_nula(N255, "congelado255")
    ext = np.column_stack([A, c])
    f = {"peso_desenho_publicado": _maxabs(W255[0] @ A - _eh(A.shape[1], h)),
         "peso_desenho_cefeidas_livres": _maxabs(W255[1] @ ext - _eh(ext.shape[1], h)),
         "peso_nulo": _maxabs(W255 @ N255), "C_nulo": _maxabs(C @ N255)}
    for nome, v in f.items():
        if not v < TOL_INT:
            _falha("congelado %s = %.3e (limite %.0e)" % (nome, v, TOL_INT))
    out["congelado255"] = f
    # ---- d. escalas
    logK = float(bg["logK"])
    gh, gk = np.asarray(bg["gradient_h"], float), np.asarray(bg["gradient_k"], float)
    Cb = np.asarray(bg["covariance"], float)
    dl = {"s0": abs(float(s0["logK"]) - logK), "congelado": abs(float(congelado["logK"]) - logK)}
    for k, v in dl.items():
        if not v <= 1e-15:
            _falha("logK de %s difere do BG1 (%.3e)" % (k, v))
    dg = {"s0_h": _maxabs(np.asarray(s0["gradient_h"], float) - gh), "s0_k": _maxabs(np.asarray(s0["gradient_k"], float) - gk),
          "cong_h": _maxabs(np.asarray(congelado["gradient_h"], float) - gh), "cong_k": _maxabs(np.asarray(congelado["gradient_k"], float) - gk)}
    for k, v in dg.items():
        if not v <= 1e-15:
            _falha("gradiente %s difere do BG1 (%.3e)" % (k, v))
    H0 = float(bg["H0"])
    dH = {"s0": abs(float(s0["H0"]) - H0), "congelado": abs(float(congelado["H0"]) - H0)}
    for k, v in dH.items():
        if not v <= 1e-12:
            _falha("H0 de %s difere do BG1 (%.3e)" % (k, v))
    vb, vbt = float(gh @ Cb @ gh), float((gh + gk) @ Cb @ (gh + gk))

    def checar_escalas(rotulo, Wd, Cs, sdn, sdt, D):
        sdn, sdt, D = np.asarray(sdn, float), np.asarray(sdt, float), np.asarray(D, float)
        vs = np.array([float(Wd[i] @ Cs @ Wd[i]) for i in range(2)])
        rn = np.abs(np.sqrt(vs + vb) - sdn) / sdn
        rt = np.abs(np.sqrt(vs + vbt) - sdt) / sdt
        dD = np.abs(D - logK / sdn)
        if not (np.all(rn <= TOL_SD_REL) and np.all(rt <= TOL_SD_REL)):
            _falha("%s: sd_null/sd_tgl nao batem com o recalculo (rel %.3e / %.3e)" % (rotulo, rn.max(), rt.max()))
        if not np.all(dD <= TOL_SD_REL):
            _falha("%s: D difere de logK/sd_null (%.3e)" % (rotulo, dD.max()))
        return {"sd_null_rel": rn.tolist(), "sd_tgl_rel": rt.tolist(), "D_dif": dD.tolist()}
    out["escalas"] = {"logK_dif": dl, "gradientes_dif": dg, "H0_dif": dH,
                      "S0": checar_escalas("S0", W, Csub, s0["sd_null"], s0["sd_tgl"], s0["D"])}
    # ---- ancoras unicas (pesos·desenho, escalas)
    out["ancoras"] = {}
    keep_set = set(int(i) for i in keep)
    for a in s0.get("anchor_names", []):
        ka = np.asarray(s0["keep_" + a])
        if ka.ndim != 1 or ka.dtype.kind not in "iu" or ka.size == 0 or not np.all(np.diff(ka) > 0) or not set(int(i) for i in ka) <= keep_set:
            _falha("ancora %s: keep_ nao e' subconjunto unico e crescente do S0" % a)
        cm = np.asarray(s0["colmask_" + a], bool)
        ha = int(s0["h_index_" + a])
        if cm.shape != (A.shape[1],) or not cm[h] or ha != int(np.sum(cm[:h])):
            _falha("ancora %s: colmask/h_index incoerentes" % a)
        Aa, ca = A[ka][:, cm], c[ka]
        Wa = np.asarray(s0["weights_" + a], float)
        if Wa.shape != (2, ka.shape[0]):
            _falha("ancora %s: forma de weights" % a)
        exta = np.column_stack([Aa, ca])
        da1 = _maxabs(Wa[0] @ Aa - _eh(Aa.shape[1], ha))
        da2 = _maxabs(Wa[1] @ exta - _eh(exta.shape[1], ha))
        for nome, v in (("weights[0] @ A - e_h", da1), ("weights[1] @ [A,c] - e_h", da2)):
            if not v < TOL_INT:
                _falha("ancora %s %s = %.3e (limite %.0e)" % (a, nome, v, TOL_INT))
        esc = checar_escalas("ancora " + a, Wa, C[np.ix_(ka, ka)], s0["sd_null_" + a], s0["sd_tgl_" + a], s0["D_" + a])
        out["ancoras"][a] = {"n_linhas": int(ka.shape[0]), "peso_desenho_publicado": da1, "peso_desenho_cefeidas_livres": da2, "escalas": esc}
    out["ancoras_recusadas_na_preparacao"] = list(s0.get("anchors_refused", []))
    # ---- e. ramos
    if not isinstance(ramos, dict) or ramos.get("limiar") != 5.0 or ramos.get("compat_95") != 1.959963984540054:
        _falha("ramos: limiar deve ser 5.0 e compat_95 1.959963984540054")
    V = ramos.get("vereditos")
    if not isinstance(V, dict) or any(k not in V for k in CHAVES_VEREDITOS):
        _falha("ramos: faltam chaves de vereditos %s" % [k for k in CHAVES_VEREDITOS if not isinstance(V, dict) or k not in V])
    if len(V["faixas"]) < 3 or not isinstance(V["leitura_partes"], (list, tuple)):
        _falha("ramos: faixas/leitura_partes mal formadas")
    out["ramos"] = {"limiar": ramos["limiar"], "compat_95": ramos["compat_95"], "chaves_vereditos": sorted(V)}
    return out


# ------------------------------------------------------------------ coerencia entre estimativas lineares do mesmo h (so' relatada)
def _pad255(w, keep, n):
    out = np.zeros(n)
    out[np.asarray(keep, int)] = np.asarray(w, float)
    return out


def pares_de_coerencia(rede, congelado, s0):
    """Independe do vetor. Devolve {nome: {wa, wb, d, sd_dif, sd_null_primario, sd_null_wa}} (pesos levados as 255 linhas)."""
    C = rede["C"]
    n = C.shape[0]
    keep = s0["keep"]
    Wp = _pad255(s0["weights"][0], keep, n)
    Wl = _pad255(s0["weights"][1], keep, n)
    sdn = np.asarray(s0["sd_null"], float)
    pares = {"primario_vs_rede_completa": (Wp, np.asarray(congelado["weights"][0], float), float(sdn[0])),
             "cefeidas_livres_vs_primario": (Wl, Wp, float(sdn[1]))}
    for a in s0.get("anchor_names", []):
        pares["ancora_%s_vs_primario" % a] = (_pad255(s0["weights_" + a][0], s0["keep_" + a], n), Wp, float(np.asarray(s0["sd_null_" + a])[0]))
    for a, b in itertools.combinations(list(s0.get("anchor_names", [])), 2):
        pares["ancora_%s_vs_%s" % (a, b)] = (_pad255(s0["weights_" + a][0], s0["keep_" + a], n), _pad255(s0["weights_" + b][0], s0["keep_" + b], n),
                                             float(np.asarray(s0["sd_null_" + a])[0]))
    out = {}
    for nome, (wa, wb, sd_wa) in pares.items():
        d = wa - wb
        sd_dif = float(np.sqrt(max(float(d @ C @ d), 0.0)))
        out[nome] = {"wa": wa, "wb": wb, "d": d, "sd_dif": sd_dif, "sd_null_primario": float(sdn[0]), "sd_null_wa": sd_wa}
    return out


def coerencia(y, pares):
    res = {}
    for nome, p in pares.items():
        dif = float(p["wa"] @ y - p["wb"] @ y)
        sd = p["sd_dif"]
        res[nome] = {"dif": dif, "sd_dif": sd, "z_dif": (dif / sd if sd >= 1e-15 else None),
                     "sd_dif_em_desvios_do_nulo": sd / p["sd_null_primario"],
                     "sd_dif_em_desvios_do_nulo_do_modelo_wa": sd / p["sd_null_wa"]}
    return res


# ------------------------------------------------------------------ decomposicao do desvio no nulo (so' relato)
def decomposicao(rede, s0, local0, support_l2):
    """Linhas tocadas pelo nulo (111), por hospedeira e por ancora: pesos, residuo nulo (componente de N0 N0' local0) e somas.
    Conferencias: soma r^2 = support_l2^2 (1e-10 rel); soma_g |a_g| = sum_abs_s_host; soma w^2 = sum_w2_touched (1e-12 rel).
    Falha = ValueError("integridade: decomposicao ...")."""
    keep = np.asarray(s0["keep"], int)
    touched = np.asarray(s0["touched"], int)
    N0, W = np.asarray(s0["null_basis"], float), np.asarray(s0["weights"], float)
    r_all = N0 @ (N0.T @ local0)
    names0 = [rede["row_names"][i] for i in keep]
    host_names = list(s0["host_names"])
    s_host = np.asarray(s0["s_host"], float)
    linhas = []
    for i in touched:
        m = _RE_TOC.match(names0[int(i)])
        linhas.append({"indice_s0": int(i), "indice_255": int(keep[int(i)]), "hospedeira": m.group(1), "ancora": m.group(2),
                       "peso_primario": float(W[0][int(i)]), "peso_cefeidas_livres": float(W[1][int(i)]), "residuo_nulo": float(r_all[int(i)])})
    por_h = {}
    for j, g in enumerate(host_names):
        ls = [l for l in linhas if l["hospedeira"] == g]
        por_h[g] = {"a_g_primario": float(s_host[0, j]), "a_g_cefeidas_livres": float(s_host[1, j]), "n_linhas_tocadas": len(ls),
                    "soma_w2_primario": float(sum(l["peso_primario"] ** 2 for l in ls)), "soma_r2": float(sum(l["residuo_nulo"] ** 2 for l in ls))}
    por_a = {}
    for a in ANCORAS:
        ls = [l for l in linhas if l["ancora"] == a]
        por_a[a] = {"n_linhas": len(ls), "soma_w2_primario": float(sum(l["peso_primario"] ** 2 for l in ls)),
                    "soma_r2": float(sum(l["residuo_nulo"] ** 2 for l in ls))}
    sr2 = float(sum(l["residuo_nulo"] ** 2 for l in linhas))
    l2sq = float(support_l2) ** 2
    sa_g = [float(sum(abs(v["a_g_primario"]) for v in por_h.values())), float(sum(abs(v["a_g_cefeidas_livres"]) for v in por_h.values()))]
    sa_st = np.asarray(s0["sum_abs_s_host"], float)
    sw2 = [float(sum(l["peso_primario"] ** 2 for l in linhas)), float(sum(l["peso_cefeidas_livres"] ** 2 for l in linhas))]
    s2_st = np.asarray(s0["sum_w2_touched"], float)
    conf = {"soma_r2": sr2, "support_l2_ao_quadrado": l2sq, "soma_r2_ok": bool(abs(sr2 - l2sq) <= 1e-10 * max(l2sq, 1e-30)),
            "soma_abs_a_g": sa_g, "sum_abs_s_host": sa_st.tolist(), "soma_abs_a_g_ok": bool(np.all(np.abs(np.array(sa_g) - sa_st) <= 1e-12 * np.maximum(sa_st, 1e-12))),
            "soma_w2": sw2, "sum_w2_touched": s2_st.tolist(), "soma_w2_ok": bool(np.all(np.abs(np.array(sw2) - s2_st) <= 1e-12 * s2_st))}
    for k in ("soma_r2_ok", "soma_abs_a_g_ok", "soma_w2_ok"):
        if not conf[k]:
            raise ValueError("integridade: decomposicao falhou em %s (%s)" % (k, json.dumps(conf)))
    return {"linhas_tocadas": linhas, "por_hospedeira": por_h, "por_ancora": por_a, "conferencias": conf}


# ------------------------------------------------------------------ a abertura
def abrir(y255, rede, congelado, s0, bg, alvos, ramos, emenda=None):
    """Devolve um dicionario. Se o portao 1 falhar: veredito = ramo (1); estatistica/coerencia/decomposicao/estresse = None.
    ValueError("integridade: ...") = fiacao nossa; ValueError("vetor: ...") = vetor mal formado: recusas duras, sem veredito.
    `emenda` (opcional) e' copiado para resultado["emenda"]."""
    integ = conferir_integridade(rede, congelado, s0, bg, ramos)
    _alvos_completos(alvos)
    A, C, h = rede["A"], rede["C"], int(rede["h_index"])
    if not (isinstance(y255, np.ndarray) and y255.dtype == np.float64 and y255.shape == (A.shape[0],) and bool(np.isfinite(y255).all())):
        raise ValueError("vetor: float64 (255,) finito exigido")
    y = y255
    H0_bg = float(bg["H0"])
    D_s0 = np.asarray(s0["D"], float)
    models = list(s0["model_names"])
    port = {"dims_finitos": True, "1b": None, "1c": None, "1d": None, "motivos": []}
    resultado = {"integridade": integ, "portao_1": port, "portao_1_ok": False, "estatistica": None, "veredito": None,
                 "linha_ao_lado_cefeidas_livres": None, "coerencia": None, "decomposicao": None, "estresse": None, "model_names": models,
                 "emenda": (json.loads(json.dumps(emenda)) if emenda is not None else None)}
    # ---- 1b: reproducao do numero local publicado (formulas da colaboracao, rede completa)
    nc = numeros_colaboracao(y, A, C, h)
    w0 = congelado["weights"][0]
    b1 = {"H0": nc["H0"], "sig": nc["sig"], "chi2": nc["chi2"], "ndof": nc["ndof"], "rank": nc["rank"], "logh": nc["logh"],
          "dif_H0": float(abs(nc["H0"] - alvos["H0"])), "dif_sig": float(abs(nc["sig"] - alvos["sig"])),
          "dif_chi2": float(abs(nc["chi2"] - alvos["chi2"])), "ndof_alvo": int(alvos["ndof"]),
          "dif_pesos_congelados_logh": None, "pesos_consistentes": None}
    b1["reproduz"] = bool(b1["dif_H0"] <= TOL_H0 and b1["dif_sig"] <= TOL_SIG and b1["dif_chi2"] <= TOL_CHI2 and nc["ndof"] == int(alvos["ndof"]))
    b1["ok"] = b1["reproduz"]
    port["1b"] = b1
    x_ref = np.zeros(A.shape[1])
    x_ref[h] = np.log10(H0_bg)
    local255 = y - A @ x_ref
    if b1["reproduz"]:
        # o vetor e' o esperado: as conferencias internas viram INTEGRIDADE (falha = nosso erro de fiacao)
        d_pesos = float(abs(w0 @ y - nc["logh"]))
        b1["dif_pesos_congelados_logh"] = d_pesos
        b1["pesos_consistentes"] = bool(d_pesos <= TOL_W)
        esperado_c = nc["logh"] - np.log10(H0_bg)
        c1 = {"w0_local": float(w0 @ local255), "esperado": float(esperado_c)}
        c1["dif"] = float(abs(c1["w0_local"] - esperado_c))
        c1["ok"] = bool(c1["dif"] <= TOL_W)
        port["1c"] = c1
        if not b1["pesos_consistentes"]:
            raise ValueError("integridade: pesos congelados nao reproduzem logh da colaboracao (dif %.3e > %.0e)" % (d_pesos, TOL_W))
        if not c1["ok"]:
            raise ValueError("integridade: identidade de centragem 1c falhou (dif %.3e > %.0e)" % (c1["dif"], TOL_W))
    else:
        port["motivos"].append("falhou_1b")
    # ---- 1d: impressao digital do vetor
    fp = impressao_digital(y, congelado["null_basis"])
    d1 = {"fp": fp, "alvo": float(alvos["fp"]), "dif": float(abs(fp - float(alvos["fp"])))}
    d1["ok"] = bool(d1["dif"] <= TOL_FP)
    port["1d"] = d1
    if not d1["ok"]:
        port["motivos"].append("falhou_1d")
    resultado["portao_1_ok"] = bool(b1["reproduz"] and d1["ok"])
    if not resultado["portao_1_ok"]:
        v = _ramo_vazio(D_s0[0], ramos)
        resultado["veredito"] = {"cabeca": v[0], "outcome": v[1], "ramo": v[2]}
        resultado["linha_ao_lado_cefeidas_livres"] = {"rotulo": "LINHA AO LADO, NAO E VEREDITO",
                                                      "cabeca": v[0], "outcome": v[1], "ramo": v[2]}
        return resultado
    # ---- estatistica primaria (S0)
    keep = np.asarray(s0["keep"], int)
    colmask = np.asarray(s0["colmask"], bool)
    A0 = A[keep][:, colmask]
    x_ref0 = np.zeros(A0.shape[1])
    x_ref0[int(s0["h_index_s0"])] = np.log10(H0_bg)
    local0 = y[keep] - A0 @ x_ref0
    if float(np.max(np.abs(local0 - local255[keep]))) > 1e-12:
        raise ValueError("integridade: local0 inconsistente com local255[keep]")
    est0 = _pack_estimator(s0)
    data = {"local": local0[None, :], "background": np.zeros((1, len(est0["gradient_h"])))}
    ev = evaluate(data, est0)
    t = np.asarray(ev["t"])[0]
    zn = np.asarray(ev["z_null"])[0]
    zt = np.asarray(ev["z_tgl"])[0]
    sup_l2 = float(np.asarray(ev["support_l2"])[0])
    resultado["estatistica"] = {"t": t.tolist(), "z_null": zn.tolist(), "z_tgl": zt.tolist(),
                                "support_max_abs": float(ev["support_max_abs"]), "support_l2": sup_l2,
                                "D_s0": D_s0.tolist()}
    # ---- veredito (modelo publicado, indice 0); Cefeidas livres (indice 1) como linha ao lado
    v0 = veredito_h0dn_v411(zn[0], zt[0], D_s0[0], True, ramos)
    resultado["veredito"] = {"modelo": models[0], "cabeca": v0[0], "outcome": v0[1], "ramo": v0[2]}
    if len(models) > 1:
        v1 = veredito_h0dn_v411(zn[1], zt[1], D_s0[1], True, ramos)
        resultado["linha_ao_lado_cefeidas_livres"] = {"rotulo": "LINHA AO LADO, NAO E VEREDITO", "modelo": models[1],
                                                      "cabeca": v1[0], "outcome": v1[1], "ramo": v1[2]}
    # ---- coerencia entre estimativas do mesmo h (SO' relatada; nao entra em portao nem em veredito)
    resultado["coerencia"] = coerencia(y, pares_de_coerencia(rede, congelado, s0))
    # ---- decomposicao do desvio no nulo (so' relato; conferencias internas = integridade)
    resultado["decomposicao"] = decomposicao(rede, s0, local0, sup_l2)
    # ---- estresses
    sd_null, sd_tgl, logK = np.asarray(s0["sd_null"], float), np.asarray(s0["sd_tgl"], float), float(s0["logK"])
    s2 = np.asarray(s0["sum_w2_touched"], float)
    bk = float(data["background"][0] @ est0["gradient_k"])
    # (i) ruido independente por linha nas linhas tocadas pelo nulo, com tau estimado do proprio vetor
    nnull = est0["null_basis"].shape[1]
    tau_hat = sup_l2 / np.sqrt(nnull) if nnull else 0.0
    sdp = np.sqrt(sd_null ** 2 + tau_hat ** 2 * s2)
    sdtp = np.sqrt(sd_tgl ** 2 + tau_hat ** 2 * s2)
    est_i = {"modelo": MODELO_ESTRESSE_I, "tau_hat": float(tau_hat), "sd_null_linha": sdp.tolist(), "z_null": (t / sdp).tolist(),
             "z_tgl": ((t - logK - bk) / sdtp).tolist(), "D": (logK / sdp).tolist()}
    # (ii) ancora unica
    est_ii = {"ancoras": {}, "dispersao_t": None}
    t_por_ancora = {}
    for a in s0.get("anchor_names", []):
        ea = _pack_estimator(s0, "_" + a)
        keep_a = np.asarray(s0["keep_" + a], int)
        eva = evaluate({"local": local255[keep_a][None, :], "background": data["background"]}, ea)
        ta = np.asarray(eva["t"])[0]
        t_por_ancora[a] = ta
        est_ii["ancoras"][a] = {"n_linhas": int(len(keep_a)), "t": ta.tolist(), "z_null": np.asarray(eva["z_null"])[0].tolist(),
                                "z_tgl": np.asarray(eva["z_tgl"])[0].tolist(), "D": np.asarray(s0["D_" + a], float).tolist(),
                                "support_l2": float(np.asarray(eva["support_l2"])[0])}
    for a in s0.get("anchors_refused", []):
        est_ii["ancoras"][a] = {"recusada": True}
    if t_por_ancora:
        T = np.stack(list(t_por_ancora.values()))
        est_ii["dispersao_t"] = (T.max(axis=0) - T.min(axis=0)).tolist()
    # (iii) vies de Cefeidas variando por hospedeira: pior caso b * sum|s_host|
    sum_abs = np.abs(np.asarray(s0["s_host"], float)).sum(axis=1)
    est_iii = {"formula": FORMULA_III}
    for b in TAUS_B:
        delta = b * sum_abs
        est_iii["b_%g" % b] = {"delta_t": delta.tolist(), "z_null_min": (zn - delta / sd_null).tolist(),
                               "z_null_max": (zn + delta / sd_null).tolist()}
    # dois numeros de DESENHO (nao dependem do vetor): vies comum que tira o modelo do portao de 90 % / que fabrica 5 sigma
    D90 = float(5 - norm.ppf(0.10))
    soma_a = np.asarray(s0["s_host"], float).sum(axis=1)
    est_iii["D90"] = D90
    est_iii["soma_g_a_g"] = soma_a.tolist()
    est_iii["vies_comum_que_tira_do_portao_90"] = [
        (float((logK - D90 * sd_null[i]) / abs(soma_a[i])) if (D_s0[i] > D90 and abs(soma_a[i]) >= 1e-12) else None) for i in range(len(sd_null))]
    est_iii["vies_comum_que_fabrica_5_sigma"] = [
        (float(5 * sd_null[i] / abs(soma_a[i])) if abs(soma_a[i]) >= 1e-12 else None) for i in range(len(sd_null))]
    resultado["estresse"] = {"i_tau_por_linha": est_i, "ii_ancora_unica": est_ii, "iii_vies_por_hospedeira": est_iii}
    return resultado
