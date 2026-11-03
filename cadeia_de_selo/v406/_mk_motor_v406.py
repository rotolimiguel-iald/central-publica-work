# -*- coding: utf-8 -*-
"""_mk_motor_v406.py -- gera derivar_v406_motor.py a partir de derivar_v405_motor.py (mesmo motor, origem unica "v405", mapa 404 -> 405 e 405 -> 406), por substituicoes de contagem EXATA. Nao executa nada derivado.
Molde: _mk_motor_v405.py (cadeia_de_selo/v405). Escrito pela ferramenta Write (as barras invertidas nao colapsam). Preparacao da v406 (02/11/2026, executor mecanico a servico da gerencia c1; receita: work\\fechamento_02nov\\RECEITA_CADEIA_DE_SELO_v404_para_v405_para_a_v406.md, secoes 1(a) e 5)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(os.path.dirname(HERE), "v405", "derivar_v405_motor.py"), "rb").read().decode("utf-8")
t = src


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:80], t.count(old), n)
    t = t.replace(old, new)


i = t.index('"""derivar_v405_motor.py'); j = t.index("import ast, hashlib, json, os, re, sys")
DOC = '''"""derivar_v406_motor.py -- o MOTOR da derivacao dos scripts da cadeia v406 a partir dos da cadeia v405 (a que foi USADA no rito real de 01/11 e na custodia de 02/11), sem executar nada: o mapa mecanico das versoes, o PROTEGIDO e as regras com contagem exata.
Molde: derivar_v405_motor.py (cadeia_de_selo/v405). Uma ORIGEM so': "v405" (o arquivo da cadeia v405 FINAL, com as licoes de v399 a v405 ja' dentro); o mapa sobe 404 -> 405 (a base selada) e 405 -> 406 (esta rodada); o 399 a 403 NAO sobem (os nomes e rotulos
de 399 a 403 sao historicos: a pedra Testemunho, os registros selo_pela_propria_tecnologia_v399, ponte_da_escala_dual_v402 etc.).
 - O PROTEGIDO (nomes que NASCERAM no um.py e por isso NAO sobem: o um.py v406 os traz com o nome da v399/v400/v401/v402/v403/v404/v405): todo identificador com 399/400/401/402/403/404/405 que existe no TEXTO da base v405 selada (lido do disco, nao digitado) + PROT_EXTRA do arquivo.
   Palavras nuas (v404, v405, E405, V405...) NAO sao protegidas: sao o rotulo da versao e sobem.
 - As REGRAS: (antigo_depois_do_mapa, novo, contagem) ou funcoes (texto -> texto) que ASSERTAM a propria contagem; o motor ABORTA se uma regra nao casar o numero esperado de vezes.
 - ast.parse de cada saida .py; sha256 de entrada e de saida de cada arquivo no relatorio. NUNCA executa o derivado. Nao sobrescreve um derivado que ja' existe e difere (autoral editado depois) sem --refazer."""
'''
t = t[:i] + DOC + t[j:]
sub('ORIGENS = {"v404": os.path.join(CH, "v404")}', 'ORIGENS = {"v405": os.path.join(CH, "v405")}')
sub('NUM3 = re.compile(r"(?<![0-9])(399|400|401|402|403|404)(?![0-9])")', 'NUM3 = re.compile(r"(?<![0-9])(399|400|401|402|403|404|405)(?![0-9])")')
sub('MAPAS = {"v404": {"403": "404", "404": "405"}}', 'MAPAS = {"v405": {"404": "405", "405": "406"}}')
sub('"""Os identificadores de 399/400/401/402/403/404 que existem no um.py base (v404 selada): nascidos no programa, nao sobem."""', '"""Os identificadores de 399/400/401/402/403/404/405 que existem no um.py base (v405 selada): nascidos no programa, nao sobem."""')
sub('_pb = os.path.join(HERE, "base_v404", "um.py")', '_pb = os.path.join(HERE, "base_v405", "um.py")')
sub("# antes de copiar_base_v405.py: o um.py do Nos (a v404 SELADA; os mesmos bytes que a copia vai trazer, conferidos por sha256 la)", "# antes de copiar_base_v406.py: o um.py do Nos (a v405 SELADA; os mesmos bytes que a copia vai trazer, conferidos por sha256 la)")
sub('re.fullmatch(r"[A-Za-z]?(399|400|401|402|403|404)", w)', 're.fullmatch(r"[A-Za-z]?(399|400|401|402|403|404|405)", w)', 2)   # (em prot_um e em protegida)
sub('"""w (palavra com 399/400/401/402/403/404) nasceu no um.py:', '"""w (palavra com 399/400/401/402/403/404/405) nasceu no um.py:')
sub('def bump(t, prot_extra=(), origem="v404"):', 'def bump(t, prot_extra=(), origem="v405"):')
sub('re.fullmatch(r"v(399|400|401|402|403|404)", w)', 're.fullmatch(r"v(399|400|401|402|403|404|405)", w)')
sub('def derivar(src, dst, regras=(), prot_extra=(), com_bump=True, refazer=False, fantasmas=None, origem="v404"):', 'def derivar(src, dst, regras=(), prot_extra=(), com_bump=True, refazer=False, fantasmas=None, origem="v405"):')
sub('"""src: caminho relativo a pasta da origem (v404); dst: relativo a v405.', '"""src: caminho relativo a pasta da origem (v405); dst: relativo a v406.')
sub("(na v405 o E402 do original nao e' tocado pelo mapa 403 -> 404 -> 405; o replace fica como guarda)", "(na v406 o E402 do original nao e' tocado pelo mapa 404 -> 405 -> 406; o replace fica como guarda)")
sub('def linhas_com(dst, padrao=r"39[9]|40[012345]"):', 'def linhas_com(dst, padrao=r"39[9]|40[0123456]"):')
sub('    if estado == "gravado":\n        open(pd + ".tmp", "wb").write(novo); os.replace(pd + ".tmp", pd)',
    '    if estado == "gravado":\n        if os.path.exists(pd):    # AJUSTE v406: --refazer so\' substitui depois de um backup de BYTES (.bak_<ts> na mesma pasta); a v405 substituia sem backup\n            open(pd + ".bak_" + __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S"), "wb").write(open(pd, "rb").read())\n        open(pd + ".tmp", "wb").write(novo); os.replace(pd + ".tmp", pd)')
sub('def lista_hunks(a_rel, b_rel, origem_a="v404", origem_b="v404", ancho=170):', 'def lista_hunks(a_rel, b_rel, origem_a="v405", origem_b="v405", ancho=170):')
sub('def aplica_hunks(b_rel, indices, a_rel=None, origem_a="v404", origem_b="v404"):', 'def aplica_hunks(b_rel, indices, a_rel=None, origem_a="v405", origem_b="v405"):')
sub('re.fullmatch(r"k(399|400|401|402|403|404)[a-z]?", w)', 're.fullmatch(r"k(399|400|401|402|403|404|405)[a-z]?", w)')
out = os.path.join(HERE, "derivar_v406_motor.py")
if os.path.exists(out):
    assert open(out, "rb").read() == t.encode("utf-8"), "derivar_v406_motor.py ja existe e DIFERE: nao sobrescrevo"
else:
    open(out + ".tmp", "wb").write(t.encode("utf-8")); assert os.path.getsize(out + ".tmp") == len(t.encode("utf-8")); os.replace(out + ".tmp", out)
print("ok", len(src), len(t))
