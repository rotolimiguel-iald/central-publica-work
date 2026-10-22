"""Chama o CLI da memoria ACOM (protocolo da casa) com JSON construido em Python. Referencia PROPRIA desta tarefa (ESTRATEGIA A)."""
import json, subprocess, sys, uuid, hashlib, pathlib
OUT = pathlib.Path(r"C:\IALD\Central de Patentes\work\organismo_iald_12out\1_ESTRATEGIA_A")
MEM = OUT / "memoria"; MEM.mkdir(exist_ok=True)
CLI = [r"C:\Python314\python.exe", "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"]
REF = str(MEM / "REFERENCIA_SESSAO.json")
ORDEM = r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt"
ACTOR = {"id": "claude-c1-estrategista-A-prova-distintiva-12out", "kind": "agent"}
def run(req, name):
    (MEM / f"{name}_request.json").write_text(json.dumps(req, ensure_ascii=False, indent=1), encoding="utf-8")
    p = subprocess.run(CLI, input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
    out = p.stdout.decode("utf-8", "replace")
    (MEM / f"{name}_out.json").write_text(out, encoding="utf-8")
    print(name, "rc=", p.returncode); print(out[:1800])
    if p.stderr: print("STDERR:", p.stderr.decode("utf-8","replace")[:600])
    return p.returncode, out
op = sys.argv[1]
if op == "init":
    rid_file = MEM / "request_id.txt"
    rid = rid_file.read_text().strip().split("=")[-1] if rid_file.exists() else str(uuid.uuid4())
    rid_file.write_text("request_id=" + rid)
    sha = hashlib.sha256(open(ORDEM, "rb").read()).hexdigest()
    req = {"operation": "init", "objective_file": ORDEM, "objective_sha256": sha, "request_id": rid,
           "scope": {"house": "IALD", "principal": "operator"}, "actor": ACTOR,
           "constraints": {"escrita": str(OUT), "lente": "ESTRATEGIA A: o canal mais forte hoje (razao de Hubble, z_disc 4,28) a 5 sigma ou mostrar que nao chega",
                           "proibido": "quadro, mapa (registrar), memoria Claude/Atlas, tunel, Nos, kernel do Nos, Bancada, site, git; um.py nao roda; sem dado observado para veredito; sem provedor remoto; sem chamada paga; projecao so sintetica e condicional",
                           "beta": "ALPHA_FINE_CODATA_2018 (um.py l.5557) x sqrt(e) em runtime, nunca literal"},
           "write_reference": REF}
    run(req, "init")
elif op == "project":
    run({"operation": "project", "reference": REF, "max_chars": 24000}, "project_" + (sys.argv[2] if len(sys.argv) > 2 else "01"))
elif op == "transition":
    changes_file = sys.argv[2]; event_id = sys.argv[3]; expected_revision = int(sys.argv[4])
    raw = open(changes_file, "rb").read()
    run({"operation": "transition", "reference": REF, "changes_file": changes_file, "changes_sha256": hashlib.sha256(raw).hexdigest(),
         "expected_revision": expected_revision, "event_id": event_id, "actor": ACTOR}, "transition_" + event_id)
elif op == "verify":
    run({"operation": "verify", "reference": REF}, "verify")
