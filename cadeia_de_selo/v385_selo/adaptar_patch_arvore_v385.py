# -*- coding: utf-8 -*-
"""Reescreve o corpo do patch_arvore_indice_v385.py (gerado pelo conversor) com as ANCORAS da v384 (as linhas que a cadeia da v384 inseriu) e os textos
da v385. Backup de bytes; temporario -> conferir -> substituir; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "patch_arvore_indice_v385.py")
s0 = open(P, encoding="utf-8", newline="").read()
k = s0.index("P = os.path.join(TOOLS, 'arvore_da_prova.py')")
CORPO = r'''P = os.path.join(TOOLS, 'arvore_da_prova.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
TAG_A = '- **O AXIOMA (v385)'
if TAG_A not in s:
    backup(P)
    L = s.split('\n'); idx = [i for i, l in enumerate(L) if l.startswith("L.append('- **O PILAR QUÂNTICO (v384)")]
    assert len(idx) == 1, ('ancora v384', len(idx))
    linha = 'L.append(%s)   # v385' % repr(textos_v385.arvore_linha(V))
    assert linha.count(TAG_A) == 1
    L.insert(idx[0], linha); s = '\n'.join(L); assert s.count(TAG_A) == 1
    grava(P, s); print('arvore_da_prova.py: +linha (v385)')
else:
    print('arvore_da_prova.py: a linha v385 ja esta (idempotente)')
P = os.path.join(TOOLS, 'atlas_indice.py'); s = open(P, encoding='utf-8', newline='').read(); assert '\r' not in s
if 'v385_incorporacao_manifesto' not in s:
    backup(P)
    L = s.split('\n')

    def acha(prefixo):
        idx = [i for i, l in enumerate(L) if l.startswith(prefixo)]; assert len(idx) == 1, (prefixo, len(idx)); return idx[0]
    i = acha('_i384p = ')
    L.insert(i + 1, "_i385p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v385_incorporacao_manifesto.json'); _i385 = json.load(open(_i385p, encoding='utf-8')) if os.path.exists(_i385p) else {}   # v385")
    i = acha('verbetes = [')
    L.insert(i, '_V385TXT = %s   # v385' % repr(textos_v385.verbete(V)))
    i = acha(" ('O pilar quântico na GPU:")
    L.insert(i + 1, " (%s, _V385TXT)," % repr(textos_v385.titulo_verbete(V)))
    i = acha("       '- **O pilar quântico (v384)")
    L.insert(i + 1, '       %s,' % repr(textos_v385.remissivo(V)))
    s = '\n'.join(L)
    assert s.count('v385_incorporacao_manifesto') == 1 and s.count('_i385p') == 3 and s.count('_V385TXT') == 2, (s.count('v385_incorporacao_manifesto'), s.count('_i385p'), s.count('_V385TXT'))
    grava(P, s); print('atlas_indice.py: +manifesto +verbete +remissivo (v385)')
else:
    print('atlas_indice.py: a v385 ja esta (idempotente)')
'''
s = s0[:k] + CORPO
s = s.replace("# No molde do _v384 (ancoras = as linhas da v384)", "# No molde do _v384 (ancoras = as linhas que a cadeia da v384 inseriu: «O PILAR QUÂNTICO (v384)», _i384p, «O pilar quântico na GPU», «O pilar quântico (v384)»)")
ast.parse(s)
st = time.strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + st + "_adapt", "wb").write(s0.encode("utf-8"))
open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
print("OK patch_arvore_indice_v385.py:", len(s0), "->", len(s))
