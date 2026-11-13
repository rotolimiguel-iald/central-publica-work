# -*- coding: utf-8 -*-
"""Conferência independente de DESENHO e AGREGADOS da ordem H0DN-05.

Não importa nem executa código do pacote v411, não usa sementes, não abre y_obs,
não chama abertura/evaluate/solver e não calcula qualquer quantidade observada.
Lê somente matrizes de desenho, agregados públicos e hashes. Escreve apenas neste diretório.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy
from scipy import linalg

BASE = Path(r"C:\IALD\Central de Patentes\work")
PACOTE = BASE / "h0dn_bg1_v411_emenda_11nov"
ORIGEM = BASE / "astra_bell_fock_tt_05nov" / "h0dn_bg1_06nov"
DESTINO = BASE / "h0dn_bg1_v410_09nov" / "kimi" / "ordem05"
ORDEM = BASE / "h0dn_bg1_v410_09nov" / "ORDEM_KIMI_H0DN_05_11nov.md"
REDE = ORIGEM / "network" / "network.npz"
BG1 = ORIGEM / "background" / "BG1.json"
CONGELADO = ORIGEM / "estimator_frozen.npz"
README = ORIGEM / "network" / "upstream" / "h0_constrainer" / "README.md"
S0 = PACOTE / "artefatos" / "estimador_s0_v411.npz"
AGREGADOS = PACOTE / "artefatos" / "ESPERADO_PELOS_AGREGADOS.json"
MANIFESTO = PACOTE / "artefatos" / "MANIFESTO_S0.json"
PINOS = PACOTE / "artefatos" / "PINOS.json"
RELATORIO = DESTINO / "VERIFICACAO_PESOS_AGREGADOS.json"

HASH_ESPERADO = {
    S0: "6cc9a23c4aa7b9ffe4d925273d044ac007d3646506bc5d3d80160e1ee839a617",
    AGREGADOS: "47302eec3c17752dc3e54dca1f5a28c26abe1d7eb250c6fd33cd167fbc62b872",
    PINOS: "cad7160ee22b18d6a05a714192fe88215d2903b076d1799bbf5c1786be424f18",
}
TOL_PESOS = 1.0e-12
TOL_DERIVADOS = 1.0e-12
TOL_AGREGADOS_ATOL = 1.0e-12
TOL_AGREGADOS_RTOL = 1.0e-10
ANCHOR_NAMES = ("N4258", "LMC", "MW")
MODEL_NAMES = ("published_baseline", "free_cepheid_host_differential_bias")


def pin(path: Path) -> dict:
    raw = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def carregar_npz(path: Path, chaves: tuple[str, ...]) -> dict[str, np.ndarray]:
    """Abre apenas as chaves explicitamente listadas; nunca usa pickle."""
    with np.load(path, allow_pickle=False) as z:
        ausentes = [k for k in chaves if k not in z.files]
        if ausentes:
            raise KeyError(f"{path}: chaves ausentes: {ausentes}")
        return {k: z[k].copy() for k in chaves}


def max_abs(a: np.ndarray, b: np.ndarray) -> tuple[float | None, list[int] | None]:
    if a.shape != b.shape:
        return None, None
    if a.size == 0:
        return 0.0, []
    delta = np.abs(np.asarray(a, dtype=float) - np.asarray(b, dtype=float))
    pos = np.unravel_index(int(np.argmax(delta)), delta.shape)
    return float(delta[pos]), [int(x) for x in pos]


def comparar_array(registros: list[dict], desenho: str, chave: str,
                   calculado: np.ndarray, armazenado: np.ndarray,
                   tolerancia: float, exato: bool = False) -> None:
    calculado = np.asarray(calculado)
    armazenado = np.asarray(armazenado)
    mesma_forma = calculado.shape == armazenado.shape
    if exato:
        igual = bool(mesma_forma and np.array_equal(calculado, armazenado))
    else:
        igual = False
    delta, pos = max_abs(calculado, armazenado) if (mesma_forma and np.issubdtype(calculado.dtype, np.number)) else (None, None)
    if not exato:
        igual = bool(delta is not None and np.isfinite(delta) and delta <= tolerancia)
    registros.append({
        "desenho": desenho,
        "chave_npz": chave,
        "forma_calculada": list(calculado.shape),
        "forma_armazenada": list(armazenado.shape),
        "diferenca_maxima_absoluta": delta,
        "indice_da_diferenca_maxima": pos,
        "tolerancia_absoluta": 0.0 if exato else tolerancia,
        "comparacao_exata": exato,
        "ok": igual,
    })


def calcular_desenho(A: np.ndarray, C: np.ndarray, c: np.ndarray, h: int,
                     gh: np.ndarray, gk: np.ndarray, cov_bg: np.ndarray,
                     logK: float) -> dict:
    """GLS por autovetores de C e SVD dos dois desenhos branqueados."""
    A = np.asarray(A, dtype=float)
    C = np.asarray(C, dtype=float)
    c = np.asarray(c, dtype=float)
    n = A.shape[0]
    if C.shape != (n, n) or c.shape != (n,):
        raise ValueError("Forma incompatível entre A, C e c")
    assimetria = float(np.max(np.abs(C - C.T)))
    if assimetria > 1.0e-12 * max(1.0, float(np.max(np.abs(C)))):
        raise ValueError("Covariância assimétrica")
    valores, U = linalg.eigh((C + C.T) / 2.0)
    tol_posto = 64.0 * np.finfo(float).eps * n * float(valores[-1])
    if float(valores[0]) < -tol_posto:
        raise ValueError("Covariância não PSD")
    suporte = valores > tol_posto
    if not suporte.any() or float(valores[suporte].min()) < 100.0 * tol_posto:
        raise ValueError("Posto vazio ou ambíguo")
    nulo = U[:, ~suporte]
    ext = np.column_stack((A, c))
    erro_suporte = float(np.linalg.norm(nulo.T @ ext) / max(1.0, np.linalg.norm(ext)))
    if erro_suporte > 1.0e-10:
        raise ValueError("Desenho fora do suporte")
    branqueador = U[:, suporte].T / np.sqrt(valores[suporte])[:, None]
    pesos = []
    variancas = []
    erros_identidade = []
    postos = []
    condicoes = []
    respostas_c = []
    for design in (A, ext):
        design_w = branqueador @ design
        Ua, sing, Vat = linalg.svd(design_w, full_matrices=False)
        limite_svd = max(design_w.shape) * np.finfo(float).eps * float(sing[0]) * 64.0
        if float(sing[-1]) <= limite_svd:
            raise ValueError("Desenho não identificado")
        inversa_w = (Vat.T / sing) @ Ua.T
        influencia = inversa_w[h] @ branqueador
        esperado = np.zeros(design.shape[1])
        esperado[h] = 1.0
        erro_identidade = float(np.max(np.abs(influencia @ design - esperado)))
        if erro_identidade > 1.0e-9:
            raise ValueError("Falha de não viesamento dos pesos")
        pesos.append(influencia)
        variancas.append(float(influencia @ C @ influencia))
        erros_identidade.append(erro_identidade)
        postos.append(int(len(sing)))
        condicoes.append(float(sing[0] / sing[-1]))
        respostas_c.append(float(influencia @ c))
    W = np.stack(pesos)
    var_h = np.asarray(variancas)
    var_bg_h = float(gh @ cov_bg @ gh)
    var_bg_hk = float((gh + gk) @ cov_bg @ (gh + gk))
    sd_null = np.sqrt(var_h + var_bg_h)
    sd_tgl = np.sqrt(var_h + var_bg_hk)
    return {
        "weights": W,
        "variance_h": var_h,
        "sd_null": sd_null,
        "sd_tgl": sd_tgl,
        "D": logK / sd_null,
        "null_basis": nulo,
        "cov_rank": int(suporte.sum()),
        "cov_nullity": int((~suporte).sum()),
        "rank_tolerance": float(tol_posto),
        "support_design_error": erro_suporte,
        "identity_errors": erros_identidade,
        "design_rank": postos,
        "condition_design_whitened": condicoes,
        "response_cepheid": respostas_c,
        "covariance_asymmetry": assimetria,
        "variance_fundo_logH": var_bg_h,
        "variance_fundo_logHK": var_bg_hk,
    }


def selecionar_colunas(A: np.ndarray, C: np.ndarray, c: np.ndarray,
                       keep: np.ndarray, h_rede: int) -> tuple:
    mascara = np.abs(A[keep]).sum(axis=0) > 0
    if not mascara[h_rede]:
        raise ValueError("Coluna H0 removida")
    h = int(np.sum(mascara[:h_rede]))
    return (A[keep][:, mascara], C[np.ix_(keep, keep)], c[keep], mascara, h)


def normal_sf(x: float) -> float:
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def comparar_json(recalculado, original, caminho: str, registros: list[dict]) -> None:
    if isinstance(original, dict) or isinstance(recalculado, dict):
        if not isinstance(original, dict) or not isinstance(recalculado, dict):
            registros.append({"caminho_json": caminho, "ok": False, "erro": "tipo diferente"})
            return
        chaves = sorted(set(original) | set(recalculado))
        for chave in chaves:
            p = f"{caminho}/{chave}"
            if chave not in original or chave not in recalculado:
                registros.append({"caminho_json": p, "ok": False, "erro": "chave ausente"})
            else:
                comparar_json(recalculado[chave], original[chave], p, registros)
        return
    if isinstance(original, list) or isinstance(recalculado, list):
        if not isinstance(original, list) or not isinstance(recalculado, list) or len(original) != len(recalculado):
            registros.append({"caminho_json": caminho, "ok": False, "erro": "lista ou comprimento diferente"})
            return
        for i, (novo, velho) in enumerate(zip(recalculado, original)):
            comparar_json(novo, velho, f"{caminho}/{i}", registros)
        return
    if isinstance(original, bool) or isinstance(recalculado, bool) or original is None or recalculado is None:
        registros.append({"caminho_json": caminho, "original": original, "recalculado": recalculado,
                          "ok": bool(type(original) is type(recalculado) and original == recalculado)})
        return
    if isinstance(original, (int, float)) and isinstance(recalculado, (int, float)):
        if isinstance(original, int) and isinstance(recalculado, int):
            registros.append({"caminho_json": caminho, "original": original, "recalculado": recalculado,
                              "diferenca_absoluta": abs(recalculado - original),
                              "tolerancia_absoluta": 0.0, "ok": bool(recalculado == original)})
            return
        diferenca = abs(float(recalculado) - float(original))
        tolerancia = max(TOL_AGREGADOS_ATOL, TOL_AGREGADOS_RTOL * abs(float(original)))
        registros.append({"caminho_json": caminho, "original": float(original), "recalculado": float(recalculado),
                          "diferenca_absoluta": diferenca, "tolerancia_absoluta": tolerancia,
                          "tolerancia_relativa": TOL_AGREGADOS_RTOL,
                          "ok": bool(math.isfinite(diferenca) and diferenca <= tolerancia)})
        return
    registros.append({"caminho_json": caminho, "original": original, "recalculado": recalculado,
                      "ok": bool(type(original) is type(recalculado) and original == recalculado)})


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    entradas_pin = {str(p): pin(p) for p in (
        ORDEM, REDE, BG1, CONGELADO, README, S0, AGREGADOS, MANIFESTO, PINOS,
        PACOTE / "codigo" / "preparar_estimador_s0.py",
        PACOTE / "codigo" / "esperado_pelos_agregados.py",
        PACOTE / "codigo" / "estimator_v411.py",
        Path(__file__),
    )}
    hashes_obrigatorios = []
    for path, esperado in HASH_ESPERADO.items():
        atual = entradas_pin[str(path)]["sha256"]
        hashes_obrigatorios.append({"path": str(path), "sha256_esperado": esperado,
                                    "sha256_atual": atual, "ok": atual == esperado})

    pinos_doc = json.loads(PINOS.read_text(encoding="utf-8"))
    pinos_pacote = []
    for relativo, esperado in sorted(pinos_doc["arquivos"].items()):
        path = PACOTE / relativo
        atual = pin(path)
        ok = atual["bytes"] == esperado["bytes"] and atual["sha256"] == esperado["sha256"]
        pinos_pacote.append({"arquivo": relativo, "bytes_esperados": esperado["bytes"],
                             "bytes_atuais": atual["bytes"], "sha256_esperado": esperado["sha256"],
                             "sha256_atual": atual["sha256"], "ok": ok})

    rede = carregar_npz(REDE, ("A", "C", "c_cepheid", "h_index", "row_names", "param_names"))
    A = np.asarray(rede["A"], dtype=float)
    C = np.asarray(rede["C"], dtype=float)
    c = np.asarray(rede["c_cepheid"], dtype=float)
    h_rede = int(rede["h_index"])
    rows = [str(x) for x in rede["row_names"]]
    params = [str(x) for x in rede["param_names"]]
    bg = json.loads(BG1.read_text(encoding="utf-8"))
    gh = np.asarray(bg["gradient_h"], dtype=float)
    gk = np.asarray(bg["gradient_k"], dtype=float)
    cov_bg = np.asarray(bg["covariance"], dtype=float)
    logK = float(bg["logK"])
    H0_bg = float(bg["H0"])
    sig_bg = float(bg["sigma_H0"])

    comparacoes: list[dict] = []
    completo = calcular_desenho(A, C, c, h_rede, gh, gk, cov_bg, logK)
    congelado = carregar_npz(CONGELADO, ("weights", "sd_null", "sd_tgl"))
    for chave in ("weights", "sd_null", "sd_tgl"):
        comparar_array(comparacoes, "rede_completa_255_vs_estimator_frozen", chave,
                       completo[chave], congelado[chave], TOL_DERIVADOS)

    sn = [i for i, nome in enumerate(rows) if nome.startswith("SNe Ia equation")]
    retiradas = sn[42:]
    set_retiradas = set(retiradas)
    keep = np.asarray([i for i in range(len(rows)) if i not in set_retiradas], dtype=int)
    A0, C0, c0, colmask, h0 = selecionar_colunas(A, C, c, keep, h_rede)
    primario = calcular_desenho(A0, C0, c0, h0, gh, gk, cov_bg, logK)
    primario.update({"keep": keep, "colmask": colmask, "h_index": h0})

    chaves_s0 = ["keep", "colmask", "h_index_s0", "weights", "sd_null", "sd_tgl", "D",
                 "touched", "sum_w2_touched", "s_host", "host_names", "sum_abs_s_host",
                 "row_names", "param_names", "model_names", "anchor_names", "gradient_h", "gradient_k",
                 "logK", "H0"]
    for a in ANCHOR_NAMES:
        chaves_s0 += [f"keep_{a}", f"colmask_{a}", f"h_index_{a}", f"weights_{a}",
                      f"null_basis_{a}", f"sd_null_{a}", f"sd_tgl_{a}", f"D_{a}"]
    s0 = carregar_npz(S0, tuple(chaves_s0))
    comparar_array(comparacoes, "S0_242", "keep", keep, s0["keep"], 0.0, exato=True)
    comparar_array(comparacoes, "S0_242", "colmask", colmask, s0["colmask"], 0.0, exato=True)
    comparar_array(comparacoes, "S0_242", "h_index_s0", np.asarray(h0), s0["h_index_s0"], 0.0, exato=True)
    for chave in ("weights", "sd_null", "sd_tgl", "D"):
        comparar_array(comparacoes, "S0_242", chave, primario[chave], s0[chave], TOL_DERIVADOS)

    touched = np.where(np.linalg.norm(primario["null_basis"], axis=1) > 1.0e-9)[0]
    sum_w2 = np.asarray([np.sum(primario["weights"][i][touched] ** 2) for i in range(2)])
    comparar_array(comparacoes, "S0_242", "touched", touched, s0["touched"], 0.0, exato=True)
    comparar_array(comparacoes, "S0_242", "sum_w2_touched", sum_w2, s0["sum_w2_touched"], TOL_DERIVADOS)
    host_re = re.compile(r"^Host equation for (\S+)")
    hosts: dict[str, list[int]] = {}
    rows0 = [rows[i] for i in keep]
    for j, nome in enumerate(rows0):
        if c0[j] != 0:
            match = host_re.match(nome)
            if not match:
                raise ValueError(f"Linha com c != 0 sem hospedeira: {nome}")
            hosts.setdefault(match.group(1), []).append(j)
    host_names = sorted(hosts)
    s_host = np.asarray([[sum(primario["weights"][i][j] for j in hosts[host]) for host in host_names]
                         for i in range(2)])
    comparar_array(comparacoes, "S0_242", "s_host", s_host, s0["s_host"], TOL_DERIVADOS)
    comparar_array(comparacoes, "S0_242", "sum_abs_s_host", np.abs(s_host).sum(axis=1),
                   s0["sum_abs_s_host"], TOL_DERIVADOS)
    for chave, calculado in (("row_names", np.asarray(rows0)),
                             ("param_names", np.asarray([p for p, m in zip(params, colmask) if m])),
                             ("model_names", np.asarray(MODEL_NAMES)),
                             ("host_names", np.asarray(host_names)),
                             ("anchor_names", np.asarray(ANCHOR_NAMES))):
        comparar_array(comparacoes, "S0_242", chave, calculado, s0[chave], 0.0, exato=True)
    comparar_array(comparacoes, "S0_242", "gradient_h", gh, s0["gradient_h"], 0.0, exato=True)
    comparar_array(comparacoes, "S0_242", "gradient_k", gk, s0["gradient_k"], 0.0, exato=True)
    comparar_array(comparacoes, "S0_242", "logK", np.asarray(logK), s0["logK"], 0.0, exato=True)
    comparar_array(comparacoes, "S0_242", "H0", np.asarray(H0_bg), s0["H0"], 0.0, exato=True)

    anc_tok = re.compile(r"ceph_hst&([^&]+)&R22$")
    token_linha = {}
    for j, nome in enumerate(rows0):
        match = anc_tok.search(nome)
        if match:
            token_linha[j] = match.group(1)
    if sorted(set(token_linha.values())) != sorted(ANCHOR_NAMES):
        raise ValueError("Âncoras inesperadas nos nomes das linhas")
    ancoras: dict[str, dict] = {}
    for anchor in ANCHOR_NAMES:
        outras = {j for j, token in token_linha.items() if token != anchor}
        keep_a_s0 = np.asarray([j for j in range(len(rows0)) if j not in outras], dtype=int)
        keep_a = keep[keep_a_s0]
        Aa, Ca, ca, colmask_a, ha = selecionar_colunas(A, C, c, keep_a, h_rede)
        calc = calcular_desenho(Aa, Ca, ca, ha, gh, gk, cov_bg, logK)
        calc.update({"keep": keep_a, "colmask": colmask_a, "h_index": ha})
        ancoras[anchor] = calc
        desenho = f"ancora_unica_{anchor}_168"
        comparar_array(comparacoes, desenho, f"keep_{anchor}", keep_a, s0[f"keep_{anchor}"], 0.0, exato=True)
        comparar_array(comparacoes, desenho, f"colmask_{anchor}", colmask_a, s0[f"colmask_{anchor}"], 0.0, exato=True)
        comparar_array(comparacoes, desenho, f"h_index_{anchor}", np.asarray(ha), s0[f"h_index_{anchor}"], 0.0, exato=True)
        for chave in ("weights", "sd_null", "sd_tgl", "D"):
            comparar_array(comparacoes, desenho, f"{chave}_{anchor}", calc[chave], s0[f"{chave}_{anchor}"], TOL_DERIVADOS)
        # Bases nulas podem girar; compara-se o projetor, que é invariante de base.
        projetor_calc = calc["null_basis"] @ calc["null_basis"].T
        projetor_npz = s0[f"null_basis_{anchor}"] @ s0[f"null_basis_{anchor}"].T
        comparar_array(comparacoes, desenho, f"projetor_de_null_basis_{anchor}",
                       projetor_calc, projetor_npz, TOL_DERIVADOS)

    readme_text = README.read_text(encoding="utf-8")
    match = re.search(r"H0=([0-9.]+)\+/-([0-9.]+) km/s/Mpc \| Chi-squared=([0-9.]+) \| ndof=([0-9]+)", readme_text)
    if not match:
        raise ValueError("Linha de agregados não encontrada no README")
    H0_pub, sig_pub = float(match.group(1)), float(match.group(2))
    t_pub = float(np.log10(H0_pub) - np.log10(H0_bg))

    def pad(w: np.ndarray, indices: np.ndarray) -> np.ndarray:
        saida = np.zeros(C.shape[0])
        saida[indices] = w
        return saida

    w_ref = completo["weights"][0]
    agregados_calc = {
        "o_que_e": "esperado pelos agregados publicos; NAO e' resultado do rito; nenhum vetor observado lido",
        "entradas": {"H0_publicado": H0_pub, "desvio_publicado": sig_pub, "H0_fundo": H0_bg,
                     "desvio_fundo": sig_bg, "logK": logK, "previsao_K_para_o_local": H0_bg * 10 ** logK},
        "pinos_das_entradas": {p.name: {"bytes": pin(p)["bytes"], "sha256": pin(p)["sha256"]}
                                for p in (README, BG1, REDE, CONGELADO, S0)},
        "t_dos_agregados": t_pub,
        "conta_linear": {"z_nulo": (H0_pub - H0_bg) / float(np.hypot(sig_pub, sig_bg)),
                         "z_K": (H0_pub - H0_bg * 10 ** logK) / float(np.hypot(sig_pub, sig_bg))},
        "rede_completa_255": {"z_nulo": t_pub / float(completo["sd_null"][0]),
                              "z_K": (t_pub - logK) / float(completo["sd_tgl"][0])},
        "linhas": {},
    }

    def linha_agregado(nome: str, w: np.ndarray, sd_n: float, sd_t: float) -> None:
        d = w - w_ref
        variancia_diferenca = float(d @ C @ d)
        sdd = math.sqrt(max(variancia_diferenca, 0.0))
        zc = t_pub / sd_n
        zk = (t_pub - logK) / sd_t
        s = sdd / sd_n
        agregados_calc["linhas"][nome] = {
            "desvio_da_diferenca_para_a_publicada_em_desvios_da_linha": s,
            "z_nulo_esperado": zc,
            "z_K_esperado": zk,
            "prob_z_nulo_ge_5_dado_o_publicado": normal_sf((5.0 - zc) / s) if s > 0 else float(zc >= 5.0),
            "sd_null": sd_n,
            "D": logK / sd_n,
        }

    linha_agregado("primario_publicado_13_fora", pad(primario["weights"][0], keep),
                   float(primario["sd_null"][0]), float(primario["sd_tgl"][0]))
    linha_agregado("cefeidas_livres_13_fora", pad(primario["weights"][1], keep),
                   float(primario["sd_null"][1]), float(primario["sd_tgl"][1]))
    for anchor in ANCHOR_NAMES:
        calc = ancoras[anchor]
        linha_agregado(f"ancora_unica_{anchor}_publicado", pad(calc["weights"][0], calc["keep"]),
                       float(calc["sd_null"][0]), float(calc["sd_tgl"][0]))

    agregados_original = json.loads(AGREGADOS.read_text(encoding="utf-8"))
    comparacoes_agregados: list[dict] = []
    comparar_json(agregados_calc, agregados_original, "", comparacoes_agregados)

    diagnosticos = {}
    for nome, calc in [("rede_completa_255", completo), ("S0_242", primario)] + [
            (f"ancora_unica_{a}_168", ancoras[a]) for a in ANCHOR_NAMES]:
        diagnosticos[nome] = {k: calc[k] for k in (
            "cov_rank", "cov_nullity", "rank_tolerance", "support_design_error", "identity_errors",
            "design_rank", "condition_design_whitened", "response_cepheid", "covariance_asymmetry",
            "variance_fundo_logH", "variance_fundo_logHK")}
        diagnosticos[nome]["variance_h"] = calc["variance_h"].tolist()

    falhas_arrays = [x for x in comparacoes if not x["ok"]]
    falhas_agregados = [x for x in comparacoes_agregados if not x["ok"]]
    falhas_hash = [x for x in hashes_obrigatorios if not x["ok"]]
    falhas_pinos = [x for x in pinos_pacote if not x["ok"]]
    pesos = [x for x in comparacoes if x["chave_npz"] == "weights" or x["chave_npz"].startswith("weights_")]
    resumo_pesos = [{
        "desenho": x["desenho"], "chave_npz": x["chave_npz"],
        "forma": x["forma_calculada"], "diferenca_maxima_absoluta": x["diferenca_maxima_absoluta"],
        "indice_da_diferenca_maxima": x["indice_da_diferenca_maxima"],
        "tolerancia_absoluta": x["tolerancia_absoluta"], "ok": x["ok"],
    } for x in pesos]
    divergencias = (falhas_arrays + falhas_agregados + falhas_hash + falhas_pinos)
    flags = {
        "hashes_obrigatorios_ok": not falhas_hash,
        "todos_os_19_pinos_do_pacote_ok": not falhas_pinos and len(pinos_pacote) == 19,
        "pesos_das_cinco_matrizes_ok": len(pesos) == 5 and all(x["ok"] for x in pesos),
        "todas_as_chaves_de_desenho_comparadas_ok": not falhas_arrays,
        "todos_os_campos_dos_agregados_ok": not falhas_agregados,
        "nenhuma_divergencia_fora_das_tolerancias": not divergencias,
    }
    relatorio = {
        "titulo": "Verificação independente de pesos de desenho e agregados — H0DN ordem 05",
        "data_utc": datetime.now(timezone.utc).isoformat(),
        "escopo": {
            "permitido": "Matrizes A/C/c, seleção de linhas, álgebra linear, agregados públicos e hashes.",
            "nao_executado": "Nenhuma abertura/evaluate/solver; nenhum y_obs; nenhuma estimativa, H0, razão ou Z observada; nenhuma semente; nenhuma revisão de pré-registro ou S1/S2/S4.",
            "escrita": str(RELATORIO),
            "codigo_do_pacote_importado_ou_executado": False,
        },
        "ambiente": {"numpy": np.__version__, "scipy": scipy.__version__},
        "metodo": {
            "pesos": "C=U diag(lambda) U^T; B=diag(lambda_+^-1/2) U_+^T; para D=A e D=[A,c], SVD de B D; w_h=e_h^T(BD)^+B.",
            "posto": "lambda > 64*eps*n*lambda_max, com verificação lambda_min_positivo >= 100*tolerância.",
            "desvios": "sd_null=sqrt(w C w + gh^T CovBG gh); sd_tgl=sqrt(w C w + (gh+gk)^T CovBG (gh+gk)).",
            "agregados": "Recalculados com os pesos independentes das redes de 255, 242 e três de 168 linhas; sobrevivência normal por erfc.",
            "tolerancias": {"pesos_abs": TOL_PESOS, "derivados_abs": TOL_DERIVADOS,
                            "agregados_atol": TOL_AGREGADOS_ATOL, "agregados_rtol": TOL_AGREGADOS_RTOL,
                            "indices_formas_textos_bytes_hashes": "exatos",
                            "base_nula": "comparação por projetor; tolerância absoluta 1e-12"},
        },
        "bandeiras": flags,
        "resultado_geral": "CONFORME" if flags["nenhuma_divergencia_fora_das_tolerancias"] else "DIVERGENCIA",
        "resumo_pesos_por_matriz_e_chave": resumo_pesos,
        "comparacoes_desenho_por_chave": comparacoes,
        "diagnosticos_algebricos_recalculados": diagnosticos,
        "agregados_recalculados": agregados_calc,
        "comparacoes_agregados_campo_a_campo": comparacoes_agregados,
        "divergencias_concretas_fora_das_tolerancias": divergencias,
        "contagens": {
            "comparacoes_desenho": len(comparacoes), "falhas_desenho": len(falhas_arrays),
            "comparacoes_agregados": len(comparacoes_agregados), "falhas_agregados": len(falhas_agregados),
            "pinos_pacote": len(pinos_pacote), "falhas_pinos_pacote": len(falhas_pinos),
            "divergencias_totais": len(divergencias),
        },
        "hashes_das_entradas_e_do_script": entradas_pin,
        "verificacao_dos_hashes_exigidos_na_ordem": hashes_obrigatorios,
        "verificacao_dos_19_arquivos_pinados": pinos_pacote,
        "selecao": {
            "linhas_rede": len(rows), "linhas_SN": len(sn), "ultimas_linhas_SN_retiradas": len(retiradas),
            "indices_retirados_na_rede_255": [int(i) for i in retiradas], "linhas_S0": len(keep),
            "linhas_por_ancora": {a: int(len(ancoras[a]["keep"])) for a in ANCHOR_NAMES},
        },
    }
    RELATORIO.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"relatorio": str(RELATORIO), "resultado_geral": relatorio["resultado_geral"],
                      "bandeiras": flags, "resumo_pesos": resumo_pesos,
                      "contagens": relatorio["contagens"],
                      "divergencias": divergencias}, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
