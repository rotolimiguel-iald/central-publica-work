# -*- coding: utf-8 -*-
# SO LEITURA: extrai _qp_summary e o comparador do candidato e aplica ao result.json do cache real (v384)
import json, math, os, re, hashlib, sys
sys.stdout.reconfigure(encoding="utf-8")
PK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(PK, "um_v385_candidato.py"), encoding="utf-8").read().splitlines()
def grab(start_pat):
    i = [k for k, l in enumerate(src) if l.startswith(start_pat)][0]
    j = i + 1
    while j < len(src) and (src[j].startswith((" ", "\t")) or src[j].strip() == ""):
        j += 1
    return "\n".join(src[i:j])
ns = {"os": os, "hashlib": hashlib, "json": json}
for p in ("def _qp_summary(", "_QP_REPRO_SKIP_V385 =", "def _qp_flat_v385(", "def quantum_pillar_reproducibility_v385("):
    exec(grab(p), ns)
C = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache\checkpoints\quantum_pillar\75dc30bc9cc8d330e31f99ca"
raw = open(os.path.join(C, "result.json"), "rb").read()
print("sha256 result.json:", hashlib.sha256(raw).hexdigest())
print("sha256 file      :", open(os.path.join(C, "result.json.sha256")).read().strip())
R = json.loads(raw)
print("top keys:", list(R.keys()))
S = ns["_qp_summary"](R)
flat = dict(ns["_qp_flat_v385"](S))
print("n campos achatados:", len(flat))
# campos nao-finitos
bad = {k: v for k, v in flat.items() if isinstance(v, float) and not math.isfinite(v)}
print("nao finitos:", bad)
# campos com nome suspeito de tempo/ambiente/caminho
sus = {k: v for k, v in flat.items() if re.search(r"(time|second|_s$|\.s$|elapsed|started|finished|date|stamp|path|dir|pid|host|run_id|env|gpu|device|wall|clock|version|uuid)", k, re.I)}
print("suspeitos:", json.dumps(sus, ensure_ascii=False, indent=0)[:4000])
# strings
strs = {k: v for k, v in flat.items() if isinstance(v, str)}
print("strings:", json.dumps(strs, ensure_ascii=False)[:3000])
# floats muito pequenos (residuos de maquina)
small = {k: v for k, v in flat.items() if isinstance(v, float) and v != 0.0 and abs(v) < 1e-10}
print("floats |v|<1e-10 (residuos):", len(small)); print(json.dumps(dict(list(small.items())[:60]), indent=0)[:5000])
json.dump(flat, open(os.path.join(PK, "afericao_codigo", "sumario_cache_flat.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
