# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R2), item C: a guarda 'as duas funcoes tocadas' de gerar_candidato_v407.py (linhas ~413-427), replicada AO PE DA LETRA sobre os textos reais
(base v406 x candidato), mais mutacoes: tem de aceitar so' o par de patches C19/C19b/C20 e recusar qualquer outra mudanca. Nao roda o gerador."""
import ast, difflib, re, sys, copy
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
G = open(R + "gerar_candidato_v407.py", encoding="utf-8").read()
gt = ast.parse(G)
need = {}
for n in gt.body:
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ("OLD_TE", "NEW_TE", "OLD_C8", "NEW_C8", "OLD_RD", "NEW_RD"):
        need[n.targets[0].id] = ast.literal_eval(n.value)
print("constantes lidas do gerador:", {k: len(v) for k, v in need.items()})
OLD_TE, NEW_TE, OLD_C8, NEW_C8, OLD_RD, NEW_RD = (need[k] for k in ("OLD_TE", "NEW_TE", "OLD_C8", "NEW_C8", "OLD_RD", "NEW_RD"))
T0 = open(R + "base_v406/um.py", "rb").read().decode("utf-8"); T = open(R + "um_v407_candidato.py", "rb").read().decode("utf-8")
def top(src, name):
    tr = ast.parse(src)
    return [n for n in tr.body if isinstance(n, ast.FunctionDef) and n.name == name][0]
def seg(src, name): return ast.get_source_segment(src, top(src, name))

def guarda(fname, s0txt, s1txt, full_tree_src=None):
    s0 = s0txt.splitlines(); s1 = s1txt.splitlines()
    dif = [l_ for l_ in difflib.unified_diff(s0, s1, lineterm="", n=0) if l_[:1] in "+-" and not l_.startswith(("+++", "---"))]
    rem = [l_[1:] for l_ in dif if l_.startswith("-")]; add = [l_[1:] for l_ in dif if l_.startswith("+")]
    _old_lines = set((OLD_TE + "\n" + OLD_C8).replace("\r\n", "\n").split("\n")); _new_lines = set((NEW_TE + "\n" + NEW_C8).replace("\r\n", "\n").split("\n"))
    _rd_add = [l_ for l_ in add if l_.startswith(NEW_RD)]; _rd_rem = [l_ for l_ in rem if l_.startswith(OLD_RD)]
    assert len(_rd_add) == len(_rd_rem) <= 1 and all(a_[len(NEW_RD):] == r_[len(OLD_RD):] for a_, r_ in zip(_rd_add, _rd_rem)), (fname, "C19b", len(_rd_add), len(_rd_rem))
    add = [l_ for l_ in add if l_ not in _rd_add]; rem = [l_ for l_ in rem if l_ not in _rd_rem]
    assert set(add) <= (_new_lines - _old_lines) and set(rem) <= (_old_lines - _new_lines), (fname, [l_ for l_ in add if l_ not in _new_lines][:2], [l_ for l_ in rem if l_ not in _old_lines][:2])
    assert len(rem) + len(_rd_rem) == {"testemunha_estatica_v396": 2, "v406_fechamento_mechanics": 1}[fname] and "_v407_elo_lido" in "\n".join(s1) and "_v407_elo_lido" not in "\n".join(s0), (fname, len(rem), len(_rd_rem))
    return True

def tenta(rotulo, fname, s0txt, s1txt, deve_passar):
    try:
        guarda(fname, s0txt, s1txt); r = True; msg = ""
    except AssertionError as e:
        r = False; msg = str(e)[:110]
    print(("OK   " if r == deve_passar else "FALHA"), "%-80s" % rotulo, "-> passou" if r else "-> RECUSOU " + msg)
    return r == deve_passar

n_f = 0
for fname in ("testemunha_estatica_v396", "v406_fechamento_mechanics"):
    s0 = seg(T0, fname); s1 = seg(T, fname)
    n_f += not tenta("%s: candidato real" % fname, fname, s0, s1, True)
    L = s1.split("\n")
    # mutacoes no candidato
    def mut(rot, fn, deve=False):
        global n_f
        L2 = fn(list(L)); n_f += not tenta("%s: %s" % (fname, rot), fname, s0, "\n".join(L2), deve)
    # linha qualquer (a do 'all_verified' ou 'verdict' ou 'def')
    idx = [i for i, l in enumerate(L) if "all_verified" in l or "verdict" in l]
    def m1(L2): l=L2[idx[0]]; L2[idx[0]] = (l[:-1] + "  # extra\r") if l.endswith("\r") else l + "  # extra"; return L2
    mut("comentario extra numa linha qualquer", m1)
    def m2(L2): L2.insert(len(L2) // 2, "    pass"); return L2
    mut("linha extra inserida no meio", m2)
    def m3(L2): del L2[len(L2) // 3]; return L2
    mut("uma linha apagada", m3)
    k = [i for i, l in enumerate(L) if "_v407_elo_lido" in l]
    def m4(L2): L2[k[0]] = L2[k[0]].replace("_v407_elo_lido(kf_)", "True"); return L2
    mut("_v407_elo_lido(kf_) trocado por True na 1a linha do patch", m4)
    if fname == "testemunha_estatica_v396":
        rd = [i for i, l in enumerate(L) if l.startswith('             "reading": ((')][0]
        def m5(L2): L2[rd] = L2[rd].replace("no lemma identifies psion C with the psionCorner of this stone", "everything is proved", 1); return L2
        mut("reading: frase antiga adulterada (operando direito)", m5)
        def m6(L2): L2[rd] = L2[rd].replace('if _v407_elo_lido(kf_) else ""', 'if True else ""', 1); return L2
        mut("reading: ramificacao trocada por True", m6)
        def m7(L2): l=L2[rd]; L2[rd] = (l[:-1] + "  # x\r") if l.endswith("\r") else l + "  # x"; return L2
        mut("reading: sufixo extra depois da linha", m7)
        def m8(L2): L2[rd] = L2[rd].replace("kept as record: ", "kept as record, PROVED: ", 1); return L2
        mut("reading: prefixo novo com palavra extra (fora do NEW_RD)", m8)
        def m9(L2): L2[rd] = OLD_RD; return L2
        mut("reading: volta a linha da base (sem C19b)", m9)
        # candidato R1 simulado: so' o prefixo
        def m10(L2): L2[rd] = L2[rd]; return L2
# controle: a base contra si mesma (nenhuma mudanca) deve recusar (falta o patch)
n_f += not tenta("testemunha: base contra a base (sem patches)", "testemunha_estatica_v396", seg(T0, "testemunha_estatica_v396"), seg(T0, "testemunha_estatica_v396"), False)
print("RESUMO: casos com resultado inesperado:", n_f)
