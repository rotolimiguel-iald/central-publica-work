# -*- coding: utf-8 -*-
"""Adapta a superficies_v385.py (gerada pelo conversor): as memorias-topico da v385 (missao, central, a do posto, a do pilar) e, no indice, a linha do
pilar ganha AO LADO o caminho do marcador do servidor no pacote v385 (o texto antigo fica). Pares (antigo, novo) contados; backup de bytes; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "superficies_v385.py")
s0 = open(P, encoding="utf-8", newline="").read(); s = s0
T = []
T.append(("""for nome, bloco, marca in (('missao-ultima-flag-um-py.md', T.topico_missao(V), T.marca_topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V), T.marca_central(V)),
                           ('beta-e-a-regra-matriz-02out.md', T.topico_regra(V), None), ('regra-dos-dois-regimes.md', T.topico_regimes(V), None),
                           ('v382-custodia-suspensa.md', T.topico_suspensao(V), None), ('v384-pilar-quantico-gpu-02out.md', T.topico_pilar(V), None)):""",
"""# v385: as memorias-topico que esta versao toca: a missao, o estado da Central, a do POSTO (as palavras do operador de 05/10 ligadas a pedra) e a do PILAR
# (a segunda rodada sob o mesmo V1 e a reprodutibilidade; a regra do marcador do servidor passa ao pacote v385)
for nome, bloco, marca in (('missao-ultima-flag-um-py.md', T.topico_missao(V), T.marca_topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V), T.marca_central(V)),
                           ('um-posto-jamais-pressuposto-e-h2-17set.md', T.topico_posto(V), None), ('v384-pilar-quantico-gpu-02out.md', T.topico_pilar(V), None)):"""))
T.append(("""    assert MARCA in lines[k[0]]
""", """    assert MARCA in lines[k[0]]
    # (3) v385: a linha do PILAR no indice ganha, AO LADO, o marcador do servidor no pacote v385 (o caminho antigo fica, como registro)
    kp = [i for i, l in enumerate(lines) if '(v384-pilar-quantico-gpu-02out.md) — ' in l]; assert len(kp) == 1, ('linha do pilar', len(kp))
    if MARCA_PILAR not in lines[kp[0]]:
        lines[kp[0]] = lines[kp[0]] + MARCA_PILAR
"""))
T.append(("""FOLGA_HANDOFF = len((T.linha_handoff(V) + '\\n').encode('utf-8'))""",
          """FOLGA_HANDOFF = len((T.linha_handoff(V) + '\\n').encode('utf-8'))
MARCA_PILAR = (' · **v385 (%s): o marcador agora é `%s`**' % (V['data'][:5], os.path.join(A.PK, '.servidor_parado_pelo_rito')))"""))
T.append(("""# memorias-topico (missao-ultima-flag-um-py, central-de-patentes-estado, beta-e-a-regra-matriz-02out, regra-dos-dois-regimes, v382-custodia-suspensa""",
          """# memorias-topico (v385: missao-ultima-flag-um-py, central-de-patentes-estado, um-posto-jamais-pressuposto-e-h2-17set, v384-pilar-quantico-gpu-02out;
# na v384 eram: missao-ultima-flag-um-py, central-de-patentes-estado, beta-e-a-regra-matriz-02out, regra-dos-dois-regimes, v382-custodia-suspensa"""))
for a, b in T:
    n = s.count(a)
    assert n == 1, ("a troca nao e unica", n, a[:100])
    s = s.replace(a, b)
ast.parse(s)
st = time.strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + st + "_adapt", "wb").write(s0.encode("utf-8"))
open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); assert os.path.getsize(P + ".tmp") > len(s0.encode("utf-8")); os.replace(P + ".tmp", P)
print("OK superficies_v385.py: %d trocas" % len(T))
