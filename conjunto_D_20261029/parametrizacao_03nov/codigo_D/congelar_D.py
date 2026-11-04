# -*- coding: utf-8 -*-
"""congelar_D.py -- O ATO DE CONGELAMENTO: gera JOBS_D_V1.json (criacao EXCLUSIVA) e CONGELAMENTO_D.json (sha256 de tudo: pinos, jobs, cada job, arvore de codigo, copias RO,
diff das pecas derivadas, V1, compromisso da semente), ANTES de qualquer PE. O guarda (load_jobs) so executa job que esteja neste arquivo e cujo sha256 confira.

OPCAO (c): F4.1 (1 analise sintetica so-RG, SNR 14, com o amostrador congelado) + 10 analises CEGAS de D ate o estagio cego + as 10 repeticoes D5 PRE-REGISTRADAS
(maxcall x 2, nova semente do amostrador; so rodam se a primaria terminar sem convergir, decididas por bandeira de convergencia, nunca por dtau220). Nao ha injecoes C2 na opcao (c).
D2 (escrito ANTES): nlive 512, walks 50, dlogz 0,1, ESS >= 100, maxcall 16 000 000 e parede 40 h por analise (24 workers; vazao medida no piloto da GW250114: ~220-250 chamadas/s, e ~180 no mini-ensaio de 4 workers escalado
=> 16 M chamadas ~ 18-25 h; margem para 2 analises em paralelo disputando os 48 nucleos); repeticao: 32 M chamadas e 80 h. A F4.1 usa EXATAMENTE o mesmo amostrador e o mesmo teto: se nao convergir ali, a fila nao lanca.
"""
import hashlib
import json
import sys
import time
from pathlib import Path

CODE = Path(__file__).resolve().parent
BASE = CODE.parent
sys.path.insert(0, str(CODE))
import gerar_jobs_D as J  # noqa: E402
import guard_D as G  # noqa: E402
import v1_ramo_b as V  # noqa: E402

PRIMARIO = {"nlive": 512, "walks": 50, "maxcall": 16_000_000, "workers": 24}
WALL_PRIMARIO_S = 40 * 3600
FATOR_REPETICAO = 2
WALL_REPETICAO_S = 80 * 3600
MINI = {"nlive": 64, "walks": 20, "maxcall": 15_000, "workers": 4}
WALL_MINI_S = 1800


def _sha_cfg(cfg):
    return hashlib.sha256(json.dumps(cfg, sort_keys=True, allow_nan=False).encode()).hexdigest()


def construir_jobs(reg):
    jobs = {}
    jobs.update([J.job_sintetico(reg, "F41_SMOKE_MINI", MINI, WALL_MINI_S)])
    jobs.update([J.job_sintetico(reg, "F41_SYN_GR", PRIMARIO, WALL_PRIMARIO_S)])
    for ev in reg["eventos_d10"]:
        nome, cfg = J.job_cego(reg, ev, PRIMARIO, WALL_PRIMARIO_S)
        jobs[nome] = cfg
        n2, c2 = J.job_repeticao(reg, nome, cfg, FATOR_REPETICAO, WALL_REPETICAO_S)
        jobs[n2] = c2
    return jobs


def congelar(opcao="c", ordem_fila=None):
    if G.JOBS.exists() or G.CONGELAMENTO.exists():
        raise FileExistsError("ja congelado: JOBS_D_V1.json/CONGELAMENTO_D.json existem (criacao exclusiva)")
    reg, dig = G.checked_registration(verificar_relogio=False)
    reg = dict(reg)
    reg["limites"] = {"wall_max_por_job_s": WALL_REPETICAO_S, "wall_max_calibracao_s": WALL_PRIMARIO_S}
    jobs = construir_jobs(reg)
    for nome, cfg in jobs.items():
        G.validate_job_D(reg, nome, cfg)
    J.validar_com_pe_runner(jobs)
    raw = (json.dumps(jobs, indent=2, allow_nan=False, ensure_ascii=False, sort_keys=True) + "\n").encode()
    with open(G.JOBS, "xb") as f:
        f.write(raw)
    h_jobs = hashlib.sha256(raw).hexdigest()
    pinos, _ = G.carregar_pinos()
    diff = BASE / "DIFF_PECAS_MECANICAS.txt"
    cong = {"schema": "CONGELAMENTO_D", "congelado_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "opcao": opcao,
            "pinos_sha256": dig, "jobs_sha256": h_jobs, "limites": reg["limites"],
            "jobs": {n: _sha_cfg(c) for n, c in sorted(jobs.items())},
            "amostrador_primario": PRIMARIO, "wall_primario_s": WALL_PRIMARIO_S, "amostrador_repeticao": dict(PRIMARIO, maxcall=PRIMARIO["maxcall"] * FATOR_REPETICAO),
            "wall_repeticao_s": WALL_REPETICAO_S, "amostrador_mini_smoke": MINI,
            "regra_D5": "uma repeticao (D_<evento>_R1, maxcall x 2, nova semente do amostrador) SO se a analise primaria terminar com status PARTIAL_* ou BUDGET_STOPPED_PARTIAL_NOT_POSTERIOR "
                        "(bandeiras de convergencia do PE; nunca pelo valor de dtau220); depois disso o evento falha e n < 10; os 4 holds e os 8 pendentes NAO sao promovidos",
            "ordem_fila": ordem_fila or list(reg["eventos_d10"]), "concorrencia": 2, "workers_por_job": PRIMARIO["workers"],
            "F41": {"job": "F41_SYN_GR", "criterio": "status CONVERGENCE_CRITERIA_MET_REQUIRES_INDEPENDENT_REVIEW (dlogz < 0,1; ESS >= 100; >= 1000 amostras; sem EDOM na regiao do posterior) dentro do teto; "
                                                      "se nao convergir a fila NAO lanca (parede medida); o estimador do ramo B nao e tocado"},
            "estagio_cego": "automatico ao fim da fila: grava so o hash dos posteriores e o poder REAL (estagio_cego/PODER_RAMO_B_ANTES_DE_ABRIR.json); a ABERTURA nao faz parte da fila",
            "v1_sha256": pinos["v1"]["json_sha256"], "semente_compromisso_sha256": pinos["semente"]["compromisso_sha256"],
            "codigo_sha256": pinos["codigo"], "copias_somente_leitura_sha256": pinos["copias_somente_leitura"],
            "diff_pecas_mecanicas_sha256": hashlib.sha256(diff.read_bytes()).hexdigest() if diff.exists() else None,
            "estatuto": "[DESENHO] D2 e a ordem da fila escritos ANTES de qualquer analise; NOT_FALSIFIED nunca e CONFIRMED; o gate nao se move"}
    rawc = (json.dumps(cong, indent=2, allow_nan=False, ensure_ascii=False, sort_keys=True) + "\n").encode()
    with open(G.CONGELAMENTO, "xb") as f:
        f.write(rawc)
    return cong, h_jobs, hashlib.sha256(rawc).hexdigest()


if __name__ == "__main__":
    c, hj, hc = congelar()
    print("JOBS_D_V1.json", hj)
    print("CONGELAMENTO_D.json", hc, "| jobs", len(c["jobs"]))
