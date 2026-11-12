# -*- coding: utf-8 -*-
"""Prepara o estimador do desenho S0 (os 13 calibradores extras fora) e as tres linhas de ancora unica.
SO' desenho: rede (A, C, c), BG1 e README da colaboracao; NENHUM vetor observado e' aberto.
Saidas: artefatos/estimador_s0_v411.npz e artefatos/MANIFESTO_S0.json."""
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import scipy.linalg
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from estimator_v411 import geometry               # noqa: E402  (geometry identica a' congelada, conferida em T8)
from abertura_v411 import ler_alvos_readme        # noqa: E402

OUT = HERE.parent / "artefatos"
B = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov")
NETWORK = B / "network" / "network.npz"
FROZEN = B / "estimator_frozen.npz"
BG1 = B / "background" / "BG1.json"
EST_PY = B / "estimator.py"
PREP_PY = B / "prepare_estimator.py"
UP = B / "network" / "upstream" / "h0_constrainer"
README = UP / "README.md"
SOLVER = UP / "h0_constrainer" / "solver.py"
ANCHORS = ("N4258", "LMC", "MW")
TAUS = (0.02, 0.035, 0.05, 0.10)
D_ESPERADO = (6.710150598579, 5.191312010024)        # spec: conferencia, tolerancia 1e-9


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pin(p):
    b = Path(p).read_bytes()
    return {"path": str(Path(p).resolve()), "bytes": len(b), "sha256": sha(b)}


def main():
    OUT.mkdir(exist_ok=True)
    checks = []

    def chk(nome, valor, esperado, ok):
        checks.append({"nome": nome, "valor": valor, "esperado": esperado, "ok": bool(ok)})
        print(("OK   " if ok else "FALHA"), nome, valor, "|", esperado)

    b = json.loads(BG1.read_text(encoding="utf-8"))
    with np.load(NETWORK, allow_pickle=False) as d:
        A = d["A"].copy(); C = d["C"].copy(); c = d["c_cepheid"].copy(); h = int(d["h_index"])
        rows = [str(x) for x in d["row_names"]]; pars = [str(x) for x in d["param_names"]]
    nr = len(rows)
    gh = np.asarray(b["gradient_h"], float); gk = np.asarray(b["gradient_k"], float); cb = np.asarray(b["covariance"], float)
    if np.linalg.eigvalsh(cb).min() <= 0:
        raise ValueError("BG covariance not positive definite")
    vb = float(gh @ cb @ gh); vbt = float((gh + gk) @ cb @ (gh + gk)); logK = float(b["logK"]); H0 = float(b["H0"])

    # ---- 1. as 13 linhas fora
    sn = [i for i, r in enumerate(rows) if r.startswith("SNe Ia equation")]
    fora = sn[42:]
    chk("n_linhas_SN", len(sn), 55, len(sn) == 55)
    chk("n_linhas_retiradas", len(fora), 13, len(fora) == 13)
    fora_set = set(fora)
    keep = np.array([i for i in range(nr) if i not in fora_set], dtype=int)
    colmask = np.abs(A[keep]).sum(axis=0) > 0
    assert colmask[h]
    h0 = int(np.sum(colmask[:h]))
    A0 = A[keep][:, colmask]; C0 = C[np.ix_(keep, keep)]; c0 = c[keep]; rows0 = [rows[i] for i in keep]
    pars0 = [p for p, m in zip(pars, colmask) if m]
    chk("linhas_S0", int(len(keep)), 242, len(keep) == 242)
    chk("h_index_S0 aponta log_10(H0)", pars0[h0], "log_10(H0)", pars0[h0] == "log_10(H0)")

    # ---- 2. geometria congelada sobre S0
    res, meta, null = geometry(A0, C0, c0, h0)
    models = list(res)
    W = np.stack([res[m]["influence"] for m in models])
    vs = np.array([res[m]["variance_h"] for m in models])
    sd_null = np.sqrt(vs + vb); sd_tgl = np.sqrt(vs + vbt)
    D = logK / sd_null
    Cp, posto = scipy.linalg.pinv(C0, atol=1e-10, rtol=0.0, return_rank=True)
    chk("posto de C0 (pinv atol=1e-10)", int(posto), 170, posto == 170)
    chk("posto de C0 (geometry)", meta["cov_rank"], 170, meta["cov_rank"] == 170)
    chk("nulidade (geometry)", meta["cov_nullity"], 72, meta["cov_nullity"] == 72)
    chk("D modelo publicado", float(D[0]), D_ESPERADO[0], abs(D[0] - D_ESPERADO[0]) < 1e-9)
    chk("D Cefeidas livres", float(D[1]), D_ESPERADO[1], abs(D[1] - D_ESPERADO[1]) < 1e-9)
    # pesos vs formula da colaboracao
    dif_colab = []
    desenhos = [A0, np.column_stack([A0, c0])]
    for i, Dm in enumerate(desenhos):
        X = np.linalg.inv(Dm.T @ Cp @ Dm) @ Dm.T @ Cp
        dif_colab.append(float(np.max(np.abs(W[i] - X[h0]))))
    chk("max|pesos - colaboracao|", dif_colab, "< 1e-12", max(dif_colab) < 1e-12)
    wn = [float(np.max(np.abs(W[i] @ null))) for i in range(2)]
    chk("max|pesos @ nulo|", wn, "< 1e-12", max(wn) < 1e-12)
    ident = []
    for i, Dm in enumerate(desenhos):
        e = np.zeros(Dm.shape[1]); e[h0] = 1.0
        ident.append(float(np.max(np.abs(W[i] @ Dm - e))))
    chk("max|pesos @ desenho - e_h|", ident, "< 1e-9", max(ident) < 1e-9)
    # linhas tocadas pelo nulo
    nrm = np.linalg.norm(null, axis=1)
    touched = np.where(nrm > 1e-9)[0]
    chk("linhas tocadas pelo nulo", int(len(touched)), 111, len(touched) == 111)
    chk("tocadas sao ceph_hst&..&R22", True, True,
        all("ceph_hst&" in rows0[i] and rows0[i].endswith("&R22") for i in touched))
    s2 = np.array([float(np.sum(W[i][touched] ** 2)) for i in range(2)])

    # ---- 3. s_host: soma dos pesos nas linhas com c0 != 0, por hospedeira
    host_re = re.compile(r"^Host equation for (\S+)")
    hosp = {}
    n_c_nonzero = 0
    for j, r in enumerate(rows0):
        if c0[j] != 0:
            n_c_nonzero += 1
            m = host_re.match(r)
            if not m:
                raise ValueError("linha com c0 != 0 que nao e' 'Host equation for': " + r)
            hosp.setdefault(m.group(1), []).append(j)
    host_names = sorted(hosp)
    s_host = np.array([[float(sum(W[i][j] for j in hosp[hn])) for hn in host_names] for i in range(2)])
    sum_abs_s_host = np.abs(s_host).sum(axis=1)

    # ---- 4. D_tau e o tau do portao de 90 %
    D90 = float(5 - norm.ppf(0.10))
    D_tau = {("%g" % tau): [float(logK / np.sqrt(sd_null[i] ** 2 + tau ** 2 * s2[i])) for i in range(2)] for tau in TAUS}
    tau90 = [float(np.sqrt(((logK / D90) ** 2 - sd_null[i] ** 2) / s2[i])) if D[i] > D90 else None for i in range(2)]

    # ---- 5. linhas de ancora unica
    anc_tok = re.compile(r"ceph_hst&([^&]+)&R22$")
    tok_por_linha = {}
    for j, r in enumerate(rows0):
        m = anc_tok.search(r)
        if m:
            tok_por_linha[j] = m.group(1)
    toks = sorted(set(tok_por_linha.values()))
    chk("ancoras achadas nos nomes", toks, sorted(ANCHORS), toks == sorted(ANCHORS))
    anchor_out = {}
    anchor_arrays = {}
    anchors_ok, anchors_refused = [], []
    for a in ANCHORS:
        outras = [j for j, t in tok_por_linha.items() if t != a]
        keep_a_s0 = np.array([j for j in range(len(rows0)) if j not in set(outras)], dtype=int)
        chk("ancora %s: linhas retiradas" % a, len(outras), 74, len(outras) == 74)
        keep_a = keep[keep_a_s0]                                  # indices na rede de 255
        colmask_a = np.abs(A[keep_a]).sum(axis=0) > 0
        info = {"n_linhas": int(len(keep_a)), "n_colunas": int(colmask_a.sum()), "linhas_retiradas": int(len(outras))}
        try:
            Aa = A[keep_a][:, colmask_a]; Ca = C[np.ix_(keep_a, keep_a)]; ca = c[keep_a]
            ha = int(np.sum(colmask_a[:h])); assert colmask_a[h]
            ra, ma, na = geometry(Aa, Ca, ca, ha)
            Wa = np.stack([ra[m]["influence"] for m in ra])
            vsa = np.array([ra[m]["variance_h"] for m in ra])
            sd0a = np.sqrt(vsa + vb); sdta = np.sqrt(vsa + vbt)
            Da = logK / sd0a
            info.update({"refused": None, "cov_rank": ma["cov_rank"], "cov_nullity": ma["cov_nullity"], "D": Da.tolist(),
                         "sd_null": sd0a.tolist(), "sd_tgl": sdta.tolist(), "variance_h": vsa.tolist(),
                         "design_rank": [ra[m]["design_rank"] for m in ra],
                         "condition_design_whitened": [ra[m]["condition_design_whitened"] for m in ra],
                         "response_cepheid": [ra[m]["response_cepheid"] for m in ra]})
            anchor_arrays.update({"keep_" + a: keep_a, "colmask_" + a: colmask_a, "h_index_" + a: np.array(ha),
                                  "weights_" + a: Wa, "null_basis_" + a: na, "sd_null_" + a: sd0a, "sd_tgl_" + a: sdta, "D_" + a: Da})
            anchors_ok.append(a)
        except Exception as e:  # recusa da geometry() e' RESULTADO, nao se contorna
            info.update({"refused": "%s: %s" % (type(e).__name__, e)})
            anchors_refused.append(a)
        anchor_out[a] = info

    failed = [k for k in checks if not k["ok"]]
    if failed:
        print("CHECKS QUE FALHARAM:", [k["nome"] for k in failed])
        raise SystemExit("falha de conferencia; nada gravado")

    # ---- 6. gravacao
    npz_path = OUT / "estimador_s0_v411.npz"
    tmp = OUT / "estimador_s0_v411.tmp.npz"
    np.savez_compressed(tmp, keep=keep, colmask=colmask, h_index_s0=np.array(h0), weights=W, null_basis=null,
                        gradient_h=gh, gradient_k=gk, sd_null=sd_null, sd_tgl=sd_tgl, logK=np.array(logK), H0=np.array(H0),
                        model_names=np.asarray(models), D=D, touched=touched, sum_w2_touched=s2,
                        s_host=s_host, host_names=np.asarray(host_names), sum_abs_s_host=sum_abs_s_host,
                        row_names=np.asarray(rows0), param_names=np.asarray(pars0),
                        anchor_names=np.asarray(anchors_ok, dtype="<U8"), anchors_refused=np.asarray(anchors_refused, dtype="<U8"),
                        **anchor_arrays)
    tmp.replace(npz_path)

    alvos = ler_alvos_readme(README, sha(README.read_bytes()))
    chk_readme = {"ndof_readme": alvos["ndof"], "rank_C_menos_colunas_de_A_na_rede_completa": None}
    Cp255, rank255 = scipy.linalg.pinv(C, atol=1e-10, rtol=0.0, return_rank=True)
    chk_readme["rank_C_menos_colunas_de_A_na_rede_completa"] = int(rank255 - A.shape[1])
    manifest = {
        "titulo": "Estimador S0 da emenda v411 (SO' DESENHO; nenhum vetor observado)",
        "convencoes": {"keep, keep_<ancora>": "indices de linha na rede de 255 (ordem original)",
                       "colmask, colmask_<ancora>": "mascara booleana sobre as 64 colunas de A da rede de 255",
                       "h_index_s0, h_index_<ancora>": "indice da coluna log_10(H0) depois de retiradas as colunas nulas",
                       "touched": "indices de linha DENTRO do S0 (0..241) das 111 linhas tocadas pelo nulo",
                       "weights/null_basis/sd_null/sd_tgl/D": "ordem dos modelos = model_names (published_baseline, free_cepheid_host_differential_bias)",
                       "s_host": "soma dos pesos nas linhas com c0 != 0 por hospedeira (colunas = host_names); uma linha por modelo",
                       "ancora unica": "do S0 retiram-se as linhas ceph_hst&<outra>&R22 (74) e as colunas nulas; geometry() congelada decide"},
        "entradas": {k: pin(p) for k, p in (("network.npz", NETWORK), ("estimator_frozen.npz", FROZEN), ("BG1.json", BG1),
                                            ("estimator.py", EST_PY), ("prepare_estimator.py", PREP_PY),
                                            ("README.md (colaboracao)", README), ("solver.py (colaboracao)", SOLVER),
                                            ("estimator_v411.py", HERE / "estimator_v411.py"))},
        "saidas": {"estimador_s0_v411.npz": pin(npz_path)},
        "linhas_retiradas_13": [rows[i] for i in fora], "indices_retirados_na_rede_255": [int(i) for i in fora],
        "colunas_retiradas": [p for p, m in zip(pars, colmask) if not m], "n_colunas_S0": int(colmask.sum()),
        "h_index_s0": h0, "h_index_rede255": h,
        "desenho_S0": {"linhas": int(len(keep)), "posto_C0_pinv": int(posto), "posto_C0_geometry": meta["cov_rank"],
                       "nulidade": meta["cov_nullity"], "eig_min_positivo": meta["eig_min_positive"], "eig_max": meta["eig_max"],
                       "tolerancia_geometry": meta["tolerance"], "support_design_error": meta["support_design_error"],
                       "models": models, "variance_h": vs.tolist(), "variance_fundo_logH": vb, "variance_fundo_logHK": vbt,
                       "sd_null": sd_null.tolist(), "sd_tgl": sd_tgl.tolist(), "logK": logK, "H0_BG1": H0,
                       "D": D.tolist(), "poder_em_5sigma": [float(norm.sf(5 - x)) for x in D],
                       "design_rank": [res[m]["design_rank"] for m in models],
                       "condition_design_whitened": [res[m]["condition_design_whitened"] for m in models],
                       "resposta_vies_comum": [res[m]["response_cepheid"] for m in models],
                       "max_dif_pesos_vs_colaboracao": dif_colab, "max_pesos_vezes_nulo": wn, "max_pesos_vezes_desenho_menos_eh": ident,
                       "linhas_tocadas_pelo_nulo": int(len(touched)), "sum_w2_touched": s2.tolist(),
                       "D_portao_90": D90, "D_tau": D_tau, "tau_que_derruba_portao_90": tau90,
                       "n_hospedeiras_cefeidas": len(host_names), "n_linhas_c0_nao_nulas": n_c_nonzero,
                       "sum_abs_s_host": sum_abs_s_host.tolist(), "soma_s_host": s_host.sum(axis=1).tolist()},
        "ancora_unica": anchor_out,
        "base_da_colaboracao_README": {k: alvos[k] for k in ("H0", "sig", "chi2", "ndof", "linha", "sha256", "bytes")},
        "conferencia_ndof": chk_readme,
        "conferencias": checks,
    }
    mp = OUT / "MANIFESTO_S0.json"
    mp.write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"D": D.tolist(), "D_tau": D_tau, "tau90": tau90, "sum_abs_s_host": sum_abs_s_host.tolist(),
                      "ancoras": {a: {k: v for k, v in anchor_out[a].items() if k in ("refused", "D", "cov_nullity", "n_linhas")} for a in anchor_out},
                      "ndof": chk_readme}, indent=1))


if __name__ == "__main__":
    main()
