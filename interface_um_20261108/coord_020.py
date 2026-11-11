"""Track the direction handoff in the existing mission; the recipient owns implementation."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

base = Path(__file__).resolve().parent
reference = str(base / "SESSION_REFERENCE.json")
actor = {"kind": "agent", "id": "codex-interface-um"}
task = "direcao020"

def call(program, operation, **kwargs):
    data = dict(reference=reference, operation=operation, **kwargs)
    result = subprocess.run([sys.executable, "-B", "-X", "utf8", str(Path(r"C:\IALD\MEMORIA_IALD") / program)],
                            input=json.dumps(data).encode(), capture_output=True)
    reply = json.loads(result.stdout)
    if not reply.get("ok"):
        raise RuntimeError(reply)
    return reply["result"]

def mission(op, **kwargs):
    return call("mission_cli.py", op, **kwargs)

def pin(name):
    path = base / name
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}

def current():
    snap = mission("project", max_chars=200000)
    return dict(expected_revision=snap["receipt"]["revision"], projection_sha256=snap["projection_sha256"], actor=actor)

def lease():
    for row in reversed(mission("get")["q"]["records"]):
        node = row.get("meta", {}).get("iald_mission_state_v1", {}).get("tasks", {}).get(task, {})
        if node.get("lease"): return node["lease"]["id"]
    raise RuntimeError("missing lease")

if sys.argv[1] == "start":
    mission("extend", **current(), event_id="um-020-extend", reason="Nova direção visual e de distribuição pelo túnel.",
            requirements=[dict(id=task, criterion="Examinar a 019 e depositar a ordem de Luiz, com direção visual e aceite do produto.", depends_on=[])],
            sources=[pin("ADENDO_PROGRAMA_COMPLETO_020.txt")])
    mission("claim", **current(), event_id="um-020-claim", task_id=task, lease_seconds=43200)
    print("preflight:", mission("check", **current(), task_id=task, lease_id=lease())["ready"])
elif sys.argv[1] == "finish":
    name = "TUNEL/020_CODEX.md"
    evidence = [pin(name), pin("direcao/020-a-dobra.html")]
    print("preflight:", mission("check", **current(), task_id=task, lease_id=lease())["ready"])
    mission("submit", **current(), task_id=task, lease_id=lease(), event_id="um-020-submit", evidence=evidence,
            note="Ordem escrita no túnel, com seis quadros de direção. Implementação e aceite visual não presumidos.")
    memory = lambda op, **kw: call("session_memory.py", op, **kw)
    revision = memory("project", max_chars=200000)["receipt"]["revision"]
    records = []
    for name, kind, statute, message in [
        ("ADENDO_PROGRAMA_COMPLETO_020.txt", "decision", "INPUT", "Luiz pede direção ao Kimi pelo túnel; a inscrição, a torção, a leitura pelo ângulo e a distribuição ACOM estão no adendo integral."),
        ("TUNEL/020_CODEX.md", "fact", "REAL", "Ordem 020 depositada no túnel após exame do executável, do ZIP, das telas e dos recibos 016–019. Inclui prancha de direção; leitura pelo Kimi, nova implementação e aceite de Luiz não presumidos.")]:
        src = pin(name)
        records.append(dict(id="um-020-"+kind, kind=kind, statute=statute, text=message,
                            sources=[dict(kind="operator" if kind=="decision" else "artifact", ref=src["path"], sha256=src["sha256"])]))
    saved = memory("transition", expected_revision=revision, actor=actor, event_id="um-020-direction",
                   changes=dict(records=records,flow=dict(phase="Direção 020 disponível no túnel",next_action="Kimi devolve o corte comparativo e os recibos; Luiz avalia a legibilidade do novo plano.")))
    print("memory:", memory("project", max_chars=200000)["receipt"]["revision"], "verify:", memory("verify"))
