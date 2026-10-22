# -*- coding: utf-8 -*-
"""Adapta o chain_pos_rito_v385.sh (memorias-topico da v385; as linhas [v384] do pilar E as [v385]; o cabecalho datado) e o compactar_memory_para_v385.py
(a folga pedida inclui a marca do pilar que a superficies_v385 poe ao lado). Pares contados; backup de bytes."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
st = time.strftime("%Y%m%d_%H%M%S")


def aplica(nome, pares, py=True):
    P = os.path.join(HERE, nome)
    s0 = open(P, encoding="utf-8", newline="").read(); s = s0
    for a, b in pares:
        n = s.count(a)
        assert n == 1, (nome, "a troca nao e unica", n, a[:100])
        s = s.replace(a, b)
    if py:
        ast.parse(s)
    open(P + ".bak_" + st + "_adapt", "wb").write(s0.encode("utf-8"))
    open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
    print("OK", nome, len(pares), "trocas")


aplica("chain_pos_rito_v385.sh", [
    ('TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md beta-e-a-regra-matriz-02out.md regra-dos-dois-regimes.md v382-custodia-suspensa.md v384-pilar-quantico-gpu-02out.md"',
     'TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md um-posto-jamais-pressuposto-e-h2-17set.md v384-pilar-quantico-gpu-02out.md"'),
    ('grep -n "\\[v384\\]" "$STD" | grep -v "em curso" | cut -c1-260',
     'grep -n -E "\\[v38[45]\\]" "$STD" | grep -v "em curso" | cut -c1-260   # v385: as do pilar seguem [v384] (o codigo e\' o da v384); as novas sao [v385]'),
    ('# v385 (04/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v384.sh.',
     '# v385 (05/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v384.sh (gerada pelo converter_cadeia_v385.py e adaptada a mao: as memorias-topico e as linhas [v38x]).'),
    ('por ensaio_guardas_v385.py (04/10, corretor).', 'por ensaio_guardas_v384.py (04/10, corretor; na v385 o ensaio da cadeia e\' o ensaio_v385.py).'),
], py=False)
aplica("compactar_memory_para_v385.py", [
    ("    precisa = len(T.marca_missao(V).encode('utf-8')) + len((T.linha_handoff(V) + '\\n').encode('utf-8')) + MARGEM\n"
     "    origem = 'lida dos textos da v385 (marcador da missão + linha do handoff) + %d B de margem' % MARGEM",
     "    _mp = (' · **v385 (%s): o marcador agora é `%s`**' % (V['data'][:5], os.path.join(A.PK, '.servidor_parado_pelo_rito')))   # a MESMA da superficies_v385\n"
     "    precisa = len(T.marca_missao(V).encode('utf-8')) + len((T.linha_handoff(V) + '\\n').encode('utf-8')) + len(_mp.encode('utf-8')) + MARGEM\n"
     "    origem = 'lida dos textos da v385 (marcador da missão + linha do handoff + a marca do pilar) + %d B de margem' % MARGEM"),
])
