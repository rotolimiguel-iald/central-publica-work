# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R1): toda citacao entre « » nos textos publicos NOVOS da v407 e' substring exata de uma fala do operador (corpus: 3 de 03/11 + as de 02/11 e anteriores)?
Comparacao em tres niveis: (1) exata (espaco normalizado); (2) exata ignorando aspas curvas/pontuacao final; (3) sem acentos (para docstrings Lean em ASCII). O que nao passa em (1) e' listado para classificacao manual."""
import ast, glob, hashlib, json, os, re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
WK = "C:/IALD/Central de Patentes/work/"
falas = {}
for pat in (R + "insumos/cunhagens/*.txt", WK + "cadeia_de_selo/v406/insumos/cunhagens/*.txt", WK + "cadeia_de_selo/v405/insumos/cunhagens/*.txt", WK + "cunhagens_13out/*.txt"):
    for p in sorted(glob.glob(pat)):
        try:
            falas[hashlib.sha256(open(p, "rb").read()).hexdigest()[:16] + "|" + os.path.basename(p)[:60]] = open(p, "rb").read().decode("utf-8", "replace")
        except Exception as e:
            print("erro", p, e)
print("falas no corpus:", len(falas))
norm = lambda s: re.sub(r"\s+", " ", s.replace("\u2019", "'").replace("`", "")).strip()
noacc = lambda s: "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()
corpus = {k: norm(v) for k, v in falas.items()}
corpus_all = " || ".join(corpus.values())
corpus_na = noacc(corpus_all)
q_rx = re.compile(r"«([^»]+)»")


def classe(q):
    qn = norm(q)
    alvo = qn.strip(" .,;:\u201c\u201d\"")
    segs = [x.strip(" .,;:\u201c\u201d\"") for x in re.split(r"…|\[\.\.\.\]|\.\.\.", alvo) if len(x.strip(" .,;:\u201c\u201d\"")) >= 4]
    if qn in corpus_all or alvo in corpus_all: return "exata"
    if segs and all(s in corpus_all for s in segs): return "exata_com_elisao"
    if segs and all(noacc(s) in corpus_na for s in segs): return "sem_acentos"
    return "NAO"


def checa(texto):
    out = []
    for m in q_rx.finditer(texto):
        q = m.group(1)
        out.append((norm(q), classe(q)))
    return out


fontes = {}
rd = lambda p: open(p, "rb").read().decode("utf-8")
for f in ("artigo_pt_v407.pysnip", "artigo_en_v407.pysnip", "runtime_v407.py", "registros_v407.py", "delta_v407.py", "guarda_frases_v407.py"):
    fontes[f] = rd(R + f)
for f in ("textos_v407.py", "textos_v407_novo.pysnip", "textos_custodia_handoff_v407_03nov.py"):
    fontes["pos_rito/" + f] = rd(R + "pos_rito/" + f)
for f in sorted(glob.glob(R + "pedra/*.lean")):
    fontes["pedra/" + os.path.basename(f)] = rd(f)
cs = rd(R + "um_v407_candidato.py"); tr = ast.parse(cs); L = cs.split("\n")
for n in tr.body:
    if isinstance(n, ast.FunctionDef) and n.name in ("build_pt", "build_en", "emit_canonical_md", "psion_canto_v407", "v407_psion_mechanics", "_v407_guarda_frases", "_v407_elo_lido", "testemunha_estatica_v396", "v406_fechamento_mechanics"):
        fontes["cand:" + n.name] = "\n".join(L[n.lineno - 1:n.end_lineno])
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("_V407_PSION_TEXT", "_V407_SPECS", "_V407_PSION_CONTRACT", "_V406_SPECS", "_V407_VERBATINS2"):
        fontes["cand:" + n.targets[0].id] = "\n".join(L[n.lineno - 1:n.end_lineno])
res = {}
for k, t in fontes.items():
    r = checa(t); cont = {}
    for q, c in r: cont[c] = cont.get(c, 0) + 1
    nao = [q for q, c in r if c == "NAO"]
    res[k] = {"n": len(r), "por_classe": cont, "NAO": sorted(set(nao))}
    print("==", k, "n=", len(r), cont)
    for q in sorted(set(nao))[:40]: print("    ?", repr(q[:230]))
json.dump(res, open(R + "revisao_terceiro/r3_e_citacoes_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
