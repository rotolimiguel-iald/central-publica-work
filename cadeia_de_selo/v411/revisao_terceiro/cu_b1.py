"""CU-B1: a D181 por meio proprio (nao importa guarda_conversa_v411). Nunca imprime nem grava o texto de uma fala: so' indice, sha16 da linha, alvo, posicao, contagens."""
import ast, hashlib, json, os, re, sys, unicodedata, time
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
OUTD = r"C:\t\k411c\revisao_CU"
sha256 = lambda b: hashlib.sha256(b).hexdigest()
h16 = lambda s: hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]
# ---- as falas
VC = json.load(open(os.path.join(V, "VERBATIM_CONGELADO_v411.json"), encoding="utf-8"))
falas = []   # (idx, label, path, text, sha_ok)
for i, r in enumerate(VC["registro"]):
    p = r["arquivo"]
    raw = open(p, "rb").read()
    ok = sha256(raw) == r["sha256"]
    falas.append((i, "fala%02d" % i, p, raw.decode("utf-8-sig"), ok))
CUN = r"C:\IALD\Central de Patentes\work\cunhagens_13out"
D181_SHA = "93d812a00da1c8a613005115803bb55a4833ec4299159f35de132df01938a59a"
d181 = []
for f in os.listdir(CUN):
    pf = os.path.join(CUN, f)
    if os.path.isfile(pf) and os.path.getsize(pf) < 100000 and sha256(open(pf, "rb").read()) == D181_SHA:
        d181.append(f)
print("falas lidas:", len(falas), "sha ok:", [f[4] for f in falas].count(True))
print("D181: arquivos com o sha256 dado:", len(d181))
if d181:
    p = os.path.join(CUN, d181[0])
    raw = open(p, "rb").read()
    falas.append((11, "d181", p, raw.decode("utf-8-sig"), True))
fora = VC["fora_do_desenho"]
for j, nm in enumerate(fora):
    p = os.path.join(CUN, nm)
    if os.path.exists(p):
        raw = open(p, "rb").read()
        falas.append((12 + j, "fora%d" % j, p, raw.decode("utf-8-sig"), None))
print("total de alvos-agulha:", len(falas), [f[1] for f in falas])


# ---- agulhas
def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s)).strip()


def toks(s):
    return re.findall(r"\w+", unicodedata.normalize("NFC", s).lower())


NEEDLES = []   # (idx, kind, text)
WIN = {}       # janela -> set(idx)
NAMES = []
for i, lab, p, t, ok in falas:
    tn = norm(t)
    NEEDLES.append((i, "inteiro", t.strip()))
    NEEDLES.append((i, "inteiro_norm", tn))
    seen = set()
    for ln in t.splitlines():
        for sent in re.split(r"(?<=[.!?\u2026])\s+", ln):
            s = norm(sent)
            if len(s) >= 24 and s not in seen:
                seen.add(s)
                NEEDLES.append((i, "linha_frase24", s))
    tk = toks(t)
    for k in range(len(tk) - 5):
        WIN.setdefault(" ".join(tk[k:k + 6]), set()).add(i)
    nm = os.path.basename(p)
    NAMES.append((i, nm))
    NAMES.append((i, nm[:-4] if nm.endswith(".txt") else nm))
NAMES = list({(i, n) for i, n in NAMES})
FIRST = {w.split(" ", 1)[0] for w in WIN}
print("agulhas: inteiros", sum(1 for n in NEEDLES if n[1].startswith("inteiro")), "linhas/frases>=24:", sum(1 for n in NEEDLES if n[1] == "linha_frase24"), "janelas de 6 palavras:", len(WIN), "nomes:", len(NAMES))


def formas(s):
    out = {"cru": s, "json_ascii": json.dumps(s, ensure_ascii=True)[1:-1], "json_utf8": json.dumps(s, ensure_ascii=False)[1:-1],
           "repr": repr(s)[1:-1], "ascii_repr": ascii(s)[1:-1], "uesc": s.encode("unicode_escape").decode("ascii")}
    out["uesc_upper"] = re.sub(r"\\u([0-9a-f]{4})", lambda m: "\\u" + m.group(1).upper(), out["json_ascii"])
    return out


def lin_de(texto, pos):
    return texto.count("\n", 0, pos) + 1


def varrer(label, texto, base_texto, extra_streams=None, topo_win=None):
    res = {"alvo": label, "chars": len(texto), "ocorrencias": [], "nomes": [], "janelas_excedentes": []}
    streams = [("texto", texto)] + (extra_streams or [])
    for i, kind, n in NEEDLES:
        for fk, fs in formas(n).items():
            if not fs:
                continue
            achou = False
            for sn, st in streams:
                pos = st.find(fs)
                if pos >= 0:
                    res["ocorrencias"].append({"fala": i, "tipo": kind, "forma": fk, "stream": sn, "linha": lin_de(st, pos), "pos": pos, "sha16_agulha": h16(n), "len": len(n),
                                               "n_no_alvo": st.count(fs), "n_na_base": base_texto.count(fs) if base_texto else None})
                    achou = True
                    break
            if achou:
                break
    for i, n in NAMES:
        for sn, st in streams:
            c = st.count(n)
            if c:
                res["nomes"].append({"fala": i, "nome_sha16": h16(n), "stream": sn, "n_no_alvo": c, "n_na_base": base_texto.count(n) if base_texto else None})
    res["radical_OPERADOR_1xnov_alvo"] = len(re.findall(r"OPERADOR_1[0-2]nov", texto))
    res["radical_OPERADOR_1xnov_base"] = len(re.findall(r"OPERADOR_1[0-2]nov", base_texto)) if base_texto else None

    def contar(st):
        cnt = {}
        first = {}
        tk = toks(st)
        for k in range(len(tk) - 5):
            if tk[k] in FIRST:
                w = " ".join(tk[k:k + 6])
                if w in WIN:
                    cnt[w] = cnt.get(w, 0) + 1
                    first.setdefault(w, k)
        return cnt, first, len(tk)

    cn, fn, ntk = contar("\n".join(st for _, st in streams))
    cb, _, ntb = contar(base_texto) if base_texto else ({}, {}, 0)
    # os streams extras do alvo repetem o mesmo conteudo: a contagem do alvo e' feita so' no primeiro stream quando ha extras identicos em substancia
    if extra_streams:
        cn1, fn1, _ = contar(streams[0][1])
        cn2, fn2, _ = contar("\n".join(st for _, st in streams[1:]))
        cn = {w: max(cn1.get(w, 0), cn2.get(w, 0)) for w in set(cn1) | set(cn2)}
        fn = {w: fn1.get(w, fn2.get(w)) for w in cn}
    res["tokens_alvo"] = ntk
    res["tokens_base"] = ntb
    res["janelas_distintas_no_alvo"] = len(cn)
    res["janelas_distintas_na_base"] = len(cb)
    exc = [(w, c, cb.get(w, 0)) for w, c in cn.items() if c > cb.get(w, 0)]
    res["n_janelas_excedentes"] = len(exc)
    for w, c, b in exc:
        res["janelas_excedentes"].append({"fala": sorted(WIN[w]), "sha16": h16(w), "n_alvo": c, "n_base": b, "pos_token": fn[w], "no_topo": (w in topo_win) if topo_win is not None else None})
    return res


# ---- topo ratificado: janelas
topo = json.load(open(os.path.join(V, "TOPO_RATIFICADO_v411.json"), encoding="utf-8"))


def strs(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from strs(k)
            yield from strs(v)
    elif isinstance(x, (list, tuple)):
        for v in x:
            yield from strs(v)


TOPO_STR = "\n".join(strs(topo))
tk = toks(TOPO_STR)
TOPO_WIN = {" ".join(tk[k:k + 6]) for k in range(len(tk) - 5)}
alvos = {}


def rd(p):
    return open(p, "rb").read().decode("utf-8", errors="replace")


t0 = time.time()
csrc = rd(os.path.join(V, "um_v411_candidato.py"))
bsrc = rd(os.path.join(NOS, "um.py"))


def ast_strs(src):
    t = ast.parse(src)
    out = []
    for n in ast.walk(t):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and len(n.value) < 5000:
            out.append(n.value)
    return "\n".join(out)


cast_ = ast_strs(csrc)
bast_ = ast_strs(bsrc)
print("candidato lido, AST decodificado", len(cast_), "| base", len(bast_), "| %.0fs" % (time.time() - t0))
sys.stdout.flush()
alvos["1_candidato_fonte"] = varrer("candidato (texto cru + strings decodificadas do AST)", csrc, bsrc + "\n" + bast_, [("ast_strings", cast_)], TOPO_WIN)
print("1 ok | %.0fs" % (time.time() - t0))
sys.stdout.flush()
cj = json.load(open(r"C:\t\k411c\dry_v411\core_ensaio.json", encoding="utf-8"))["core"]
bj = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]
cs = "\n".join(strs(cj))
bs = "\n".join(strs(bj))
cs_j = " ".join(strs(cj))
alvos["2_core_ensaio"] = varrer("core do ensaio (todas as cadeias, chaves incluidas)", cs, bs, [("juncao_por_espaco", cs_j)], TOPO_WIN)
print("2 ok | %.0fs" % (time.time() - t0))
sys.stdout.flush()
for nm, a, b in (("3a_artigo_pt_tex", r"C:\t\k411c\dry_v411\dry_v411_pt.tex", "um_absoluto_pt.tex"), ("3b_artigo_pt_txt", r"C:\t\k411c\dry_v411\dry_v411_pt.txt", "um_absoluto_pt.txt"),
                 ("3c_artigo_en_tex", r"C:\t\k411c\dry_v411\dry_v411_en.tex", "um_absoluto_en.tex"), ("3d_artigo_en_txt", r"C:\t\k411c\dry_v411\dry_v411_en.txt", "um_absoluto_en.txt"),
                 ("4_forma_canonica", r"C:\t\k411c\falso_nos_v411\um_absoluto_forma_canonica.md", "um_absoluto_forma_canonica.md"),
                 ("5_manifesto", r"C:\t\k411c\falso_nos_v411\um_absoluto_manifest.md", "um_absoluto_manifest.md"),
                 ("6_saida_do_rito", r"C:\t\k411c\falso_nos_v411\rodada_v411_stdout.txt", "rodada_v410_stdout.txt")):
    alvos[nm] = varrer(nm, rd(a), rd(os.path.join(NOS, b)), None, TOPO_WIN)
    print(nm, "ok | %.0fs" % (time.time() - t0))
    sys.stdout.flush()
json.dump({"falas": [(f[0], f[1], f[4]) for f in falas], "alvos": alvos}, open(os.path.join(OUTD, "b1_resultado.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, r in alvos.items():
    print("==", k, "chars", r["chars"], "| ocorrencias:", len(r["ocorrencias"]), "| nomes:", len(r["nomes"]), "| radical alvo/base:", r["radical_OPERADOR_1xnov_alvo"], r["radical_OPERADOR_1xnov_base"],
          "| janelas distintas alvo/base:", r["janelas_distintas_no_alvo"], r["janelas_distintas_na_base"], "| EXCEDENTES:", r["n_janelas_excedentes"], "(no topo:", sum(1 for j in r["janelas_excedentes"] if j["no_topo"]), ")")
    for o in r["ocorrencias"][:8]:
        print("   OCOR", {k2: o[k2] for k2 in ("fala", "tipo", "forma", "stream", "linha", "n_no_alvo", "n_na_base", "sha16_agulha", "len")})
    for o in r["nomes"][:8]:
        print("   NOME", o)
