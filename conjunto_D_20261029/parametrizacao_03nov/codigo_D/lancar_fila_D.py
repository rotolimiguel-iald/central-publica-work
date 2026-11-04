# -*- coding: utf-8 -*-
"""lancar_fila_D.py -- LANCADOR DE FILA do conjunto D (WSL/posix). Roda jobs do JOBS_D_V1.json congelado, ate N em paralelo (cada um via run_controlled_D.py, que e o UNICO
caminho aceito pelo guarda), com a REGRA D5: uma repeticao por evento (D_<evento>_R1, pre-registrada no congelamento: maxcall x 2, nova semente do amostrador) SO se a
analise primaria terminar com bandeira de convergencia negativa (status PARTIAL_* ou BUDGET_STOPPED_PARTIAL_NOT_POSTERIOR); nunca pelo valor de dtau220 -- este modulo NAO le
nenhum posterior: so CONTROLLER.json, ANALYST_STATUS.json e PRIVATE_CONVERGENCE.json (estatisticas de convergencia, sem deformacao).
Estado atomico em fila/ESTADO_FILA_D.json (consultavel por consultar_fila_D.py); log por job em fila/logs/<job>.log (so a saida do controlador).
"""
import json
import os
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

CODE = Path(__file__).resolve().parent
BASE = CODE.parent
sys.path.insert(0, str(CODE))
import guard_D as G  # noqa: E402

FILA = BASE / "fila"
LOGS = FILA / "logs"
ESTADO = FILA / "ESTADO_FILA_D.json"
RUN = CODE / "run_controlled_D.py"
_LOCK = threading.Lock()
REPETIVEIS_PREFIXO = ("PARTIAL_",)
REPETIVEIS_EXATOS = ("BUDGET_STOPPED_PARTIAL_NOT_POSTERIOR",)


def agora():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def carregar_estado():
    if ESTADO.exists():
        return json.loads(ESTADO.read_text(encoding="utf-8"))
    return {"criado_utc": agora(), "fase": "NOVO", "jobs": {}}


def gravar_estado(estado):
    with _LOCK:
        estado["atualizado_utc"] = agora()
        FILA.mkdir(parents=True, exist_ok=True)
        for tentativa in range(10):                      # outra thread pode estar mutando o dicionario durante a serializacao
            try:
                raw = json.dumps(estado, indent=1, ensure_ascii=False, sort_keys=True)
                break
            except RuntimeError:
                time.sleep(0.05)
        else:
            raise RuntimeError("nao foi possivel serializar o estado da fila")
        tmp = ESTADO.with_name(ESTADO.name + ".tmp")
        tmp.write_text(raw, encoding="utf-8")
        tmp.replace(ESTADO)


def _json(p):
    return json.loads(Path(p).read_text(encoding="utf-8")) if Path(p).exists() else None


def info_job(nome):
    """Resumo de convergencia/custo de um job. NUNCA le posterior, ANALYST_OUTPUT nem PRIVATE.log."""
    out = G.output_path(nome)
    ctl, st, conv = _json(out / "CONTROLLER.json"), _json(out / "ANALYST_STATUS.json"), _json(out / "PRIVATE_CONVERGENCE.json")
    info = {"existe": out.exists(), "controlador": ctl is not None, "status_controlador": ctl.get("status") if ctl else None,
            "returncode": ctl.get("returncode") if ctl else None, "wall_s": ctl.get("wall_seconds") if ctl else None,
            "cpu_s": (ctl["children_user_cpu_seconds"] + ctl["children_system_cpu_seconds"]) if ctl else None,
            "falhou": (out / "FAILURE.json").exists(), "status_pe": (conv or st or {}).get("status")}
    if conv:
        info.update(aceito=conv.get("accepted_for_analysis"), ncall=conv.get("ncall"), delta_logz=conv.get("delta_logz"), ess=conv.get("ess"),
                    posterior_samples=conv.get("posterior_samples"))
    else:
        info["aceito"] = False if st else None
    return info


def aceito(info):
    return bool(info.get("aceito")) and info.get("status_controlador") == "CHILD_COMPLETED_REQUIRES_REVIEW"


def deve_repetir(info):
    """D5: decide SO por bandeira de convergencia."""
    s1, s2 = info.get("status_controlador") or "", info.get("status_pe") or ""
    if aceito(info):
        return False
    return s1 in REPETIVEIS_EXATOS or s1.startswith(REPETIVEIS_PREFIXO) or s2.startswith(REPETIVEIS_PREFIXO)


def executar_job(nome, estado):
    LOGS.mkdir(parents=True, exist_ok=True)
    out = G.output_path(nome)
    reg = estado["jobs"].setdefault(nome, {})
    if out.exists():
        reg.update(estado="JA_EXISTIA_NAO_REEXECUTADO", **{k: v for k, v in info_job(nome).items() if v is not None})
        gravar_estado(estado)
        return info_job(nome)
    reg.update(estado="EM_CURSO", inicio_utc=agora())
    gravar_estado(estado)
    with open(LOGS / (nome + ".log"), "ab") as log:
        rc = subprocess.run([sys.executable, "-B", str(RUN), "--job", nome], stdout=log, stderr=subprocess.STDOUT, cwd=str(CODE)).returncode
    info = info_job(nome)
    reg.update(estado="CONCLUIDO" if info["controlador"] else "FALHOU_SEM_CONTROLADOR", fim_utc=agora(), rc_lancador=rc, **{k: v for k, v in info.items() if v is not None})
    gravar_estado(estado)
    return info


def rodar_com_d5(nomes, estado, concorrencia=2, existe_repeticao=lambda n: True):
    """Roda `nomes` com ate `concorrencia` em paralelo; cada primaria que nao convergir dispara SUA repeticao `<nome>_R1` na mesma vaga. Devolve {evento_job: info_final}."""
    fila = list(nomes)
    finais = {}
    trava = threading.Lock()

    def trabalhador():
        while True:
            with trava:
                if not fila:
                    return
                nome = fila.pop(0)
            info = executar_job(nome, estado)
            final, usado = info, nome
            if deve_repetir(info) and not nome.endswith("_R1") and existe_repeticao(nome + "_R1"):
                estado["jobs"][nome]["repetir_D5"] = "sim: " + (info.get("status_controlador") or "") + " / " + (info.get("status_pe") or "")
                gravar_estado(estado)
                final, usado = executar_job(nome + "_R1", estado), nome + "_R1"
            with trava:
                finais[nome] = {"job_usado": usado, "info": final, "aceito": aceito(final)}

    ths = [threading.Thread(target=trabalhador, daemon=False) for _ in range(concorrencia)]
    for t in ths:
        t.start()
    for t in ths:
        t.join()
    return finais


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", nargs="+", required=True)
    ap.add_argument("--concorrencia", type=int, default=1)
    a = ap.parse_args()
    assert os.name == "posix"
    reg, dig = G.checked_registration()
    jobs = G.load_jobs(reg, dig)
    for n in a.jobs:
        if n not in jobs:
            raise SystemExit("job fora do congelamento: " + n)
    estado = carregar_estado()
    finais = rodar_com_d5(a.jobs, estado, a.concorrencia, existe_repeticao=lambda n: n in jobs)
    print(json.dumps({n: {"job_usado": v["job_usado"], "aceito": v["aceito"], "status": v["info"].get("status_controlador"), "status_pe": v["info"].get("status_pe")} for n, v in finais.items()}))


if __name__ == "__main__":
    main()
