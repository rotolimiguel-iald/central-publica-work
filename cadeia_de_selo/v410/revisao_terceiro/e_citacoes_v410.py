# -*- coding: utf-8 -*-
"""Revisor terceiro v410 (R1): toda citacao entre « » nos textos publicos NOVOS da v410 e' substring exata de uma fala do operador?
Fontes: (a) literais _V410_* do candidato (literais_v410.json, por ast.literal_eval); (b) as pedras (.lean: insumos/*.lean, pedra/*.lean, e a R2_aspas); (c) artigo/pysnips; (d) textos RENDIDOS
(dry_v410_pt/en.txt, forma canonica .md, harness C:/t/h410/harness_saida_v410/textos); (e) pos_rito textos. Corpus: cunhagens_13out + v410/insumos/cunhagens + versoes anteriores.
Niveis: exata (espaco normalizado), exata com elisao, sem acentos. O que nao passa e' listado (>= 12 chars) para classificacao manual. Tambem: as falas de VERBATIM_CONGELADO_v410 existem com o sha256."""
import glob, hashlib, json, os, re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
WK = "C:/IALD/Central de Patentes/work/"
falas = {}
for pat in (WK + "cunhagens_13out/*.txt", R + "insumos/cunhagens/*.txt", WK + "cadeia_de_selo/v409/insumos/cunhagens/*.txt", WK + "cadeia_de_selo/v408/insumos/cunhagens/*.txt", WK + "cadeia_de_selo/v407/insumos/cunhagens/*.txt",
            WK + "cadeia_de_selo/v406/insumos/cunhagens/*.txt", WK + "cadeia_de_selo/v405/insumos/cunhagens/*.txt"):
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
lit = json.load(open(R + "revisao_terceiro/literais_v410.json", encoding="utf-8"))
for nm, v in lit.items():
    if nm in ("_V410_H0DN_INSUMOS", "_V410_HMS13_INSUMOS"): continue
    acc = []; strs(v, acc); fontes["reg:" + nm] = "\n".join(acc)
for f in ("artigo_pt_v410.pysnip", "artigo_en_v410.pysnip", "artigo_pt_aescala_v410.pysnip", "artigo_en_aescala_v410.pysnip", "artigo_pt_h0dn_v410.pysnip", "artigo_en_h0dn_v410.pysnip",
          "registros_v410.py", "registros_h0dn_v410.py", "registros_aescala_v410.py", "registros_hms13_v410.py", "delta_v410.py", "runtime_v410.py", "runtime_h0dn_v410.py", "runtime_aescala_v410.py", "runtime_hms13_v410.py", "guarda_frases_v410.py"):
    fontes[f] = rd(R + f)
for f in ("textos_v410.semente", "textos_v410.py", "textos_custodia_handoff_v410.py", "CUSTODIA_v410_RASCUNHO.txt", "leitura_v410.py"):
    if os.path.exists(R + "pos_rito/" + f): fontes["pos_rito/" + f] = rd(R + "pos_rito/" + f)
for p in sorted(glob.glob(R + "pedra/*.lean")) + sorted(glob.glob(R + "insumos/AEscala.lean")) + sorted(glob.glob(R + "insumos/IALD2.lean")) + sorted(glob.glob(WK + "pedras_candidatas_09nov/R6_a_constante_da_escala/*.lean")):
    fontes["pedra:" + p.replace(WK, "")] = rd(p)
for p in (R + "dry_v410/dry_v410_pt.txt", R + "dry_v410/dry_v410_en.txt"):
    if os.path.exists(p): fontes["dry:" + os.path.basename(p)] = rd(p)
for p in glob.glob(R + "dry_v410/*.md"): fontes["dry:" + os.path.basename(p)] = rd(p)
for p in sorted(glob.glob("C:/t/h410/harness_saida_v410/textos/*.txt")): fontes["harness:" + os.path.basename(p)] = rd(p)
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
    if len(q) >= 12: print(len(q), repr(q[:330]), "<-", sorted({x.split(":")[-1][:34] for x in ks})[:4])
vc = json.load(open(R + "VERBATIM_CONGELADO_v410.json", encoding="utf-8")); ok14 = []
for reg in vc["registro"]:
    p = reg["arquivo"]; existe = os.path.exists(p)
    sh = hashlib.sha256(open(p, "rb").read()).hexdigest() if existe else None
    ok14.append((os.path.basename(p)[:70], existe, sh == reg["sha256"] if existe else None, reg.get("autor")))
print("\nVERBATIM_CONGELADO:", vc["n"], "falas; registro:", len(vc["registro"]), "| todas existem e o sha256 confere:", all(x[1] and x[2] for x in ok14), "| autores:", sorted({str(x[3]) for x in ok14}))
for x in ok14: print("   ", x)
json.dump({"por_fonte": res, "nao_casadas": {q: sorted(set(ks)) for q, ks in todos_nao.items()}, "verbatim_congelado": ok14}, open(R + "revisao_terceiro/e_citacoes_v410_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
