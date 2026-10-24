import hashlib, json, statistics
from pathlib import Path
CAD = Path(r"C:\Users\rotol\Documents\kimi\workspace\estudo_iald_qg")
raw = (CAD / "pacote_corrida_turbina.json").read_bytes()
print("pacote bytes:", len(raw), "sha256:", hashlib.sha256(raw).hexdigest())
P = json.loads(raw.decode("utf-8"))
print("keys:", [k for k in P if k != "itens"], "| n itens:", len(P["itens"]))
gv = json.loads((CAD / "gabarito_vivo_20261020.json").read_text(encoding="utf-8"))
gf = json.loads((CAD / "gabarito_f9_9.json").read_text(encoding="utf-8"))
A_hashes = {hashlib.sha256(it["braco_A"]["contexto"].encode()).hexdigest()[:16] for it in P["itens"]}
print("distinct A contexts:", len(A_hashes), "| A chars:", {it["braco_A"]["chars"] for it in P["itens"]}, "| A tokens_est:", {it["braco_A"]["tokens_est"] for it in P["itens"]})
print("A instrucao == B instrucao for all:", all(it["braco_A"]["instrucao"] == it["braco_B"]["instrucao"] for it in P["itens"]))
fact = [it for it in P["itens"] if it["tipo"] == "factual"]
ctrl = [it for it in P["itens"] if it["tipo"] == "controle"]
print("factual:", len(fact), "controle:", len(ctrl))
tb = [it["braco_B"]["tokens_est"] for it in P["itens"]]
ta = P["itens"][0]["braco_A"]["tokens_est"]
print("B tokens_est min/mean/max:", min(tb), int(statistics.mean(tb)), max(tb), "| A:", ta)
ratios = [ta / it["braco_B"]["tokens_est"] for it in P["itens"]]
print("A/B token ratio min/mean/max: %.1f / %.1f / %.1f" % (min(ratios), statistics.mean(ratios), max(ratios)))
print("A truncated to 128k window -> ratio with B mean: %.1f ; to 200k: %.1f" % (128000 / statistics.mean(tb), 200000 / statistics.mean(tb)))
# H2 arithmetic: density_B/density_A = (S_B/S_A) * (T_A/T_B); H2 needs > 5
need = 5 / statistics.mean(ratios)
print("H2 (>5x) holds whenever S_B/S_A > %.3f (full dump) ; > %.3f if A is cut to 128k" % (need, 5 / (128000 / statistics.mean(tb))))
# oracle: does B contain the expected answer text verbatim?
leak_B = leak_A = 0
for it in fact:
    g = gv[it["id"]]
    q = it["pergunta"]
    if "veredito" in q:
        key = g["veredito"]
    elif "próximo passo" in q:
        key = g["proximo_passo"]
    else:
        key = None  # artefatos
    if key:
        leak_B += int(key in it["braco_B"]["contexto"])
        leak_A += int(key in it["braco_A"]["contexto"])
n_keyed = sum(1 for it in fact if "artefatos" not in it["pergunta"])
print("answer text verbatim in B context (veredito/proximo_passo items):", leak_B, "/", n_keyed, "| in A (full dump):", leak_A, "/", n_keyed)
# B includes only the target c1 record? count how many c1 records are embedded in B for factuals
import re
def n_c1(ctx):
    i = ctx.find("[c1 — registro do alvo]")
    return 0 if i < 0 else 1
print("B factual with the target c1 record appended:", sum(n_c1(it["braco_B"]["contexto"]) for it in fact), "/", len(fact), "| B controls with c1:", sum(n_c1(it["braco_B"]["contexto"]) for it in ctrl), "/", len(ctrl))
# which item arms contain the rota_id of the question in the c2 index (all do)
print("B contains the full c2 index in all items:", all("[c2 — índice]" in it["braco_B"]["contexto"] for it in P["itens"]))
# 'artefatos' items: is the snapshot key missing?
art = [it for it in fact if "artefatos" in it["pergunta"]]
print("artefatos questions:", len(art), "| gabarito_vivo carries the artefatos list for them:", any("artefatos" in gv[it["id"]] for it in art))
# header: shows confidence header text of the first B
print("\n--- B header (first 900 chars of first B context)\n", P["itens"][0]["braco_B"]["contexto"][:900])
print("\ncriterios in pacote:", P.get("criterios"))
print("rubrica:", P.get("rubrica_fidelidade"))
