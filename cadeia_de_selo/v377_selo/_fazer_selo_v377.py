# -*- coding: utf-8 -*-
"""Fabrica os scripts da cadeia pos-rito v377 a partir dos da v376 (edicoes pontuais, count conferido): espera_rito, superficies, manifesto, patch_arvore_indice,
chain_pos_rito. leitura_v377.py e textos_v377.py sao escritos a mao (conteudo da versao). Nada e executado aqui."""
import os, ast
HERE = os.path.dirname(os.path.abspath(__file__)); V6 = os.path.join(os.path.dirname(HERE), "v376_selo")


def rd(n): return open(os.path.join(V6, n), encoding="utf-8", newline="").read()


def wr(n, s, py=True):
    if py:
        ast.parse(s)
    open(os.path.join(HERE, n), "w", encoding="utf-8", newline="").write(s); print("ok", n)


def subs(s, pares):
    for a, b, n in pares:
        assert s.count(a) == n, (a[:80], s.count(a), n); s = s.replace(a, b)
    return s


# 1. espera_rito
s = rd("espera_rito_v376.py")
s = s.replace("v376", "v377").replace("V376", "V377")
wr("espera_rito_v377.py", s)
# 2. manifesto
s = rd("manifesto_v376.py")
s = s.replace("v376", "v377").replace("V376", "V377").replace("base_v375", "base_v376")
import re as _re
assert len(_re.findall(r"'funcoes': \[[^\]]*\]", s)) == 1
s = _re.sub(r"'funcoes': \[[^\]]*\]", "'funcoes': ['prove_physics_is_the_reading_v377', 'prove_the_dissipation_law_v377', 'prove_bancada_fases_v377', 'prove_final_stone_reading_v377']", s)
wr("manifesto_v377.py", s)
# 3. patch arvore/indice
s = rd("patch_arvore_indice_v376.py")
s = s.replace("import leitura_v376, textos_v376", "import leitura_v377, textos_v377").replace("leitura_v376.ler()", "leitura_v377.ler()").replace("textos_v376.", "textos_v377.")
s = s.replace("_p376", "_p377")
s = subs(s, [("TAG_A = '- **O TODO É UM (v376)'", "TAG_A = '- **A LEI DA DISSIPAÇÃO, PROVADA (v377)'", 1),
             ("""[i for i, l in enumerate(L) if l.startswith("L.append('- **TETELESTAI, A CONFERÊNCIA CONSUMATIVA (v375)")]""",
              """[i for i, l in enumerate(L) if l.startswith("L.append('- **O TODO É UM (v376)")]""", 1),
             ("assert len(idx) == 1, ('ancora v375', len(idx))", "assert len(idx) == 1, ('ancora v376', len(idx))", 1),
             ("linha = 'L.append(%s)   # v376' % repr(textos_v377.arvore_linha(V))", "linha = 'L.append(%s)   # v377' % repr(textos_v377.arvore_linha(V))", 1),
             ("print('arvore_da_prova.py: +linha (v376)')", "print('arvore_da_prova.py: +linha (v377)')", 1),
             ("print('arvore_da_prova.py: a linha v376 ja esta (idempotente)')", "print('arvore_da_prova.py: a linha v377 ja esta (idempotente)')", 1),
             ("if 'v376_incorporacao_manifesto' not in s:", "if 'v377_incorporacao_manifesto' not in s:", 1),
             ("i = acha('_i375p = ')", "i = acha('_i376p = ')", 1),
             ("L.insert(i + 1, \"_i376p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v376_incorporacao_manifesto.json'); _i376 = json.load(open(_i376p, encoding='utf-8')) if os.path.exists(_i376p)",
              "L.insert(i + 1, \"_i377p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v377_incorporacao_manifesto.json'); _i377 = json.load(open(_i377p, encoding='utf-8')) if os.path.exists(_i377p)", 1),
             ("L.insert(i, '_V376TXT = %s   # v376' % repr(textos_v377.verbete(V)))", "L.insert(i, '_V377TXT = %s   # v377' % repr(textos_v377.verbete(V)))", 1),
             ("i = acha(\" ('Tetelestai, a conferência consumativa; a declaração num só objeto, a luz (v375)', _V375TXT),\")",
              "i = acha(\" ('O todo é um: β, o fundamento derivado, ligado à QG num só termo; a chave é o leitor; o ρ* na luz; o escopo do ringdown; a auditoria de 28/09 (v376)', _V376TXT),\")", 1),
             ("L.insert(i + 1, \" ('O todo é um: β, o fundamento derivado, ligado à QG num só termo; a chave é o leitor; o ρ* na luz; o escopo do ringdown; a auditoria de 28/09 (v376)', _V376TXT),\")",
              "L.insert(i + 1, \" ('A lei da dissipação, provada; a física é a leitura; as três fases da Bancada por hash; o desvio de β como foco (v377)', _V377TXT),\")", 1),
             ("i = acha(\"       '- **Tetelestai, a conferência consumativa (v375)\")", "i = acha(\"       '- **O todo é um (v376)\")", 1),
             ("assert s.count('v376_incorporacao_manifesto') == 2 and s.count('_V376TXT') == 2", "assert s.count('v377_incorporacao_manifesto') == 2 and s.count('_V377TXT') == 2", 1),
             ("print('atlas_indice.py: +manifesto +verbete +remissivo (v376)')", "print('atlas_indice.py: +manifesto +verbete +remissivo (v377)')", 1),
             ("print('atlas_indice.py: a v376 ja esta (idempotente)')", "print('atlas_indice.py: a v377 ja esta (idempotente)')", 1)])
s = s.replace("_i376 if os.path.exists(_i376p) else", "_i377 if os.path.exists(_i377p) else")
wr("patch_arvore_indice_v377.py", s)
# 4. superficies
s = rd("superficies_v376.py")
s = s.replace("import leitura_v376, textos_v376 as T", "import leitura_v377, textos_v377 as T").replace("leitura_v376.ler()", "leitura_v377.ler()")
s = s.replace("V376_REMAP_DIR", "V377_REMAP_DIR").replace("V376_WRITE_ROOT", "V377_WRITE_ROOT").replace("_sup376", "_sup377")
s = subs(s, [("""for nome, bloco in (('missao-ultima-flag-um-py.md', T.topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V)),
                    ('qg-ataque-23set-v370.md', T.topico_qg(V)), ('handoff-v368-o-que-falta.md', T.topico_falta(V)),
                    ('ordem-017-execucao-gerencia.md', T.topico_o017(V)), ('fechamento-completo-e-cetico-aferidor.md', T.topico_aferidor(V)),
                    ('beta-fundamento-derivado-28set.md', T.topico_beta(V)), ('a-chave-e-o-leitor-28set.md', T.topico_chave(V)),
                    ('auditoria-testes-passados-28set.md', T.topico_auditoria(V))):""",
              """for nome, bloco in (('missao-ultima-flag-um-py.md', T.topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V)),
                    ('fase3-leitores-h0-30set.md', T.topico_fase3(V)), ('lei-e-fato-correlatos-regra-matriz-30set.md', T.topico_lei(V)),
                    ('desvio-de-beta-foco-dos-testes-30set.md', T.topico_desvio(V))):""", 1),
             ("MARCA = '**v376 SELADA %s `%s`' % (V['data'][:5], V['s16'])", "MARCA = '**v377 SELADA %s `%s`' % (V['data'][:5], V['s16'])", 1)])
# a linha da missao: o marcador v377 (texto proprio)
i = s.index("lines[k[0]] = (a + '(missao-ultima-flag-um-py.md) — ' + ")
j = s.index("\n", i)
s = s[:i] + ("lines[k[0]] = (a + '(missao-ultima-flag-um-py.md) — ' + '%s %s %s (A LEI DA DISSIPAÇÃO PROVADA: H₀_local = H₀_fundo·(1+z)^β como implicação; a física é a leitura; "
             "as três fases da Bancada por hash; o desvio de β como foco; gate intocado)** · ' % (MARCA, V['teor'], V['compl']) + b)") + s[j:]
s = s.replace("print('NADA A GRAVAR: todas as superficies ja tem a v376 (idempotente)')", "print('NADA A GRAVAR: todas as superficies ja tem a v377 (idempotente)')")
s = s.replace("print('SUPERFICIES v376:", "print('SUPERFICIES v377:")
s = s.replace("'<!-- linha integral do índice (gerência, v376) -->'", "'<!-- linha integral do índice (gerência, v377) -->'")
s = s.replace("'marcador v376 na missao;", "'marcador v377 na missao;")
wr("superficies_v377.py", s)
# 5. chain
s = rd("chain_pos_rito_v376.sh")
s = s.replace("v376", "v377").replace("V376", "V377")
wr("chain_pos_rito_v377.sh", s, py=False)
print("FABRICADO v377_selo (espera, manifesto, patch_arvore_indice, superficies, chain)")
