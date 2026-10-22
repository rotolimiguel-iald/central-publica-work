# -*- coding: utf-8 -*-
"""Fabrica os scripts da cadeia pos-rito v379 a partir dos da v378 (edicoes pontuais, count conferido): espera_rito, manifesto, superficies, chain_pos_rito.
leitura_v379.py, textos_v379.py, patch_arvore_indice_v379.py, handoff_v379.py e registrar_resultado_v379.py sao escritos a mao. Nada e executado aqui."""
import os, ast, re
HERE = os.path.dirname(os.path.abspath(__file__)); V8 = os.path.join(os.path.dirname(HERE), "v378_selo")


def rd(n): return open(os.path.join(V8, n), encoding="utf-8", newline="").read()


def wr(n, s, py=True):
    if py:
        ast.parse(s)
    open(os.path.join(HERE, n), "w", encoding="utf-8", newline="").write(s); print("ok", n)


def subs(s, pares):
    for a, b, n in pares:
        assert s.count(a) == n, (a[:80], s.count(a), n); s = s.replace(a, b)
    return s


# 1. espera_rito (o vigia fail-closed ja esta no v378)
s = rd("espera_rito_v378.py")
s = s.replace("v378", "v379").replace("V378", "V379")
wr("espera_rito_v379.py", s)
# 2. manifesto
s = rd("manifesto_v378.py")
s = s.replace("v378", "v379").replace("V378", "V379").replace("base_v377", "base_v378")
assert len(re.findall(r"'funcoes': \[[^\]]*\]", s)) == 1
s = re.sub(r"'funcoes': \[[^\]]*\]", "'funcoes': ['prove_the_elementary_reason_v379']", s)
i = s.index("'contraste': {"); j = s.index("'conferencia_v376_pinada': {")
s = s[:i] + ("'razao_elementar': {'E': V['E'], 'beta': V['beta'], 'C': V['C'], 'K_alpha': V['K'], 'reason': V['reason'], 'reason_sq': V['reason2'], 'family_half': V['fam_half'], "
             "'per_nat_v378': V['pernat'], 'delta_over_beta': V['gbar'], 'finite_time_clause': V['finite']}, ") + s[j:]
wr("manifesto_v379.py", s)
# 3. superficies
s = rd("superficies_v378.py")
s = s.replace("import leitura_v378, textos_v378 as T", "import leitura_v379, textos_v379 as T").replace("leitura_v378.ler()", "leitura_v379.ler()")
s = s.replace("V378_REMAP_DIR", "V379_REMAP_DIR").replace("V378_WRITE_ROOT", "V379_WRITE_ROOT").replace("_sup378", "_sup379")
s = subs(s, [("""for nome, bloco in (('missao-ultima-flag-um-py.md', T.topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V)),
                    ('fase4-desvio-30set.md', T.topico_fase4(V)), ('fase3-leitores-h0-30set.md', T.topico_fase3(V)),
                    ('desvio-de-beta-foco-dos-testes-30set.md', T.topico_desvio(V))):""",
              """for nome, bloco in (('missao-ultima-flag-um-py.md', T.topico_missao(V)), ('central-de-patentes-estado.md', T.topico_central(V)),
                    ('razao-elementar-existencia-beta-01out.md', T.topico_razao(V)), ('desvio-de-beta-foco-dos-testes-30set.md', T.topico_desvio(V))):""", 1),
             ("MARCA = '**v378 SELADA %s `%s`' % (V['data'][:5], V['s16'])", "MARCA = '**v379 SELADA %s `%s`' % (V['data'][:5], V['s16'])", 1)])
i = s.index("lines[k[0]] = (a + '(missao-ultima-flag-um-py.md) — ' + ")
j = s.index("\n", i)
s = s[:i] + ("lines[k[0]] = (a + '(missao-ultima-flag-um-py.md) — ' + '%s %s %s (A RAZÃO ELEMENTAR tipada: E = C × I × K > 0 = β por termo; E é a assíntota; "
             "o reconhecimento é finito por definição; gate intocado)** · ' % (MARCA, V['teor'], V['compl']) + b)") + s[j:]
s = s.replace("print('NADA A GRAVAR: todas as superficies ja tem a v378 (idempotente)')", "print('NADA A GRAVAR: todas as superficies ja tem a v379 (idempotente)')")
s = s.replace("print('SUPERFICIES v378:", "print('SUPERFICIES v379:")
s = s.replace("'<!-- linha integral do índice (gerência, v378) -->'", "'<!-- linha integral do índice (gerência, v379) -->'")
s = s.replace("'marcador v378 na missao;", "'marcador v379 na missao;")
wr("superficies_v379.py", s)
# 4. chain
s = rd("chain_pos_rito_v378.sh")
s = s.replace("v378", "v379").replace("V378", "V379")
s = subs(s, [('"$UMEM/fase4-desvio-30set.md" "$UMEM/fase3-leitores-h0-30set.md" "$UMEM/desvio-de-beta-foco-dos-testes-30set.md"',
              '"$UMEM/razao-elementar-existencia-beta-01out.md" "$UMEM/desvio-de-beta-foco-dos-testes-30set.md"', 1)])
wr("chain_pos_rito_v379.sh", s, py=False)
print("FABRICADO v379_selo (espera, manifesto, superficies, chain)")
