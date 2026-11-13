"""CU-C3: a guarda_frases_v411.violacoes() sobre o texto INTEIRO do artigo novo e do v410 selado (txt e tex, PT e EN): os paragrafos que a guarda acusa no novo sao os mesmos (por titulo/abertura) que ja' acusava no v410?"""
import os, re, sys, unicodedata
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
D = r"C:\t\k411c\dry_v411"
sys.dont_write_bytecode = True
sys.path.insert(0, V)
import guarda_frases_v411 as G
rd = lambda p: open(p, "rb").read().decode("utf-8").replace("\r\n", "\n")
PAR = re.compile(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*")


def chave(p):
    s = re.sub(r"[^\w]+", " ", unicodedata.normalize("NFC", p[:120]).lower()).strip()
    return s[:60]


for nm, novo, velho in (("pt_txt", "dry_v411_pt.txt", "um_absoluto_pt.txt"), ("en_txt", "dry_v411_en.txt", "um_absoluto_en.txt"), ("pt_tex", "dry_v411_pt.tex", "um_absoluto_pt.tex"), ("en_tex", "dry_v411_en.tex", "um_absoluto_en.tex")):
    tn, tv = rd(os.path.join(D, novo)), rd(os.path.join(NOS, velho))
    fn, fv = {}, {}
    for tx, dd in ((tn, fn), (tv, fv)):
        for m in PAR.finditer(tx):
            p = m.group(0)
            if len(p) > 60000:
                continue
            v = G.violacoes(p)
            if v:
                dd.setdefault(chave(p), []).append(tuple(sorted({x[0][:30] for x in v})))
    so_novo = [k for k in fn if k not in fv]
    mais = [k for k in fn if k in fv and len(fn[k]) > len(fv[k])]
    # regras diferentes para a mesma abertura
    difrg = [k for k in fn if k in fv and sorted(fn[k]) != sorted(fv[k])]
    print("==", nm, "| paragrafos acusados no novo:", sum(len(v) for v in fn.values()), "| no v410:", sum(len(v) for v in fv.values()), "| abertura acusada so' no novo:", len(so_novo), "| mais ocorrencias no novo:", len(mais), "| regras diferentes:", len(difrg))
    for k in so_novo[:10]:
        print("   SO NO NOVO:", k, fn[k])
    for k in difrg[:6]:
        print("   REGRAS:", k, fn[k], "x v410", fv[k])
