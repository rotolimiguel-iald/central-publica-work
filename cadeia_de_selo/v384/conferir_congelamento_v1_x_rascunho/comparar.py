# -*- coding: utf-8 -*-
# Aferidor (lente v1_x_rascunho): compara o V1 congelado com o rascunho APRESENTADO, chave a chave. So leitura.
import hashlib, json, os, sys, difflib
sys.stdout.reconfigure(encoding="utf-8")
PERM = r"C:\IALD\Bancada_Um\investigacao\preregistro_pilar_quantico_03out"
SCR = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v384"
V1J = os.path.join(PERM, "PREREGISTRO_PILAR_QUANTICO_20261003_V1.json")
V1M = os.path.join(PERM, "PREREGISTRO_PILAR_QUANTICO_20261003_V1.md")
RJ = os.path.join(SCR, "rascunho_prereg_v13", "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_AMPLIADO_D64.json")
RM = RJ[:-5] + ".md"
REG = os.path.join(SCR, "registro_rascunhos_apresentados_v384.json")
WK = os.path.join(SCR, "pilar_quantico_worker.py")
OUT = {}


def fsha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def canon(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=False)


def canon_spec(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


v1 = json.load(open(V1J, encoding="utf-8")); r = json.load(open(RJ, encoding="utf-8"))
for p in (V1J, V1M, RJ, RM, REG, WK):
    OUT.setdefault("sha256_arquivos", {})[p] = {"sha256": fsha(p), "bytes": os.path.getsize(p)}

VOL = {"id", "titulo", "gerado", "gerado_utc", "ratificacao_do_operador", "evidencias", "afericao"}
# 1) todas as chaves de topo que diferem
top = sorted(set(v1) | set(r))
dif_top = []
for k in top:
    a, b = v1.get(k, "<<AUSENTE>>"), r.get(k, "<<AUSENTE>>")
    if canon(a) != canon(b):
        dif_top.append(k)
OUT["chaves_topo_v1"] = sorted(v1); OUT["chaves_topo_rascunho"] = sorted(r)
OUT["so_no_v1"] = sorted(set(v1) - set(r)); OUT["so_no_rascunho"] = sorted(set(r) - set(v1))
OUT["chaves_topo_que_diferem"] = dif_top


# 2) folha a folha, para mostrar o que muda em cada chave diferente
def walk(a, b, path, acc):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b), key=str):
            walk(a.get(k, "<<AUSENTE>>"), b.get(k, "<<AUSENTE>>"), path + [str(k)], acc)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, path + ["[%d]" % i], acc)
    else:
        if canon(a) != canon(b):
            acc.append({"caminho": ".".join(path), "v1": a if len(canon(a)) < 400 else canon(a)[:400] + "...",
                        "rascunho": b if len(canon(b)) < 400 else canon(b)[:400] + "..."})


folhas = []
walk(v1, r, [], folhas)
OUT["folhas_que_diferem"] = folhas


def volatil(caminho):
    top_ = caminho.split(".")[0]
    if top_ in VOL:
        return True
    if caminho == "desvio_do_plano_B.ratificacao" or caminho.startswith("desvio_do_plano_B.ratificacao."):
        return True
    return False


OUT["folhas_fora_do_volatil"] = [f for f in folhas if not volatil(f["caminho"])]
# 3) a guarda do gerador reproduzida
a_ = {k: v for k, v in v1.items() if k not in VOL}; b_ = {k: v for k, v in r.items() if k not in VOL}
for d_ in (a_, b_):
    if isinstance(d_.get("desvio_do_plano_B"), dict):
        d_["desvio_do_plano_B"] = {k: v for k, v in d_["desvio_do_plano_B"].items() if k != "ratificacao"}
OUT["guarda_do_gerador_reproduzida_dif"] = sorted(k for k in set(a_) | set(b_) if canon(a_.get(k)) != canon(b_.get(k)))
# 4) spec_sha256
OUT["spec_sha256_v1_gravado"] = v1.get("spec_sha256")
OUT["spec_sha256_v1_recalculado"] = hashlib.sha256(canon_spec(v1["spec"]).encode("utf-8")).hexdigest()
OUT["spec_sha256_rascunho_gravado"] = r.get("spec_sha256")
OUT["spec_sha256_rascunho_recalculado"] = hashlib.sha256(canon_spec(r["spec"]).encode("utf-8")).hexdigest()
OUT["spec_identica_canonica"] = canon_spec(v1["spec"]) == canon_spec(r["spec"])
# 5) worker
OUT["spec_worker_sha256_v1"] = v1["spec"].get("worker_sha256")
OUT["motor_worker_sha256_v1"] = (v1.get("motor") or {}).get("worker_sha256")
OUT["worker_sha256_disco"] = fsha(WK)
OUT["worker_tem_CR"] = b"\r" in open(WK, "rb").read()
# 6) a ratificacao
rat = v1.get("ratificacao_do_operador")
OUT["ratificacao_do_operador"] = rat
OUT["rascunho_ratificacao"] = r.get("ratificacao_do_operador")
OUT["sha256_rascunho_v13_disco"] = fsha(RJ)
reg = json.load(open(REG, encoding="utf-8"))
OUT["registro_rascunhos"] = reg
# 7) evidencias do V1: rascunho_apresentado_json/md
OUT["evidencias_v1_rascunho"] = [e for e in v1.get("evidencias", []) if e.get("papel", "").startswith("rascunho") or e.get("papel") == "gerador"]
json.dump(OUT, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "comparacao.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# 8) o MD
la = open(V1M, encoding="utf-8").read().split("\n"); lb = open(RM, encoding="utf-8").read().split("\n")
diff = list(difflib.unified_diff(lb, la, "rascunho.md", "V1.md", n=0, lineterm=""))
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "diff_md.txt"), "w", encoding="utf-8").write("\n".join(diff))
print("linhas md v1", len(la), "rascunho", len(lb), "linhas de diff", len(diff))
print("CRLF v1", open(V1M, "rb").read().count(b"\r\n"), "CRLF r", open(RM, "rb").read().count(b"\r\n"))
