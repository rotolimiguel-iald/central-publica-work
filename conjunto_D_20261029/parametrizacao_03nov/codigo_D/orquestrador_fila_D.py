# -*- coding: utf-8 -*-
"""orquestrador_fila_D.py -- OPCAO (c) do conjunto D, sem supervisao (rodar no WSL com nohup/setsid):
  F4.1  1 analise SINTETICA so-RG (SNR tipico de D) com o amostrador CONGELADO -> F4_1_CONVERGENCIA.json (convergencia, Δlogz, ESS, chamadas, horas de parede, CPU)
        * nao convergiu dentro do teto => PARA (parede medida); a fila NAO lanca; o estimador do ramo B nao e tocado.
  FILA  as 10 analises CEGAS de D, 2 em paralelo (24 workers cada), regra D5 (lancar_fila_D) -- semente selada
  FIM   estagio cego (estagio_cego_fila_D): hash dos posteriores + poder REAL; a ABERTURA nao faz parte da fila (decisao do operador, com o poder na mao).
Este processo NAO le posterior de evento real; so estatisticas de convergencia/custo e, no F4.1 SINTETICO, o proprio posterior sintetico (nonblind).
"""
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

CODE = Path(__file__).resolve().parent
BASE = CODE.parent
sys.path.insert(0, str(CODE))
import estagio_cego_fila_D as EF  # noqa: E402
import guard_D as G  # noqa: E402
import lancar_fila_D as L  # noqa: E402

F41_JSON = BASE / "F4_1_CONVERGENCIA.json"
CRITERIO = "CONVERGENCE_CRITERIA_MET_REQUIRES_INDEPENDENT_REVIEW"


def avaliar_f41(nome="F41_SYN_GR"):
    info = L.info_job(nome)
    out = G.output_path(nome)
    conv = L._json(out / "PRIVATE_CONVERGENCE.json") or {}
    ctl = L._json(out / "CONTROLLER.json") or {}
    convergiu = bool(L.aceito(info)) and conv.get("status") == CRITERIO
    r = {"job": nome, "convergiu": convergiu, "status_pe": conv.get("status"), "status_controlador": ctl.get("status"),
         "delta_logz": conv.get("delta_logz"), "delta_logz_alvo": conv.get("threshold", 0.1), "ess": conv.get("ess"), "ess_minimo": conv.get("minimum_ess", 100),
         "ncall": conv.get("ncall"), "posterior_samples": conv.get("posterior_samples"), "log_evidence": conv.get("log_evidence"),
         "wall_s": ctl.get("wall_seconds"), "wall_h": (ctl["wall_seconds"] / 3600) if ctl.get("wall_seconds") else None,
         "cpu_h": ((ctl["children_user_cpu_seconds"] + ctl["children_system_cpu_seconds"]) / 3600) if ctl else None,
         "chamadas_por_s": (conv["ncall"] / ctl["wall_seconds"]) if conv.get("ncall") and ctl.get("wall_seconds") else None,
         "nucleos_efetivos_de_24": ((ctl["children_user_cpu_seconds"] + ctl["children_system_cpu_seconds"]) / ctl["wall_seconds"]) if ctl.get("wall_seconds") else None,
         "edom": (L._json(out / "EDOM_SUMMARY.json") or {}).get("status")}
    if convergiu:
        ao = L._json(out / "ANALYST_OUTPUT.json")            # SINTETICO e nonblind: leitura legitima
        x = np.asarray(ao["columns"]["dtau220"], dtype=float)
        q05, q50, q95 = np.quantile(x, [0.05, 0.5, 0.95])
        r["recuperacao_sintetica"] = {"verdade_dtau220": 0.0, "media": float(x.mean()), "sigma_ddof1": float(x.std(ddof=1)), "q05": float(q05), "q50": float(q50), "q95": float(q95),
                                      "verdade_dentro_de_q05_q95": bool(q05 <= 0.0 <= q95), "W90": float(q95 - q05), "W90_sobre_3p29_sobre_sigma": float((q95 - q05) / 3.29 / x.std(ddof=1)),
                                      "nota": "uma sintetica nao certifica cobertura (10 % cairia fora por acaso); aqui ela mede o sigma_tau tipico e a fiacao"}
        r["projecao_fila_D"] = {"analises_cegas": 10, "em_paralelo": 2, "parede_por_analise_h": r["wall_h"], "parede_total_h_sem_repeticao": r["wall_h"] * 5 if r["wall_h"] else None}
    else:
        r["parede_medida"] = ("a analise sintetica NAO convergiu dentro do teto congelado: parede medida; a fila de D NAO foi lancada; o estimador do ramo B nao foi tocado")
    return r


def main():
    assert os.name == "posix", "WSL"
    reg, dig = G.checked_registration()           # relogio aberto e pinos conferidos
    jobs = G.load_jobs(reg, dig)
    estado = L.carregar_estado()
    estado["pinos_sha256"] = dig
    # --- F4.1
    if not F41_JSON.exists():
        estado["fase"] = "F41_EM_CURSO"
        L.gravar_estado(estado)
        L.executar_job("F41_SYN_GR", estado)
        r = avaliar_f41()
        r["avaliado_utc"] = L.agora()
        F41_JSON.write_text(json.dumps(r, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    r = json.loads(F41_JSON.read_text(encoding="utf-8"))
    if not r["convergiu"]:
        estado["fase"] = "F41_NAO_CONVERGIU__PAREDE_MEDIDA__FILA_NAO_LANCADA"
        L.gravar_estado(estado)
        return
    # --- fila das 10 cegas
    estado["fase"] = "FILA_D_EM_CURSO"
    L.gravar_estado(estado)
    cegos = ["D_" + ev for ev in reg["eventos_d10"]]
    finais = L.rodar_com_d5(cegos, estado, concorrencia=2, existe_repeticao=lambda n: n in jobs)
    estado["resumo_fila"] = {n: {"job_usado": v["job_usado"], "aceito": v["aceito"]} for n, v in finais.items()}
    estado["fase"] = "FILA_CONCLUIDA__ESTAGIO_CEGO_EM_CURSO"
    L.gravar_estado(estado)
    # --- estagio cego (nunca a abertura)
    eg, h = EF.executar()
    estado["estagio_cego"] = {"arquivo": str(EF.DESTINO), "sha256": h, "eventos_aceitos": eg["n_eventos_convergidos"], "veredito_se_mantido": eg["veredito_se_mantido"],
                              "poder": eg.get("primario", {}).get("poder")}
    estado["fase"] = "ESTAGIO_CEGO_CONCLUIDO__ABERTURA_NAO_FEITA__AGUARDA_DECISAO_DO_OPERADOR"
    L.gravar_estado(estado)


if __name__ == "__main__":
    main()
