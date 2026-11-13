import sys, os, re, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
h = rd(r"C:\t\k411c\ensaio_topo_proposto\pos_rito_textos\positivo\nos\HANDOFF_v411_CUSTODIA.md")
m = re.search(r"<!-- INICIO_X_TEXTO_v411 -->(.*?)<!-- FIM_X_TEXTO_v411 -->", h, re.S)
x = m.group(1).strip()
print(len(x), "chars;", len(x.encode("utf-8")), "B"); print(x)
n = lambda s: "".join(c for c in unicodedata.normalize("NFKD", s.lower()) if not unicodedata.combining(c))
nx = n(x)
print("6,11:", "6,11" in nx or "6.11" in nx, "| 4,38:", "4,38" in nx or "4.38" in nx, "| modelo publicado:", "modelo de erros publicado" in nx or "published error model" in nx, "| retrodicao/nao cego:", ("retrodicao" in nx and ("nao e cego" in nx or "nao cego" in nx)) or ("retrodiction" in nx and "not blind" in nx), "| validade, nao creditacao:", "validade, nao creditacao" in nx or "validity, not creditation" in nx)
