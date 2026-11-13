from b_lib import *
import re, glob, os
CUN = r"C:\IALD\Central de Patentes\work\cunhagens_13out"
WK = r"C:\IALD\Central de Patentes\work"
files = glob.glob(CUN + r"\*OPERADOR_*.txt")
for d in ("cinco_sigma_fora_da_cosmologia_27out", "projecao_transversal_28out", "transicao_para_a_massa_28out", "experimento_espelho_30out", "e0_cadeia_31out", "observador_terminal_31out"):
    files += glob.glob(WK + "\\" + d + r"\*OPERADOR_*.txt")
nrm = lambda s: " ".join(s.replace("\r\n", "\n").split())
corp = {os.path.basename(f): nrm(open(f, "rb").read().decode("utf-8", "replace")) for f in files}
print("arquivos de falas:", len(corp))
d = json.load(open(SC + r"\b09c_blocos.json", encoding="utf-8"))
rx = re.compile(r"«([^«»]+)»")
tot = 0; bad = []
for lang in ("pt", "en"):
    for blk in d[lang]:
        for p in blk["new"]:
            for m in rx.finditer(p):
                c = nrm(m.group(1)); tot += 1
                src = [n for n, t in corp.items() if c in t]
                if not src: bad.append((lang, c[:140], p[:60]))
print("citacoes angulares em paragrafos novos/alterados (PT+EN):", tot, " sem fonte byte-a-byte:", len(bad))
for b in bad: print("   ", b)
# md new lines
old = set(l.rstrip("\r") for l in rd(NOS + r"\um_absoluto_forma_canonica.md").split("\n"))
totm = 0; badm = []
for l in md().split("\n"):
    l = l.rstrip("\r")
    if l in old or not l.strip(): continue
    for m in rx.finditer(l):
        c = nrm(m.group(1)); totm += 1
        if not any(c in t for t in corp.values()): badm.append(c[:140])
print("md novas:", totm, "sem fonte:", badm)
# the fala do autor vs file
T = json.loads(rd(V + r"\TOPO_RATIFICADO_v411.json"))
fa = T["fala_do_autor_para_o_quadro"]; arq = open(fa["arquivo"], "rb").read().decode("utf-8")
print("trecho_verbatim in arquivo (bytes):", fa["trecho_verbatim"] in arq, "| sha256 arquivo == declarado:", __import__("hashlib").sha256(open(fa["arquivo"], "rb").read()).hexdigest() == fa["sha256"])
print("arquivo da fala:", repr(arq))
# the rendering has the quote exactly?
for nm, tx in (("pt", pt()), ("en", en()), ("md", md())):
    print(nm, "citacao no rendido:", fa["trecho_verbatim"] in tx)
