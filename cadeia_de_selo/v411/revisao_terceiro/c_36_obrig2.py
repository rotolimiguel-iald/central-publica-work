import sys, os, re, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
def norm(s): return "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c)).replace("’", "'")
OB = {"modelo": ("sob o modelo de erros publicado", "under the published error model", "under the error model published"),
      "cef": ("cefeidas livres", "free cepheids"), "val": ("validade, nao creditacao", "validity, not creditation", "validity not creditation"),
      "retro": ("retrodicao", "retrodiction"), "nc": ("nao e cego", "nao cego", "not blind", "nao e' cego", "is not blind")}
gat = re.compile(r"6[,.]11|provad[oa]s? na natureza|proved in nature|proved_in_nature|lido na natureza acima de 5|read in nature above 5|proved in nature at|beta_tgl_proved_in_nature", re.I)
def varre(caminho, rot):
    h = norm(rd(caminho))
    blocos = [b for b in re.split(r"\n\s*\n", h) if b.strip()]
    n = 0; falhas = []
    for i, b in enumerate(blocos):
        if gat.search(b):
            n += 1
            falta = [k for k, fs in OB.items() if not any(f in b for f in fs)]
            if falta: falhas.append((i, falta, b[:110].replace("\n", " ")))
    print(rot, "| blocos com gatilho:", n, "| com obrigatorio faltando:", len(falhas))
    for f in falhas[:8]: print("    bloco", f[0], "falta", f[1], "|", f[2])
varre(r"C:\t\k411c\ensaio_topo_proposto\pos_rito_textos\positivo\nos\HANDOFF_v411_CUSTODIA.md", "handoff S6d (positivo, Nos sintetico)")
varre(r"C:\t\k411c\ensaio_topo_proposto\pos_rito_blocos\README_PROJETADO_v411.md", "README projetado (ensaio)")
varre(r"C:\t\k411c\ensaio_topo_proposto\pos_rito\..\pos_rito_x\CUSTODIA_v411_RASCUNHO.txt" if False else V + r"\pos_rito\CUSTODIA_v411_RASCUNHO.txt", "texto do X (rascunho)")
