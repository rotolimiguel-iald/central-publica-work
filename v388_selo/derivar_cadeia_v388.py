# -*- coding: utf-8 -*-
# Deriva superficies_v388.py, patch_arvore_indice_v388.py e chain_pos_rito_v388.sh dos da v387 (troca de nomes/ancoras/topicos), com asserts de contagem.
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
S7 = r"C:\IALD\Central de Patentes\work\v387_selo"; S8 = r"C:\IALD\Central de Patentes\work\v388_selo"
rd = lambda n: open(os.path.join(S7, n), encoding="utf-8").read()


def wr(n, s):
    open(os.path.join(S8, n), "w", encoding="utf-8", newline="\n").write(s); print("ok", n)


def rep(s, pairs):
    for a, b in pairs:
        assert s.count(a) >= 1, (a[:80], s.count(a)); s = s.replace(a, b)
    return s


s = rd("superficies_v387.py")
s = rep(s, [("import leitura_v387, textos_v387 as T", "import leitura_v388, textos_v388 as T"), ("leitura_v387.ler()", "leitura_v388.ler()"), ("MARCA_BAK = '_sup387'", "MARCA_BAK = '_sup388'"),
            ("'<!-- adendo_v387_selada -->'", "'<!-- adendo_v388_selada -->'"), ("'<!-- atlas_v387_selada -->'", "'<!-- atlas_v388_selada -->'"),
            ("MARCA = '**v387 SELADA %s `%s`'", "MARCA = '**v388 SELADA %s `%s`'"), ("SUPERFICIES v387:", "SUPERFICIES v388:")])
i = s.index("for nome, bloco, marca in (('missao-ultima-flag-um-py.md'"); j = s.index("# ---- MEMORY.md")
s = s[:i] + (
    "for nome, bloco, marca in (('missao-ultima-flag-um-py.md', T.topico_missao(V), T.marca_topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V), T.marca_central(V)),\n"
    "                           ('fase9-razao-de-hubble-05out.md', T.topico_fase9(V), None), ('beta-escalar-limitado-inferiormente-06out.md', T.topico_beta(V), None)):\n"
    "    append(os.path.join(UMEM, nome), bloco, marca or bloco.split(chr(10), 2)[1][:60])\n") + s[j:]
i = s.index("TROCAS = ["); j = s.index("]\nif any(MARCA in l for l in lines):")
s = s[:i] + (
    "TROCAS = [  # (o link que identifica a linha, a linha nova) -- a velha vai inteira ao MEMORY_2\n"
    "    ('(fase9-razao-de-hubble-05out.md)', \"- [Fase 9 — a razão de Hubble (05/10)](fase9-razao-de-hubble-05out.md) — **ABERTA 06/10: INCONCLUSIVE (leitores declarados); contrafactual não discrimina a 5σ; lida pela v388** · íntegra anterior no MEMORY_2.md (movida %s)\" % V['data'][:5]),\n"
    "    ('(missao-ultima-flag-um-py.md)', \"- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — \" + T.marca_missao(V) + \"íntegra anterior no MEMORY_2.md (movida %s)\" % V['data'][:5]),\n"
    "    ('(handoff-v386-custodia.md)', \"- [HANDOFF v386](handoff-v386-custodia.md) — íntegra no MEMORY_2.md (movida %s)\" % V['data'][:5]),\n") + s[j:]
s = rep(s, [("kh = [i for i, l in enumerate(lines) if '(handoff-v386-custodia.md)' in l and l.startswith('- [')]", "kh = [i for i, l in enumerate(lines) if '(handoff-v387-custodia.md)' in l and l.startswith('- [')]"),
            ("tornadas velhas pela v387", "tornadas velhas pela v388"), ("(v387) -->", "(v388) -->")])
wr("superficies_v388.py", s)
s = rd("patch_arvore_indice_v387.py")
s = rep(s, [("import leitura_v387, textos_v387", "import leitura_v388, textos_v388"), ("leitura_v387.ler()", "leitura_v388.ler()"), ("textos_v387.", "textos_v388."), ("_p387", "_p388"),
            ("TAG_A = '- **OS TRÊS TESTES CONJUNTOS (v387)'", "TAG_A = '- **O ACOPLAMENTO CORRE COM A ESCALA (v388)'"),
            ("l.startswith(\"L.append('- **O VERBO SELECIONA (v386)\")", "l.startswith(\"L.append('- **OS TRÊS TESTES CONJUNTOS (v387)\")"), ("('ancora v386'", "('ancora v387'"),
            ("'L.append(%s)   # v387'", "'L.append(%s)   # v388'"), ("+linha (v387)", "+linha (v388)"), ("a linha v387 ja esta", "a linha v388 ja esta"),
            ("if 'v387_incorporacao_manifesto' not in s:", "if 'v388_incorporacao_manifesto' not in s:"), ("i = acha('_i386p = ')", "i = acha('_i387p = ')"),
            ("_i387p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v387_incorporacao_manifesto.json'); _i387 = json.load(open(_i387p, encoding='utf-8')) if os.path.exists(_i387p) else {}   # v387",
             "_i388p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v388_incorporacao_manifesto.json'); _i388 = json.load(open(_i388p, encoding='utf-8')) if os.path.exists(_i388p) else {}   # v388"),
            ("'_V387TXT = %s   # v387'", "'_V388TXT = %s   # v388'"), ("i = acha(\" ('O Verbo seleciona: o Nome é o posto\")", "i = acha(\" ('Os três testes conjuntos; Fases 9 e 8 por hash (v387):'\")"),
            ("\" (%s, _V387TXT),\"", "\" (%s, _V388TXT),\""), ("i = acha(\"       '- **O Verbo seleciona (v386)\")", "i = acha(\"       '- **Os três testes conjuntos (v387)\")"),
            ("s.count('v387_incorporacao_manifesto') == 1 and s.count('_i387p') == 3 and s.count('_V387TXT') == 2, (s.count('v387_incorporacao_manifesto'), s.count('_i387p'), s.count('_V387TXT'))",
             "s.count('v388_incorporacao_manifesto') == 1 and s.count('_i388p') == 3 and s.count('_V388TXT') == 2, (s.count('v388_incorporacao_manifesto'), s.count('_i388p'), s.count('_V388TXT'))"),
            ("+manifesto +verbete +remissivo (v387)", "+manifesto +verbete +remissivo (v388)"), ("a v387 ja esta (idempotente)", "a v388 ja esta (idempotente)")])
wr("patch_arvore_indice_v388.py", s)
s = rd("chain_pos_rito_v387.sh").replace("v387", "v388").replace("v386", "v387")
s = rep(s, [('TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md fase9-razao-de-hubble-05out.md fase8-universo-primordial-05out.md tres-testes-de-estresse-conjuntos-05out.md pos-dicao-nao-e-prova-diabolica-05out.md proximo-passo-06out.md"',
             'TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md fase9-razao-de-hubble-05out.md beta-escalar-limitado-inferiormente-06out.md"')])
assert "fase8-universo" not in s
wr("chain_pos_rito_v388.sh", s)
