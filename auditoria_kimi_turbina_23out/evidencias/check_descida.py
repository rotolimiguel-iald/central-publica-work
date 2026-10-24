"""Independent re-measurement of the grep-c3 numbers (seq 1285/1286) on the ledger PREFIX the author used.
Read-only on the ledger and on Kimi's notebook; writes only to stdout."""
import hashlib
import json
import unicodedata
from pathlib import Path

J = Path(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl")
CAD = Path(r"C:\Users\rotol\Documents\kimi\workspace\estudo_iald_qg")
TARGET_BYTES = 3427185

raw = J.read_bytes()
# find the line-boundary prefix whose length equals the author's reported size
pos = 0
prefix_end = None
lines = raw.split(b"\n")
cum = 0
cutoff_seq = None
for i, ln in enumerate(lines):
    cum += len(ln) + 1
    if cum == TARGET_BYTES:
        prefix_end = cum
        try:
            cutoff_seq = json.loads(ln.decode("utf-8")).get("seq")
        except Exception:
            cutoff_seq = None
        break
print("prefix boundary found:", prefix_end == TARGET_BYTES, "| last seq in prefix:", cutoff_seq, "| total ledger bytes now:", len(raw))
prefix = raw[:TARGET_BYTES]


def fold(blob):
    rotas = {}
    n = 0
    for linha in blob.splitlines():
        if not linha.strip():
            continue
        n += 1
        r = json.loads(linha.decode("utf-8"))
        rid = r.get("rota_id")
        if r.get("tipo") == "ROTA":
            rotas[rid] = r
        elif rid in rotas:
            for k, v in r.items():
                if v not in (None, "", []):
                    rotas[rid][k] = v
    return rotas, n


rotas, nrec = fold(prefix)
dominios = {}
for rid in rotas:
    dominios.setdefault(rid.split(".")[0], []).append(rid)
c3 = "".join(f"{d} | {len(ids)} rotas\n" for d, ids in sorted(dominios.items()))
c2l = {rid: f"{rid} | {(r.get('titulo') or '')[:110]}" for rid, r in rotas.items()}
c2 = "\n".join(c2l[k] for k in sorted(c2l))
c1m = {rid: json.dumps(r, ensure_ascii=False) for rid, r in rotas.items()}
c1_total = sum(len(v) for v in c1m.values())
pins = {"c3": hashlib.sha256(c3.encode()).hexdigest()[:16], "c2": hashlib.sha256(c2.encode()).hexdigest()[:16],
        "c1": hashlib.sha256("".join(c1m[k] for k in sorted(c1m)).encode()).hexdigest()[:16]}
print("records:", nrec, "| rotas:", len(rotas), "| dominios:", len(dominios), "| c3:", len(c3), "| c2:", len(c2), "| c1_total:", c1_total)
print("pins:", pins, " (author: c3 052e71f93eda6d48 / c2 558296fc8db45f39 / c1 3c79115150181675)")

corpus = json.loads((CAD / "corpus_f9_9.json").read_text(encoding="utf-8"))
gab = json.loads((CAD / "gabarito_f9_9.json").read_text(encoding="utf-8"))


def norm(s):
    return unicodedata.normalize("NFKD", s.lower())


desc = []
for q in corpus:
    g = gab.get(q["id"], {})
    rid = g.get("rota_id")
    if not rid:
        continue
    alvo = c2l.get(rid)
    hit2 = alvo is not None and norm(rid) in norm(alvo)
    reg = c1m.get(rid, "")
    resp = str(g.get("resposta") or "")
    hit1 = bool(resp) and resp[:60] in reg
    desc.append(dict(id=q["id"], rota=rid, controle=g.get("tipo") == "controle", hit_c2=hit2, hit_c1=hit1,
                     custo=len(c2) + (len(reg) if hit2 else 0), pergunta=q["pergunta"], resp=resp))
fact = [d for d in desc if not d["controle"]]
rec = sum(1 for d in fact if d["hit_c2"] and d["hit_c1"]) / max(1, len(fact))
ctrl = [d for d in desc if d["controle"]]
ctrl_ok = sum(1 for d in ctrl if not d["hit_c2"])
mean_cost = sum(d["custo"] for d in desc) / max(1, len(desc))
print("n questions in descida:", len(desc), "| factuais:", len(fact), "| recall:", round(rec, 4), "| controles:", ctrl_ok, "/", len(ctrl),
      "| custo medio:", int(mean_cost), "| economia %:", round(100 * (1 - mean_cost / c1_total), 2), "| fator:", round(c1_total / mean_cost, 1))
# --- what does the 'descent' actually use as key?
print("\n[A] hit_c2 for factuals is True for", sum(1 for d in fact if d["hit_c2"]), "of", len(fact), "-> lookup by the gabarito's own rota_id (dictionary .get), not a grep of the question text")
print("[A] controls: rota_id present in gabarito? ->", [d["rota"] for d in ctrl][:6])
# test: does a REAL grep of c2 with the question text find the target? (simple token-overlap grep)
import re
def grep_c2(question):
    toks = [t for t in re.findall(r"[\w\.]{4,}", norm(question))]
    hits = []
    for rid, line in c2l.items():
        L = norm(line)
        score = sum(1 for t in set(toks) if t in L)
        if score:
            hits.append((score, rid))
    hits.sort(reverse=True)
    return [r for _, r in hits[:5]]
found_top1 = found_top5 = 0
for d in fact:
    top = grep_c2(d["pergunta"])
    found_top1 += int(bool(top) and top[0] == d["rota"])
    found_top5 += int(d["rota"] in top)
print("[A'] naive text-grep of c2 using the QUESTION: top1 =", found_top1, "/", len(fact), "| top5 =", found_top5, "/", len(fact))
# does the question literally contain the rota_id?
lit = sum(1 for d in fact if d["rota"].lower() in d["pergunta"].lower())
print("[A'] questions that contain the exact rota_id string:", lit, "/", len(fact))
# --- the 12 divergences: is the frozen answer present in ANY earlier ledger record of the same route?
hist = {}
for linha in prefix.splitlines():
    if not linha.strip():
        continue
    r = json.loads(linha.decode("utf-8"))
    hist.setdefault(r.get("rota_id"), []).append(r)
fail = [d for d in fact if not (d["hit_c2"] and d["hit_c1"])]
print("\n[B] divergences:", len(fail))
in_hist = 0
for d in fail:
    blob = json.dumps(hist.get(d["rota"], []), ensure_ascii=False)
    present = d["resp"][:60] in blob if d["resp"] else False
    in_hist += int(present)
    print("   ", d["id"], d["rota"], "| route exists:", d["rota"] in rotas, "| frozen-answer[:60] present in some record of this route's history:", present)
print("[B] explained as supersession (answer text exists in route history):", in_hist, "/", len(fail))
