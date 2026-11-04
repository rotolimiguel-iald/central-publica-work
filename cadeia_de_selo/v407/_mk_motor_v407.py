# -*- coding: utf-8 -*-
"""_mk_motor_v407.py -- gera derivar_v407_motor.py a partir de derivar_v406_motor.py (mesmo motor, origem unica "v406", mapa 405 -> 406 e 406 -> 407), por substituicoes de contagem EXATA. Nao executa nada derivado.
Molde: _mk_motor_v406.py (cadeia_de_selo/v406). claude-prep-v407, 03/11/2026. Escrito pela ferramenta Write (as barras invertidas nao colapsam)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(os.path.dirname(HERE), "v406", "derivar_v406_motor.py"), "rb").read().decode("utf-8")
t = src


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:80], t.count(old), n)
    t = t.replace(old, new)


i = t.index('"""derivar_v406_motor.py'); j = t.index("import ast, hashlib, json, os, re, sys")
DOC = '''"""derivar_v407_motor.py -- o MOTOR da derivacao dos scripts da cadeia v407 a partir dos da cadeia v406 (a que foi USADA no rito real de 03/11 e na custodia), sem executar nada: o mapa mecanico das versoes, o PROTEGIDO e as regras com contagem exata.
Molde: derivar_v406_motor.py (cadeia_de_selo/v406). Uma ORIGEM so': "v406"; o mapa sobe 405 -> 406 (a base selada) e 406 -> 407 (esta rodada); o 399 a 404 NAO sobem (os nomes e rotulos de 399 a 404 sao historicos).
 - O PROTEGIDO (nomes que NASCERAM no um.py e por isso NAO sobem): todo identificador com 399..406 que existe no TEXTO da base v406 selada (lido do disco, nao digitado) + PROT_EXTRA do arquivo. Palavras nuas (v405, v406, E406, V406...) NAO sao protegidas: sao o rotulo da versao e sobem.
 - As REGRAS: (antigo_depois_do_mapa, novo, contagem) ou funcoes (texto -> texto) que ASSERTAM a propria contagem; o motor ABORTA se uma regra nao casar o numero esperado de vezes.
 - ast.parse de cada saida .py; sha256 de entrada e de saida de cada arquivo no relatorio. NUNCA executa o derivado. Nao sobrescreve um derivado que ja' existe e difere sem --refazer (que faz backup de bytes)."""
'''
t = t[:i] + DOC + t[j:]
sub('ORIGENS = {"v405": os.path.join(CH, "v405")}', 'ORIGENS = {"v406": os.path.join(CH, "v406")}')
sub('NUM3 = re.compile(r"(?<![0-9])(399|400|401|402|403|404|405)(?![0-9])")', 'NUM3 = re.compile(r"(?<![0-9])(399|400|401|402|403|404|405|406)(?![0-9])")')
sub('MAPAS = {"v405": {"404": "405", "405": "406"}}', 'MAPAS = {"v406": {"405": "406", "406": "407"}}')
sub('"""Os identificadores de 399/400/401/402/403/404/405 que existem no um.py base (v405 selada): nascidos no programa, nao sobem."""', '"""Os identificadores de 399..406 que existem no um.py base (v406 selada): nascidos no programa, nao sobem."""')
sub('_pb = os.path.join(HERE, "base_v405", "um.py")', '_pb = os.path.join(HERE, "base_v406", "um.py")')
sub("# antes de copiar_base_v406.py: o um.py do Nos (a v405 SELADA; os mesmos bytes que a copia vai trazer, conferidos por sha256 la)", "# antes de copiar_base_v407.py: o um.py do Nos (a v406 SELADA; os mesmos bytes que a copia vai trazer, conferidos por sha256 la)")
sub('re.fullmatch(r"[A-Za-z]?(399|400|401|402|403|404|405)", w)', 're.fullmatch(r"[A-Za-z]?(399|400|401|402|403|404|405|406)", w)', 2)   # (em prot_um e em protegida)
sub('"""w (palavra com 399/400/401/402/403/404/405) nasceu no um.py:', '"""w (palavra com 399..406) nasceu no um.py:')
sub('def bump(t, prot_extra=(), origem="v405"):', 'def bump(t, prot_extra=(), origem="v406"):')
sub('re.fullmatch(r"v(399|400|401|402|403|404|405)", w)', 're.fullmatch(r"v(399|400|401|402|403|404|405|406)", w)')
sub('def derivar(src, dst, regras=(), prot_extra=(), com_bump=True, refazer=False, fantasmas=None, origem="v405"):', 'def derivar(src, dst, regras=(), prot_extra=(), com_bump=True, refazer=False, fantasmas=None, origem="v406"):')
sub('"""src: caminho relativo a pasta da origem (v405); dst: relativo a v406.', '"""src: caminho relativo a pasta da origem (v406); dst: relativo a v407.')
sub("(na v406 o E402 do original nao e' tocado pelo mapa 404 -> 405 -> 406; o replace fica como guarda)", "(na v407 o E402 do original nao e' tocado pelo mapa 405 -> 406 -> 407; o replace fica como guarda)")
sub('def linhas_com(dst, padrao=r"39[9]|40[0123456]"):', 'def linhas_com(dst, padrao=r"39[9]|40[01234567]"):')
sub('def lista_hunks(a_rel, b_rel, origem_a="v405", origem_b="v405", ancho=170):', 'def lista_hunks(a_rel, b_rel, origem_a="v406", origem_b="v406", ancho=170):')
sub('def aplica_hunks(b_rel, indices, a_rel=None, origem_a="v405", origem_b="v405"):', 'def aplica_hunks(b_rel, indices, a_rel=None, origem_a="v406", origem_b="v406"):')
sub('re.fullmatch(r"k(399|400|401|402|403|404|405)[a-z]?", w)', 're.fullmatch(r"k(399|400|401|402|403|404|405|406)[a-z]?", w)')
sub("# AJUSTE v406: --refazer so' substitui depois de um backup de BYTES (.bak_<ts> na mesma pasta); a v405 substituia sem backup", "# AJUSTE v406 (mantido): --refazer so' substitui depois de um backup de BYTES (.bak_<ts> na mesma pasta)")
out = os.path.join(HERE, "derivar_v407_motor.py")
if os.path.exists(out):
    assert open(out, "rb").read() == t.encode("utf-8"), "derivar_v407_motor.py ja existe e DIFERE: nao sobrescrevo"
else:
    open(out + ".tmp", "wb").write(t.encode("utf-8")); assert os.path.getsize(out + ".tmp") == len(t.encode("utf-8")); os.replace(out + ".tmp", out)
print("ok", len(src), len(t))
