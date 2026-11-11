import sys, re, json
sys.stdout.reconfigure(encoding="utf-8")
from cu_corpus import *
C = carregar()
RX = re.compile(r"leitura do operador|leitura dele|operator[’']s reading|reading of the operator|his reading|\[ONTO[^\]]*\]|\[INPUT/ONTO\]|\[dicionário; leitura|\[dictionary; the operator", re.I)
def segs(t):
    # segmentos pela pontuacao forte, para comparar por sentenca
    return [s.strip() for s in re.split(r"(?<=[.;:])\s+", ws(t)) if s.strip()]
res = {}
for k in ("pt", "en", "md"):
    novo = rd("novo_%s.txt" % k); velho = rd("cu_saidas/novo_%s.R3.txt" % k)
    sv = set(segs(velho)); sn = segs(novo)
    nao_estava = [s for s in sn if s not in sv]
    hits = [s for s in nao_estava if RX.search(s)]
    res[k] = (len(sn), len(nao_estava), hits)
    print("==", k, "segmentos:", len(sn), "| novos desde a R3:", len(nao_estava), "| com rotulo da regra do nome:", len(hits))
    for h in hits[:20]: print("    >", h[:420])
# registros: folhas do registro (v410) e do harness novos desde a R3 nao tenho: usar a assinatura 'R6' / D108..D123 nas folhas
REG = todos_registros(C)
print()
quais = [(p, t) for p, t in REG if re.search(r"D108|D113|D116|D117|D118|D119|D12[0-3]|R6", t) and RX.search(t)]
print("folhas de registro que citam D108..D123/R6 e trazem rotulo:", len(quais))
for p, t in quais[:25]:
    m = RX.search(t); print("   ", p, "::", ctx(t, m, 140))
