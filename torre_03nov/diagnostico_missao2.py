import sys, json, re
sys.path.insert(0, r"C:\IALD\MEMORIA_IALD\lib")
from pathlib import Path
from iald_memory import MemoryStore, guard
ref = json.load(open(r"C:\IALD\MEMORIA_IALD\sessions\claude-central-9c_patentes-atualizacao-12out.json", encoding="utf-8"))
store = MemoryStore(Path(ref["store"]))
snap = store.get(ref["context_id"], ref["scope"])
recs = snap["q"]["records"]
print("n_records", len(recs), "chaves do q:", list(snap["q"].keys()), "| chaves do p:", list(snap["p"].keys()))
pat = re.compile(r"\S*(?:[\/]|%5c|%2f|\b[a-z]:)escritorio\S*")
for i, r in enumerate(recs):
    meta = {k: (v if k not in ("text", "sources") else None) for k, v in r.items()}
    print(i, json.dumps(meta, ensure_ascii=False)[:400])
    if "text" in r:
        print("   texto (", len(r["text"]), "chars ):", r["text"][:200].replace("\n", " "))
    for j, s in enumerate(r.get("sources", [])):
        ref_s = s.get("ref", "")
        f = guard.fold(ref_s)
        m = pat.search(f)
        masc = (f[:m.start()] + "<CAMINHO_ESCRITORIO>" + f[m.end():]) if m else f
        print("   source[%d] kind=%s ref(mascarado)=%s" % (j, s.get("kind"), masc), "| outras chaves:", [k for k in s if k not in ("kind", "ref")])
print("p:", json.dumps(snap["p"], ensure_ascii=False)[:600])
print("constraints:", json.dumps(snap["constraints"], ensure_ascii=False)[:300])
print("objective:", snap["objective"][:400])
print("receipt:", json.dumps(snap["receipt"], ensure_ascii=False)[:400])
