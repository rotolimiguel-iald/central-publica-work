# -*- coding: utf-8 -*-
"""_mk_motor_v404.py -- gera derivar_v404_motor.py a partir de derivar_v403_motor.py (mesmo motor, origem unica "v403", mapa 402 -> 403 e 403 -> 404), por substituicoes de contagem EXATA. Nao executa nada derivado.
Molde: _mk_motor_v403.py (cadeia_de_selo/v403). Escrito pela ferramenta Write (as barras invertidas nao colapsam). Preparacao da v404 (28/10/2026, agente claude-prep-v404 para a gerencia c1)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(os.path.dirname(HERE), "v403", "derivar_v403_motor.py"), "rb").read().decode("utf-8")
t = src


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:80], t.count(old), n)
    t = t.replace(old, new)


i = t.index('"""derivar_v403_motor.py'); j = t.index("import ast, hashlib, json, os, re, sys")
DOC = '''"""derivar_v404_motor.py -- o MOTOR da derivacao dos scripts da cadeia v404 a partir dos da cadeia v403 (a que foi USADA no rito real de 28/10), sem executar nada: o mapa mecanico das versoes, o PROTEGIDO e as regras com contagem exata.
Molde: derivar_v403_motor.py (cadeia_de_selo/v403). Uma ORIGEM so': "v403" (o arquivo da cadeia v403 FINAL, com as licoes de v399 a v403 ja' dentro); o mapa sobe 402 -> 403 (a base selada) e 403 -> 404 (esta rodada); o 399, o 400 e o 401 NAO sobem (os nomes e rotulos
de 399, 400 e 401 sao historicos: a pedra Testemunho, os registros selo_pela_propria_tecnologia_v399 etc.).
 - O PROTEGIDO (nomes que NASCERAM no um.py e por isso NAO sobem: o um.py v404 os traz com o nome da v399/v400/v401/v402/v403): todo identificador com 399/400/401/402/403 que existe no TEXTO da base v403 selada (lido do disco, nao digitado) + PROT_EXTRA do arquivo.
   Palavras nuas (v402, v403, E403, V403...) NAO sao protegidas: sao o rotulo da versao e sobem.
 - As REGRAS: (antigo_depois_do_mapa, novo, contagem) ou funcoes (texto -> texto) que ASSERTAM a propria contagem; o motor ABORTA se uma regra nao casar o numero esperado de vezes.
 - ast.parse de cada saida .py; sha256 de entrada e de saida de cada arquivo no relatorio. NUNCA executa o derivado. Nao sobrescreve um derivado que ja' existe e difere (autoral editado depois) sem --refazer."""
'''
t = t[:i] + DOC + t[j:]
sub('ORIGENS = {"v402": os.path.join(CH, "v402")}', 'ORIGENS = {"v403": os.path.join(CH, "v403")}')
sub('NUM3 = re.compile(r"(?<![0-9])(399|400|401|402)(?![0-9])")', 'NUM3 = re.compile(r"(?<![0-9])(399|400|401|402|403)(?![0-9])")')
sub('MAPAS = {"v402": {"401": "402", "402": "403"}}', 'MAPAS = {"v403": {"402": "403", "403": "404"}}')
sub('"""Os identificadores de 399/400/401/402 que existem no um.py base (v402 selada): nascidos no programa, nao sobem."""', '"""Os identificadores de 399/400/401/402/403 que existem no um.py base (v403 selada): nascidos no programa, nao sobem."""')
sub('_pb = os.path.join(HERE, "base_v402", "um.py")', '_pb = os.path.join(HERE, "base_v403", "um.py")')
sub("# antes de copiar_base_v403.py: o um.py do Nos (a v402 SELADA; os mesmos bytes que a copia vai trazer, conferidos por sha256 la)", "# antes de copiar_base_v404.py: o um.py do Nos (a v403 SELADA; os mesmos bytes que a copia vai trazer, conferidos por sha256 la)")
sub('re.fullmatch(r"[A-Za-z]?(399|400|401|402)", w)', 're.fullmatch(r"[A-Za-z]?(399|400|401|402|403)", w)', 2)   # (em prot_um e em protegida)
sub('"""w (palavra com 399/400/401/402) nasceu no um.py:', '"""w (palavra com 399/400/401/402/403) nasceu no um.py:')
sub('def bump(t, prot_extra=(), origem="v402"):', 'def bump(t, prot_extra=(), origem="v403"):')
sub('re.fullmatch(r"v(399|400|401|402)", w)', 're.fullmatch(r"v(399|400|401|402|403)", w)')
sub('def derivar(src, dst, regras=(), prot_extra=(), com_bump=True, refazer=False, fantasmas=None, origem="v402"):', 'def derivar(src, dst, regras=(), prot_extra=(), com_bump=True, refazer=False, fantasmas=None, origem="v403"):')
sub('"""src: caminho relativo a pasta da origem (v402); dst: relativo a v403.', '"""src: caminho relativo a pasta da origem (v403); dst: relativo a v404.')
sub('    t2 = t2.replace("noqa: E403", "noqa: E402")   # E402 e\' o codigo do flake8 (import fora do topo), nao um rotulo de versao: o mapa 402 -> 403 o subiria\n',
    '    t2 = t2.replace("noqa: E403", "noqa: E402")   # E402 e\' o codigo do flake8 (import fora do topo), nao um rotulo de versao: o mapa 402 -> 403 o subiria (na v404 o E402 do original sobe para E403 e volta)\n')
sub('def linhas_com(dst, padrao=r"39[9]|40[0123]"):', 'def linhas_com(dst, padrao=r"39[9]|40[01234]"):')
sub('def lista_hunks(a_rel, b_rel, origem_a="v402", origem_b="v402", ancho=170):', 'def lista_hunks(a_rel, b_rel, origem_a="v403", origem_b="v403", ancho=170):')
sub('def aplica_hunks(b_rel, indices, a_rel=None, origem_a="v402", origem_b="v402"):', 'def aplica_hunks(b_rel, indices, a_rel=None, origem_a="v403", origem_b="v403"):')
sub("        if protegida(w):\n            return w\n        return sub(w)\n",
    "        if re.fullmatch(r\"k(399|400|401|402|403)[a-z]?\", w):    # o ROTULO do sandbox do kernel (k403c, k402x): label da cadeia, nao nome nascido no um.py (que o cita so' em comentario); sobe\n            return sub(w)\n        if protegida(w):\n            return w\n        return sub(w)\n")
out = os.path.join(HERE, "derivar_v404_motor.py")
if os.path.exists(out):
    assert open(out, "rb").read() == t.encode("utf-8"), "derivar_v404_motor.py ja existe e DIFERE: nao sobrescrevo"
else:
    open(out + ".tmp", "wb").write(t.encode("utf-8")); assert os.path.getsize(out + ".tmp") == len(t.encode("utf-8")); os.replace(out + ".tmp", out)
print("ok", len(src), len(t))
