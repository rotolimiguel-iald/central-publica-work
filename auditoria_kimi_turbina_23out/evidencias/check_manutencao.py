"""Read-only verification of the 21/10 maintenance (PROGRAMA.json title, Nos Vivo reindex), the Bancada ledger claim (seq 1302),
fold markers in the production queue DB, the state of the three Kimi jobs, and the 'EXATAMENTE o que a casa escreveu' header claim.
Every SQLite open is mode=ro&immutable=1; every file is only read."""
import difflib
import hashlib
import json
import re
import sqlite3
from pathlib import Path


def ro(p):
    return sqlite3.connect(Path(p).resolve().as_uri() + "?mode=ro&immutable=1", uri=True)


print("=== 1. PROGRAMA.json: Kimi byte backup vs the next system backup (state right after his edit)")
B = Path(r"C:\IALD\PROGRAMA_IALD")
a = (B / "PROGRAMA.json.bak_20261021_kimi_titulo_f99").read_bytes()
b = (B / "PROGRAMA.json.bak_20261021_101233_avanc").read_bytes()
ta, tb = a.decode("utf-8"), b.decode("utf-8")
d = [l for l in difflib.unified_diff(ta.splitlines(), tb.splitlines(), "antes", "depois", n=0, lineterm="")]
print("bytes:", len(a), "->", len(b), "| differing lines:", [l for l in d if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))])
ja, jb = json.loads(ta), json.loads(tb)
ua = {u["id"]: u for u in ja["unidades"]}
ub = {u["id"]: u for u in jb["unidades"]}
print("units:", len(ua), len(ub), "| units that differ:", [i for i in ua if ua[i] != ub.get(i)], "| other top-level keys differ:", [k for k in ja if k != "unidades" and ja[k] != jb.get(k)])
rd = (B / "README.md").read_text(encoding="utf-8")
m = re.search(r"\| `PROGRAMA\.json`[^\n]*", rd)
print("README rule:", m.group(0)[:200] if m else None)
n_ev = 0
for ln in (B / "eventos.jsonl").read_text(encoding="utf-8").splitlines():
    if ln.strip() and '"2026-10-21T09:4' in ln:
        n_ev += 1
print("board events (eventos.jsonl) stamped 2026-10-21T09:4x:", n_ev)

print("\n=== 2. Nos Vivo backups of 21/10")
for name in ("nos_vivo.sqlite3.bak_20261021_093151", "nos_vivo.sqlite3.bak_20261021_094237"):
    p = Path(r"C:\IALD\NOS_VIVO") / name
    db = ro(p)
    meta = dict(db.execute("select chave,valor from meta"))
    n = db.execute("select count(*) from nos").fetchone()[0]
    e = db.execute("select count(*) from arestas").fetchone()[0]
    s = db.execute("select count(*) from nos where sha256 is not null and sha256<>''").fetchone()[0]
    c = db.execute("select count(*) from nos where caminho is not null and caminho<>''").fetchone()[0]
    r_ = db.execute("select count(*) from nos where tipo='rota'").fetchone()[0]
    u = db.execute("select titulo from nos where id='unidade:F9.9.TURBINA_20261020'").fetchone()
    ok = db.execute("pragma integrity_check").fetchone()[0]
    print(name, "| bytes", p.stat().st_size, "| gerado_em", meta.get("gerado_em"), "| nos", n, "| arestas", e, "| sha256 nativo", s, "(%.1f%%)" % (100 * s / n),
          "| caminho", c, "| rotas", r_, "| unidade F9.9 no grafo:", bool(u), "| integrity", ok)

print("\n=== 3. Bancada Um ledger (seq 1302 says the observation was recorded)")
db = ro(r"C:\IALD\Bancada_Um\estado\livro.sqlite3")
print("rows", db.execute("select count(*) from consultas").fetchone()[0], "| last ts", db.execute("select max(ts) from consultas").fetchone()[0],
      "| rows from client like kimi:", db.execute("select count(*) from consultas where lower(cliente) like '%kimi%'").fetchone()[0],
      "| rows after 2026-10-20:", db.execute("select count(*) from consultas where ts>='2026-10-20'").fetchone()[0])

print("\n=== 4. Production queue DB: was the fold ever executed? (receipts) and the three Kimi jobs")
S = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\state")
blob = (S / "tasks.sqlite3").read_bytes()
for pat in (b'"folded": true', b'"folded":true', b'INDEX_ONLY_NO_PASSAGES', b'fold_notice'):
    print(pat.decode(), "->", len(re.findall(re.escape(pat), blob)))
ctx = [blob[max(0, mm.start() - 40): mm.end() + 30] for mm in re.finditer(rb"fold_notice", blob)]
print("all 'fold_notice' hits are prose inside stored job prompts:", all(b"recibo folded/fold_layers/fold_notice" in blob[max(0, mm.start() - 40): mm.end() + 30] for mm in re.finditer(rb"fold_notice", blob)))
sess = [p.name for p in (S / "session_requests").glob("*.json") if b"fold_notice" in p.read_bytes() or b'"folded": true' in p.read_bytes()]
print("session_requests with fold markers:", sess)
db = ro(S / "tasks.sqlite3")
for r in db.execute("select id,stage,created_at from coordination_jobs where id like 'e1ce17ac%' or id like '9dd45d6a%' or id like '90528e45%'"):
    print("job", r[0][:8], "stage", r[1], "created", r[2])

print("\n=== 5. 'o conteudo e EXATAMENTE o que a casa escreveu' (header v1) vs the folded c1/c2 the harness builds")
raw = Path(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl").read_bytes()
rotas, orig = {}, {}
for ln in raw.splitlines():
    if not ln.strip():
        continue
    r = json.loads(ln.decode("utf-8"))
    if r.get("seq", 0) > 1287:
        break
    rid = r.get("rota_id")
    if r.get("tipo") == "ROTA":
        rotas[rid] = dict(r)
        orig[rid] = dict(r)
    elif rid in rotas:
        for k, v in r.items():
            if v not in (None, "", []):
                rotas[rid][k] = v
print("routes:", len(rotas), "| folded 'tipo' != ROTA:", sum(1 for x in rotas if rotas[x].get("tipo") != "ROTA"),
      "| folded title != title of the ROTA record:", sum(1 for x in rotas if rotas[x].get("titulo") != orig[x].get("titulo")),
      "| c2 lines whose title is cut at 110 chars:", sum(1 for x in rotas if len(rotas[x].get("titulo") or "") > 110))
x = rotas["infra.grep_acom_camadas"]
print("example infra.grep_acom_camadas -> folded tipo:", x["tipo"], "| seq:", x["seq"], "| titulo:", x["titulo"][:80])
