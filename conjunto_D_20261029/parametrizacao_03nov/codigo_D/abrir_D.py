# -*- coding: utf-8 -*-
"""abrir_D.py -- O ATO DE ABERTURA do conjunto D e o veredito. So roda com AUTORIZACAO_ABERTURA_D.json ligada ao sha256 do estagio cego REAL, do estimador,
da funcao de veredito e dos pinos; abre UMA vez (trava exclusiva ABERTURA_D.lock); confere que sigma_i desvelado == sigma_i do estagio cego; roda o estimador
do V1 uma vez e grava RESULTADO_RAMO_B_V1.json (criacao exclusiva). Nenhum desfecho move o gate; NOT_FALSIFIED nunca e CONFIRMED.
"""
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import blinding_D as B
import estimador_ramo_b_v1 as E
import v1_ramo_b as V
import veredito_ramo_b as VR

GATES_OBRIGATORIOS = ("F41_instrumento_qualificado", "dez_de_dez_convergidas", "C1", "C2_rodado", "C5")
C2_LEITURA = "estatistico"      # E6: 'estatistico' (padrao do desenho) ou 'literal'


class AberturaError(RuntimeError):
    pass


def _sha_bytes(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def verificar_autorizacao(auth_path, arquivos, pinos_digest):
    """arquivos: {'poder': path, 'estimador': path, 'veredito': path}. Cada sha256 da autorizacao deve bater com o do arquivo no disco."""
    a = V.strict_json(Path(auth_path).read_bytes())
    for campo in ("poder_sha256", "estimador_sha256", "veredito_sha256", "pinos_sha256", "ordem_operador_sha256", "autorizado_utc", "gates"):
        if campo not in a:
            raise AberturaError("autorizacao sem o campo " + campo)
    for chave, campo in (("poder", "poder_sha256"), ("estimador", "estimador_sha256"), ("veredito", "veredito_sha256")):
        if _sha_bytes(arquivos[chave]) != a[campo]:
            raise AberturaError("a autorizacao nao esta ligada ao arquivo atual: " + chave)
    if a["pinos_sha256"] != pinos_digest:
        raise AberturaError("autorizacao ligada a outros pinos")
    faltam = [g for g in GATES_OBRIGATORIOS if a["gates"].get(g) is not True]
    if faltam:
        raise AberturaError("gates nao satisfeitos: " + ",".join(faltam))
    return a


def c2_para_pontos(c2_saidas):
    """c2_saidas: lista de {evento, classe ('GR'|'RB'), verdade, samples (dtau220 recuperado, nao deslocado: C2 e calibracao), }.
    Devolve {'GR': [...], 'RB': [...]} no formato de ajustar_vies/avaliar_c2."""
    out = {"GR": [], "RB": []}
    for r in c2_saidas:
        x = np.asarray(r["samples"], dtype=float)
        q05, q95 = np.quantile(x, [0.05, 0.95])
        out[r["classe"]].append({"evento": r["evento"], "sigma": float(np.std(x, ddof=1)), "vies": float(np.mean(x) - r["verdade"]),
                                 "sigma_vies": float(np.std(x, ddof=1)), "coberto": bool(q05 <= r["verdade"] <= q95)})
    return out


def abrir(auth_path, arquivos, pinos_digest, reg, saidas_cegas, estagio_cego, c2_saidas, saida_dir, estimador_selado=True, c2_leitura=C2_LEITURA):
    saida_dir = Path(saida_dir)
    auth = verificar_autorizacao(auth_path, arquivos, pinos_digest)
    lock = saida_dir / "ABERTURA_D.lock"
    with open(lock, "x") as f:                 # abertura UNICA: falha se ja existir
        f.write(datetime.now(timezone.utc).isoformat() + "\n")
    v1, _ = V.carregar_v1()
    CR = V.criterios_fase6()
    k = V.constantes_um_py()
    eventos, amostras = [], {}
    for ev, s in sorted(saidas_cegas.items()):
        raw = B.unblind_samples({"blinded_dtau220": s["columns"]["blinded_dtau220"]}, ev, reg)["dtau220"]
        sig = float(np.std(raw, ddof=1))
        cego = estagio_cego["por_evento"][ev]
        if abs(sig - cego["sigma"]) > 1e-9 * cego["sigma"]:
            raise AberturaError("sigma_i desvelado difere do estagio cego: " + ev)
        eventos.append({"evento": ev, "delta_hat": float(np.mean(raw)), "delta_hat_mediana": float(np.median(raw)), "sigma": sig,
                        "w90": float(np.diff(np.quantile(raw, [0.05, 0.95]))[0]), "delta_pred": cego["delta_pred"]})
        amostras[ev] = raw
    pts = c2_para_pontos(c2_saidas)
    fit_RG = E.ajustar_vies(pts["GR"]) if len(pts["GR"]) >= 2 else None
    fit_B = E.ajustar_vies(pts["RB"]) if len(pts["RB"]) >= 2 else None
    est = E.estimar(eventos, sigma_sys=estagio_cego["sigma_sys_primario"], fit_RG=fit_RG, fit_B=fit_B, amostras=amostras)
    tol = 0.2 * abs(est["delta_pred_ponderado"])
    c2 = E.avaliar_c2(pts, tol)
    chave = "status_estatistico" if c2_leitura == "estatistico" else "status_literal"
    c2_status = "NOT_RUN" if any(v.get("status") == "NOT_RUN" for v in c2.values()) else ("PASS" if all(v[chave] == "PASS" for v in c2.values()) else "FAIL")
    ctr = dict(estagio_cego["controles_avaliaveis_no_estagio_cego"])
    ctr["C9"] = "PASS" if (ctr.pop("C9_gaussianidade_conjunto") == "PASS" and 0.9 <= est["razao_gaussianidade_W90_sobre_std"] <= 1.1) else "FAIL"
    ctr["C2"] = c2_status
    ctr["C6"] = "PASS" if (fit_RG is not None and fit_B is not None) else "NOT_RUN"
    ent = {"n_eventos": len(eventos), "estimador_selado": estimador_selado, "dado_aberto": True, "controles": ctr,
           "sist_rel": estagio_cego["sigma_sys_primario"] / abs(est["delta_pred_ponderado"]), "chi2_dof": est["chi2_dof"],
           "kde_discordancias": est["kde_discordancias"], "poder": est["poder"], "z_excl": est["z_excl"], "z_RG": est["z_RG"]}
    tok, desfecho, razoes = VR.veredito(ent, CR)
    resultado = {"token": tok, "desfecho": desfecho, "razoes": razoes, "entrada_do_veredito": ent, "estimador": est, "c2": c2,
                 "ajuste_vies": {"RG": fit_RG, "B": fit_B}, "escolhas": {"c2_leitura": c2_leitura}, "autorizacao": auth,
                 "beta_runtime": k["beta"], "aberto_utc": datetime.now(timezone.utc).isoformat(),
                 "nota": "NOT_FALSIFIED nunca e CONFIRMED; FALSIFIED falsifica o PAR (k, M_X, identificacao), nunca a lei, beta ou a TGL; o gate nao se move."}
    raw = (json.dumps(resultado, indent=2, allow_nan=False, ensure_ascii=False, sort_keys=True) + "\n").encode()
    with open(saida_dir / "RESULTADO_RAMO_B_V1.json", "xb") as f:
        f.write(raw)
    return resultado, hashlib.sha256(raw).hexdigest()
