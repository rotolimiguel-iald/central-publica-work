# -*- coding: utf-8 -*-
"""Revisor independente da INSTALACAO v406 - varredura de escopo (somente leitura).
(a) tudo que mudou em producao durante a janela de manutencao [20:18:00, 20:19:36] e' o plano + os 7 backups?
(b) o unico divergente do RUNTIME_BASELINE e' o manifesto que o plano troca?
(c) o meu proprio rastro: nenhum .pyc/arquivo novo criado por mim."""
import sys
sys.dont_write_bytecode = True
import json, os, time, hashlib
from pathlib import Path

W = Path("C:/IALD/Central de Patentes/work/iald_v406_20261103")
ROOT = Path("C:/IALD/projetos_pyhton/IALD")
OUT = W / "review/revisor_sonnet-app-v406-revisor-d"
t_ini = time.mktime((2026, 11, 3, 20, 18, 0, 0, 0, -1))
t_fim = time.mktime((2026, 11, 3, 20, 19, 37, 0, 0, -1))   # novo filho web criado 20:19:36.2
t_rev = os.stat(OUT / "d1_d4_result.json").st_mtime - 60   # inicio aproximado dos meus scripts (primeiro resultado menos 1 min)
PRUNE = {"unified_env", "node_modules", ".git", "__pycache__"}


def norm(p):
    return os.path.normcase(os.path.normpath(str(p)))


plan = json.loads((W / "install_plan.json").read_bytes())
dests = {norm(it["destination"]) for it in plan["files"]}
dep = json.loads((W / "deployment.json").read_bytes())
baks = {norm(v) for v in dep["backups"].values()}

janela_plano, janela_bak, janela_outros = 0, 0, []
pyc_novos, n_visitados = [], 0
deadline = time.time() + 150
truncado = False
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in PRUNE or d == "__pycache__"]
    for f in fn:
        n_visitados += 1
        full = os.path.join(dp, f)
        try:
            m = os.stat(full).st_mtime
        except OSError:
            continue
        nf = norm(full)
        if t_ini <= m <= t_fim:
            if nf in dests:
                janela_plano += 1
            elif nf in baks:
                janela_bak += 1
            else:
                janela_outros.append(full.replace("C:\\IALD\\projetos_pyhton\\IALD\\", ""))
        if f.endswith(".pyc") and m >= t_rev:
            pyc_novos.append(full.replace("C:\\IALD\\projetos_pyhton\\IALD\\", ""))
    # nao descer em __pycache__ para a varredura de janela, mas conferir pyc novos
    if time.time() > deadline:
        truncado = True
        break

# varredura dedicada de .pyc novos (pastas __pycache__ que a poda acima manteve)
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in ("unified_env", "node_modules", ".git")]
    if os.path.basename(dp) == "__pycache__":
        for f in fn:
            full = os.path.join(dp, f)
            try:
                if os.stat(full).st_mtime >= t_rev:
                    pyc_novos.append(full.replace("C:\\IALD\\projetos_pyhton\\IALD\\", ""))
            except OSError:
                pass
    if time.time() > deadline + 60:
        truncado = True
        break
pyc_novos = sorted(set(pyc_novos))

# (b) baseline: o unico divergente
rb = json.loads((W / "app/RUNTIME_BASELINE.json").read_bytes())["files"]
mf_entry = [e for e in rb if norm(e["path"]) == norm(ROOT / "iald_nucleo_fixo.json")]
plan_mf = [it for it in plan["files"] if norm(it["destination"]) == norm(ROOT / "iald_nucleo_fixo.json")][0]
h_now = hashlib.sha256((ROOT / "iald_nucleo_fixo.json").read_bytes()).hexdigest()
b = {"entradas_no_baseline_para_o_manifesto": len(mf_entry),
     "sha_no_baseline": mf_entry[0]["sha256"] if mf_entry else None,
     "baseline_do_plano": plan_mf["baseline"], "sha_novo_do_plano": plan_mf["sha256"], "sha_no_disco_agora": h_now,
     "baseline_do_RUNTIME_BASELINE_igual_baseline_do_plano": bool(mf_entry) and mf_entry[0]["sha256"] == plan_mf["baseline"],
     "disco_igual_ao_novo_do_plano": h_now == plan_mf["sha256"]}
bak_manifest = Path(dep["backups"][str(ROOT / "iald_nucleo_fixo.json").replace("/", "\\")]) if str(ROOT / "iald_nucleo_fixo.json").replace("/", "\\") in dep["backups"] else None
if bak_manifest:
    b["sha_backup_do_manifesto"] = hashlib.sha256(bak_manifest.read_bytes()).hexdigest()
    b["backup_igual_ao_sha_do_baseline"] = b["sha_backup_do_manifesto"] == mf_entry[0]["sha256"]
nonmf_baseline_ok = sum(1 for e in rb if norm(e["path"]) != norm(ROOT / "iald_nucleo_fixo.json") and
                        hashlib.sha256(Path(e["path"]).read_bytes()).hexdigest() == e["sha256"])
b["baseline_sem_o_manifesto_intactos"] = nonmf_baseline_ok
b["baseline_sem_o_manifesto_total"] = len(rb) - len(mf_entry)

res = {"janela": [time.strftime("%H:%M:%S", time.localtime(t_ini)), time.strftime("%H:%M:%S", time.localtime(t_fim))],
       "arquivos_visitados": n_visitados, "varredura_truncada_por_tempo": truncado,
       "mudados_na_janela_que_estao_no_plano": janela_plano, "mudados_na_janela_que_sao_os_backups_do_deployment": janela_bak,
       "mudados_na_janela_FORA_do_plano_e_dos_backups": janela_outros[:20], "n_fora": len(janela_outros),
       "pyc_novos_desde_o_inicio_da_minha_revisao": pyc_novos[:10], "n_pyc_novos": len(pyc_novos),
       "W_mobile_backups_existe": (W / "mobile_backups").exists(), "W_rollback_new_files_existe": (W / "rollback_new_files").exists(),
       "baseline_manifesto": b}
res["PASS"] = (janela_plano == 1773 and janela_bak == 7 and not janela_outros and not pyc_novos and not truncado
               and not res["W_mobile_backups_existe"] and not res["W_rollback_new_files_existe"]
               and b["baseline_do_RUNTIME_BASELINE_igual_baseline_do_plano"] and b["disco_igual_ao_novo_do_plano"]
               and b["baseline_sem_o_manifesto_intactos"] == b["baseline_sem_o_manifesto_total"] == 170)
(OUT / "scope_scan_result.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print("ESCOPO", "PASS" if res["PASS"] else "FAIL")
print(json.dumps(res, ensure_ascii=False, indent=1)[:3500])
