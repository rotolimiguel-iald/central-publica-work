# -*- coding: utf-8 -*-
"""Redator r2 — pinos por sha256 dos bytes; beta em runtime a partir dos bytes do um.py (sem executar)."""
import hashlib, json, math, os, re, sys, datetime
W = r"C:\IALD\Central de Patentes\work\frequencia_defasa_12out"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()
pins = {
 "V1": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_10out_posto_rank_texto_verbatim.txt",
 "V2": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
 "V3": r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_posto_rank_verbatim.txt",
 "V4": r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt",
 "PREREGISTRO.json": W + r"\1_PREREGISTRO\PREREGISTRO.json",
 "PREREGISTRO.md": W + r"\1_PREREGISTRO\PREREGISTRO.md",
 "FREEZE.json": W + r"\1_PREREGISTRO\FREEZE.json",
 "RESULTADO_OPTICO.json": W + r"\2_OPTICO\RESULTADO_OPTICO.json",
 "run_optico.py": W + r"\2_OPTICO\run_optico.py",
 "LOG_OPTICO.txt": W + r"\2_OPTICO\LOG_OPTICO.txt",
 "RESULTADO_KERNEL_r2.json": W + r"\3_KERNEL\rodada2\RESULTADO_KERNEL.json",
 "RESULTADO_KERNEL_r1.json": W + r"\3_KERNEL\RESULTADO_KERNEL.json",
 "pedra_r2.lean": W + r"\3_KERNEL\rodada2\sandbox\TGLExt\TheUnitIsTheRank.lean",
 "pedra_r1.lean": W + r"\3_KERNEL\sandbox\TGLExt\TheUnitIsTheRank.lean",
 "olean_r2": W + r"\3_KERNEL\rodada2\olean\TheUnitIsTheRank.olean",
 "olean_r1": W + r"\3_KERNEL\olean\TheUnitIsTheRank.olean",
 "um.py": NOS + r"\um.py",
 "um_absoluto.json": NOS + r"\um_absoluto.json",
 "um_absoluto_selo.json": NOS + r"\um_absoluto_selo.json",
 "INVENTARIO_BANCADA.json": r"C:\IALD\Central de Patentes\memory\INVENTARIO_BANCADA_CHATGPT.json",
 "rotas.jsonl": r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl",
}
out = {"quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "pinos": {}}
for k, p in pins.items():
    if os.path.exists(p):
        out["pinos"][k] = {"arquivo": p, "bytes": os.path.getsize(p), "sha256": sha(p)}
    else:
        out["pinos"][k] = {"arquivo": p, "AUSENTE": True}
# recorte V2 l.1-33 unido por LF sem LF final
b = open(pins["V2"], "rb").read()
lines = b.split(b"\n")
rec = b"\n".join(l.rstrip(b"\r") for l in lines[:33])
out["V2_l1_33"] = {"bytes": len(rec), "sha256": hashlib.sha256(rec).hexdigest(), "l34_inicio": lines[33][:40].decode("utf-8", "replace")}
# beta em runtime: ler atribuicao de ALPHA_FINE_CODATA_2018 nos bytes
um = open(pins["um.py"], "rb").read()
hits = []
for i, l in enumerate(um.split(b"\n"), 1):
    if re.match(rb"^\s*ALPHA_FINE_CODATA_2018\s*=", l):
        hits.append((i, l.decode("utf-8", "replace").strip()))
sealed = [(i, l.decode("utf-8","replace").strip()) for i, l in enumerate(um.split(b"\n"), 1) if re.match(rb"^\s*SEALED_CODATA_ALPHA\s*=", l)]
out["alpha_hits"] = hits; out["sealed_hits"] = sealed
rhs = hits[0][1].split("=", 1)[1].strip()
m = re.match(r"([0-9.eE+\-]+)", rhs)
alpha_txt = m.group(1) if m else None
if alpha_txt is None:
    # pode ser alias SEALED_CODATA_ALPHA
    srhs = sealed[0][1].split("=",1)[1].strip()
    alpha_txt = re.match(r"([0-9.eE+\-]+)", srhs).group(1)
alpha = float(alpha_txt)
beta = alpha * math.sqrt(math.e)
theta = math.asin(math.sqrt(beta))
pre = json.load(open(pins["PREREGISTRO.json"], encoding="utf-8"))
def find_beta(o):
    s = json.dumps(o, ensure_ascii=False)
    m = re.search(r"0\.0120313004008\d+", s)
    return m.group(0) if m else None
out["beta_runtime"] = {"alpha_texto": alpha_txt, "receita": "float(alpha_texto)*math.sqrt(math.e)", "beta_repr": repr(beta),
    "theta_M_repr": repr(theta), "conferencia_PREREGISTRO": find_beta(pre), "confere": repr(beta) == find_beta(pre)}
v4 = open(pins["V4"], "rb").read().split(b"\n")
num = re.search(rb"0,012031|0\.012031", v4[15]).group(0).decode().replace(",", ".")
out["beta_runtime"]["numero_operador_V4_l16"] = num
out["beta_runtime"]["abs_beta_menos_numero"] = abs(beta - float(num))
# selo/core: leak e omega
core = json.load(open(pins["um_absoluto.json"], encoding="utf-8"))
fd = core.get("fractal_dephasing_principle") or {}
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + "/" + k)
    else:
        yield path, o
leak = [(p, v) for p, v in walk(core) if "leak_sin2_thetaM" in p]
anti = [(p, v) for p, v in walk(core) if "anticommutator_norm" in p]
out["core_v391"] = {"leak_sin2_thetaM": leak[:3], "anticommutator": anti[:3], "leak_igual_beta_bit_a_bit": any(v == beta for _, v in leak)}
dst = W + r"\4_RELATORIO\PINOS_R2.json"
tmp = dst + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
os.replace(tmp, dst)
print(json.dumps(out, ensure_ascii=False, indent=1))
