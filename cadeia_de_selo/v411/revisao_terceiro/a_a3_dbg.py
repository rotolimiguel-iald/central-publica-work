src = open("a_a3.py", encoding="utf-8").read().split("rep = {}")[0]
exec(compile(src, "a_a3_head", "exec"))
import copy
o = rodar(copy.deepcopy(core0))
c11 = o["values"]["a_emenda_as_claras"]
print(json.dumps({k: (v if k != "c" else {kk: vv for kk, vv in v.items() if kk != "vetores"}) for k, v in c11.items()}, ensure_ascii=False)[:1500])
print([ (x["nome"], x["ok"], x["ramo_v410"], x["ramo_v411"]) for x in c11.get("c", {}).get("vetores", [])])
