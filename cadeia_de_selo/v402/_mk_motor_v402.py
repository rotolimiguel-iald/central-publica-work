# -*- coding: utf-8 -*-
"""_mk_motor_v402.py -- gera derivar_v402_motor.py a partir de derivar_v401_motor.py (mesmo motor, origem unica "v401", mapa 400 -> 401 e 401 -> 402), por substituicoes de contagem EXATA. Nao executa nada derivado."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(os.path.dirname(HERE), "v401", "derivar_v401_motor.py"), "rb").read().decode("utf-8")
t = src


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:80], t.count(old), n)
    t = t.replace(old, new)


i = t.index('"""derivar_v401_motor.py'); j = t.index("import ast, hashlib, json, os, re, sys")
DOC = '''"""derivar_v402_motor.py -- o MOTOR da derivacao dos scripts da cadeia v402 a partir dos da cadeia v401 (a que foi USADA no rito real de 25/10), sem executar nada: o mapa mecanico das versoes, o PROTEGIDO e as regras com contagem exata.
Molde: derivar_v401_motor.py (cadeia_de_selo/v401). Uma ORIGEM so': "v401" (o arquivo da cadeia v401 FINAL, com as licoes de v399, v400 e v401 ja' dentro); o mapa sobe 400 -> 401 (a base selada) e 401 -> 402 (esta rodada); o 399 NAO sobe (os nomes e rotulos
de 399 sao historicos: a pedra Testemunho, os registros selo_pela_propria_tecnologia_v399 etc.).
 - O PROTEGIDO (nomes que NASCERAM no um.py e por isso NAO sobem: o um.py v402 os traz com o nome da v399/v400/v401): todo identificador com 399/400/401 que existe no TEXTO da base v401 selada (lido do disco, nao digitado) + PROT_EXTRA do arquivo.
   Palavras nuas (v400, v401, E401, V401...) NAO sao protegidas: sao o rotulo da versao e sobem.
 - As REGRAS: (antigo_depois_do_mapa, novo, contagem) ou funcoes (texto -> texto) que ASSERTAM a propria contagem; o motor ABORTA se uma regra nao casar o numero esperado de vezes.
 - ast.parse de cada saida .py; sha256 de entrada e de saida de cada arquivo no relatorio. NUNCA executa o derivado. Nao sobrescreve um derivado que ja' existe e difere (autoral editado depois) sem --refazer."""
'''
t = t[:i] + DOC + t[j:]
sub('ORIGENS = {"v400": os.path.join(CH, "v400"), "v399": os.path.join(CH, "v399")}', 'ORIGENS = {"v401": os.path.join(CH, "v401")}')
sub('NUM3 = re.compile(r"(?<![0-9])(398|399|400)(?![0-9])")', 'NUM3 = re.compile(r"(?<![0-9])(399|400|401)(?![0-9])")')
sub('MAPAS = {"v400": {"399": "400", "400": "401"}, "v399": {"398": "400", "399": "401"}}', 'MAPAS = {"v401": {"400": "401", "401": "402"}}')
sub('"""Os identificadores de 398/399/400 que existem no um.py base (v400 selada): nascidos no programa, nao sobem."""', '"""Os identificadores de 399/400/401 que existem no um.py base (v401 selada): nascidos no programa, nao sobem."""')
NOVO_PROT = '''_pb = os.path.join(HERE, "base_v401", "um.py")
        if not os.path.exists(_pb):    # antes de copiar_base_v402.py: o um.py do Nos (a v401 SELADA; os mesmos bytes que a copia vai trazer, conferidos por sha256 la)
            _pb = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós", "um.py")
        t = open(_pb, "rb").read().decode("utf-8")'''
sub('t = open(os.path.join(HERE, "base_v400", "um.py"), "rb").read().decode("utf-8")', NOVO_PROT)
sub('re.fullmatch(r"[A-Za-z]?(398|399|400)", w)', 're.fullmatch(r"[A-Za-z]?(399|400|401)", w)', 2)   # (em prot_um e em protegida)
sub('"""w (palavra com 398/399/400) nasceu no um.py:', '"""w (palavra com 399/400/401) nasceu no um.py:')
sub('def bump(t, prot_extra=(), origem="v400"):', 'def bump(t, prot_extra=(), origem="v401"):')
sub('re.fullmatch(r"v(398|399|400)", w)', 're.fullmatch(r"v(399|400|401)", w)')
sub('def derivar(src, dst, regras=(), prot_extra=(), com_bump=True, refazer=False, fantasmas=None, origem="v400"):', 'def derivar(src, dst, regras=(), prot_extra=(), com_bump=True, refazer=False, fantasmas=None, origem="v401"):')
sub('"""src: caminho relativo a pasta da origem (v400 ou v399); dst: relativo a v401.', '"""src: caminho relativo a pasta da origem (v401); dst: relativo a v402.')
sub('def linhas_com(dst, padrao=r"39[89]|40[01]"):', 'def linhas_com(dst, padrao=r"39[9]|40[012]"):')
sub('def lista_hunks(a_rel, b_rel, origem_a="v399", origem_b="v400", ancho=170):', 'def lista_hunks(a_rel, b_rel, origem_a="v401", origem_b="v401", ancho=170):')
sub('def aplica_hunks(b_rel, indices, a_rel=None, origem_a="v399", origem_b="v400"):', 'def aplica_hunks(b_rel, indices, a_rel=None, origem_a="v401", origem_b="v401"):')
open(os.path.join(HERE, "derivar_v402_motor.py"), "wb").write(t.encode("utf-8"))
print("ok", len(src), len(t))
