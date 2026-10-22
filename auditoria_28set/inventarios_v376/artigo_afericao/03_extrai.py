# -*- coding: utf-8 -*-
"""03_extrai.py -- item 2: correspondencia artigo (TXT PT/EN) <-> codigo (selo + core da v375).
Extrai do TXT: vereditos (tokens UPPER_SNAKE com >=3 partes ou prefixo TGL_), hashes de 16/64 hex,
contagens 'N/N teoremas|theorems', numeros com >=3 digitos significativos; confere cada um contra
o selo (um_absoluto_selo.json) e o core (um_absoluto.json). Saida: 03_extrai.json + resumo no stdout."""
import re, os, sys, json, math, collections
sys.stdout.reconfigure(encoding="utf-8")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
OUT = os.path.dirname(os.path.abspath(__file__))
SELO = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
R = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))
TXT = {l: open(os.path.join(NOS, "um_absoluto_%s.txt" % l), encoding="utf-8").read() for l in ("pt", "en")}
LINES = {l: TXT[l].splitlines() for l in TXT}

# ---- achatar selo + core: strings e numeros, com caminho
def flat(o, path, strs, nums):
    if isinstance(o, dict):
        for k, v in o.items():
            flat(v, path + "/" + str(k), strs, nums)
    elif isinstance(o, (list, tuple)):
        for i, v in enumerate(o):
            flat(v, path + "[%d]" % i, strs, nums)
    elif isinstance(o, str):
        strs.append((path, o))
    elif isinstance(o, bool):
        pass
    elif isinstance(o, (int, float)) and o is not None:
        nums.append((path, o))

S_STR, S_NUM = [], []
flat(SELO, "selo", S_STR, S_NUM)
C_STR, C_NUM = [], []
flat(R, "core", C_STR, C_NUM)
ALL_STR = S_STR + C_STR
ALL_NUM = S_NUM + C_NUM
BIG = "\n".join(s for _, s in ALL_STR)
print("selo: %d strings, %d numeros | core(json inteiro): %d strings, %d numeros" % (len(S_STR), len(S_NUM), len(C_STR), len(C_NUM)))

def lineno_of(lang, needle):
    for i, l in enumerate(LINES[lang], 1):
        if needle in l:
            return i
    return None

# ---- 1. vereditos (tokens)
RX_VER = re.compile(r"(?<![A-Za-z0-9_])(?:TGL_[A-Z0-9_]+|[A-Z][A-Z0-9]*(?:_[A-Z0-9]+){2,})(?![A-Za-z0-9_])")
# excluir tokens de LaTeX/programacao obvios
EXCL = {"ALPHA_FINE_CODATA_2018", "SEALED_CODATA_ALPHA"}
ver = {}
for l in ("pt", "en"):
    c = collections.Counter(RX_VER.findall(TXT[l]))
    ver[l] = c
tok_all = set(ver["pt"]) | set(ver["en"])
tok_rows = []
for t in sorted(tok_all):
    if t in EXCL:
        continue
    in_selo = any(t in s for _, s in S_STR)
    in_core = any(t in s for _, s in C_STR)
    where = [p for p, s in ALL_STR if t in s][:3]
    tok_rows.append({"token": t, "pt": ver["pt"].get(t, 0), "en": ver["en"].get(t, 0),
                     "in_selo": in_selo, "in_core": in_core, "where": where,
                     "pt_line": lineno_of("pt", t), "en_line": lineno_of("en", t)})
n_tok = len(tok_rows)
n_tok_ok = sum(1 for r in tok_rows if r["in_selo"] or r["in_core"])
print("tokens-veredito distintos no artigo: %d ; com correspondente no selo/core: %d ; sem: %d" % (n_tok, n_tok_ok, n_tok - n_tok_ok))
print("  so PT: %d ; so EN: %d" % (sum(1 for r in tok_rows if r["pt"] and not r["en"]), sum(1 for r in tok_rows if r["en"] and not r["pt"])))

# ---- 2. hashes
RX_H16 = re.compile(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])")
RX_H64 = re.compile(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])")
h_rows = []
hs = {}
for l in ("pt", "en"):
    hs[l] = collections.Counter(RX_H16.findall(TXT[l]) + RX_H64.findall(TXT[l]))
# hashes conhecidos: qualquer substring de 16 hex em strings do selo/core + sha256 do selo
known_hex = set()
for _, s in ALL_STR:
    for m in re.findall(r"[0-9a-f]{16,64}", s):
        known_hex.add(m)
for h in sorted(set(hs["pt"]) | set(hs["en"])):
    # um hash de 16 esta 'conhecido' se e prefixo de algum hex conhecido ou igual
    ok = any(k.startswith(h) or h.startswith(k) or h in k for k in known_hex)
    where = [p for p, s in ALL_STR if h in s or (len(h) == 16 and any(h == x[:16] for x in re.findall(r"[0-9a-f]{64}", s)))][:3]
    h_rows.append({"hash": h, "pt": hs["pt"].get(h, 0), "en": hs["en"].get(h, 0), "known": ok, "where": where,
                   "pt_line": lineno_of("pt", h), "en_line": lineno_of("en", h)})
print("hashes distintos no artigo: %d ; conhecidos no selo/core: %d ; desconhecidos: %d" % (len(h_rows), sum(1 for r in h_rows if r["known"]), sum(1 for r in h_rows if not r["known"])))

# ---- 3. contagens N/N teoremas
RX_CNT = re.compile(r"(\d[\d.,]*)\s*/\s*(\d[\d.,]*)\s*(teoremas?|theorems?|pedras?|stones?|bandeiras?|flags?|clausulas?|cl[aá]usulas?|clauses?|selos?|seals?)", re.I)
cnt = {}
for l in ("pt", "en"):
    cnt[l] = collections.Counter((a, b, w.lower()) for a, b, w in RX_CNT.findall(TXT[l]))
print("contagens N/N: PT", dict(cnt["pt"]), "| EN", dict(cnt["en"]))
RX_CNT2 = re.compile(r"(\d[\d.,]*)\s*(teoremas|theorems)\b", re.I)
cnt2 = {l: collections.Counter(a for a, _ in RX_CNT2.findall(TXT[l])) for l in TXT}
print("contagens 'N teoremas': PT", dict(cnt2["pt"]), "| EN", dict(cnt2["en"]))

# ---- 4. numeros com >=3 digitos significativos
RX_NUM = re.compile(r"(?<![A-Za-z0-9_./-])[-+]?(?:\d{1,3}(?:[.,]\d{3})+|\d+)(?:[.,]\d+)?(?:\s*[x×]\s*10\^?[-+]?\d+|e[-+]?\d+)?(?![A-Za-z0-9_])")
def sig_digits(s):
    d = re.sub(r"[eE].*$", "", s)
    d = re.sub(r"[^0-9]", "", d).lstrip("0")
    return len(d)
def to_float(s):
    t = s.replace(" ", "")
    t = re.sub(r"[x×]10\^?", "e", t)
    # decidir separador: se tem ambos , e . -> o ultimo e decimal
    if "," in t and "." in t:
        if t.rfind(",") > t.rfind("."):
            t = t.replace(".", "").replace(",", ".")
        else:
            t = t.replace(",", "")
    elif "," in t:
        # 1,234 pode ser milhar ou decimal; assume decimal (PT) salvo se 3 digitos apos e nada mais
        parts = t.split(",")
        if len(parts) == 2 and len(parts[1]) == 3 and len(parts[0]) <= 3 and not t.startswith("0"):
            # ambiguo: guardar as duas leituras
            return [float(parts[0] + "." + parts[1]), float(parts[0] + parts[1])]
        t = t.replace(",", ".")
    try:
        return [float(t)]
    except ValueError:
        return []
num_vals = collections.defaultdict(set)   # valor -> set de (lang, texto)
num_txt = {}
for l in ("pt", "en"):
    c = collections.Counter(m.group(0).strip() for m in RX_NUM.finditer(TXT[l]) if sig_digits(m.group(0)) >= 3)
    num_txt[l] = c
allnum = sorted(set(num_txt["pt"]) | set(num_txt["en"]), key=lambda s: (-max(num_txt["pt"].get(s, 0), num_txt["en"].get(s, 0)), s))
CORE_VALS = [v for _, v in ALL_NUM if isinstance(v, (int, float)) and not (isinstance(v, float) and (math.isnan(v) or math.isinf(v)))]
def close(a, b):
    if a == b:
        return True
    if b == 0:
        return abs(a) < 1e-12
    r = abs(a - b) / max(abs(a), abs(b))
    return r < 5e-4   # arredondamento a 3-4 digitos
num_rows = []
for s in allnum:
    vals = to_float(s)
    ok_num = any(close(v, c) for v in vals for c in CORE_VALS) if vals else False
    ok_str = s in BIG or s.replace(",", ".") in BIG or s.replace(".", ",") in BIG
    num_rows.append({"texto": s, "pt": num_txt["pt"].get(s, 0), "en": num_txt["en"].get(s, 0), "vals": vals,
                     "bate_num": ok_num, "bate_str": ok_str})
print("numeros (>=3 dig. sig.) distintos no artigo: %d ; batem no core/selo (num ou string): %d ; nao batem: %d" % (
    len(num_rows), sum(1 for r in num_rows if r["bate_num"] or r["bate_str"]), sum(1 for r in num_rows if not (r["bate_num"] or r["bate_str"]))))

# ---- 5. (d) vereditos do selo sem mencao no artigo
RX_SELOVER = re.compile(r"^[A-Z][A-Z0-9]*(?:_[A-Z0-9]+){2,}$")
selo_ver_rows = []
def walk_selo(o, path):
    if isinstance(o, dict):
        for k, v in o.items():
            walk_selo(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk_selo(v, path + "[%d]" % i)
    elif isinstance(o, str) and RX_SELOVER.match(o.strip()) and len(o) >= 12:
        v = o.strip()
        selo_ver_rows.append({"chave": path, "veredito": v, "pt": v in TXT["pt"], "en": v in TXT["en"],
                              "pt_prefix40": v[:40] in TXT["pt"], "en_prefix40": v[:40] in TXT["en"]})
walk_selo(SELO, "selo")
n_sv = len(selo_ver_rows)
print("vereditos-string no selo: %d ; citados integralmente no PT: %d ; no EN: %d ; ausentes nos dois: %d" % (
    n_sv, sum(1 for r in selo_ver_rows if r["pt"]), sum(1 for r in selo_ver_rows if r["en"]), sum(1 for r in selo_ver_rows if not r["pt"] and not r["en"])))

json.dump({"tokens": tok_rows, "hashes": h_rows, "contagens": {l: [[k, v] for k, v in cnt[l].items()] for l in cnt},
           "contagens_teoremas": {l: dict(cnt2[l]) for l in cnt2}, "numeros": num_rows, "selo_vereditos": selo_ver_rows},
          open(os.path.join(OUT, "03_extrai.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("gravado 03_extrai.json")
