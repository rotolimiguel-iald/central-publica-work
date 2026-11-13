# -*- coding: utf-8 -*-
"""D195 (13/11/2026, claude-site-custodia; decisão da gerência c1), parte G1: h0dn.py.
(1) o gancho da seção das sete ressalvas passa a entrar logo antes de «## The seal» (logo depois do bloco «Proved on three supports»),
    dentro dos primeiros 100.000 caracteres do ESTADO_ATUAL; a âncora antiga fica nomeada (_ANC_SECAO_12NOV) para a migração do espelho;
(2) as duas linhas de caminho para as sete ressalvas, com as palavras exatas da gerência (EN e PT), numa fonte só, e a função que as monta
    (com o nome do arquivo em link quando a superfície tem a URL gerada por script).
Edição por bytes; backup; temporário; compilação; o arquivo tem de crescer. Uso: python -X utf8 <este> [PASTA_DA_G1]"""
import os, sys, time

G1 = sys.argv[1] if len(sys.argv) > 1 else r"C:\IALD\Central de Patentes\tools\custodia_g1"
STAMP = time.strftime("%Y%m%d_%H%M%S")
P = os.path.join(G1, "h0dn.py")

VELHO_ANC = '_ANC_SECAO = "    L.append(\\"## What is NOT proved · o que NÃO está provado `[OPEN / KNOWN / nature]`\\")\\n"\n'
NOVO_ANC = (
    '# AO LADO (13/11/2026, claude-site-custodia; D195 da gerência c1): a seção sobe para logo antes de «## The seal», logo depois do bloco\n'
    '# «Proved on three supports»: a 300 mil caracteres (antes de «What is NOT proved») ela ficava fora do corte medido dos leitores de IA\n'
    '# (perto de 100.000 caracteres). As linhas da seção não mudam; só o lugar. A âncora de 12/11 fica nomeada para a migração do espelho.\n'
    '_ANC_SECAO_12NOV = "    L.append(\\"## What is NOT proved · o que NÃO está provado `[OPEN / KNOWN / nature]`\\")\\n"\n'
    '_ANC_SECAO = "    L.append(\\"## The seal · o selo `[REAL — read from the artifact]`\\")\\n"\n'
    '# AO LADO (13/11/2026, claude-site-custodia; D195 da gerência c1, palavras exatas dela): nenhuma SUPERFÍCIE mostra o primário sem o caminho\n'
    '# para as sete ressalvas (regra da gerência do acordo de 12/11, seção 8, item 4). A linha é gerada, separada dos textos ratificados.\n'
    'TITULO_SECAO_RESSALVAS = "The H0DN \\u00d7 BG1 test: the seven reservations and what the test does not decide"\n'
    'CAMINHO_RESSALVAS = {\n'
    '    "en": "The seven reservations and what the test does not decide: %s, section \\u201c" + TITULO_SECAO_RESSALVAS + "\\u201d.",\n'
    '    "pt": "As sete ressalvas e o que o teste n\\u00e3o decide: %s, se\\u00e7\\u00e3o \\u201c" + TITULO_SECAO_RESSALVAS + "\\u201d.",\n'
    '}\n'
    '\n'
    '\n'
    'def caminho_ressalvas(lingua, url=None):\n'
    '    """A linha de caminho para as sete ressalvas (EN ou PT), com `ESTADO_ATUAL.md` em código; com `url` (gerada por script), em link."""\n'
    '    nome = "`ESTADO_ATUAL.md`"\n'
    '    return CAMINHO_RESSALVAS[lingua] % (("[%s](%s)" % (nome, url)) if url else nome)\n'
)
VELHO_DOC = '    """O par (âncora, código + âncora) do gerar_estado_atual.py: a seção entra logo antes de «What is NOT proved»; sem registro aberto, nada."""\n'
NOVO_DOC = ('    """O par (âncora, código + âncora) do gerar_estado_atual.py: a seção entra logo antes de «## The seal» (D195, 13/11; em 12/11 era antes de\n'
            '    «What is NOT proved»); sem registro aberto, nada."""\n')

b = open(P, "rb").read()
assert b.count(b"\r\n") == 0, "h0dn.py e LF"
for a in (VELHO_ANC, VELHO_DOC):
    assert b.count(a.encode("utf-8")) == 1, "o trecho mudou em h0dn.py - PARAR: %r" % a[:80]
bak = P + ".bak_%s_d195" % STAMP
open(bak, "wb").write(b)
assert open(bak, "rb").read() == b
novo = b.replace(VELHO_ANC.encode("utf-8"), NOVO_ANC.encode("utf-8")).replace(VELHO_DOC.encode("utf-8"), NOVO_DOC.encode("utf-8"))
compile(novo.decode("utf-8"), P, "exec")
t = P + ".tmp_errata"
open(t, "wb").write(novo)
assert os.path.getsize(t) == len(novo) > len(b)
os.replace(t, P)
print("ok: h0dn.py", len(b), "->", len(novo), "| backup", os.path.basename(bak))
