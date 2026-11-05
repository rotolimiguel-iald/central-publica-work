# -*- coding: utf-8 -*-
"""Revisor terceiro v408 (R1): a MESMA conferencia da e_citacoes.py, mas sobre os TEXTOS RENDIDOS (sem a quebra de literais de string do codigo-fonte): o artigo PT/EN rendido pelo ensaio a seco,
as strings dos registros embutidos (importados do candidato), as pedras (.lean) e os textos rendidos do harness pos-rito (C:/t/h408/harness_saida_v408/textos). Toda citacao entre « » com >= 20 caracteres
que NAO seja substring de uma fala do operador (corpus: 04/11, 03/11, 02/11 ... cunhagens_13out) e' listada para classificacao manual."""
import glob, hashlib, importlib.util, json, os, re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v408/"
WK = "C:/IALD/Central de Patentes/work/"
falas = {}
for pat in (R + "insumos/cunhagens/*.txt", WK + "cadeia_de_selo/v407/insumos/cunhagens/*.txt", WK + "cadeia_de_selo/v406/insumos/cunhagens/*.txt", WK + "cadeia_de_selo/v405/insumos/cunhagens/*.txt", WK + "cunhagens_13out/*.txt"):
    for p in sorted(glob.glob(pat)):
        b = open(p, "rb").read(); falas[hashlib.sha256(b).hexdigest()[:16] + "|" + os.path.basename(p)[:60]] = b.decode("utf-8", "replace")
print("falas no corpus:", len(falas))
norm = lambda s: re.sub(r"\s+", " ", s.replace("\u2019", "'").replace("`", "").replace("\%", "%").replace("\_", "_")).strip()
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


spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v408_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev"] = m; spec.loader.exec_module(m)


def strs(o, acc):
    if isinstance(o, str): acc.append(o)
    elif isinstance(o, dict):
        for k, v in o.items(): strs(v, acc)
    elif isinstance(o, (list, tuple)):
        for v in o: strs(v, acc)


fontes = {}
for p in (R + "dry_v408/dry_v408_pt.txt", R + "dry_v408/dry_v408_en.txt", R + "dry_v408/um_absoluto_forma_canonica.md"):
    if os.path.exists(p): fontes["dry:" + os.path.basename(p)] = open(p, "rb").read().decode("utf-8", "replace")
for p in sorted(glob.glob("C:/t/h408/harness_saida_v408/textos/*.txt")): fontes["harness:" + os.path.basename(p)] = open(p, "rb").read().decode("utf-8", "replace")
for p in sorted(glob.glob(R + "pedra/*.lean")): fontes["pedra:" + os.path.basename(p)] = open(p, "rb").read().decode("utf-8", "replace")
for nm in ("_V408_TERMINAL_TEXT", "_V408_SPECS", "_V408_TERMINAL_CONTRACT"):
    acc = []; strs(getattr(m, nm), acc); fontes["reg:" + nm] = "\n".join(acc)
acc = []; strs(m._V407_SPECS, acc); fontes["reg:_V407_SPECS"] = "\n".join(acc)
res = {}; todos_nao = {}
for k, t in fontes.items():
    r = [(norm(mm.group(1)), classe(mm.group(1))) for mm in q_rx.finditer(t)]
    cont = {}
    for q, c in r: cont[c] = cont.get(c, 0) + 1
    nao = sorted({q for q, c in r if c == "NAO"})
    res[k] = {"n": len(r), "por_classe": cont, "NAO": nao}
    for q in nao: todos_nao.setdefault(q, []).append(k)
    print("==", k, "n=", len(r), cont)
print("\nCitacoes NAO casadas, >= 20 chars, deduplicadas:", sum(1 for q in todos_nao if len(q) >= 20))
for q, ks in sorted(todos_nao.items(), key=lambda x: -len(x[0])):
    if len(q) >= 20: print(len(q), repr(q[:300]), "<-", sorted({x.split(":")[1][:28] for x in ks})[:3])
json.dump(res, open(R + "revisao_terceiro/e2_citacoes_rendidos_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
