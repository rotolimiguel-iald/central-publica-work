import json
from pathlib import Path
J = Path(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl")
CAD = Path(r"C:\Users\rotol\Documents\kimi\workspace\estudo_iande_qg") if False else Path(r"C:\Users\rotol\Documents\kimi\workspace\estudo_iald_qg")
prefix = J.read_bytes()[:3427185]
corpus = {q["id"]: q for q in json.loads((CAD / "corpus_f9_9.json").read_text(encoding="utf-8"))}
gab = json.loads((CAD / "gabarito_f9_9.json").read_text(encoding="utf-8"))
hist = {}
for linha in prefix.splitlines():
    if linha.strip():
        r = json.loads(linha.decode("utf-8"))
        hist.setdefault(r.get("rota_id"), []).append(r)
rotas = {}
for rid, recs in hist.items():
    for r in recs:
        if r.get("tipo") == "ROTA":
            rotas[rid] = dict(r)
        elif rid in rotas:
            for k, v in r.items():
                if v not in (None, "", []):
                    rotas[rid][k] = v
# classify every factual item by the SHAPE of its frozen answer
shape = {"json_list_of_paths": 0, "plain_text": 0}
fails = []
for qid, g in gab.items():
    if g.get("tipo") == "controle" or not g.get("rota_id"):
        continue
    resp = str(g.get("resposta") or "")
    reg = json.dumps(rotas[g["rota_id"]], ensure_ascii=False)
    ok = resp[:60] in reg
    is_list = resp.startswith("[")
    shape["json_list_of_paths" if is_list else "plain_text"] += 1
    if not ok:
        fails.append((qid, is_list, g["rota_id"]))
print("answer shapes among the 36 factual items:", shape)
print("failing items:", len(fails), "| of which the frozen answer is a JSON list:", sum(1 for f in fails if f[1]))
print("passing items whose frozen answer is a JSON list:", shape["json_list_of_paths"] - sum(1 for f in fails if f[1]))
# For the failing JSON-list items: do the listed paths equal / overlap the live 'artefatos' paths?
for qid, is_list, rid in fails:
    g = gab[qid]
    try:
        lst = json.loads(g["resposta"])
    except Exception as e:
        print(qid, "resp is not valid JSON:", e)
        continue
    live = rotas[rid].get("artefatos") or []
    live_paths = [a.get("caminho") if isinstance(a, dict) else a for a in live]
    # any record in history that carried these paths?
    hist_paths = set()
    for r in hist[rid]:
        for a in (r.get("artefatos") or []):
            hist_paths.add(a.get("caminho") if isinstance(a, dict) else a)
    inter_live = len(set(lst) & set(live_paths))
    inter_hist = len(set(lst) & hist_paths)
    print(qid, rid[:48], "| pergunta:", corpus[qid]["pergunta"][:90].replace("\n", " "))
    print("      listed:", len(lst), "| live artefatos:", len(live_paths), "| overlap live:", inter_live, "| overlap any history record:", inter_hist, "| fields holding list-of-str:", [k for k, v in rotas[rid].items() if isinstance(v, list) and v and all(isinstance(x, str) for x in v)])
