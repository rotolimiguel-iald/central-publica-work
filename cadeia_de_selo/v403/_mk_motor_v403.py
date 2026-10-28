# -*- coding: utf-8 -*-
"""_mk_motor_v403.py -- gera derivar_v403_motor.py a partir de derivar_v402_motor.py (mesmo motor, origem unica "v402", mapa 401 -> 402 e 402 -> 403), por substituicoes de contagem EXATA. Nao executa nada derivado.
Molde: _mk_motor_v402.py. Escrito pela ferramenta Write (as barras invertidas nao colapsam)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(os.path.dirname(HERE), "v402", "derivar_v402_motor.py"), "rb").read().decode("utf-8")
t = src


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:80], t.count(old), n)
    t = t.replace(old, new)


i = t.index('"""derivar_v402_motor.py'); j = t.index("import ast, hashlib, json, os, re, sys")
DOC = '''"""derivar_v403_motor.py -- o MOTOR da derivacao dos scripts da cadeia v403 a partir dos da cadeia v402 (a que foi USADA no rito real de 27/10), sem executar nada: o mapa mecanico das versoes, o PROTEGIDO e as regras com contagem exata.
Molde: derivar_v402_motor.py (cadeia_de_selo/v402). Uma ORIGEM so': "v402" (o arquivo da cadeia v402 FINAL, com as licoes de v399, v400, v401 e v402 ja' dentro); o mapa sobe 401 -> 402 (a base selada) e 402 -> 403 (esta rodada); o 399 e o 400 NAO sobem (os nomes e rotulos
de 399 e 400 sao historicos: a pedra Testemunho, os registros selo_pela_propria_tecnologia_v399 etc.).
 - O PROTEGIDO (nomes que NASCERAM no um.py e por isso NAO sobem: o um.py v403 os traz com o nome da v399/v400/v401/v402): todo identificador com 399/400/401/402 que existe no TEXTO da base v402 selada (lido do disco, nao digitado) + PROT_EXTRA do arquivo.
   Palavras nuas (v401, v402, E402, V402...) NAO sao protegidas: sao o rotulo da versao e sobem.
 - As REGRAS: (antigo_depois_do_mapa, novo, contagem) ou funcoes (texto -> texto) que ASSERTAM a propria contagem; o motor ABORTA se uma regra nao casar o numero esperado de vezes.
 - ast.parse de cada saida .py; sha256 de entrada e de saida de cada arquivo no relatorio. NUNCA executa o derivado. Nao sobrescreve um derivado que ja' existe e difere (autoral editado depois) sem --refazer."""
'''
t = t[:i] + DOC + t[j:]
sub('ORIGENS = {"v401": os.path.join(CH, "v401")}', 'ORIGENS = {"v402": os.path.join(CH, "v402")}')
sub('NUM3 = re.compile(r"(?<![0-9])(399|400|401)(?![0-9])")', 'NUM3 = re.compile(r"(?<![0-9])(399|400|401|402)(?![0-9])")')
sub('MAPAS = {"v401": {"400": "401", "401": "402"}}', 'MAPAS = {"v402": {"401": "402", "402": "403"}}')
sub('"""Os identificadores de 399/400/401 que existem no um.py base (v401 selada): nascidos no programa, nao sobem."""', '"""Os identificadores de 399/400/401/402 que existem no um.py base (v402 selada): nascidos no programa, nao sobem."""')
sub('_pb = os.path.join(HERE, "base_v401", "um.py")', '_pb = os.path.join(HERE, "base_v402", "um.py")')
sub("# antes de copiar_base_v402.py: o um.py do Nos (a v401 SELADA; os mesmos bytes que a copia vai trazer, conferidos por sha256 la)", "# antes de copiar_base_v403.py: o um.py do Nos (a v402 SELADA; os mesmos bytes que a copia vai trazer, conferidos por sha256 la)")
sub('re.fullmatch(r"[A-Za-z]?(399|400|401)", w)', 're.fullmatch(r"[A-Za-z]?(399|400|401|402)", w)', 2)   # (em prot_um e em protegida)
sub('"""w (palavra com 399/400/401) nasceu no um.py:', '"""w (palavra com 399/400/401/402) nasceu no um.py:')
sub('def bump(t, prot_extra=(), origem="v401"):', 'def bump(t, prot_extra=(), origem="v402"):')
sub('re.fullmatch(r"v(399|400|401)", w)', 're.fullmatch(r"v(399|400|401|402)", w)')
sub('def derivar(src, dst, regras=(), prot_extra=(), com_bump=True, refazer=False, fantasmas=None, origem="v401"):', 'def derivar(src, dst, regras=(), prot_extra=(), com_bump=True, refazer=False, fantasmas=None, origem="v402"):')
sub('"""src: caminho relativo a pasta da origem (v401); dst: relativo a v402.', '"""src: caminho relativo a pasta da origem (v402); dst: relativo a v403.')
sub('def linhas_com(dst, padrao=r"39[9]|40[012]"):', 'def linhas_com(dst, padrao=r"39[9]|40[0123]"):')
sub('def lista_hunks(a_rel, b_rel, origem_a="v401", origem_b="v401", ancho=170):', 'def lista_hunks(a_rel, b_rel, origem_a="v402", origem_b="v402", ancho=170):')
sub('def aplica_hunks(b_rel, indices, a_rel=None, origem_a="v401", origem_b="v401"):', 'def aplica_hunks(b_rel, indices, a_rel=None, origem_a="v402", origem_b="v402"):')
sub("    t2 = bump(t, prot_extra, origem) if com_bump else t\n",
    "    t2 = bump(t, prot_extra, origem) if com_bump else t\n    t2 = t2.replace(\"noqa: E403\", \"noqa: E402\")   # E402 e' o codigo do flake8 (import fora do topo), nao um rotulo de versao: o mapa 402 -> 403 o subiria\n")
out = os.path.join(HERE, "derivar_v403_motor.py")
if os.path.exists(out):
    assert open(out, "rb").read() == t.encode("utf-8"), "derivar_v403_motor.py ja existe e DIFERE: nao sobrescrevo"
else:
    open(out + ".tmp", "wb").write(t.encode("utf-8")); assert os.path.getsize(out + ".tmp") == len(t.encode("utf-8")); os.replace(out + ".tmp", out)
print("ok", len(src), len(t))
