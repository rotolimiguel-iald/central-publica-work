# -*- coding: utf-8 -*-
"""Revisor terceiro v409 (R1): toda citacao entre « » nos textos publicos NOVOS da v409 (fontes, strings dos registros embutidos do candidato, pedras, textos rendidos do harness e artigo/md do ensaio)
e' substring exata de uma fala do operador? Corpus: cunhagens_13out (originais verbatim) + insumos/cunhagens das versoes v405-v409 (trechos). Comparacao em niveis: (1) exata (espaco normalizado); (2) exata com elisao «…»;
(3) sem acentos (docstrings Lean ASCII). O que nao passa e' listado (>= 12 chars) para classificacao manual. Tambem confere: as 14 falas de VERBATIM_CONGELADO_v409 existem em cunhagens_13out com o sha256 declarado."""
import glob, hashlib, importlib.util, json, os, re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
WK = "C:/IALD/Central de Patentes/work/"
falas = {}
for pat in (WK + "cunhagens_13out/*.txt", R + "insumos/cunhagens/*.txt", WK + "cadeia_de_selo/v408/insumos/cunhagens/*.txt", WK + "cadeia_de_selo/v407/insumos/cunhagens/*.txt", WK + "cadeia_de_selo/v406/insumos/cunhagens/*.txt", WK + "cadeia_de_selo/v405/insumos/cunhagens/*.txt"):
    for p in sorted(glob.glob(pat)):
        b = open(p, "rb").read(); falas[hashlib.sha256(b).hexdigest()[:16] + "|" + os.path.basename(p)[:70]] = b.decode("utf-8", "replace")
print("falas no corpus:", len(falas))
norm = lambda s: re.sub(r"\s+", " ", s.replace("\u2019", "'").replace("`", "").replace("\\%", "%").replace("\\_", "_")).strip()
noacc = lambda s: "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()
corpus_all = " || ".join(norm(v) for v in falas.values()); corpus_na = noacc(corpus_all)
q_rx = re.compile(r"«([^»]+)»")


def classe(q):
    qn = norm(q); alvo = qn.strip(" .,;:\u201c\u201d\"")
    segs = [x.strip(" .,;:\u201c\u201d\"") for x in re.split(r"…|\[\.\.\.\]|\.\.\.", alvo) if len(x.strip(" .,;:\u201c\u201d\"")) >= 4]
    if qn in corpus_all or alvo in corpus_all: return "exata"
    if segs and all(s in corpus_all for s in segs): return "exata_com_elisao"
    if segs and all(noacc(s) in corpus_na for s in segs): return "sem_acentos"
    return "NAO"


def strs(o, acc):
    if isinstance(o, str): acc.append(o)
    elif isinstance(o, dict):
        for k, v in o.items(): strs(v, acc)
    elif isinstance(o, (list, tuple)):
        for v in o: strs(v, acc)


rd = lambda p: open(p, "rb").read().decode("utf-8", "replace")
fontes = {}
for f in ("artigo_pt_v409.pysnip", "artigo_en_v409.pysnip", "registros_v409.py", "delta_v409.py", "runtime_v409.py", "guarda_frases_v409.py"):
    fontes[f] = rd(R + f)
for f in ("textos_v409_novo.pysnip", "textos_v409.py", "textos_custodia_handoff_v409.py", "CUSTODIA_v409_RASCUNHO.txt"):
    fontes["pos_rito/" + f] = rd(R + "pos_rito/" + f)
for p in sorted(glob.glob(R + "pedra/*.lean")): fontes["pedra/" + os.path.basename(p)] = rd(p)
for p in (R + "dry_v409/dry_v409_pt.txt", R + "dry_v409/dry_v409_en.txt", R + "dry_v409/um_absoluto_forma_canonica.md"): fontes["dry:" + os.path.basename(p)] = rd(p)
for p in sorted(glob.glob("C:/t/h409/harness_saida_v409/textos/*.txt")): fontes["harness:" + os.path.basename(p)] = rd(p)
spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v409_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev"] = m; spec.loader.exec_module(m)
for nm in ("_V409_TRADUCAO_TEXT", "_V409_SPECS", "_V409_TRADUCAO_CONTRACT"):
    acc = []; strs(getattr(m, nm), acc); fontes["reg:" + nm] = "\n".join(acc)
res = {}; todos_nao = {}
for k, t in fontes.items():
    r = [(norm(mm.group(1)), classe(mm.group(1))) for mm in q_rx.finditer(t)]
    cont = {}
    for q, c in r: cont[c] = cont.get(c, 0) + 1
    nao = sorted({q for q, c in r if c == "NAO"})
    res[k] = {"n": len(r), "por_classe": cont, "NAO": nao}
    for q in nao: todos_nao.setdefault(q, []).append(k)
    print("==", k, "n=", len(r), cont)
print("\nCitacoes NAO casadas, >= 12 chars, deduplicadas:", sum(1 for q in todos_nao if len(q) >= 12))
for q, ks in sorted(todos_nao.items(), key=lambda x: -len(x[0])):
    if len(q) >= 12: print(len(q), repr(q[:330]), "<-", sorted({x.split(":")[-1][:30] for x in ks})[:4])
# as 14 falas do VERBATIM_CONGELADO
vc = json.load(open(R + "VERBATIM_CONGELADO_v409.json", encoding="utf-8")); ok14 = []
for reg in vc["registro"]:
    p = reg["arquivo"]; existe = os.path.exists(p)
    sh = hashlib.sha256(open(p, "rb").read()).hexdigest() if existe else None
    ok14.append((os.path.basename(p)[:70], existe, sh == reg["sha256"] if existe else None, reg.get("autor")))
print("\nVERBATIM_CONGELADO:", vc["n"], "falas; registro:", len(vc["registro"]), "| todas existem e o sha256 confere:", all(x[1] and x[2] for x in ok14), "| autores:", sorted({x[3] for x in ok14}))
for x in ok14: print("   ", x)
json.dump({"por_fonte": res, "nao_casadas": {q: sorted(set(ks)) for q, ks in todos_nao.items()}, "verbatim_congelado": ok14}, open(R + "revisao_terceiro/e_citacoes_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
