# -*- coding: utf-8 -*-
"""A FUMACA da v384: o trabalhador de ponta a ponta (modo run) com a especificacao CONGELADA reduzida SO nas contagens -- d = 8 e 16, poucas
instancias, d = 128 desligado (prazo de inicio 0) --, para pegar defeito de caminho de codigo ANTES do rito de duas horas e alimentar o ensaio a seco.
O resultado da fumaca NUNCA e' resultado do pilar: hash de especificacao proprio, pasta propria, marcado FUMACA. Roda so depois do congelamento
e do OK do operador para calcular. uso: python fumaca_v384.py <PREREGISTRO_..._V1.json> <worker.py>"""
import copy, hashlib, json, os, subprocess, sys, time, uuid
if sys.flags.optimize:   # as guardas sao assert: com -O elas sumiriam sem aviso (9a afericao)
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PJ = json.load(open(sys.argv[1], encoding="utf-8")); WK = os.path.abspath(sys.argv[2])
# a fumaca CALCULA com os operadores da teoria: so com o pre-registro V1 RATIFICADO, do lugar permanente (3a afericao)
_pp = os.path.abspath(sys.argv[1]).replace(chr(92), "/")
assert _pp.startswith("C:/IALD/Bancada_Um/investigacao/preregistro_pilar_quantico_03out/") and "RASCUNHO" not in _pp.upper(), "a fumaca so roda com o V1 do lugar permanente: " + _pp
assert (PJ.get("ratificacao_do_operador") or {}).get("verbatim"), "o pre-registro nao foi ratificado pelo operador -- a fumaca nao roda"
assert ((PJ.get("ratificacao_do_operador") or {}).get("transcrito") or {}).get("de_teste") is False, "a ratificacao veio de transcrito de TESTE (ou nao diz qual) -- a fumaca nao roda"   # 8a
assert hashlib.sha256(open(WK, "rb").read()).hexdigest() == PJ["spec"]["worker_sha256"], "o trabalhador nao e' o congelado no pre-registro"
S = copy.deepcopy(PJ["spec"])
assert hashlib.sha256(json.dumps(S, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest() == PJ["spec_sha256"]
S["id"] = S["id"] + "__FUMACA"
S["T2"]["d"] = [8, 16]; S["T2"]["n_gamma"] = {"8": 6, "16": 4, "32": 2, "64": 2}
S["T1"]["d_counts"] = {"8": 6, "16": 3}
S["T3"]["d"] = [8, 16]; S["T3"]["N3_counts"] = {"8": 4, "16": 2}
S["T4"]["d_counts"] = {"8": 20, "16": 6}
S["D128"]["start_deadline_s"] = 0
S["cpuref"]["d_all"] = [8]; S["cpuref"]["d_pick"] = {"16": [[3, 0], [3, 3]]}
RUN_ID = uuid.uuid4().hex   # a marca da rodada (afericao 2): o trabalhador exige; a pasta e' NOVA por rodada e nunca se le saida velha
OUT = os.path.join(HERE, "fumaca_v384_" + time.strftime("%Y%m%d_%H%M%S") + "_" + RUN_ID[:8]); os.makedirs(OUT, exist_ok=False)
sp = os.path.join(OUT, "spec_fumaca.json")
canon = json.dumps(S, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
open(sp, "w", encoding="utf-8").write(canon)
sh = hashlib.sha256(canon.encode("utf-8")).hexdigest()
sys.path.insert(0, os.path.dirname(os.path.abspath(sys.argv[1])))
# beta pelo MESMO motor do um.py (forma de Lagrange); lido do canonico importado? nao: o motor e' publico -- alpha selado do um.py, lido do arquivo
import re
um_src = open(os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "um.py"), encoding="utf-8").read()
m = re.search(r"^SEALED_CODATA_ALPHA\s*=\s*([0-9.eE+-]+)", um_src, re.M)
alpha = float(m.group(1)); import math
beta = alpha * math.sqrt(math.e)          # para a FUMACA basta alpha*sqrt(e) (o rito usa o motor de Lagrange; a diferenca e' < 1e-12 relativa)
t0 = time.time()
r = subprocess.run([sys.executable, WK, "--mode", "run", "--spec", sp, "--spec-sha256", sh, "--beta-hex", beta.hex(), "--run-id", RUN_ID, "--out", OUT], capture_output=True, text=True, encoding="utf-8")
R = json.load(open(os.path.join(OUT, "result.json"), encoding="utf-8")) if os.path.exists(os.path.join(OUT, "result.json")) else {}
assert not R or R.get("run_id") == RUN_ID, "o resultado lido nao e' desta fumaca"
print("pasta da fumaca:", OUT)
print("fumaca rc", r.returncode, "em %.0f s" % (time.time() - t0))
print("veredito da FUMACA (nao e' resultado):", R.get("verdict"))
print("fases (s):", R.get("phase_seconds"), "| cpuref:", {k: (R.get("cpuref_compare") or {}).get(k) for k in ("read", "compared", "disagreements", "ok")})
for ph in ("T3", "T2", "T1", "T4", "D128"):
    if isinstance(R.get(ph), dict) and R[ph].get("error"):
        print("ERRO na fase", ph, R[ph]["error"]); print(R[ph].get("trace", "")[-1500:])
if r.returncode != 0 or not R:
    print(r.stdout[-3000:]); print(r.stderr[-3000:])
    print("FUMACA FALHOU (rc %s; resultado %s)" % (r.returncode, "presente" if R else "AUSENTE")); sys.exit(1)   # fail-closed (3a afericao)
print("resultado da fumaca:", os.path.join(OUT, "result.json"))
