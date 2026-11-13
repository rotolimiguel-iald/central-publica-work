"""CU-F3: toda ocorrencia do primario nos textos do pos-rito leva a linha das Cefeidas livres (com o numero) no MESMO item (paragrafo, linha de tabela ou item de lista)."""
import json, os, re, sys
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
sys.dont_write_bytecode = True
sys.path.insert(0, V)
import guarda_frases_v411 as G
rd = lambda p: open(p, "rb").read().decode("utf-8", errors="replace").replace("\r\n", "\n")
OCC = re.compile(r"6[,.]11|above\s+5\s*[\u03c3]|acima\s+de\s+5\s*[\u03c3]|provad[oa]\s+na\s+natureza|proved\s+in\s+nature|PROVED_IN_NATURE|read\s+in\s+nature|lido\s+na\s+natureza|Z\$?\s+(?:contra\s+o\s+nulo|against\s+the\s+null)|AT_?6SIGMA", re.I)
CL = re.compile(r"(?:Cefeidas\s+livres|free\s+Cepheids)[^\n]{0,260}?(?:\d+(?:\{,\}|[,.])\d+|abaixo\s+de\s+5|below\s+5)", re.I)
PAR = re.compile(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*")


def strs(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from strs(v)
    elif isinstance(x, list):
        for v in x:
            yield from strs(v)


fontes = {
    "readme_projetado": rd(r"C:\t\k411c\ensaio_topo_proposto\pos_rito_blocos\README_PROJETADO_v411.md"),
    "handoff_de_ensaio": rd(r"C:\t\k411c\ensaio_topo_proposto\pos_rito_blocos\HANDOFF_v411_CUSTODIA.md"),
    "rascunho_do_X": rd(os.path.join(V, "pos_rito", "CUSTODIA_v411_RASCUNHO.txt")),
}
PR = json.load(open(os.path.join(V, "PRONTO_POS_RITO_v411.json"), encoding="utf-8"))
for k, v in (PR.get("textos_da_custodia") or {}).get("renderizados_no_ensaio", {}).items():
    fontes["pronto/" + k] = v if isinstance(v, str) else "\n".join(strs(v))
H = json.load(open(os.path.join(V, "pos_rito", "HARNESS_TEXTOS_ENSAIO_v411.json"), encoding="utf-8"))
for i, s in enumerate(strs(H)):
    if len(s) > 200:
        fontes["harness/str%d" % i] = s
tot_occ = tot_viol = 0
for nome, tx in fontes.items():
    itens = []
    for m in PAR.finditer(tx):
        p = m.group(0)
        # um paragrafo com varias linhas de tabela ou de lista: cada linha e' um item
        linhas = p.split("\n")
        if len(linhas) > 1 and sum(1 for l in linhas if l.lstrip().startswith(("|", "- ", "* ", "> -", ">  -"))) >= 2:
            itens += [(m.start(), l) for l in linhas]
        else:
            itens.append((m.start(), p))
    n_occ = 0
    viol = []
    for pos, it in itens:
        if OCC.search(it):
            n_occ += 1
            if not CL.search(it):
                viol.append((pos, len(it), it[:110].replace("\n", " ")))
    gv = [x[0][:30] for it in (i[1] for i in itens) for x in G.violacoes(it)]
    tot_occ += n_occ
    tot_viol += len(viol)
    print("%-42s itens %4d | com o primario %3d | SEM as Cefeidas livres+numero %2d | guarda_frases acusa %d" % (nome, len(itens), n_occ, len(viol), len(gv)))
    for v in viol[:6]:
        print("     ", v)
    for x in gv[:3]:
        print("      GUARDA", x)
print("TOTAL: ocorrencias do primario", tot_occ, "| sem as Cefeidas livres", tot_viol)
