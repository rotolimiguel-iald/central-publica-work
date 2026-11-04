# -*- coding: utf-8 -*-
"""ensaio_pecas_wsl.py -- ENSAIO (WSL /opt/lal_env) das pecas mecanicas em AMBIENTE TEMPORARIO, 100 % SINTETICO e fora da configuracao oficial:
pinos/relogio/congelamento/saidas proprios em ~/.iald_privado/conjunto_D_20261029/ensaio_pecas/ ; semente de TESTE (descartavel); dados = os 2 arquivos sinteticos F4.1 copiados.
O redirecionamento dos processos filhos e feito por um sitecustomize.py que mora SO no diretorio do ensaio e e ativado SO por PYTHONPATH deste script -- o codigo
oficial (codigo_D) nao tem nenhuma porta de teste.  Cadeia exercitada: lancar_fila_D -> run_controlled_D -> pe_runner_D (job F41_SMOKE_MINI, amostrador minusculo, 4 workers):
guarda (pinos, relogio, congelamento, validate_job_D, validate_launch), controlador, injecao C2 pelo injetor original, PE (dynesty/bilby), convergencia, estado da fila,
consultar_fila_D, e a recusa do CLI direto. Nenhum dado real. Saida: ENSAIO_PECAS_saida.json."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = HERE / "codigo_D"
sys.path.insert(0, str(CODE))
import blinding_D as B  # noqa: E402
import congelar_D as CG  # noqa: E402
import gerar_pinos_D as GP  # noqa: E402
import guard_D as G  # noqa: E402
import lancar_fila_D as L  # noqa: E402

T0 = time.time()
E = Path(G.V.native("C:/Users/rotol/.iald_privado/conjunto_D_20261029/ensaio_pecas"))
if E.exists():
    raise SystemExit("ensaio anterior existe (nao sobrescrevo): " + str(E))
(E / "priv" / "sintetico").mkdir(parents=True)
(E / "shim").mkdir()
PRIV = E / "priv"
cfg = {"PINOS": str(E / "PINOS.json"), "RELOGIO": str(E / "RELOGIO.json"), "JOBS": str(E / "JOBS.json"), "CONGELAMENTO": str(E / "CONG.json"),
       "PRIV": str(PRIV), "SAIDAS": str(PRIV / "pe"), "FILA": str(E / "fila")}
(E / "ensaio_cfg.json").write_text(json.dumps(cfg))
(E / "shim" / "sitecustomize.py").write_text(
    "import json, os, sys\nfrom pathlib import Path\n"
    "c = json.load(open(os.environ['ENSAIO_D_CFG']))\n"
    "import guard_D as G\n"
    "G.PINOS, G.RELOGIO, G.JOBS, G.CONGELAMENTO = Path(c['PINOS']), Path(c['RELOGIO']), Path(c['JOBS']), Path(c['CONGELAMENTO'])\n"
    "G.PRIV, G.SAIDAS = Path(c['PRIV']), Path(c['SAIDAS'])\n")
(E / "shim" / "runner_lancador.py").write_text(
    "import json, os, sys\nfrom pathlib import Path\n"
    "c = json.load(open(os.environ['ENSAIO_D_CFG']))\n"
    "import lancar_fila_D as L\n"
    "L.FILA = Path(c['FILA']); L.LOGS = L.FILA / 'logs'; L.ESTADO = L.FILA / 'ESTADO_FILA_D.json'\n"
    "L.main()\n")
G.PINOS, G.RELOGIO, G.JOBS, G.CONGELAMENTO = Path(cfg["PINOS"]), Path(cfg["RELOGIO"]), Path(cfg["JOBS"]), Path(cfg["CONGELAMENTO"])
G.PRIV, G.SAIDAS = PRIV, Path(cfg["SAIDAS"])
G.SAIDAS.mkdir()
L.FILA = Path(cfg["FILA"]); L.LOGS = L.FILA / "logs"; L.ESTADO = L.FILA / "ESTADO_FILA_D.json"
seed = PRIV / "seed_teste.bin"
seed.write_bytes(os.urandom(32))
B.SEMENTE_PADRAO = str(seed)
man = json.loads((HERE / "SINTETICO_F41_MANIFESTO.json").read_text())
for det in ("H1", "L1"):
    src = Path(G.V.native(man["strain"][det]["hdf5"]))
    dst = PRIV / "sintetico" / src.name
    shutil.copyfile(src, dst)
    man["strain"][det]["hdf5"] = str(dst)
    assert hashlib.sha256(dst.read_bytes()).hexdigest() == man["strain"][det]["hdf5_sha256"]
(E / "MAN.json").write_text(json.dumps(man))
out = {"ambiente": str(E), "etapas": {}}
pinos, dig = GP.montar(destino=G.PINOS, sinteticos_manifesto=str(E / "MAN.json"), runtime_json=str(HERE / "runtime_wsl.json"))
ordem = E / "ordem.json"
ordem.write_text(json.dumps({"opcao": "c", "ordem_operador_sha256": "4" * 64, "decidido_utc": "2026-11-03T00:00:00Z"}))
G.abrir_relogio(1, ordem)
cong, hj, hc = CG.congelar()
out["etapas"]["pinos_relogio_congelamento"] = {"pinos_sha16": dig[:16], "jobs": len(cong["jobs"]), "congelamento_sha16": hc[:16]}
env = dict(os.environ, PYTHONPATH=str(E / "shim") + os.pathsep + str(CODE), ENSAIO_D_CFG=str(E / "ensaio_cfg.json"))
# (1) CLI direto do pe_runner_D e recusado
r = subprocess.run([sys.executable, "-B", str(CODE / "pe_runner_D.py"), "--job", "F41_SMOKE_MINI", "--launch-context", str(PRIV / "pe" / "x" / "LAUNCH_CONTEXT.json")], env=env, capture_output=True, text=True)
out["etapas"]["CLI_direto_pe_runner_D"] = {"returncode": r.returncode, "recusado": r.returncode != 0, "ultima_linha_stderr": (r.stderr.strip().splitlines() or [""])[-1][:140]}
# (2) lancador -> run_controlled_D -> pe_runner_D (job sintetico minusculo)
t = time.time()
r = subprocess.run([sys.executable, "-B", str(E / "shim" / "runner_lancador.py"), "--jobs", "F41_SMOKE_MINI", "--concorrencia", "1"], env=env, capture_output=True, text=True, cwd=str(CODE))
out["etapas"]["lancador"] = {"returncode": r.returncode, "s": round(time.time() - t, 1), "stdout": r.stdout.strip()[-400:], "stderr_fim": r.stderr.strip()[-300:]}
info = L.info_job("F41_SMOKE_MINI")
out["etapas"]["info_job"] = {k: info.get(k) for k in ("controlador", "status_controlador", "status_pe", "aceito", "ncall", "delta_logz", "ess", "wall_s", "cpu_s", "falhou", "returncode")}
d = G.output_path("F41_SMOKE_MINI")
out["etapas"]["arquivos_de_saida"] = sorted(p.name for p in d.iterdir()) if d.exists() else None
conv = json.loads((d / "PRIVATE_CONVERGENCE.json").read_text()) if (d / "PRIVATE_CONVERGENCE.json").exists() else None
if conv:
    out["etapas"]["custo_do_mini"] = {k: conv["cost"].get(k) for k in ("wall_seconds", "source_calls", "source_seconds_per_call", "sampler_ncall", "workers")}
    out["etapas"]["injecao_no_job"] = json.loads((d / "PRIVATE_INJECTION.json").read_text()) if (d / "PRIVATE_INJECTION.json").exists() else None
    if out["etapas"]["injecao_no_job"]:
        out["etapas"]["injecao_no_job"] = {k: out["etapas"]["injecao_no_job"].get(k) for k in ("status", "optimal_network_SNR")}
# (3) consultar_fila
r2 = subprocess.run([sys.executable, "-B", str(CODE / "consultar_fila_D.py"), "--json"], env=env, capture_output=True, text=True, cwd=str(CODE))
out["etapas"]["consultar_fila_D"] = {"returncode": r2.returncode, "contagem": (json.loads(r2.stdout)["contagem_por_estado"] if r2.returncode == 0 else r2.stderr[-200:])}
out["tempo_total_s"] = round(time.time() - T0, 1)
(HERE / "ENSAIO_PECAS_saida.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps(out, indent=1, ensure_ascii=False))
