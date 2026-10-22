# -*- coding: utf-8 -*-
"""Registra no MAPA DE ROTAS os achados da auditoria de 28/09 que JÁ passaram pela verificação adversarial, lidos do diário do workflow.
Cada achado entra na rota do teste auditado, com o veredicto do verificador ao lado; os refutados também entram (para não voltarem).
Idempotente: guarda em ja_registrados.json os ids já gravados."""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\IALD\MAPA_DE_ROTAS")
import rotas  # noqa: E402

J = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\subagents\workflows\wf_58da7663-e79\journal.jsonl"
AQUI = os.path.dirname(os.path.abspath(__file__))
FEITOS = os.path.join(AQUI, "ja_registrados.json")
QUEM = "claude-code/central-de-patentes (gerência) sessão 6da8f00d — auditoria 28/09 (aferidor + verificador adversarial)"
feitos = set(json.load(open(FEITOS, encoding="utf-8"))) if os.path.exists(FEITOS) else set()

aud, ver = {}, {}
for l in open(J, encoding="utf-8"):
    try:
        e = json.loads(l)
    except Exception:
        continue
    if e.get("type") != "result":
        continue
    r = e.get("result") or e.get("value") or e.get("output")
    if isinstance(r, str):
        try:
            r = json.loads(r)
        except Exception:
            continue
    if not isinstance(r, dict):
        continue
    if "veredictos" in r:
        ver[r["familia"].split(" ")[0]] = r
    elif "achados" in r:
        aud[r["familia"]] = r

estado = rotas._estado(rotas._le())
seq_rota = {rid: e["historico"][0]["seq"] for rid, e in estado.items()}
regs, novos = [], []
for fam, v in ver.items():
    a = aud.get(fam)
    if not a:
        continue
    vv = {x["id"]: x for x in v["veredictos"]}
    for ach in a["achados"] + v.get("achados_novos", []):
        if ach["id"] in feitos:
            continue
        rid = ach["rota_id"] if ach["rota_id"] in estado else None
        if rid is None:
            print("rota inexistente no mapa, achado fica para mão:", ach["id"], ach["rota_id"])
            continue
        x = vv.get(ach["id"])
        vered = x["veredicto"] if x else ("ACHADO_DO_VERIFICADOR" if ach in v.get("achados_novos", []) else "SEM_VEREDICTO")
        sev = x["severidade_revista"] if x else ach["severidade"]
        txt = ("[%s · %s · verificador: %s, severidade revista %s] %s. Afirmação auditada: %s. Correção proposta: %s. Razão do verificador: %s" % (
            ach["id"], ach["classe"], vered, sev, ach["titulo"], ach["afirmacao_auditada"][:700], ach["correcao_proposta"][:1200],
            (x["razao"][:1400] if x else "achado novo do próprio verificador")))
        corrige = ach["classe"] in ("SOBREAFIRMACAO_DE_ESCOPO", "INCONSISTENCIA_TEORICA", "ERRO_TECNICO", "ERRO_ESTATISTICO")
        base = dict(rota_id=rid, estatuto="[REAL — auditoria 28/09; verificação adversarial: %s]" % vered, nota=txt[:5900])
        if vered in ("SUSTENTADO", "PARCIAL", "ACHADO_DO_VERIFICADOR") and sev in ("CRITICO", "ALTO", "MEDIO"):
            base["status"] = "EXAMINADA_COM_DEFEITO"
        if corrige and vered in ("SUSTENTADO", "PARCIAL", "ACHADO_DO_VERIFICADOR"):
            reg = dict(base, tipo="ERRATA", corrige=seq_rota[rid])
        else:
            reg = dict(base, tipo="ANOTACAO")
        regs.append(reg)
        novos.append(ach["id"])
if regs:
    out = rotas.registrar(regs, QUEM)
    feitos |= set(novos)
    b = json.dumps(sorted(feitos), ensure_ascii=False, indent=1).encode("utf-8")
    open(FEITOS + ".tmp", "wb").write(b)
    os.replace(FEITOS + ".tmp", FEITOS)
    print("registrados", len(regs), "| cabeça", out["cabeca"][:16], "| total", out["n_registros"])
else:
    print("nada novo para registrar")
print("famílias verificadas:", sorted(ver), "| auditadas:", sorted(aud))
