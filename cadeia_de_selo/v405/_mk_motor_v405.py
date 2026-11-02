# -*- coding: utf-8 -*-
"""_mk_motor_v405.py -- gera derivar_v405_motor.py a partir de derivar_v404_motor.py (mesmo motor, origem unica "v404", mapa 403 -> 404 e 404 -> 405), por substituicoes de contagem EXATA. Nao executa nada derivado.
Molde: _mk_motor_v404.py (cadeia_de_selo/v404). Escrito pela ferramenta Write (as barras invertidas nao colapsam). Preparacao da v405 (01/11/2026, agente claude-prep-v405 para a gerencia c1)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(os.path.dirname(HERE), "v404", "derivar_v404_motor.py"), "rb").read().decode("utf-8")
t = src


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:80], t.count(old), n)
    t = t.replace(old, new)


i = t.index('"""derivar_v404_motor.py'); j = t.index("import ast, hashlib, json, os, re, sys")
DOC = '''"""derivar_v405_motor.py -- o MOTOR da derivacao dos scripts da cadeia v405 a partir dos da cadeia v404 (a que foi USADA no rito real de 28/10 e na custodia de 29/10), sem executar nada: o mapa mecanico das versoes, o PROTEGIDO e as regras com contagem exata.
Molde: derivar_v404_motor.py (cadeia_de_selo/v404). Uma ORIGEM so': "v404" (o arquivo da cadeia v404 FINAL, com as licoes de v399 a v404 ja' dentro); o mapa sobe 403 -> 404 (a base selada) e 404 -> 405 (esta rodada); o 399 a 402 NAO sobem (os nomes e rotulos
de 399 a 402 sao historicos: a pedra Testemunho, os registros selo_pela_propria_tecnologia_v399, ponte_da_escala_dual_v402 etc.).
 - O PROTEGIDO (nomes que NASCERAM no um.py e por isso NAO sobem: o um.py v405 os traz com o nome da v399/v400/v401/v402/v403/v404): todo identificador com 399/400/401/402/403/404 que existe no TEXTO da base v404 selada (lido do disco, nao digitado) + PROT_EXTRA do arquivo.
   Palavras nuas (v403, v404, E404, V404...) NAO sao protegidas: sao o rotulo da versao e sobem.
 - As REGRAS: (antigo_depois_do_mapa, novo, contagem) ou funcoes (texto -> texto) que ASSERTAM a propria contagem; o motor ABORTA se uma regra nao casar o numero esperado de vezes.
 - ast.parse de cada saida .py; sha256 de entrada e de saida de cada arquivo no relatorio. NUNCA executa o derivado. Nao sobrescreve um derivado que ja' existe e difere (autoral editado depois) sem --refazer."""
'''
t = t[:i] + DOC + t[j:]
sub('ORIGENS = {"v403": os.path.join(CH, "v403")}', 'ORIGENS = {"v404": os.path.join(CH, "v404")}')
sub('NUM3 = re.compile(r"(?<![0-9])(399|400|401|402|403)(?![0-9])")', 'NUM3 = re.compile(r"(?<![0-9])(399|400|401|402|403|404)(?![0-9])")')
sub('MAPAS = {"v403": {"402": "403", "403": "404"}}', 'MAPAS = {"v404": {"403": "404", "404": "405"}}')
sub('"""Os identificadores de 399/400/401/402/403 que existem no um.py base (v403 selada): nascidos no programa, nao sobem."""', '"""Os identificadores de 399/400/401/402/403/404 que existem no um.py base (v404 selada): nascidos no programa, nao sobem."""')
sub('_pb = os.path.join(HERE, "base_v403", "um.py")', '_pb = os.path.join(HERE, "base_v404", "um.py")')
sub("# antes de copiar_base_v404.py: o um.py do Nos (a v403 SELADA; os mesmos bytes que a copia vai trazer, conferidos por sha256 la)", "# antes de copiar_base_v405.py: o um.py do Nos (a v404 SELADA; os mesmos bytes que a copia vai trazer, conferidos por sha256 la)")
sub('re.fullmatch(r"[A-Za-z]?(399|400|401|402|403)", w)', 're.fullmatch(r"[A-Za-z]?(399|400|401|402|403|404)", w)', 2)   # (em prot_um e em protegida)
sub('"""w (palavra com 399/400/401/402/403) nasceu no um.py:', '"""w (palavra com 399/400/401/402/403/404) nasceu no um.py:')
sub('def bump(t, prot_extra=(), origem="v403"):', 'def bump(t, prot_extra=(), origem="v404"):')
sub('re.fullmatch(r"v(399|400|401|402|403)", w)', 're.fullmatch(r"v(399|400|401|402|403|404)", w)')
sub('def derivar(src, dst, regras=(), prot_extra=(), com_bump=True, refazer=False, fantasmas=None, origem="v403"):', 'def derivar(src, dst, regras=(), prot_extra=(), com_bump=True, refazer=False, fantasmas=None, origem="v404"):')
sub('"""src: caminho relativo a pasta da origem (v403); dst: relativo a v404.', '"""src: caminho relativo a pasta da origem (v404); dst: relativo a v405.')
sub("(na v404 o E402 do original sobe para E403 e volta)", "(na v405 o E402 do original nao e' tocado pelo mapa 403 -> 404 -> 405; o replace fica como guarda)")
sub('def linhas_com(dst, padrao=r"39[9]|40[01234]"):', 'def linhas_com(dst, padrao=r"39[9]|40[012345]"):')
sub('def lista_hunks(a_rel, b_rel, origem_a="v403", origem_b="v403", ancho=170):', 'def lista_hunks(a_rel, b_rel, origem_a="v404", origem_b="v404", ancho=170):')
sub('def aplica_hunks(b_rel, indices, a_rel=None, origem_a="v403", origem_b="v403"):', 'def aplica_hunks(b_rel, indices, a_rel=None, origem_a="v404", origem_b="v404"):')
sub('re.fullmatch(r"k(399|400|401|402|403)[a-z]?", w)', 're.fullmatch(r"k(399|400|401|402|403|404)[a-z]?", w)')
out = os.path.join(HERE, "derivar_v405_motor.py")
if os.path.exists(out):
    assert open(out, "rb").read() == t.encode("utf-8"), "derivar_v405_motor.py ja existe e DIFERE: nao sobrescrevo"
else:
    open(out + ".tmp", "wb").write(t.encode("utf-8")); assert os.path.getsize(out + ".tmp") == len(t.encode("utf-8")); os.replace(out + ".tmp", out)
print("ok", len(src), len(t))
